#!/usr/bin/env python3
"""Attach reproducible source leads without granting identity or visual approval."""
import argparse,hashlib,json,re
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def norm(s):return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('evidence',type=Path);a=ap.parse_args()
    log=json.loads((a.evidence/'manifest.json').read_text());out=ROOT/'data/image-campaign'
    manifest=json.loads((out/'manifest.json').read_text());registry=json.loads((out/'source-registry.json').read_text())
    index=[];private=[];now=datetime.now(timezone.utc).isoformat()
    for source in log:
        code=source['code'];jid='US-'+code;gallery=source.get('gallery',{})
        source_path=gallery.get('source_html')
        page_hash=hashlib.sha256(Path(source_path).read_bytes()).hexdigest() if source_path else None
        for asset in gallery.get('records',[]):
            if asset.get('status')!='downloaded':continue
            file=Path(asset['file']);assert hashlib.sha256(file.read_bytes()).hexdigest()==asset['sha256']
            record={'id':asset['sha256'],'jurisdiction_id':jid,'source_page_url':asset['source_page_url'],'source_page_sha256':page_hash,'direct_asset_url':asset['direct_image_url'],'sha256':asset['sha256'],'width_px':asset.get('width_px'),'height_px':asset.get('height_px'),'retrieved_at':now,'source_authority':'issuing_agency','public_use_status':'unassessed'}
            index.append(record);private.append({**record,'file':str(file.relative_to(a.evidence)),'alt_text':asset.get('alt_text','')})
            text=norm(asset.get('alt_text','')+' '+asset.get('context','')+' '+asset['direct_image_url'].rsplit('/',1)[-1])
            for plate in manifest:
                if plate['jurisdiction_id']!=jid:continue
                name=norm(plate['name'])
                if len(name)<4 or not re.search(r'\b'+re.escape(name)+r'\b',text):continue
                if not any(e['sha256']==record['sha256'] for e in plate['evidence']):
                    plate['evidence'].append({**record,'mapping_status':'name_match_candidate','mapping_confidence':'medium','mapping_basis':'Catalog name occurs in official asset label or filename; design era is not established.'})
                plate['disposition']='evidence_candidate';plate['next_action']='Resolve exact design/era, then extract visual specification and public-use route before human review.'
        for r in registry:
            if r['jurisdiction_id']==jid:r['status']='pilot_retrieved' if source['status']=='downloaded' else 'retrieval_failed';r['last_attempt']=now
    # Original files remain private. This index exposes citations and hashes only.
    for name,value in [('manifest.json',manifest),('source-registry.json',registry),('evidence-index-batch01.json',index)]:
        (out/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
    (a.evidence/'portable-evidence-index.json').write_text(json.dumps(private,indent=2)+'\n')
    inventory=[]
    for p in sorted(a.evidence.rglob('*')):
        if p.is_file():inventory.append({'file':str(p.relative_to(a.evidence)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    (a.evidence/'archive-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    summary={'total_catalog':len(manifest),'unique_uids':len({p['uid'] for p in manifest}),'sources_attempted':len(log),'sources_retrieved':sum(s['status']=='downloaded' for s in log),'assets_archived':len(index),'plate_candidates':sum(bool(p['evidence']) for p in manifest),'verified_images':0,'human_review_ready':0,'phase_1':'in_progress','exception':'Bounded Washington pilot after full catalog baseline; global source registry gate is not yet complete.'}
    assert summary['total_catalog']==summary['unique_uids']==1138
    (out/'batch01-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
