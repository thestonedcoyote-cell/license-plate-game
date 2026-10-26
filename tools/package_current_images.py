#!/usr/bin/env python3
"""Package the present source-matched LPG web image manifest into portable SQLite.

The package stores all 1,138 canonical records and all current public display
copies, NOT original agency source binaries. Source SHA-256 strings are only
external evidence references; the package does not assert source rights, design
era, or human approval. Historic external-report candidates are not imported.
"""
from __future__ import annotations
import argparse,base64,csv,gzip,hashlib,io,json,os,re,shutil,sqlite3,zipfile
from pathlib import Path
from PIL import Image

def digest(data):return hashlib.sha256(data).hexdigest()
def to_json(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def build(root:Path,out:Path,expected_selections:int):
    root=root.resolve();out=out.resolve()
    if out.exists():raise ValueError('Package destination exists; overwrite forbidden')
    out.mkdir(parents=True)
    (out/'images').mkdir();(out/'thumbnails').mkdir();(out/'exports').mkdir()
    source=gzip.decompress(base64.b64decode(b''.join((root/f'data/catalog.part{i}.b64').read_bytes() for i in range(5))))
    catalog=json.loads(source)
    plates=catalog['plates']
    if len(plates)!=1138 or len({r['plate_uid'] for r in plates})!=1138:raise ValueError('Canonical catalog changed; investigate before publishing')
    path=root/'data/catalog-images.js';m=path.read_text()
    if not m.startswith('globalThis.LPG_CATALOG_IMAGES='):raise ValueError('Unrecognized app-image format')
    mappings=json.loads(m.split('=',1)[1].strip().rstrip(';'))
    if len(mappings)!=expected_selections:raise ValueError(f'Current manifest changed: {len(mappings)} vs explicit expected {expected_selections}; refresh packaging acceptance counts')
    original_ids={r['plate_uid'] for r in plates}
    if not set(mappings).issubset(original_ids):raise ValueError('Orphan app image UID')
    db=sqlite3.connect(out/'lpg.sqlite');db.row_factory=sqlite3.Row
    db.executescript((root/'database/schema.sql').read_text())
    db.execute('CREATE TABLE app_image_selections(plate_uid TEXT PRIMARY KEY REFERENCES plates(uid), asset_sha256 TEXT NOT NULL REFERENCES assets(sha256), status TEXT NOT NULL, era_status TEXT NOT NULL, human_approval INTEGER NOT NULL, source_asset_sha256 TEXT NOT NULL, source_url TEXT NOT NULL, package_image_role TEXT NOT NULL)')
    db.execute('CREATE INDEX app_image_selection_status ON app_image_selections(status,era_status,human_approval)')
    db.execute('CREATE TABLE runtime_image_files(plate_uid TEXT NOT NULL REFERENCES plates(uid), kind TEXT NOT NULL CHECK(kind IN ("display","thumbnail")), asset_sha256 TEXT NOT NULL REFERENCES assets(sha256), path TEXT NOT NULL UNIQUE, sha256 TEXT NOT NULL, width INTEGER NOT NULL, height INTEGER NOT NULL, PRIMARY KEY(plate_uid,kind))')
    for jurisdiction in catalog['jurisdictions']:
        db.execute('INSERT INTO jurisdictions(id,country,code,name,kind,scope) VALUES(?,?,?,?,?,?)',(
            jurisdiction['id'],jurisdiction['country'],jurisdiction['code'],jurisdiction['name'],jurisdiction.get('type'),'existing_catalog'))
    for plate in plates:
        db.execute('INSERT INTO plates(uid,jurisdiction_id,name,category,record_origin,era_status,identity_status,visual_status,catalog_json) VALUES(?,?,?,?,?,?,?,?,?)',(
            plate['plate_uid'],plate['jurisdiction_id'],plate['name'],plate.get('category'),'lpg_catalog','unknown','catalog_only','unverified',json.dumps(plate,ensure_ascii=False)))
    prov=[];source_ids={};all_jpg=set();seen_hashes={};shared=[]
    for uid,row in sorted(mappings.items()):
        if row.get('match_status')!='source_matched' or row.get('era_status')!='unverified' or row.get('human_approval') is not False:
            raise ValueError(f'Selection approval/status assumption changed: {uid}')
        ref=row.get('source_sha256')
        if not isinstance(ref,str) or not re.fullmatch('[0-9a-f]{64}',ref):raise ValueError(f'Bad source SHA-256 pointer: {uid}')
        url=row.get('source_url')
        if not isinstance(url,str) or not url.startswith('https://'):raise ValueError(f'No official source URL: {uid}')
        for kind,subdir in [('display','images'),('thumbnail','thumbnails')]:
            public_ref=row['image' if kind=='display' else 'thumbnail']
            if public_ref != f'./assets/plates/{uid}-{kind}.jpg':raise ValueError(f'Asset filename mismatch {uid} {kind}')
            file=(root/public_ref[2:]).resolve()
            if not file.is_relative_to(root) or not file.is_file():raise ValueError(f'Asset missing: {file}')
            data=file.read_bytes()
            with Image.open(io.BytesIO(data)) as im:
                im.verify()
            with Image.open(io.BytesIO(data)) as im:
                width,height=im.size
            if min(width,height)<25 or width/height<1.3 or width/height>4.0:
                raise ValueError(f'Unexpected plate display shape for {uid}: {width}x{height}')
            loc=f'{subdir}/{uid}-{kind}.jpg'
            (out/loc).write_bytes(data)
            row[kind+'_runtime_sha256']=digest(data)
            row[kind+'_width']=width;row[kind+'_height']=height
            all_jpg.add(loc)
        source_id=digest(url.encode())
        if source_id not in source_ids:
            db.execute('INSERT INTO sources(id,page_url,authority,retrieved_at,archive_path,archive_sha256) VALUES(?,?,?,?,?,?)',(
                source_id,url,'source_attributed_in_app','2026-10-26',None,None))
            source_ids[source_id]=url
        copyhash=row['display_runtime_sha256']
        if copyhash not in seen_hashes:
            seen_hashes[copyhash]=uid
            db.execute('INSERT INTO assets(sha256,source_id,direct_url,original_path,width,height,media_type,asset_role,source_label,creator,source_license,license_url,license_status,project_use_basis,retrieved_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(
                copyhash,source_id,url,f'images/{uid}-display.jpg',row['display_width'],row['display_height'],'image/jpeg',
                'published_runtime_display_derivative_not_original',row.get('source_label',row['name']),
                None,None,None,'not_claimed',row.get('project_use_basis','owner_directed_fair_use_reference'),'2026-10-26'))
            for kind,subdir in [('display','images'),('thumbnail','thumbnails')]:
                db.execute('INSERT INTO derivatives(asset_sha256,kind,path,sha256,width,height,transform) VALUES(?,?,?,?,?,?,?)',(
                    copyhash,kind,f'{subdir}/{uid}-{kind}.jpg',row[kind+'_runtime_sha256'],row[kind+'_width'],row[kind+'_height'],
                    'Existing public game JPEG copied byte-for-byte; source original not packaged'))
        else:
            other_uid=seen_hashes[copyhash]
            shared.append({'uid':uid,'same_display_bytes_as_uid':other_uid,'display_sha256':copyhash,'requires_identity_review':True})
            db.execute('INSERT INTO issues(plate_uid,asset_sha256,kind,detail,next_action,status) VALUES(?,?,?,?,?,?)',(
                uid,copyhash,'shared_identical_runtime_image',f'Identical display JPEG content also assigned to {other_uid}',
                'Inspect independent official visual and issue-era evidence; do not treat identical bytes as independent verification','open'))
        for kind,subdir in [('display','images'),('thumbnail','thumbnails')]:
            db.execute('INSERT INTO runtime_image_files(plate_uid,kind,asset_sha256,path,sha256,width,height) VALUES(?,?,?,?,?,?,?)',(
                uid,kind,copyhash,f'{subdir}/{uid}-{kind}.jpg',row[kind+'_runtime_sha256'],row[kind+'_width'],row[kind+'_height']))
        db.execute('INSERT INTO plate_assets(plate_uid,asset_sha256,match_status,match_basis,human_review) VALUES(?,?,?,?,?)',(
            uid,copyhash,'candidate',row.get('mapping_basis','Prior source-matched app mapping; historical era unverified'),'pending'))
        db.execute('INSERT INTO app_image_selections VALUES(?,?,?,?,?,?,?,?)',(
            uid,copyhash,'source_matched','unverified',0,ref,url,'runtime_display_only__source_original_external'))
        prov.append({k:row[k] for k in ('name','source_sha256','source_url','source_date','match_status','era_status','human_approval','display_runtime_sha256','thumbnail_runtime_sha256') if k in row}|{'uid':uid,'other_metadata':{k:v for k,v in row.items() if k not in ('name','source_sha256','source_url','source_date','match_status','era_status','human_approval','display_runtime_sha256','thumbnail_runtime_sha256','image','thumbnail','display_width','display_height','thumbnail_width','thumbnail_height')}})
    assert len(all_jpg)==2*expected_selections
    metadata={
        'package_kind':'runtime_snapshot_not_original_evidence_archive',
        'canonical_plate_uids':'1138','source_matched_runtime_image_selections':str(expected_selections),
        'selected_images_have_human_approval':'false',
        'original_issuing_agency_source_binaries_included':'false',
        'legacy_report_candidate_entries_included':'false',
        'catalog_sha256':digest(source),
        'github_head_sha':os.environ.get('GITHUB_SHA','local_test'),
        'current_sources':'See exports/source-provenance.json and separate private Library evidence archives',
        'identical_display_image_shared_uid_count':str(len(shared)),
    }
    db.executemany('INSERT INTO metadata(key,value) VALUES(?,?)',sorted(metadata.items()))
    db.commit()
    fk=db.execute('PRAGMA foreign_key_check').fetchall()
    check=db.execute('PRAGMA integrity_check').fetchone()[0]
    assert check=='ok' and not fk,(check,fk)
    counts={table:db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0] for table in ['plates','jurisdictions','sources','assets','derivatives','plate_assets','app_image_selections','runtime_image_files','issues']}
    assert counts['plates']==1138 and counts['assets']==len(seen_hashes) and counts['derivatives']==len(seen_hashes)*2 and counts['app_image_selections']==expected_selections and counts['runtime_image_files']==2*expected_selections
    assert db.execute('SELECT COUNT(*) FROM app_image_selections WHERE human_approval!=0 OR era_status!="unverified"').fetchone()[0]==0
    for table in ['app_image_selections','plate_assets','sources','runtime_image_files','issues']:
        (out/'exports'/f'{table}.json').write_text(to_json([dict(x) for x in db.execute('SELECT * FROM '+table)]))
    (out/'exports/shared-identical-display-images.json').write_text(to_json(shared))
    (out/'exports/catalog.json').write_text(to_json(catalog))
    (out/'exports/source-provenance.json').write_text(to_json(prov))
    (out/'exports/app-image-manifest.json').write_text(to_json(mappings))
    (out/'schema.sql').write_text(';\n'.join(r[0] for r in db.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%' ORDER BY type,name"))+';\n')
    db.close()
    readme='''# License Plate Game portable source-image snapshot\n\nThis ZIP is derived from the **current GitHub runtime manifest**, not from a newly rebuilt original-source evidence archive.\n\n- 1,138 immutable existing catalog UIDs and 58 existing catalog jurisdictions.\n- 370 selected source-matched display examples; 740 published JPEG display/thumbnail files copied byte-for-byte.\n- Each source entry retains its URL, original source asset SHA-256 **as a reference string**, app source metadata and the exact published derivative hashes.\n- `assets.original_path` is a legacy schema column but points at the packaged **runtime display derivative**, NOT the issuing-agency original. Rows declare `asset_role=published_runtime_display_derivative_not_original`. The original agency files remain in independent evidence archives stored in the user Library.\n- Content-identical published display images are deduplicated in the content-addressed `assets` table. The separate `runtime_image_files` table keeps every plate UID and all 740 actual display/thumbnail paths; duplicate source-image use is flagged in `issues` and `exports/shared-identical-display-images.json` for review.
- `app_image_selections` is separate from `plate_assets`: selections are source-matched runtime reference images but **not** historically era-verified, rights-cleared, or human-approved.\n- Historic 3 non-canonical report candidates from the older research database are omitted; preserve the historical 149-image archive separately. This snapshot is not a superset of that research archive.\n- No original issuing-agency source binaries, access credentials or signing keys are included.\n\nValidation: SQLite integrity and foreign keys, 370 unique selections, 740 byte-for-byte runtime JPEG copies and a SHA-256 inventory of all packaged files.\n'''
    readme=readme.replace('370',str(expected_selections)).replace('740',str(2*expected_selections))
    (out/'README.md').write_text(readme)
    (out/'validation.json').write_text(to_json({'status':'PASS','sqlite_integrity':check,'foreign_key_errors':len(fk),'counts':counts,'runtime_jpeg_files':len(all_jpg),'canonical_catalog_count':1138,'approved_images':0,'source_display_byte_duplicates':len(shared),'original_source_binaries_in_package':0}))
    hashes=[{'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(out.rglob('*')) if p.is_file() and p.name!='checksums.json']
    (out/'checksums.json').write_text(to_json(hashes))
    for h in hashes:
        assert digest((out/h['path']).read_bytes())==h['sha256']
    return counts,len(hashes)

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-selections',type=int,required=True)
    args=p.parse_args();counts,num=build(args.root,args.out,args.expected_selections)
    archive=args.out.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for file in sorted(args.out.rglob('*')):
            if file.is_file():z.write(file,arcname=str(file.relative_to(args.out.parent)))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    print(json.dumps({'archive':str(archive),'sha256':digest(archive.read_bytes()),'bytes':archive.stat().st_size,'inventory_files':num,'counts':counts},indent=2))
if __name__=='__main__':main()