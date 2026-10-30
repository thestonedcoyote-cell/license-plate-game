#!/usr/bin/env python3
"""Source-pinned integration for 22 Michigan SOS + 39 ServiceOntario plates.

Every image is checked against its official harvest SHA; the archived source
page HTML and gallery asset registry are independently SHA-pinned. No legal,
issue-era or human artwork approval follows from source matching.
"""
from __future__ import annotations
import argparse,base64,gzip,hashlib,io,json,pathlib
from PIL import Image,ImageOps
ROOT=pathlib.Path(__file__).resolve().parents[1]
REVIEW='data/image-batches/mi-on-61-reviewed-20261029.json'
OLD='lpg-current-images-20261029-al28'
NEW='lpg-current-images-20261029-mion61'
def digest(x):return hashlib.sha256(x).hexdigest()

def jpeg(raw,max_size):
    with Image.open(io.BytesIO(raw)) as src:
        src.load()
        im=ImageOps.exif_transpose(src).convert('RGBA')
        if im.width<150 or im.height<70 or not 1.35<=im.width/im.height<=3.8:
            raise ValueError('Suspicious source sample dimensions '+str(im.size))
        white=Image.new('RGBA',im.size,'#FFFFFF')
        white.alpha_composite(im)
        rgb=white.convert('RGB')
        rgb.thumbnail((max_size,max_size),Image.Resampling.LANCZOS)
        out=io.BytesIO();rgb.save(out,'JPEG',quality=90,optimize=True,subsampling=0)
        return out.getvalue(),list(rgb.size)

def integrate(root,evidence):
    review=json.loads((root/REVIEW).read_text(encoding='utf-8'))
    rows=review['rows']
    if review['selected_count']!=61 or len(rows)!=61 or len({x['uid'] for x in rows})!=61:
        raise ValueError('Expected 61 distinct reviewed MI/ON catalog IDs')
    if review['baseline_source_matched']!=636 or review['target_selected']!=697:
        raise ValueError('Reviewed selection totals have changed')
    gallery={}
    for key,entry in review['agencies'].items():
        folder=evidence/entry['folder']
        ab=(folder/'assets.json').read_bytes()
        hb=(folder/'source.html').read_bytes()
        if digest(ab)!=entry['registry_sha256'] or digest(hb)!=entry['html_sha256']:
            raise ValueError('Archived issuing-agency source registry/page SHA drift: '+key)
        assets=json.loads(ab)
        numbers={}
        for x in assets:
            if x.get('status')!='downloaded' or not x.get('file','').startswith('harvest-output/'):
                continue
            filename=pathlib.Path(x['file']).name
            n=int(filename.removeprefix('asset_').split('.')[0])
            if n in numbers:raise ValueError('Duplicate original asset number: '+key)
            numbers[n]=x
        gallery[key]=numbers
    canonical=json.loads(gzip.decompress(base64.b64decode(b''.join(
        (root/f'data/catalog.part{i}.b64').read_bytes() for i in range(5)))))
    if len(canonical['plates'])!=1138:raise ValueError('Original 1138 catalog design UIDs changed')
    catalog={p['plate_uid']:p for p in canonical['plates']}
    mf=root/'data/catalog-images.js';prefix='globalThis.LPG_CATALOG_IMAGES='
    s=mf.read_text()
    if not s.startswith(prefix):raise ValueError('Unexpected catalog image format')
    current=json.loads(s[len(prefix):].strip().removesuffix(';'))
    if len(current)!=636:raise ValueError(f'Expected 636 existing source selections, got {len(current)}')
    selected={};files={};records=[]
    for row in rows:
        uid=row['uid'];g=row['gallery'];n=row['asset_number']
        if g not in gallery or n not in gallery[g] or uid in current or uid in selected:
            raise ValueError(f'Unreviewed, duplicate or missing asset for {uid}')
        if (g=='ontario')!=(uid.startswith('LPG-CA-ON-')):
            raise ValueError(f'Jurisdiction to source gallery mismatch: {uid}')
        p=catalog.get(uid)
        if not p or (p['jurisdiction_id']!='CA-ON' if g=='ontario' else p['jurisdiction_id']!='US-MI'):
            raise ValueError(f'Original canonical UID mapping missing {uid}')
        x=gallery[g][n]
        url=x['direct_image_url'];page=x['source_page_url']
        host='www.ontario.ca' if g=='ontario' else 'www.michigan.gov'
        if not url.startswith('https://'+host+'/') or not page.startswith('https://'+host+'/'):
            raise ValueError(f'Original agency source host mismatch: {uid}')
        name=x['file'].removeprefix('harvest-output/')
        file=(evidence/name).resolve()
        if not file.is_relative_to(evidence.resolve()) or not file.is_file():
            raise ValueError(f'Invalid original source location: {name}')
        raw=file.read_bytes()
        if digest(raw)!=x['sha256']:raise ValueError(f'Original official source image sha changed: {uid}')
        variants={};sizes={}
        for kind,limit in [('display',800),('thumbnail',300)]:
            j,size=jpeg(raw,limit)
            path=f'assets/plates/{uid}-{kind}.jpg'
            if path in files or (root/path).exists():raise ValueError(f'Refusing to overwrite original image {path}')
            files[path]=j
            variants[kind]=digest(j);sizes[kind]=size
        selected[uid]={
            'name':p['name'],'image':f'./assets/plates/{uid}-display.jpg',
            'thumbnail':f'./assets/plates/{uid}-thumbnail.jpg',
            'source_sha256':digest(raw),'source_url':page,
            'source_asset_url':url,'source_date':'2026-10-29',
            'source_label':x.get('alt_text','') or x['direct_image_url'].rsplit('/',1)[-1],
            'match_status':'source_matched','era_status':'unverified',
            'human_approval':False,'project_use_basis':'owner_directed_fair_use_reference'}
        records.append({'uid':uid,'name':p['name'],'gallery':g,'official_source_page':page,
                        'direct_asset_url':url,'asset_number':n,'source_file':name,
                        'source_original_sha256':digest(raw),
                        'source_alt_text':x.get('alt_text',''),
                        'archived_gallery_manifest_sha256':review['agencies'][g]['registry_sha256'],
                        'match_basis':'Official state/province plate graphic indexed by archived issuing-agency HTML with visible plate sample and catalog name',
                        'display_sha256':variants['display'],'thumbnail_sha256':variants['thumbnail'],
                        'display_size':sizes['display'],'thumbnail_size':sizes['thumbnail'],
                        'era_status':'unverified','human_approval':False,'match_status':'source_matched'})
    if len(files)!=122 or len(current)+len(selected)!=697 or len(selected)!=61:
        raise ValueError('Expected 697 image selections and 122 new JPG files')
    swfile=root/'sw.js';sw=swfile.read_text()
    if sw.count(OLD)!=1:raise ValueError('Unexpected offline cache version')
    testfile=root/'tests/catalog-images.cjs'
    test=testfile.read_text()
    anchor="await page.locator('#researchState').selectOption('US-WA');await page.locator('#researchResults .catalog-thumb img').evaluateAll"
    add="await page.locator('#researchState').selectOption('US-MI');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),22);await page.locator('#researchState').selectOption('CA-ON');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),39);"
    if test.count(anchor)!=1 or test.count('assert.equal(cacheCount,1272)')!=1 or test.count(OLD)!=1:
        raise ValueError('Focused source-image browser test changed')
    test=test.replace(anchor,add+anchor).replace('assert.equal(cacheCount,1272)','assert.equal(cacheCount,1394)').replace(OLD,NEW).replace('1272 cached images','1394 cached images')
    for path,j in files.items():
        dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(j)
    mf.write_text(prefix+json.dumps(dict(sorted({**current,**selected}.items())),ensure_ascii=False,separators=(',',':'))+';\n')
    swfile.write_text(sw.replace(OLD,NEW))
    testfile.write_text(test)
    dest=root/'database/image-reconciliation-mi-on-20261029.json'
    dest.write_text(json.dumps({'selected_count':61,'michigan_count':22,
        'ontario_count':39,'cumulative_source_matched':697,
        'original_gallery_manifest_hashes':{k:v['registry_sha256'] for k,v in review['agencies'].items()},
        'source_description_discrepancies':review['special_review'],
        'era_status':'unverified','human_approval':False,'rows':records},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'selected':61,'mi':22,'on':39,'source_matched_total':697,'runtime_jpegs_total':1394,'approval':False}))
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=pathlib.Path,default=ROOT)
    p.add_argument('--evidence-dir',type=pathlib.Path,required=True)
    a=p.parse_args()
    integrate(a.root,a.evidence_dir.resolve())
if __name__=='__main__':main()
