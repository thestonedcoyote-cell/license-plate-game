#!/usr/bin/env python3
"""Integrate inspected, source-pinned gallery plate examples into LPG web runtime.

Never auto-approve identity eras, rights, or human visual accuracy. Only accepts
explicit one-to-one review rows with official source names, UIDs and SHA-256.
Writes no source originals into the public repository. For repeatability, can
run against a privately archived GitHub Actions harvest ZIP (--evidence-zip).
Otherwise reacquires the same direct official image URL and verifies its hash.
"""
from __future__ import annotations
import argparse, hashlib, io, json, os, pathlib, re, shutil, tempfile, zipfile
from PIL import Image, ImageOps, UnidentifiedImageError

ROOT=pathlib.Path(__file__).resolve().parents[1]
PREVIOUS_CACHE='lpg-current-images-20261012-or'
NEXT_CACHE='lpg-current-images-20261012-akms'


def digest(b): return hashlib.sha256(b).hexdigest()


def load_data(path):
    j=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(j,dict) or j.get('selected_count')!=len(j.get('rows',[])):
        raise ValueError('Invalid reviewed manifest or mismatch selection count')
    return j


def source_bytes(row,evidence,session,evidence_dir=None):
    name=row['asset_file'].removeprefix('harvest-output/')
    if evidence is not None:
        b=evidence.read(name)
    elif evidence_dir is not None:
        path=(evidence_dir/name).resolve()
        if not path.is_relative_to(evidence_dir.resolve()): raise ValueError('Unsafe evidence path')
        b=path.read_bytes()
    else:
        import requests
        res=session.get(row['direct_asset_url'],timeout=90,headers={'User-Agent':'LicensePlateGameResearch/0.3 (+official-source archival research)'})
        res.raise_for_status();b=res.content
    if digest(b)!=row['source_sha256']:
        raise ValueError(f'Official source image changed or corrupted: {row["uid"]}')
    return b


def convert(b, limit):
    with Image.open(io.BytesIO(b)) as raw:
        im=ImageOps.exif_transpose(raw)
        im.load()
        if im.width<90 or im.height<35 or im.width/im.height<1.35 or im.width/im.height>3.8:
            raise ValueError(f'Unlikely license plate aspect or low-resolution source: {im.size}')
        if im.mode in ('RGBA','LA','P'):
            im=im.convert('RGBA')
            white=Image.new('RGBA',im.size,'white');white.alpha_composite(im)
            im=white.convert('RGB')
        else: im=im.convert('RGB')
        im.thumbnail((limit,limit),Image.Resampling.LANCZOS)
        dest=io.BytesIO();im.save(dest,format='JPEG',quality=90,subsampling=0,optimize=True)
        return dest.getvalue(),tuple(im.size)


def integrate(root,manifest,evidence_zip=None,evidence_dir=None):
    # Check all metadata and sources before writing any runtime artifact.
    original_path=root/'data/catalog-images.js'
    code=original_path.read_text(encoding='utf-8').strip()
    prefix='globalThis.LPG_CATALOG_IMAGES='
    if not code.startswith(prefix) or not code.endswith(';'):
        raise ValueError('Existing catalog image manifest format has changed')
    existing=json.loads(code[len(prefix):-1]); old_count=len(existing)
    if old_count!=73:
        raise ValueError(f'Source image manifest is no longer the expected 73-entry baseline: {old_count}')
    sw_path=root/'sw.js';sw=sw_path.read_text(encoding='utf-8')
    if sw.count(PREVIOUS_CACHE)!=1 or NEXT_CACHE in sw:
        raise ValueError('Expected prior service worker cache version missing or new version already present')
    test_path=root/'tests/catalog-images.cjs'
    test=test_path.read_text(encoding='utf-8')
    if test.count('assert.equal(cacheCount,146)')!=1 or test.count(PREVIOUS_CACHE)!=1:
        raise ValueError('Focused image test differs from reviewed baseline')
    canon_file=root/'data/image-campaign/manifest.json'
    if canon_file.exists():
        catalog={r['uid']:r for r in json.loads(canon_file.read_text(encoding='utf-8'))}
        if len(catalog)!=1138: raise ValueError('Catalog UID baseline changed')
    else:
        catalog=None
    uidset=set();new_assets={};records=[]
    rows=manifest['rows'];
    if len(rows)!=76 or len({r['uid'] for r in rows})!=76:
        raise ValueError('Not the approved 76-UID Alaska/Mississippi batch')
    if {r['jurisdiction_id'] for r in rows}!={'US-AK','US-MS'}:
        raise ValueError('Unexpected jurisdiction in reviewed batch')
    evidence=zipfile.ZipFile(evidence_zip) if evidence_zip else None
    try:
        session=None
        if evidence is None and evidence_dir is None:
            import requests
            session=requests.Session()
        for r in rows:
            uid=r['uid'];jid=r['jurisdiction_id']
            if uid in existing or uid in uidset or not uid.startswith('LPG-'+jid+'-'):
                raise ValueError(f'Existing/duplicate/invalid UID: {uid}')
            uidset.add(uid)
            if catalog is not None:
                p=catalog.get(uid)
                if p is None or p['jurisdiction_id']!=jid or p['name']!=r['name']:
                    raise ValueError(f'Catalog UID/name mismatch: {uid}')
            if r['match_status']!='source_matched' or r['human_approval'] is not False or r['era_status']!='unverified':
                raise ValueError(f'Approval or era state is not supported: {uid}')
            if not r['direct_asset_url'].startswith('https://') or not r['source_page_url'].startswith('https://'):
                raise ValueError('Provenance URL must be HTTPS')
            raw=source_bytes(r,evidence,session,evidence_dir)
            display,shape=convert(raw,800);thumb,tshape=convert(raw,300)
            for kind,output in [('display',display),('thumbnail',thumb)]:
                name=f'assets/plates/{uid}-{kind}.jpg'
                if (root/name).exists():raise ValueError(f'Overwriting existing image: {name}')
                new_assets[name]=output
            row_out={
                'uid':uid,'name':r['name'],'jurisdiction_id':jid,
                'source_url':r['source_page_url'],'source_asset_url':r['direct_asset_url'],
                'source_label':r['source_label'],'source_sha256':r['source_sha256'],
                'match_status':'source_matched','era_status':'unverified','human_approval':False,
                'evidence_method':r['evidence_method'],'project_use_basis':'owner_directed_fair_use_reference',
                'display_sha256':digest(display),'thumbnail_sha256':digest(thumb),
                'display_size':list(shape),'thumbnail_size':list(tshape),
                'source_run_id':manifest['source_run_id'],
            }
            records.append(row_out)
            existing[uid]={
                'name':r['name'], 'image':f'./assets/plates/{uid}-display.jpg',
                'thumbnail':f'./assets/plates/{uid}-thumbnail.jpg',
                'source_sha256':r['source_sha256'], 'source_url':r['source_page_url'],
                'source_date':'2026-10-11','match_status':'source_matched',
                'era_status':'unverified','human_approval':False,
                'project_use_basis':'owner_directed_fair_use_reference',
                'source_label':r['source_label'],
            }
    finally:
        if evidence is not None: evidence.close()
    if len(existing)!=149 or len(new_assets)!=152 or len(records)!=76:
        raise ValueError('Expected output counts do not reconcile')
    # Serialize all outputs once validations pass. Git commits are atomic at PR boundary.
    for name,contents in new_assets.items():
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(contents)
    original_path.write_text(prefix+json.dumps(dict(sorted(existing.items())),ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    sw_path.write_text(sw.replace(PREVIOUS_CACHE,NEXT_CACHE),encoding='utf-8')
    needle="assert.equal(await page.locator('#researchResults .catalog-thumb').count(),19);"
    if test.count(needle)!=1:raise ValueError('Oregon test marker missing')
    test=test.replace(needle,needle+"await page.locator('#researchState').selectOption('US-AK');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),41);await page.locator('#researchState').selectOption('US-MS');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),35);")
    test=test.replace(PREVIOUS_CACHE,NEXT_CACHE).replace('assert.equal(cacheCount,146)','assert.equal(cacheCount,298)')
    test=test.replace('PASS: 54 WA and 19 OR thumbnails,','PASS: 54 WA, 19 OR, 41 AK, 35 MS thumbnails,').replace('146 cached images','298 cached images')
    test_path.write_text(test,encoding='utf-8')
    (root/'database/image-reconciliation-ak-ms-20261011.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return {'selected_prior':73,'selected_new':76,'selected_total':len(existing),'remaining':1138-len(existing),'derivatives_new':len(new_assets),'source_status':'source_matched_not_era_approved','unresolved_ambiguous':manifest['ambiguous_cases']}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=pathlib.Path,default=ROOT)
    ap.add_argument('--manifest',type=pathlib.Path,default=ROOT/'data/image-batches/ak-ms-reviewed.json')
    ap.add_argument('--evidence-zip',type=pathlib.Path)
    ap.add_argument('--evidence-dir',type=pathlib.Path)
    a=ap.parse_args()
    print(json.dumps(integrate(a.root,load_data(a.manifest),a.evidence_zip,a.evidence_dir),indent=2))
if __name__=='__main__':main()