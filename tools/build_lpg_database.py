#!/usr/bin/env python3
"""Build a portable SQLite/image database without changing LPG identifiers.

No network access. Inputs are a recovered evidence archive, the report image
download manifest, and the frozen repository catalog. Pillow is required.
"""
import argparse,base64,csv,gzip,hashlib,json,mimetypes,shutil,sqlite3
from datetime import datetime,timezone
from pathlib import Path
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1]
def digest(data):return hashlib.sha256(data).hexdigest()
def read(path):return json.loads(path.read_text())
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--report-images',type=Path,required=True);ap.add_argument('--report',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    out=a.out
    if out.exists():raise SystemExit('Output already exists; choose a new version directory')
    for folder in ['originals','images','thumbnails','sources','exports']: (out/folder).mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(out/'lpg.sqlite');db.row_factory=sqlite3.Row;db.executescript((ROOT/'database/schema.sql').read_text())
    def insert(table,**row):
        keys=list(row);db.execute('INSERT INTO '+table+' ('+','.join(keys)+') VALUES ('+','.join('?' for _ in keys)+')',[row[k] for k in keys])
    def issue(kind,detail,action,uid=None,asset=None):insert('issues',plate_uid=uid,asset_sha256=asset,kind=kind,detail=detail,next_action=action,status='open')
    def source(url,authority,date,path=None):
        sid=digest(url.encode());exists=db.execute('SELECT id FROM sources WHERE id=?',(sid,)).fetchone()
        if not exists:
            dest=None;sha=None
            if path and path.exists():
                dest='sources/'+sid+path.suffix;data=path.read_bytes();(out/dest).write_bytes(data);sha=digest(data)
            insert('sources',id=sid,page_url=url,authority=authority,retrieved_at=date,archive_path=dest,archive_sha256=sha)
        return sid
    def asset(file,sid,url,role,label,creator,license,license_url,license_status,date,expected=None):
        data=file.read_bytes();sha=digest(data)
        if expected:assert sha==expected,f'Corrupt evidence: {file}'
        if db.execute('SELECT sha256 FROM assets WHERE sha256=?',(sha,)).fetchone():return sha
        rel='originals/'+sha+file.suffix.lower();(out/rel).write_bytes(data);width=height=None
        try:
            with Image.open(file) as im:
                im.load();width,height=im.size;original=ImageOps.exif_transpose(im).convert('RGB')
            for kind,folder,size in [('display','images',(800,800)),('thumbnail','thumbnails',(300,300))]:
                im=original.copy();im.thumbnail(size,Image.Resampling.LANCZOS);dest=f'{folder}/{sha}.jpg';im.save(out/dest,quality=90)
                # Add derivative rows after the asset FK exists.
        except Exception as e:
            if file.suffix.lower()!='.svg':issue('image_decode_failed',str(e),'Inspect original before display',asset=None)
        insert('assets',sha256=sha,source_id=sid,direct_url=url,original_path=rel,width=width,height=height,media_type=mimetypes.guess_type(file.name)[0],asset_role=role,source_label=label,creator=creator,source_license=license,license_url=license_url,license_status=license_status,project_use_basis='owner_directed_fair_use_reference',retrieved_at=date)
        for kind,folder in [('display','images'),('thumbnail','thumbnails')]:
            dest=f'{folder}/{sha}.jpg'
            if (out/dest).exists():
                with Image.open(out/dest) as im:w,h=im.size
                insert('derivatives',asset_sha256=sha,kind=kind,path=dest,sha256=digest((out/dest).read_bytes()),width=w,height=h,transform='EXIF orientation applied; aspect preserved; no upscale; RGB JPEG; metadata stripped; resized only')
        return sha
    catalog=json.loads(gzip.decompress(base64.b64decode(''.join((ROOT/f'data/catalog.part{i}.b64').read_text() for i in range(5)))))
    campaign=read(ROOT/'data/image-campaign/manifest.json');camp={p['uid']:p for p in campaign}
    assert len(catalog['plates'])==len(camp)==1138
    for j in catalog['jurisdictions']:insert('jurisdictions',id=j['id'],country=j['country'],code=j['code'],name=j['name'],kind=j.get('type'),scope='existing_catalog')
    # Add report-scope jurisdictions without fabricating plate designs for them.
    territories={'US-AS':'American Samoa','US-GU':'Guam','US-MP':'Northern Mariana Islands','US-PR':'Puerto Rico','US-VI':'U.S. Virgin Islands'}
    for jid,name in territories.items():
        if not db.execute('SELECT 1 FROM jurisdictions WHERE id=?',(jid,)).fetchone():insert('jurisdictions',id=jid,country='United States',code=jid[3:],name=name,kind='territory',scope='report_scope_no_designs_yet')
    for p in catalog['plates']:
        c=camp[p['plate_uid']];insert('plates',uid=p['plate_uid'],jurisdiction_id=p['jurisdiction_id'],name=p['name'],category=p.get('category'),record_origin='lpg_catalog',era_status='unknown',identity_status=c.get('identity_status','unverified'),visual_status=c.get('visual_status','unverified'),catalog_json=json.dumps(p,ensure_ascii=False))
    mapped={e['sha256'] for c in campaign for e in c.get('evidence',[])}
    evidence=read(a.evidence/'portable-evidence-index.json')
    for e in evidence:
        page=a.evidence/'WA/Washington_DOL_Special_Design_Plates_html/source.html'
        if e.get('source_page_sha256'):assert digest(page.read_bytes())==e['source_page_sha256']
        sid=source(e['source_page_url'],'issuing_agency',e['retrieved_at'],page)
        role='mapped_plate_candidate' if e['sha256'] in mapped else 'unclassified_gallery_asset'
        asset(a.evidence/e['file'],sid,e['direct_asset_url'],role,e.get('alt_text',''),'Washington Department of Licensing',None,None,'not_claimed',e['retrieved_at'],e['sha256'])
    for c in campaign:
        for e in c.get('evidence',[]):
            insert('plate_assets',plate_uid=c['uid'],asset_sha256=e['sha256'],match_status='candidate',match_basis=e.get('mapping_basis','Legacy candidate match'),human_review='pending')
    samples={'AL':('REPORT-AL-AUBURN-2001','Auburn University — report sample','specialty','2001–present'), 'AR':('REPORT-AR-STANDARD-2011','Standard passenger — 2011 photograph sample','standard','2011–2023'), 'PR':('REPORT-PR-MAYAGUEZ-2010','Mayagüez 2010 — report image conflict','unresolved','2023–present')}
    fetched=read(a.report_images/'manifest.json');now=datetime.now(timezone.utc).isoformat()
    for e in fetched:
        code=e['code'];uid,name,category,years=samples[code];insert('plates',uid=uid,jurisdiction_id='US-'+code,name=name,category=category,record_origin='report_candidate',era_status='conflict' if code=='PR' else 'unverified_report_claim',identity_status='candidate',visual_status='unverified',catalog_json='{}')
        insert('claims',plate_uid=uid,field='issue_years',claimed_value=years,source_ref='sources/input-report.md',status='conflict' if code=='PR' else 'unverified',note='Report assertion, not a confirmed date range; issue_start/end intentionally NULL.')
        sid=source(e['source_page'],'wikimedia_file_description',e['retrieved_at'],a.report_images/(code+'.html'))
        if e['status']=='downloaded':
            sha=asset(Path(e['path']),sid,e['image_url'],'report_plate_candidate',e['title'],e['author'],e['source_license'],e['license_url'],'observed_on_source_page',e['retrieved_at'],e['sha256'])
            insert('plate_assets',plate_uid=uid,asset_sha256=sha,match_status='conflict' if code=='PR' else 'candidate',match_basis='Linked by report; exact existing LPG design mapping and era require reconciliation.',human_review='pending')
        else:issue('download_failed',e.get('error','Unknown failure'),'Retry source acquisition after its rate-limit window; preserve provisional row',uid)
        issue('catalog_reconciliation','Report sample has no established match to an existing LPG UID.','Match design and era or approve a new canonical UID; do not replace an existing design.',uid)
    issue('report_date_conflict','Report calls PR image a 2023 standard but linked source identifies Mayagüez 2010; source photo is dated 2015.','Keep the image out of the 2023 standard mapping; find the intended modern design.',samples['PR'][0])
    issue('report_credit_correction','Arkansas source credits SuperSonic337, not Mattes as reported.','Use the source-page creator stored on the image record.',samples['AR'][0])
    issue('report_license_correction','Puerto Rico source distinguishes the object public-domain statement from CC BY 2.0 DE for the photograph.','Preserve photograph credit and license separately from the project fair-use basis.',samples['PR'][0])
    issue('report_scope_gap','Input report provides three sample links, not images for all 56 US jurisdictions.','Continue the campaign from the coverage export. Do not mark empty jurisdictions complete.')
    shutil.copy2(a.report,out/'sources/input-report.md');shutil.copy2(ROOT/'database/schema.sql',out/'schema.sql')
    for k,v in {'schema_version':'1','catalog_sha256':digest(json.dumps(catalog,sort_keys=True).encode()),'built_at':now,'project_use_basis':'Owner directed fair-use reference project on 2026-10-10; does not assert public-domain status or alter source licenses.','report_sha256':digest(a.report.read_bytes()),'canonical_plate_count':'1138','live_app_modified':'false'}.items():insert('metadata',key=k,value=v)
    assert not db.execute('PRAGMA foreign_key_check').fetchall();assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';db.commit()
    tables=['jurisdictions','plates','sources','assets','derivatives','plate_assets','claims','issues','coverage']
    for table in tables:
        records=[dict(r) for r in db.execute('SELECT * FROM '+table)];write(out/'exports'/f'{table}.json',records)
    app=[]
    for row in db.execute('SELECT * FROM plates'):
        p=dict(row);p.pop('catalog_json');p['images']=[dict(i) for i in db.execute('SELECT pa.match_status,pa.human_review,a.sha256,a.original_path,d.path AS thumbnail_path,a.creator,a.source_license,a.license_url,s.page_url FROM plate_assets pa JOIN assets a ON a.sha256=pa.asset_sha256 JOIN sources s ON s.id=a.source_id LEFT JOIN derivatives d ON d.asset_sha256=a.sha256 AND d.kind=\'thumbnail\' WHERE pa.plate_uid=?',(p['uid'],))];app.append(p)
    write(out/'exports/lpg-import.json',{'schema_version':1,'project_use_basis':'owner_directed_fair_use_reference','plates':app})
    write(out/'exports/approved-app-images.json',[dict(r) for r in db.execute('SELECT * FROM approved_app_images')])
    with (out/'ATTRIBUTION.csv').open('w',newline='') as f:
        rows=[dict(r) for r in db.execute('SELECT a.sha256,a.creator,a.source_license,a.license_url,s.page_url,a.direct_url,a.project_use_basis FROM assets a JOIN sources s ON s.id=a.source_id')];w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    counts={t:db.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in tables}
    counts.update(canonical_plates=db.execute("SELECT COUNT(*) FROM plates WHERE record_origin='lpg_catalog'").fetchone()[0],report_candidates=3,canonical_plates_with_candidate_images=db.execute("SELECT COUNT(*) FROM coverage WHERE record_origin='lpg_catalog' AND candidate_images>0").fetchone()[0],canonical_plates_without_images=db.execute("SELECT COUNT(*) FROM coverage WHERE record_origin='lpg_catalog' AND candidate_images=0").fetchone()[0],approved_app_images=db.execute('SELECT COUNT(*) FROM approved_app_images').fetchone()[0],image_download_failures=sum(e['status']!='downloaded' for e in fetched))
    # Verify packaged files, actual image decodability and all recorded hashes.
    for row in db.execute('SELECT original_path AS path,sha256 FROM assets UNION ALL SELECT path,sha256 FROM derivatives'):
        assert digest((out/row['path']).read_bytes())==row['sha256'],row['path']
    assert {p['plate_uid'] for p in catalog['plates']}=={r[0] for r in db.execute("SELECT uid FROM plates WHERE record_origin='lpg_catalog'")}
    counts['validation']='PASS: SQLite integrity, foreign keys, canonical UID preservation and every packaged asset/derivative hash'
    write(out/'validation.json',counts);db.close()
    (out/'README.md').write_text(f'''# LPG image database — 2026-10-10

Portable SQLite database plus actual image files, thumbnails, source records and JSON imports.

## Open/use
Open `lpg.sqlite` with a SQLite browser. All paths are relative to this folder; keep the folder intact. `exports/lpg-import.json` provides app-friendly records; candidate status is explicit. `approved_app_images` is intentionally empty until identity and human visual review pass. The existing live app/APK has not been changed.

## Contents and coverage
{json.dumps(counts,indent=2)}

There are 1,138 preserved LPG IDs plus three separate REPORT-prefixed candidates. They have not been silently merged into the catalog. Most catalog designs still have no acquired image. The report contains only three examples. Washington's gallery archive includes logos/site graphics; the asset_role column distinguishes mapped candidates from unclassified gallery assets. Do not equate asset count with plate count.

## Project use
Owner-directed fair-use reference project. This basis is recorded independently of source licenses and attribution. No source image was labeled public domain merely because it came from a government site. Source-license descriptions are observed source claims, not new legal conclusions.

## Report corrections
Puerto Rico: the report's 2023-standard row links a Mayagüez 2010 image photographed in 2015. Keep it as a conflict. Arkansas: source credits SuperSonic337, not Mattes. Puerto Rico's photograph has CC BY 2.0 DE alongside a separate public-domain claim about the object. Date ranges and physical dimensions in the report are not promoted to confirmed per-design facts. Fewer than 1200 pixels does not cause a useful official sample to be silently discarded.

## Images and attribution
Original bytes are preserved by SHA-256 filename. Display copies fit within 800×800 and thumbnails within 300×300, preserve aspect and never upscale. No generated art is presented as a source photograph. Copies strip metadata (including photo GPS), correct orientation and resize only. See ATTRIBUTION.csv and the linked license. AL photographs/derivatives: Zul32, CC BY-SA 3.0. AR: SuperSonic337, CC0. PR: Mattes, CC BY 2.0 DE when downloaded. Washington: issuing-agency attribution, source license not claimed.

## Useful queries
```sql
SELECT * FROM coverage WHERE candidate_images=0;
SELECT * FROM issues WHERE status='open';
SELECT * FROM coverage WHERE candidate_images>0;
SELECT * FROM approved_app_images;
```

## Next step
Resolve design/era matches and acquire missing images. Human visual comparison stays late in the campaign. Do not show name-match candidates as verified reference images. Report links that fail download remain tracked rather than replaced by invented images. Rebuild using tools/build_lpg_database.py with the retained inputs; schema.sql is included.
''')
    inventory=[{'path':str(p.relative_to(out)),'sha256':digest(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()]
    write(out/'checksums.json',inventory);print(json.dumps(counts,indent=2))
if __name__=='__main__':main()
