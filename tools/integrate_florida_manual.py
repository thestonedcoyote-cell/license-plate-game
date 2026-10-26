#!/usr/bin/env python3
"""Pinned official FLHSMV 2026 brochure -> 132 immutable Florida plate-image samples.

Only accepts individually mapped xrefs/captions/sha256. This records source
matches, not human art approvals, established issue dates, or licenses.
"""
from __future__ import annotations
import argparse, base64, gzip, hashlib, io, json
from pathlib import Path

import fitz
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_CACHE = 'lpg-current-images-20261026-cawi'
NEXT_CACHE = 'lpg-current-images-20261026-fl'
MANIFEST_PREFIX = 'globalThis.LPG_CATALOG_IMAGES='

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def render(raw: bytes, max_dim: int):
    with Image.open(io.BytesIO(raw)) as inp:
        img = ImageOps.exif_transpose(inp)
        img.load()
        if img.width < 100 or img.height < 45 or not 1.35 < img.width/img.height < 4.5:
            raise ValueError(f'Not recognizable plate artwork dimensions: {img.size}')
        img = img.convert('RGB')
        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        result_size = img.size
        buf = io.BytesIO()
        img.save(buf, 'JPEG', quality=90, optimize=True, subsampling=0)
        return buf.getvalue(), result_size

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--mapping', type=Path, default=None)
    ap.add_argument('--pdf', type=Path, required=True, help='Exact Florida 2026 PDF from official harvested evidence (private)')
    args = ap.parse_args()
    root = args.root.resolve()
    reviewed = args.mapping or root/'data/image-batches/florida-manual-reviewed-20261026.json'
    frozen = json.loads(reviewed.read_text(encoding='utf-8'))
    rows = frozen['rows']
    if frozen['selected_count'] != 132 or len(rows)!=132 or len({r['uid'] for r in rows})!=132:
        raise ValueError('Expected precisely 132 unique reviewed Florida UIDs')
    source_pdf = args.pdf.read_bytes()
    if sha(source_pdf) != frozen['source_sha256'] or len(frozen['source_sha256'])!=64:
        raise ValueError('Unexpected official PDF hash: no substituting altered document')
    doc = fitz.open(stream=source_pdf, filetype='pdf')
    if len(doc) != frozen['source_pages'] or len(doc)!=27:
        raise ValueError('Source PDF pages changed')
    old_js = (root/'data/catalog-images.js').read_text(encoding='utf-8')
    if not old_js.startswith(MANIFEST_PREFIX):
        raise ValueError('Unexpected app source-image JS manifest format')
    prior = json.loads(old_js[len(MANIFEST_PREFIX):].strip().removesuffix(';'))
    if len(prior)!=370 or any(u.startswith('LPG-US-FL-') for u in prior):
        raise ValueError('Baseline is not 370 existing selections or Florida already integrated')
    catalog = json.loads(gzip.decompress(base64.b64decode(''.join((root/f'data/catalog.part{i}.b64').read_text(encoding='utf-8') for i in range(5)))))
    catalog_by_uid = {p['plate_uid']:p for p in catalog['plates']}
    if len(catalog_by_uid)!=1138 or len(catalog['plates'])!=1138:
        raise ValueError('Frozen canonical catalog changed')
    fl_uid_set={uid for uid,p in catalog_by_uid.items() if p['jurisdiction_id']=='US-FL'}
    if len(fl_uid_set)!=132 or {r['uid'] for r in rows} != fl_uid_set:
        raise ValueError('The official plate mapping does not cover the full immutable Florida catalog')
    swfile=root/'sw.js'; sw=swfile.read_text(encoding='utf-8')
    testfile=root/'tests/catalog-images.cjs'; test=testfile.read_text(encoding='utf-8')
    if sw.count(PREVIOUS_CACHE)!=1 or test.count(PREVIOUS_CACHE)!=1 or test.count('assert.equal(cacheCount,740)')!=1:
        raise ValueError('Prior cache/current functional regression changed: review before updating')
    needle="await page.locator('#researchState').selectOption('US-WI');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),31);"
    if test.count(needle)!=1:
        raise ValueError('Existing source image region regression changed: stop before generating')
    candidates={}; records=[]; all_selected=dict(prior)
    for item in sorted(rows,key=lambda r:r['uid']):
        uid=item['uid']; catalog_plate=catalog_by_uid.get(uid)
        if uid in all_selected or not catalog_plate or catalog_plate['name']!=item['name']:
            raise ValueError(f'Unknown, duplicate or mislabeled canonical UID: {uid}')
        if item['era_status']!='unverified' or item['human_approval'] is not False:
            raise ValueError('Source images are not approved for historical issue eras or final review')
        page=doc[item['pdf_page']-1]
        if not any(img[0]==item['xref'] for img in page.get_images(full=True)):
            raise ValueError(f'Image xref {item["xref"]} not on PDF page {item["pdf_page"]} for {uid}')
        rects=page.get_image_rects(item['xref'])
        expected=fitz.Rect(item['image_rect'])
        if not any(max(abs(a-b) for a,b in zip(tuple(rc),tuple(expected)))<0.03 for rc in rects):
            raise ValueError(f'Image visual position drift for {uid}')
        pic=doc.extract_image(item['xref'])['image']
        if sha(pic)!=item['source_image_sha256']:
            raise ValueError(f'Embedded official source artwork hash drift for {uid}')
        detail={'uid':uid,'name':item['name'],'source_pdf_url':frozen['source_url'],'source_document_sha256':frozen['source_sha256'],
            'source_embedded_image_sha256':sha(pic),'source_pdf_page':item['pdf_page'],'source_xref':item['xref'],
            'source_image_rect':item['image_rect'],'source_printed_caption':item['printed_caption'],
            'match_basis':'inspected 2026 FLHSMV official sample and positional printed-caption association',
            'match_status':'source_matched','era_status':'unverified','human_approval':False,
            'project_use_basis':'owner_directed_fair_use_reference'}
        for kind,limit in [('display',800),('thumbnail',300)]:
            output,size=render(pic,limit)
            rel=f'assets/plates/{uid}-{kind}.jpg'
            if (root/rel).exists():raise ValueError(f'Would overwrite existing runtime artwork: {rel}')
            candidates[rel]=output
            detail[kind+'_sha256']=sha(output)
            detail[kind+'_size']=list(size)
        records.append(detail)
        all_selected[uid]={'name':item['name'],'image':f'./assets/plates/{uid}-display.jpg',
            'thumbnail':f'./assets/plates/{uid}-thumbnail.jpg',
            'source_sha256':sha(pic),'source_document_sha256':frozen['source_sha256'],
            'source_url':frozen['source_url'],'source_date':'2026-10-26',
            'match_status':'source_matched','era_status':'unverified','human_approval':False,
            'project_use_basis':'owner_directed_fair_use_reference',
            'manual_page':item['pdf_page'],'source_caption':item['printed_caption']}
    if len(records)!=132 or len(candidates)!=264 or len(all_selected)!=502:
        raise ValueError('Counts did not reconcile to 502 selected images')
    # Serialize only after validating all source bytes and existing app state.
    for rel,data in candidates.items():
        file=root/rel;file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(data)
    (root/'data/catalog-images.js').write_text(MANIFEST_PREFIX+json.dumps(dict(sorted(all_selected.items())),ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    swfile.write_text(sw.replace(PREVIOUS_CACHE,NEXT_CACHE),encoding='utf-8')
    test=test.replace(needle,needle+"await page.locator('#researchState').selectOption('US-FL');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),132);")
    test=test.replace(PREVIOUS_CACHE,NEXT_CACHE).replace('assert.equal(cacheCount,740)','assert.equal(cacheCount,1004)')
    test=test.replace('740 cached images','1004 cached images').replace('740 staged JPEGs','1004 staged JPEGs')
    testfile.write_text(test,encoding='utf-8')
    out=root/'database/image-reconciliation-fl-20261026.json'
    out.write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'official_document_sha256':sha(source_pdf),'new_florida_selections':len(records),
       'previous_app_selections':len(prior),'current_selections':len(all_selected),'remaining':1138-len(all_selected),
       'added_jpegs':len(candidates),'total_expected_jpegs':1004,
       'status':'source_matched__era_unverified__human_approval_false'},indent=2))

if __name__=='__main__':main()