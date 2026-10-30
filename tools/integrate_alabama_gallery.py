#!/usr/bin/env python3
"""Integrate 28 visually reviewed Alabama Department of Revenue plate samples.

Original issuing-agency bytes are recovered from a previous private archive.
The precise archived source HTML/asset manifest are SHA-pinned and each
selected image original is checked against its recorded SHA. Does not promote
historical issue date, rights or user artwork approval.
"""
from __future__ import annotations
import argparse,base64,gzip,hashlib,io,json,pathlib
from PIL import Image,ImageOps
ROOT=pathlib.Path(__file__).resolve().parents[1]
REVIEW='data/image-batches/alabama-28-reviewed-20261029.json'
FOLDER='AL/Alabama_License_Plates_Archive_html'
OLD='lpg-current-images-20261029-nv84'
NEW='lpg-current-images-20261029-al28'
def sha(b):return hashlib.sha256(b).hexdigest()
def convert(raw,limit):
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        im=ImageOps.exif_transpose(im).convert('RGB')
        if im.width<90 or im.height<35 or not 1.35<=im.width/im.height<=3.8:
            raise ValueError(f'Suspicious image dimensions {im.size}')
        im.thumbnail((limit,limit),Image.Resampling.LANCZOS)
        out=io.BytesIO();im.save(out,'JPEG',quality=91,optimize=True,subsampling=0)
        return out.getvalue(),list(im.size)
def integrate(root,evidence):
    review=json.loads((root/REVIEW).read_text())
    rows=review['rows']
    if review['selected_count']!=28 or len(rows)!=28 or len({r['uid'] for r in rows})!=28:
        raise ValueError('Alabama reviewed manifest must be exactly 28 unique catalog UIDs')
    assets_file=evidence/FOLDER/'assets.json'
    html_file=evidence/FOLDER/'source.html'
    if sha(assets_file.read_bytes())!=review['assets_registry_sha256']:
        raise ValueError('Original Alabama agency image registry has changed')
    if sha(html_file.read_bytes())!=review['source_html_sha256']:
        raise ValueError('Original Alabama official page HTML changed')
    assets=json.loads(assets_file.read_text())
    assets={a['direct_image_url'].split('/')[-1].split('?')[0]:a for a in assets
            if a.get('status')=='downloaded' and
            a.get('source_page_url')==review['source_url'] and
            a.get('direct_image_url','').startswith('https://www.revenue.alabama.gov/')}
    if len(assets)<100:raise ValueError('Missing most official gallery image source assets')
    canonical=json.loads(gzip.decompress(base64.b64decode(b''.join(
        (root/f'data/catalog.part{i}.b64').read_bytes() for i in range(5)))))
    if len(canonical['plates'])!=review['expected_canonical_uids'] or len(canonical['plates'])!=1138:
        raise ValueError('Canonical catalog count drift')
    names={p['plate_uid']:p for p in canonical['plates']}
    path=root/'data/catalog-images.js';prefix='globalThis.LPG_CATALOG_IMAGES='
    content=path.read_text()
    if not content.startswith(prefix):raise ValueError('Unexpected catalog image manifest syntax')
    existing=json.loads(content[len(prefix):].strip().removesuffix(';'))
    if len(existing)!=608:raise ValueError(f'Expected existing 608 source matches, found {len(existing)}')
    output={};new={};rec=[]
    for item in rows:
        uid=item['uid'];filename=item['source_filename']
        if uid in existing or uid in new or not uid.startswith('LPG-US-AL-'):
            raise ValueError(f'Invalid/duplicate UID: {uid}')
        plate=names.get(uid)
        if not plate or plate['jurisdiction_id']!='US-AL':raise ValueError(f'Unrecognized canonical Alabama UID: {uid}')
        source=assets.get(filename)
        if not source:raise ValueError(f'Archived issuing-agency image not found: {filename}')
        orig_rel=source['file'].removeprefix('harvest-output/')
        file=(evidence/orig_rel).resolve()
        if not file.is_relative_to(evidence.resolve()) or not file.is_file():
            raise ValueError('Unsafe or missing official source path')
        original=file.read_bytes()
        digest=sha(original)
        if digest!=source['sha256']:raise ValueError(f'Official original image hash mismatch for {uid}')
        variants={};sizes={}
        for kind,limit in [('display',800),('thumbnail',300)]:
            data,dims=convert(original,limit)
            dest=f'assets/plates/{uid}-{kind}.jpg'
            if dest in output or (root/dest).exists():raise ValueError('Refusing image overwrite '+dest)
            output[dest]=data
            variants[kind]=sha(data);sizes[kind]=dims
        new[uid]={'name':plate['name'],'image':f'./assets/plates/{uid}-display.jpg',
            'thumbnail':f'./assets/plates/{uid}-thumbnail.jpg',
            'source_sha256':digest,'source_url':review['source_url'],
            'source_asset_url':source['direct_image_url'],'source_date':'2026-10-26',
            'source_label':filename,'match_status':'source_matched',
            'era_status':'unverified','human_approval':False,
            'project_use_basis':'owner_directed_fair_use_reference'}
        rec.append({'uid':uid,'name':plate['name'],'source_page_url':review['source_url'],
            'direct_asset_url':source['direct_image_url'],'original_file':orig_rel,
            'source_filename':filename,'source_original_sha256':digest,
            'source_archive_assets_manifest_sha256':review['assets_registry_sha256'],
            'match_basis':'reviewed original Alabama issuing agency gallery + exact plate depiction',
            'display_sha256':variants['display'],'thumbnail_sha256':variants['thumbnail'],
            'display_size':sizes['display'],'thumbnail_size':sizes['thumbnail'],
            'match_status':'source_matched','era_status':'unverified','human_approval':False})
    if len(new)!=28 or len(output)!=56 or len(existing)+len(new)!=636:
        raise ValueError('Unexpected result count')
    swfile=root/'sw.js';sw=swfile.read_text()
    if sw.count(OLD)!=1:raise ValueError('Unexpected service-worker cache version')
    testfile=root/'tests/catalog-images.cjs';test=testfile.read_text()
    old_test="assert.equal(await page.locator('#researchResults .plate-image-pending').count(),0);\nawait page.locator('#researchState').selectOption('US-WA');"
    new_test="assert.equal(await page.locator('#researchResults .plate-image-pending').count(),0);\nawait page.locator('#researchState').selectOption('US-AL');\nassert.equal(await page.locator('#researchResults .catalog-thumb').count(),28);\nassert((await page.locator('#researchSummary').textContent()).includes('28 sourced photos'));\nassert((await page.locator('#researchResults .plate-image-pending').count())==2);\nawait page.locator('#researchState').selectOption('US-WA');"
    if test.count(old_test)!=1 or test.count('assert.equal(cacheCount,1216)')!=1 or test.count(OLD)!=1:
        raise ValueError('Previous focused browser test changed')
    test=test.replace(old_test,new_test).replace('assert.equal(cacheCount,1216)','assert.equal(cacheCount,1272)').replace(OLD,NEW).replace('1216 cached images','1272 cached images')
    for rel,b in output.items():
        dest=root/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
    path.write_text(prefix+json.dumps(dict(sorted({**existing,**new}.items())),separators=(',',':'),ensure_ascii=False)+';\n')
    swfile.write_text(sw.replace(OLD,NEW));testfile.write_text(test)
    recfile=root/'database/image-reconciliation-al-20261029.json'
    recfile.write_text(json.dumps({'new_match_count':28,'source_matched_total':636,
        'unmatched_alabama_catalog_uids':review['known_unresolved'],'source_registry_sha256':review['assets_registry_sha256'],'rows':rec},indent=2)+'\n')
    print(json.dumps({'added':28,'total_source_selected':636,'total_runtime_jpegs':1272,'excluded':review['known_unresolved']}))
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=pathlib.Path,default=ROOT)
    ap.add_argument('--evidence-dir',type=pathlib.Path,required=True)
    args=ap.parse_args();integrate(args.root,args.evidence_dir.resolve())
if __name__=='__main__':main()
