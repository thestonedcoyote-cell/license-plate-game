#!/usr/bin/env python3
"""Source-pinned NJ MVC SP-100D PDF plate integration; no era/human/rights approvals."""
import argparse, hashlib, io, json
from pathlib import Path
import fitz
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parents[1]
BATCH='data/image-batches/nj-mvc-dedicated-17-reviewed-20261104.json'
PDF='NJ/NJ_MVC_Dedicated_Plate_Form_SP-100D.pdf'
EXTRACT='NJ/NJ_MVC_Dedicated_Plate_Form_SP-100D_extracted'
OLD='lpg-current-images-20261102-idaho3'
NEW='lpg-current-images-20261104-njmvc17'
PREFIX='globalThis.LPG_CATALOG_IMAGES='

def sha(b):return hashlib.sha256(b).hexdigest()
def once(s,old,new):
    if s.count(old)!=1 or new in s:raise ValueError('Unexpected baseline marker '+old[:90])
    return s.replace(old,new)
def jpg(b,limit):
    with Image.open(io.BytesIO(b)) as img:
        img.load()
        im=ImageOps.exif_transpose(img).convert('RGBA')
        if not (im.width>=100 and im.height>=35 and 1.35<=im.width/im.height<=3.8):
            raise ValueError('Unlikely original license plate dimensions')
        bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im)
        rgb=bg.convert('RGB');rgb.thumbnail((limit,limit),Image.Resampling.LANCZOS)
        out=io.BytesIO();rgb.save(out,'JPEG',quality=90,optimize=True,subsampling=0)
        return out.getvalue(),list(rgb.size)
def integrate(root,evidence):
    cfg=json.loads((root/BATCH).read_text())
    rows=cfg['rows']
    if (cfg['selected_count'],cfg['baseline_source_matched'],cfg['target_source_matched'],cfg['remaining_after'])!=(17,701,718,420):
        raise ValueError('Unexpected batch totals')
    if len(rows)!=17 or len({r['uid'] for r in rows})!=17 or len({r['image_xref'] for r in rows})!=17:
        raise ValueError('Ambiguous original image to immutable UID assignments')
    raw=(evidence/PDF).read_bytes()
    if len(raw)!=cfg['source_pdf_bytes'] or sha(raw)!=cfg['official_pdf_source_sha256']:
        raise ValueError('Source PDF byte/hash mismatch')
    harvest=json.loads((evidence/'manifest.json').read_text())
    matches=[x for x in harvest if x.get('url')==cfg['government_pdf_url']]
    if len(matches)!=1 or matches[0].get('status')!='downloaded' or matches[0].get('sha256')!=sha(raw):
        raise ValueError('Government harvest manifest mismatch')
    canon_rows=json.loads((root/'data/image-campaign/manifest.json').read_text())
    if len(canon_rows)!=1138 or len({x['uid'] for x in canon_rows})!=1138:
        raise ValueError('Original catalog changed')
    canon={x['uid']:x for x in canon_rows}
    manifest_path=root/'data/catalog-images.js';s=manifest_path.read_text()
    if not s.startswith(PREFIX):raise ValueError('Image map format changed')
    existing=json.loads(s[len(PREFIX):].strip().removesuffix(';'))
    if len(existing)!=701:raise ValueError('Baseline is no longer 701')
    assets={};new={};recon=[];all_y=[]
    pdf=fitz.open(stream=raw,filetype='pdf')
    try:
        if pdf.page_count!=1:raise ValueError('Expected one-page official form')
        page=pdf[0];valid_refs={x[0] for x in page.get_images(full=True)}
        for row in rows:
            uid=row['uid'];xref=row['image_xref'];cat=canon.get(uid)
            if not cat or cat['name']!=row['catalog_name'] or cat['jurisdiction_id']!='US-NJ' or uid in existing or uid in new:
                raise ValueError('Unknown, changed, or duplicated exact UID '+uid)
            if (row['match_status'],row['era_status'],row['human_approval'])!=('source_matched','unverified',False):
                raise ValueError('Forbidden approval claim '+uid)
            if xref not in valid_refs:raise ValueError('Original embedded source absent '+uid)
            rect=page.get_image_rects(xref)
            if len(rect)!=1 or rect[0].x0>40 or abs(rect[0].y0-row['image_y0'])>0.3:
                raise ValueError('Original PDF visual positioning drift '+uid)
            labels=page.search_for(row['official_form_label'])
            if not any(q.x0<110 and -11<(rect[0].y0-q.y1)<15 for q in labels):
                raise ValueError('PDF image not adjacent to its printed design label '+uid)
            original=pdf.extract_image(xref)
            if original['ext']!='jpeg':raise ValueError('Expected JPEG source object '+uid)
            b=original['image']
            extract=evidence/EXTRACT/f'p001_xref{xref}.jpeg'
            if sha(b)!=row['original_image_sha256'] or not extract.is_file() or b!=extract.read_bytes():
                raise ValueError('Original embedded source SHA/extraction differs '+uid)
            with Image.open(io.BytesIO(b)) as im:
                if list(im.size)!=[row['image_width_px'],row['image_height_px']]:
                    raise ValueError('Source dimensions changed '+uid)
            all_y.append(rect[0].y0)
            variants={}
            for kind,size in [('display',800),('thumbnail',300)]:
                path=f'assets/plates/{uid}-{kind}.jpg'
                if (root/path).exists() or path in assets:raise ValueError('Refuse overwrite '+path)
                data,shape=jpg(b,size);assets[path]=data
                variants[kind]=(sha(data),shape)
            new[uid]={'name':cat['name'],'image':f'./assets/plates/{uid}-display.jpg',
                'thumbnail':f'./assets/plates/{uid}-thumbnail.jpg',
                'source_sha256':sha(b),'source_url':cfg['government_pdf_url'],
                'source_asset_url':cfg['government_pdf_url']+f'#page=1&xref={xref}',
                'source_date':'2026-11-04','source_label':'MVC SP-100D: '+row['official_form_label'],
                'match_status':'source_matched','era_status':'unverified','human_approval':False,
                'project_use_basis':'owner_directed_fair_use_reference'}
            recon.append({'uid':uid,'name':cat['name'],'source_page_url':cfg['government_pdf_url'],
                'source_original_pdf_sha256':sha(raw),'pdf_page':1,'pdf_xref':xref,
                'official_form_label':row['official_form_label'],'original_image_sha256':sha(b),
                'original_image_bytes':len(b),'original_image_size':[row['image_width_px'],row['image_height_px']],
                'display_sha256':variants['display'][0],'display_size':variants['display'][1],
                'thumbnail_sha256':variants['thumbnail'][0],'thumbnail_size':variants['thumbnail'][1],
                'low_resolution_original':True,'match_status':'source_matched','era_status':'unverified',
                'human_approval':False,'commercial_rights_approval':False})
    finally:pdf.close()
    if all_y!=sorted(all_y) or len(assets)!=34 or len(existing)+len(new)!=718:
        raise ValueError('17 plate source ordering or derivative count changed')
    worker=root/'sw.js';sw=once(worker.read_text(),OLD,NEW)
    testpath=root/'tests/catalog-images.cjs';test=testpath.read_text()
    test=once(test,OLD,NEW)
    test=once(test,'assert.equal(cacheCount,1402)','assert.equal(cacheCount,1436)')
    test=once(test,"selectOption('US-NJ');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),1);",
        "selectOption('US-NJ');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),18);assert.equal(await page.locator('#researchResults .plate-image-pending').count(),20);")
    qp=root/'docs/CURRENT_IMAGE_CAMPAIGN_QUEUE.md';q=qp.read_text()
    for old,new_text in [
        ('**701 / 1,138 source-matched','**718 / 1,138 source-matched'),
        ('(61.60%)','(63.09%)'),
        ('**437 UIDs remain unresolved**','**420 UIDs remain unresolved**'),
        ('**1,402** public display/thumbnail','**1,436** public display/thumbnail'),
        ('CA-ON 39, NJ 1, ID 3.','CA-ON 39, NJ 18, ID 3.'),
        ('All 701 current image entries remain','All 718 current image entries remain'),
        ('| New Jersey | 37 |','| New Jersey | 20 |'),
        ('Remaining **437** distributed','Remaining **420** distributed'),
        ('## November 2 follow-up: official NJ MVC PDF artwork leads (not yet matched)',
         '## November 2-4 follow-up: official NJ MVC PDF artwork')
    ]:q=once(q,old,new_text)
    q=once(q,
      'A grid of actual plate artwork is **not verified**. Treat as historical textual evidence; no PDF source hash, illustration count, issue-era approval or design mapping is claimed.',
      'The downloaded PDF has 12 actual sports-plate illustrations on PDF page 10. These are source-pinned historical evidence only; no current catalog UID corresponds to a sports plate, so zero are integrated.')
    q=once(q,
      '- **Status:** Research leads only. 0 newly integrated UIDs from these documents; existing 701/1,138 and 437 unresolved unchanged. No original PDF SHA or derivative JPG was verified in this follow-up.',
      '- **2026-11-04 completed source matches:** 17 dedicated plate images integrated with original PDF SHA-256 9d6a73ed7e56b741af5ab7ccb1f11f44de575dada9103372a885a841ac8ffe67 and individually recorded embedded JPEG source hashes. 718 of 1138 mapped; 420 remain. The historical annual report SHA-256 is 1138083ba3139e75e09b8f287247ef4560a699d4a128425173fbd14bf438210b. Private source archive Library libfile_33529bf051ac819190e84b7e5c26d76c. Source image quality is low-resolution (100-135px wide); dates, final human approval and commercial rights remain unverified.')
    q=once(q,'## Current truth\n',
      '## Current truth\n- **2026-11-04 NJ MVC +17:** Official dedicated-plate form provides 17 source-matched original image objects (source PDF, image xref, page label, exact SHA-256). NJ now 18 mapped, 20 unresolved. Archive preserved privately; no human review or issue era approved.\n')
    recpath=root/'database/image-reconciliation-nj-mvc-form-20261104.json'
    if recpath.exists():raise ValueError('Refusing to overwrite existing reconciliation')
    for path,b in assets.items():
        p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    manifest_path.write_text(PREFIX+json.dumps(dict(sorted({**existing,**new}.items())),separators=(',',':'),ensure_ascii=False)+';\n')
    worker.write_text(sw);testpath.write_text(test);qp.write_text(q)
    recpath.write_text(json.dumps({'selected_count':17,'baseline_source_matched':701,'source_matched_total':718,
        'remaining':420,'government_pdf_original_sha256':cfg['official_pdf_source_sha256'],
        'private_library_archive':cfg['private_archive_library_file_id'],
        'historic_sports_plate_art_count_unmatched':12,'era_status':'unverified','human_approval':False,
        'rows':recon},indent=2,ensure_ascii=False)+'\n')
    return {'added':17,'total':718,'remaining':420,'jpeg_files_total':1436}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--evidence-dir',type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(integrate(a.root,a.evidence_dir.resolve()),indent=2))
