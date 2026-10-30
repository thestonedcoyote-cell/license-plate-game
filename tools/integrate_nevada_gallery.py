#!/usr/bin/env python3
"""Integrate only 84 explicitly mapped, source-hashed Nevada DMV plate samples.

The frozen archive includes raw government gallery image files and associated
source HTML. Source-image correspondence is pinned by UID + gallery filename;
each original image SHA-256 is verified against the SHA-pinned harvest registry.
No human review, independent copyright permission or historical era verification
is implied by source matching.
"""
from __future__ import annotations
import argparse, base64, gzip, hashlib, io, json, pathlib
import cairosvg
from PIL import Image, ImageOps

ROOT=pathlib.Path(__file__).resolve().parents[1]
REVIEW='data/image-batches/nevada-84-reviewed-20261029.json'
OLD_CACHE='lpg-current-images-20261027-ne22'
NEW_CACHE='lpg-current-images-20261029-nv84'
SOURCE_FOLDER='NV/Nevada_DMV_License_Plates_html'

def sha(data): return hashlib.sha256(data).hexdigest()

def output_jpeg(image, max_w):
    image=ImageOps.exif_transpose(image).convert('RGB')
    if image.width<90 or image.height<35 or not 1.35<=image.width/image.height<=3.8:
        raise ValueError(f'Unexpected plate sample image dimensions {image.size}')
    target=image.copy()
    target.thumbnail((max_w,max_w),Image.Resampling.LANCZOS)
    out=io.BytesIO()
    target.save(out,'JPEG',quality=90,optimize=True,subsampling=0)
    return out.getvalue(),list(target.size)

def source_image(raw,filename):
    if filename.lower().endswith('.svg'):
        # The official SVG plate art has 400x190 intrinsic dimensions and inline artwork.
        png=cairosvg.svg2png(bytestring=raw)
        with Image.open(io.BytesIO(png)) as img:
            img.load()
            return img.copy()
    with Image.open(io.BytesIO(raw)) as img:
        img.load()
        return img.copy()

def integrate(root,evidence):
    review=json.loads((root/REVIEW).read_text())
    rows=review['rows']
    if review['selected_count']!=84 or len(rows)!=84 or len({r['uid'] for r in rows})!=84:
        raise ValueError('Review not 84 distinct Nevada immutable UIDs')
    if review['expected_prior_source_matches']!=524:
        raise ValueError('Unexpected previous selection count')
    folder=evidence/SOURCE_FOLDER
    mf=folder/'assets.json'
    html=folder/'source.html'
    if sha(mf.read_bytes())!=review['archived_assets_json_sha256']:
        raise ValueError('Nevada archived asset registry hash mismatch')
    if sha(html.read_bytes())!=review['archived_source_html_sha256']:
        raise ValueError('Nevada archived source HTML hash mismatch')
    sources=json.loads(mf.read_text())
    assets={x['direct_image_url'].rsplit('/',1)[-1].split('?',1)[0]:x
        for x in sources if x.get('status')=='downloaded' and
        x.get('direct_image_url','').startswith('https://dmv.nv.gov/images/platesmain/')}
    if len(assets)<90: raise ValueError('Incomplete Nevada gallery archive')
    catalog_bytes=gzip.decompress(base64.b64decode(b''.join(
        (root/f'data/catalog.part{i}.b64').read_bytes() for i in range(5))))
    cat=json.loads(catalog_bytes)
    if len(cat['plates'])!=1138 or review['expected_original_catalog_uids']!=1138:
        raise ValueError('Immutable 1138 design catalog changed')
    canonical={p['plate_uid']:p for p in cat['plates']}
    selected_path=root/'data/catalog-images.js'
    prefix='globalThis.LPG_CATALOG_IMAGES='
    content=selected_path.read_text()
    if not content.startswith(prefix):raise ValueError('Unexpected current image map representation')
    existing=json.loads(content[len(prefix):].strip().removesuffix(';'))
    if len(existing)!=524:raise ValueError(f'Previous selection count {len(existing)} differs from 524')
    new={};copies={};recon=[]
    expected_source_hashes={}
    for row in rows:
        uid=row['uid'];filename=row['source_filename']
        if uid in existing or uid in new or not uid.startswith('LPG-US-NV-'):
            raise ValueError(f'UID already linked or invalid: {uid}')
        p=canonical.get(uid)
        if not p or p['jurisdiction_id']!='US-NV':raise ValueError(f'Noncanonical Nevada ID {uid}')
        source=assets.get(filename)
        if source is None: raise ValueError(f'Missing pinned official gallery asset: {filename}')
        direct_url='https://dmv.nv.gov/images/platesmain/'+filename
        if source['direct_image_url']!=direct_url or source['source_page_url']!=review['source_url']:
            raise ValueError(f'Official URL provenance mismatch for {uid}')
        candidate=source['file'].removeprefix('harvest-output/')
        file=(evidence/candidate).resolve()
        if not file.is_relative_to(evidence.resolve()) or not file.is_file():
            raise ValueError(f'Unsafe or missing evidence file: {candidate}')
        raw=file.read_bytes()
        raw_hash=sha(raw)
        if raw_hash!=source['sha256']:raise ValueError(f'Original source image SHA drift: {uid}')
        expected_source_hashes[uid]=raw_hash
        img=source_image(raw,filename)
        generated={};sizes={}
        for kind,max_w in [('display',800),('thumbnail',300)]:
            data,size=output_jpeg(img,max_w)
            path=f'assets/plates/{uid}-{kind}.jpg'
            if (root/path).exists() or path in copies:raise ValueError(f'Image overwrite: {path}')
            copies[path]=data
            generated[kind]=sha(data);sizes[kind]=size
        new[uid]={
            'name':p['name'],'image':f'./assets/plates/{uid}-display.jpg',
            'thumbnail':f'./assets/plates/{uid}-thumbnail.jpg',
            'source_sha256':raw_hash,'source_url':review['source_url'],
            'source_asset_url':direct_url,'source_date':'2026-10-26',
            'source_label':filename,'match_status':'source_matched',
            'era_status':'unverified','human_approval':False,
            'project_use_basis':'owner_directed_fair_use_reference'}
        recon.append({'uid':uid,'name':p['name'],'source_page_url':review['source_url'],
            'direct_asset_url':direct_url,'source_filename':filename,
            'source_original_sha256':raw_hash,'source_asset_file':candidate,
            'archived_assets_json_sha256':review['archived_assets_json_sha256'],
            'source_match_basis':'visual plate gallery inspection + exact filename + catalog design name',
            'display_sha256':generated['display'],'thumbnail_sha256':generated['thumbnail'],
            'display_size':sizes['display'],'thumbnail_size':sizes['thumbnail'],
            'match_status':'source_matched','era_status':'unverified','human_approval':False})
    shared={}
    for uid,h in expected_source_hashes.items():
        shared.setdefault(h,[]).append(uid)
    actual_aliases=sorted(sorted(v) for v in shared.values() if len(v)>1)
    expected_aliases=sorted(sorted(v) for v in review['intentional_aliases'])
    if actual_aliases!=expected_aliases or len(shared)!=82:
        raise ValueError(f'Unreviewed duplicate imagery: {actual_aliases}')
    if len(existing)+len(new)!=608 or len(copies)!=168:
        raise ValueError('Wrong total: expected 608 mapped plates, 168 new JPEGs')
    sw_path=root/'sw.js'
    sw=sw_path.read_text()
    if sw.count(OLD_CACHE)!=1:raise ValueError('Offline cache changed; adjust carefully')
    test_path=root/'tests/catalog-images.cjs'
    tests=test_path.read_text()
    old_state="await page.locator('#researchState').selectOption('US-NV');\nassert.equal(await page.locator('#researchResults .catalog-thumb').count(),0);\nassert((await page.locator('#researchSummary').textContent()).includes('0 sourced photos'));\nassert((await page.locator('#researchResults .plate-image-pending').count())>0);"
    new_state="await page.locator('#researchState').selectOption('US-NV');\nassert.equal(await page.locator('#researchResults .catalog-thumb').count(),84);\nassert((await page.locator('#researchSummary').textContent()).includes('84 sourced photos'));\nassert.equal(await page.locator('#researchResults .plate-image-pending').count(),0);"
    if old_state not in tests or tests.count(OLD_CACHE)!=1 or tests.count('assert.equal(cacheCount,1048)')!=1:
        raise ValueError('Focused browser test no longer matches pinned previous state')
    tests=tests.replace(old_state,new_state).replace(OLD_CACHE,NEW_CACHE).replace('assert.equal(cacheCount,1048)','assert.equal(cacheCount,1216)')
    tests=tests.replace('1048 cached images','1216 cached images')
    for rel,data in copies.items():
        target=root/rel;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
    selected_path.write_text(prefix+json.dumps(dict(sorted({**existing,**new}.items())),ensure_ascii=False,separators=(',',':'))+';\n')
    sw_path.write_text(sw.replace(OLD_CACHE,NEW_CACHE))
    test_path.write_text(tests)
    dest=root/'database/image-reconciliation-nv-20261029.json'
    dest.write_text(json.dumps({'selected_count':84,'total_selected':608,'source_manifest_sha256':review['archived_assets_json_sha256'],
        'intentional_aliases':actual_aliases,'rows':recon},indent=2)+'\n')
    print(json.dumps({'selected':84,'new_image_files':len(copies),
        'total_source_matched':608,'source_unique':len(shared),
        'intentionally_shared_aliases':actual_aliases,
        'source_asset_manifest_sha256':review['archived_assets_json_sha256']}))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=pathlib.Path,default=ROOT)
    ap.add_argument('--evidence-dir',type=pathlib.Path,required=True)
    args=ap.parse_args()
    integrate(args.root,args.evidence_dir.resolve())
if __name__=='__main__':main()
