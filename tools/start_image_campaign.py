#!/usr/bin/env python3
"""Freeze the complete catalog and make an honest, reproducible image baseline."""
import base64,csv,gzip,hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    chunks=[(ROOT/f'data/catalog.part{i}.b64').read_bytes() for i in range(5)]
    raw=gzip.decompress(base64.b64decode(b''.join(chunks)))
    catalog=json.loads(raw);plates=catalog['plates'];uids=[p['plate_uid'] for p in plates]
    assert len(uids)==1138 and len(set(uids))==1138,'Catalog gate failed'
    refs=set()
    for name in ['reference-renders-v10.js','reference-renders-tx-v10.1.js']:
        refs.update(re.findall(r'"(LPG-[A-Z0-9-]+)"\s*:',(ROOT/'data'/name).read_text()))
    assert not refs-set(uids),'Orphan public reference UID'
    jurisdictions={j['id']:j for j in catalog['jurisdictions']}
    sources=list(csv.DictReader((ROOT/'data/harvest_sources.csv').open()))
    out=ROOT/'data/image-campaign';out.mkdir(exist_ok=True)
    if (out/'manifest.json').exists():raise SystemExit('Baseline already exists; do not overwrite campaign progress')
    rows=[]
    for p in plates:
        uid=p['plate_uid'];rows.append({'uid':uid,'jurisdiction_id':p['jurisdiction_id'],'name':p['name'],'category':p.get('category'),'issue_years':p.get('issue_years'),'aliases':p.get('aliases',[]),'existing_schematic':uid in refs,'catalog_evidence_count':len(p.get('images',[])),'identity_status':'unverified','visual_status':'unverified','public_use_status':'unassessed','credential_safety_status':'unassessed','human_review_status':'not_ready','disposition':'source_unresolved','source_candidates':p.get('images',[]),'evidence':[],'uncertainties':['Catalog source leads and existing schematic are not verified evidence.'],'next_action':'Retrieve authoritative source and establish design/era mapping.'})
    registry=[];counts=Counter(p['jurisdiction_id'] for p in plates)
    for jid,count in sorted(counts.items()):
        j=jurisdictions[jid];matches=[s for s in sources if jid.startswith('US-') and s['code']==j['code']]
        registry.append({'jurisdiction_id':jid,'name':j['name'],'plate_count':count,'source_leads':matches,'status':'leads_need_retrieval' if matches else 'discovery_pending','fallback_search':f'{j["name"]} official vehicle registration license plate designs government'})
    summary={'catalog_sha256':hashlib.sha256(raw).hexdigest(),'catalog_generated':catalog['generated'],'total':len(rows),'unique_uids':len(set(uids)),'existing_schematics':len(refs),'without_schematic':len(rows)-len(refs),'represented_jurisdictions':len(counts),'jurisdictions_with_source_leads':sum(bool(r['source_leads']) for r in registry),'verified_images':0,'phase_0':'passed','phase_1':'in_progress','human_review':'not_requested'}
    for name,value in [('manifest.json',rows),('source-registry.json',registry),('baseline.json',summary)]:
        (out/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
