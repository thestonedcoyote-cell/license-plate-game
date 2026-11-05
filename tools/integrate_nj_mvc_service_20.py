#!/usr/bin/env python3
"""Integrate 20 exact official NJ MVC service-organization plate source images.
No government originals, unknown issuance eras or rights approvals are published.
"""
import argparse,hashlib,io,json,pathlib
from PIL import Image,ImageOps
ROOT=pathlib.Path(__file__).resolve().parents[1]
CONFIG='data/image-batches/nj-mvc-service-20-reviewed-20261104.json'
OLD='lpg-current-images-20261104-njmvc17'
NEW='lpg-current-images-20261104-njservice20'
PREFIX='globalThis.LPG_CATALOG_IMAGES='

def sha(b):return hashlib.sha256(b).hexdigest()
def once(text,old,new):
    if text.count(old)!=1 or new in text:
        raise ValueError('Baseline changed or new marker already exists: '+old[:100])
    return text.replace(old,new)
def convert(raw,limit):
    with Image.open(io.BytesIO(raw)) as source:
        source.load()
        if source.format!='GIF' or source.n_frames!=1:
            raise ValueError('Expected one-frame official GIF sample')
        im=ImageOps.exif_transpose(source).convert('RGBA')
        if im.width<200 or im.height<90 or not (1.35<=im.width/im.height<=3.8):
            raise ValueError('Unlikely government plate illustration dimensions')
        white=Image.new('RGBA',im.size,'white');white.alpha_composite(im)
        rgb=white.convert('RGB');rgb.thumbnail((limit,limit),Image.Resampling.LANCZOS)
        dst=io.BytesIO();rgb.save(dst,'JPEG',quality=90,optimize=True,subsampling=0)
        return dst.getvalue(),list(rgb.size)

def integrate(root,evidence):
    cfg=json.loads((root/CONFIG).read_text())
    rows=cfg['rows']
    if (cfg['selected_count'],cfg['baseline_source_matched'],cfg['target_source_matched'],cfg['remaining_after'])!=(20,718,738,400):
        raise ValueError('Batch scope changed')
    if len(rows)!=20 or len({r['uid'] for r in rows})!=20 or len({r['source_asset_number'] for r in rows})!=20:
        raise ValueError('Expected 20 distinct sources and catalog UIDs')
    gallery=evidence/cfg['source_gallery_folder']
    registry=(gallery/'assets.json').read_bytes()
    html=(gallery/'source.html').read_bytes()
    if sha(registry)!=cfg['official_asset_registry_sha256'] or sha(html)!=cfg['official_html_sha256']:
        raise ValueError('Official HTML or source-asset registry SHA changed')
    original_records=json.loads(registry)
    if len(original_records)!=20 or any(r['status']!='downloaded' for r in original_records):
        raise ValueError('Expected exactly 20 downloaded MVC originals')
    harvest=json.loads((evidence/'manifest.json').read_text())
    source=[x for x in harvest if x.get('url')==cfg['source_page_url']]
    if len(source)!=1 or source[0]['status']!='downloaded':
        raise ValueError('Expected original issuing-agency gallery harvest')
    canonrows=json.loads((root/'data/image-campaign/manifest.json').read_text())
    if len(canonrows)!=1138 or len({p['uid'] for p in canonrows})!=1138:
        raise ValueError('Immutable plate catalog changed')
    canon={p['uid']:p for p in canonrows}
    mf=root/'data/catalog-images.js'
    existing_code=mf.read_text()
    if not existing_code.startswith(PREFIX):raise ValueError('Unexpected image catalog format')
    existing=json.loads(existing_code[len(PREFIX):].strip().removesuffix(';'))
    if len(existing)!=718:raise ValueError('Baseline source-matched image count is no longer 718')
    output={};new={};recon=[]
    for row in rows:
        uid=row['uid'];p=canon.get(uid)
        n=row['source_asset_number']
        rec=original_records[n-1]
        if not p or p['name']!=row['catalog_name'] or p['jurisdiction_id']!='US-NJ' or uid in existing or uid in new:
            raise ValueError('Unknown, duplicated or shifted canonical UID '+uid)
        if (row['match_status'],row['era_status'],row['human_approval'])!=('source_matched','unverified',False):
            raise ValueError('Unreviewed issue-era or human approval claimed')
        filename=f'asset_{n:04d}.gif'
        if (rec['status']!='downloaded' or rec.get('alt_text')!=row['official_page_alt_text']
            or rec.get('source_page_url')!=cfg['source_page_url']
            or not rec.get('direct_image_url','').startswith('https://www.nj.gov/mvc/images/')
            or pathlib.Path(rec.get('file','')).name!=filename
            or rec.get('same_host') is not True):
            raise ValueError('Original government asset filename / label / URL mismatch '+uid)
        original=(gallery/filename).resolve()
        if not original.is_relative_to(evidence.resolve()):raise ValueError('Untrusted archived source path')
        binary=original.read_bytes()
        if len(binary)!=rec['bytes'] or sha(binary)!=rec['sha256']:
            raise ValueError('Original government GIF SHA-256 changed '+uid)
        with Image.open(io.BytesIO(binary)) as src:
            if src.format!='GIF' or src.n_frames!=1 or list(src.size)!=[rec['width_px'],rec['height_px']]:
                raise ValueError('Official sample dimensions or filetype changed '+uid)
        variants={}
        for kind,limit in [('display',800),('thumbnail',300)]:
            path=f'assets/plates/{uid}-{kind}.jpg'
            if (root/path).exists() or path in output:raise ValueError('Would overwrite existing image '+path)
            jpg,shape=convert(binary,limit);output[path]=jpg
            variants[kind]=(sha(jpg),shape)
        new[uid]={
            'name':p['name'],'image':f'./assets/plates/{uid}-display.jpg',
            'thumbnail':f'./assets/plates/{uid}-thumbnail.jpg',
            'source_sha256':sha(binary),'source_url':cfg['source_page_url'],
            'source_asset_url':rec['direct_image_url'],'source_date':'2026-11-04',
            'source_label':row['official_page_alt_text']+' — '+row['visually_checked_bottom_rim_text'],
            'match_status':'source_matched','era_status':'unverified','human_approval':False,
            'project_use_basis':'owner_directed_fair_use_reference'}
        recon.append({'uid':uid,'name':p['name'],'source_label':row['official_page_alt_text'],
            'visual_plate_rim':row['visually_checked_bottom_rim_text'],
            'source_page_url':cfg['source_page_url'],'direct_asset_url':rec['direct_image_url'],
            'archived_html_sha256':cfg['official_html_sha256'],
            'archived_source_registry_sha256':cfg['official_asset_registry_sha256'],
            'source_original_sha256':sha(binary),'source_original_bytes':len(binary),
            'source_asset_archive_member':cfg['source_gallery_folder']+'/'+filename,
            'original_size':[rec['width_px'],rec['height_px']],
            'display_sha256':variants['display'][0],'display_size':variants['display'][1],
            'thumbnail_sha256':variants['thumbnail'][0],'thumbnail_size':variants['thumbnail'][1],
            'match_status':'source_matched','era_status':'unverified','human_approval':False,
            'commercial_rights_approval':False})
    if len(output)!=40 or len(existing)+len(new)!=738 or len({r['source_original_sha256'] for r in recon})!=20:
        raise ValueError('Unreviewed source identity collision or image count')
    worker=root/'sw.js';sw=once(worker.read_text(),OLD,NEW)
    testpath=root/'tests/catalog-images.cjs';tests=testpath.read_text()
    tests=once(tests,OLD,NEW)
    tests=once(tests,'assert.equal(cacheCount,1436)','assert.equal(cacheCount,1476)')
    tests=once(tests,"selectOption('US-NJ');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),18);assert.equal(await page.locator('#researchResults .plate-image-pending').count(),20);",
        "selectOption('US-NJ');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),38);assert.equal(await page.locator('#researchResults .plate-image-pending').count(),0);")
    queue=root/'docs/CURRENT_IMAGE_CAMPAIGN_QUEUE.md';q=queue.read_text()
    for old,new_str in [
        ('**Verified November 2, 2026.**','**Verified November 4, 2026.**'),
        ('**718 / 1,138 source-matched','**738 / 1,138 source-matched'),
        ('(63.09%)','(64.85%)'),
        ('**420 UIDs remain unresolved**','**400 UIDs remain unresolved**'),
        ('**1,436** public display/thumbnail','**1,476** public display/thumbnail'),
        ('CA-ON 39, NJ 18, ID 3.','CA-ON 39, NJ 38, ID 3.'),
        ('All 718 current image entries remain','All 738 current image entries remain'),
        ('| New Jersey | 20 |','| New Jersey | 0 |'),
        ('Remaining **420** distributed','Remaining **400** distributed')
    ]:q=once(q,old,new_str)
    q=once(q,'## Current truth\n',
        '## Current truth\n- **2026-11-04 NJ MVC service organizations +20:** all 20 remaining New Jersey immutable design UIDs source-matched by official named MVC original GIFs, individually SHA-pinned with source page registry/HTML hashes. Total NJ 38/38, no unmatched NJ designs; 40 reproducible display/thumbnail JPGs added. Originals archived privately at Library libfile_6115422589ac8191987c2eefe051841d. All issue-era/human-review/rights approvals unverified.\n')
    q=once(q,'718 of 1138 mapped; 420 remain.',
        '718 mapped after the form PDF batch; a subsequent MVC service-organization batch brings the current total to 738/1138 with 400 remaining.')
    rec=root/'database/image-reconciliation-nj-mvc-service-20261104.json'
    if rec.exists():raise ValueError('Would overwrite reconciliation')
    for name,b in output.items():
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b)
    mf.write_text(PREFIX+json.dumps(dict(sorted({**existing,**new}.items())),separators=(',',':'),ensure_ascii=False)+';\n')
    worker.write_text(sw);testpath.write_text(tests);queue.write_text(q)
    rec.write_text(json.dumps({'selected_count':20,'baseline_source_matched':718,
        'source_matched_total':738,'remaining':400,'jurisdiction':'US-NJ',
        'official_registry_sha256':cfg['official_asset_registry_sha256'],
        'source_html_sha256':cfg['official_html_sha256'],
        'private_library_archive_id':cfg['private_source_archive_library_file_id'],
        'harvest_run':cfg['harvest_run_id'],'era_status':'unverified','human_approval':False,
        'rows':recon},indent=2,ensure_ascii=False)+'\n')
    return {'added':20,'mapped_total':738,'remaining':400,'NJ_mapped':38,'derivatives_total':1476}
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=pathlib.Path,default=ROOT)
    ap.add_argument('--evidence-dir',type=pathlib.Path,required=True)
    a=ap.parse_args()
    print(json.dumps(integrate(a.root,a.evidence_dir.resolve()),indent=2))
