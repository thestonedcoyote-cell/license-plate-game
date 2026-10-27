#!/usr/bin/env python3
"""Pin 22 Nebraska DMV 2023 sample images by 26-page source hash, xref and caption."""
from __future__ import annotations
import argparse,base64,gzip,hashlib,io,json,pathlib
import fitz
from PIL import Image,ImageOps

ROOT=pathlib.Path(__file__).resolve().parents[1]
OLD='lpg-current-images-20261027-sourcelabels'
NEW='lpg-current-images-20261027-ne22'
BATCH='data/image-batches/nebraska-2023-reviewed-20261027.json'

def digest(b):return hashlib.sha256(b).hexdigest()
def norm(x):return ' '.join(str(x).casefold().split())

def integrate(root,pdf):
    review=json.loads((root/BATCH).read_text(encoding='utf-8'));rows=review['rows']
    if review['selected_count']!=22 or len(rows)!=22 or len({r['uid'] for r in rows})!=22:raise ValueError('Expected exactly 22 reviewed UIDs')
    source=pdf.read_bytes()
    if digest(source)!=review['source_document_sha256']:raise ValueError('Source PDF SHA-256 drift')
    doc=fitz.open(stream=source,filetype='pdf')
    if len(doc)!=26:raise ValueError('Official PDF page count changed')
    mf=root/'data/catalog-images.js';prefix='globalThis.LPG_CATALOG_IMAGES='
    text=mf.read_text(encoding='utf-8')
    if not text.startswith(prefix):raise ValueError('Unknown image manifest')
    existing=json.loads(text[len(prefix):].strip().removesuffix(';'))
    if len(existing)!=502:raise ValueError('Prior app image count not 502')
    cat=json.loads(gzip.decompress(base64.b64decode(b''.join((root/f'data/catalog.part{i}.b64').read_bytes() for i in range(5)))))
    catalog={p['plate_uid']:p for p in cat['plates']}
    if len(catalog)!=1138:raise ValueError('Canonical catalog changed')
    selected={};recon=[];output={}
    for r in rows:
        uid=r['uid'];name=r['name']
        if not uid.startswith('LPG-US-NE-') or uid in selected or uid in existing:raise ValueError('Duplicate/invalid Nebraska ID: '+uid)
        if catalog.get(uid,{}).get('name')!=name or catalog[uid]['jurisdiction_id']!='US-NE':raise ValueError('Frozen catalog name/UID mismatch: '+uid)
        if r['match_status']!='source_matched' or r['era_status']!='unverified' or r['human_approval'] is not False:raise ValueError('Approval unexpectedly present')
        page=doc[int(r['manual_page'])-1];xref=int(r['source_xref'])
        if norm(r['source_printed_caption']) not in norm(page.get_text()):raise ValueError('Official source caption missing: '+uid)
        rectangles=page.get_image_rects(xref)
        if len(rectangles)!=1:raise ValueError('Unclear image position: '+uid)
        rect=rectangles[0]
        if not(rect.x0>=55 and rect.x1<=235 and 1.7<rect.width/rect.height<2.4):raise ValueError('Unlikely left-column plate image: '+uid)
        raw=doc.extract_image(xref)
        if digest(raw['image'])!=r['source_embedded_image_sha256']:raise ValueError('Official source plate image SHA changed: '+uid)
        with Image.open(io.BytesIO(raw['image'])) as im:
            source_image=ImageOps.exif_transpose(im).convert('RGB');w,h=source_image.size
        if w<200 or h<95 or not 1.7<w/h<2.4:raise ValueError('Unlikely plate aspect/resolution: '+uid)
        sizes={};hashes={};paths={}
        for kind,width in [('display',800),('thumbnail',300)]:
            image=source_image.copy();image.thumbnail((width,width),Image.Resampling.LANCZOS)
            buf=io.BytesIO();image.save(buf,'JPEG',quality=88,optimize=True,subsampling=0)
            path=root/'assets/plates'/f'{uid}-{kind}.jpg'
            if path.exists():raise ValueError('Refusing to overwrite previous image: '+uid)
            output[path]=buf.getvalue();sizes[kind]=list(image.size);hashes[kind]=digest(output[path]);paths[kind]='./assets/plates/'+path.name
        selected[uid]={'name':name,'image':paths['display'],'thumbnail':paths['thumbnail'],
          'source_sha256':r['source_embedded_image_sha256'],'source_document_sha256':review['source_document_sha256'],
          'source_url':review['official_pdf_url'],'source_date':'2026-10-27','match_status':'source_matched',
          'era_status':'unverified','human_approval':False,'project_use_basis':'owner_directed_fair_use_reference',
          'manual_page':r['manual_page'],'source_caption':r['source_printed_caption']}
        recon.append({'uid':uid,'name':name,'source_pdf_url':review['official_pdf_url'],
          'source_document_sha256':review['source_document_sha256'],'source_pdf_page':r['manual_page'],
          'source_xref':xref,'source_image_rect':[round(float(x),4) for x in rect],
          'source_printed_caption':r['source_printed_caption'],'source_embedded_image_sha256':r['source_embedded_image_sha256'],
          'match_basis':r['evidence_method'],'match_status':'source_matched','era_status':'unverified',
          'human_approval':False,'project_use_basis':'owner_directed_fair_use_reference',
          'display_sha256':hashes['display'],'thumbnail_sha256':hashes['thumbnail'],
          'display_size':sizes['display'],'thumbnail_size':sizes['thumbnail']})
    if len(selected)!=22 or len(output)!=44:raise ValueError('Incorrect output count')
    merged=dict(sorted({**existing,**selected}.items()))
    if len(merged)!=524:raise ValueError('Expected 524 source-matched plates')
    sw=root/'sw.js';sw_content=sw.read_text()
    if sw_content.count(OLD)!=1:raise ValueError('Unrecognized service worker version')
    testpath=root/'tests/catalog-images.cjs';test=testpath.read_text()
    marker="await page.locator('#researchState').selectOption('US-NV');"
    if test.count(OLD)!=1 or test.count(marker)!=1 or test.count('assert.equal(cacheCount,1004)')!=1:raise ValueError('Image test needs manual review')
    test=test.replace(marker,"await page.locator('#researchState').selectOption('US-NE');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),22);"+marker)
    test=test.replace(OLD,NEW).replace('assert.equal(cacheCount,1004)','assert.equal(cacheCount,1048)')
    for p,data in output.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    mf.write_text(prefix+json.dumps(merged,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    sw.write_text(sw_content.replace(OLD,NEW));testpath.write_text(test)
    (root/'database/image-reconciliation-ne-20261027.json').write_text(json.dumps(recon,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'new_reviewed_Nebraska':22,'total_image_samples':524,'new_JPEGs':44,'excluded_uid':review['exclusions'][0]['uid']},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--pdf',type=pathlib.Path,required=True);ap.add_argument('--root',type=pathlib.Path,default=ROOT)
    a=ap.parse_args();integrate(a.root.resolve(),a.pdf)
