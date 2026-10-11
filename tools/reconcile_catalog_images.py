#!/usr/bin/env python3
"""Apply reviewed source selections to a copy of the portable database package."""
import argparse,hashlib,json,shutil,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--database-package',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
if a.out.exists():raise SystemExit('Output exists; choose a new package version')
shutil.copytree(a.database_package,a.out)
review=json.loads((ROOT/'database/image-reconciliation-20261011.json').read_text());db=sqlite3.connect(a.out/'lpg.sqlite');db.row_factory=sqlite3.Row;db.execute('PRAGMA foreign_keys=ON')
db.execute('CREATE TABLE app_image_selections(plate_uid TEXT PRIMARY KEY REFERENCES plates(uid), asset_sha256 TEXT NOT NULL REFERENCES assets(sha256), status TEXT NOT NULL, era_status TEXT NOT NULL, human_approval INTEGER NOT NULL, review_date TEXT NOT NULL)')
for r in review:
 if r['decision']=='source_matched':db.execute('INSERT INTO app_image_selections VALUES(?,?,?,?,?,?)',(r['uid'],r['sha256'],'source_matched','unverified',0,'2026-10-11'))
 else:
  db.execute("UPDATE plate_assets SET match_status='conflict',match_basis='Rejected during visual reconciliation: image depicts another design' WHERE plate_uid=? AND asset_sha256=?",(r['uid'],r['sha256']))
  db.execute("INSERT INTO issues(plate_uid,asset_sha256,kind,detail,next_action,status) VALUES(?,?,'rejected_wrong_design','Automatic name match linked the wrong plate artwork','Do not display this association; retain the independently matched sample','resolved')",(r['uid'],r['sha256']))
assert db.execute('SELECT COUNT(*) FROM app_image_selections').fetchone()[0]==54
assert not db.execute('PRAGMA foreign_key_check').fetchall();assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
db.execute("INSERT OR REPLACE INTO metadata VALUES('app_image_reconciliation','54 source-matched samples selected for display; 2 wrong associations rejected; no human visual approval or era claim')");db.commit()
for table in ['app_image_selections','plate_assets','issues']:(a.out/'exports'/f'{table}.json').write_text(json.dumps([dict(r) for r in db.execute('SELECT * FROM '+table)],indent=2)+'\n')
export=json.loads((a.out/'exports/lpg-import.json').read_text());selected={r['uid']:r['sha256'] for r in review if r['decision']=='source_matched'}
rejected={(r['uid'],r['sha256']) for r in review if r['decision']!='source_matched'}
for plate in export['plates']:
 for img in plate['images']:
  img['selected_for_app']=selected.get(plate['uid'])==img['sha256']
  if (plate['uid'],img['sha256']) in rejected:img['match_status']='conflict'
(a.out/'exports/lpg-import.json').write_text(json.dumps(export,indent=2)+'\n')
(a.out/'schema.sql').write_text(';\n'.join(r[0] for r in db.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%' ORDER BY type,name"))+';\n')
db.close()
shutil.copyfile(ROOT/'data/catalog-images.js',a.out/'app-image-manifest.js');shutil.copyfile(ROOT/'database/image-reconciliation-20261011.json',a.out/'reconciliation.json')
with (a.out/'README.md').open('a') as f:f.write('\n## 2026-10-11 app reconciliation\n54 official source samples are selected for app display. Two wrong automatic associations were rejected (Seahawks as generic Throwback, Breast Cancer as Square Dancer). app_image_selections and exports/lpg-import.json record these decisions. These are source-matched examples, not final human-approved or era-verified artwork. The live app uses the selected examples with source/date disclosure.\n')
v=json.loads((a.out/'validation.json').read_text());v.update(selected_app_images=54,rejected_associations=2,reconciliation_validation='PASS: foreign keys, integrity, unique selection per UID');(a.out/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
files=[{'path':str(f.relative_to(a.out)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in sorted(a.out.rglob('*')) if f.is_file() and f.name!='checksums.json'];(a.out/'checksums.json').write_text(json.dumps(files,indent=2)+'\n');print('Reconciled database: 54 selected, 2 rejected')
