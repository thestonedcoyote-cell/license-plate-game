#!/usr/bin/env python3
"""Reproducibly add verified-name Oregon DMV manual plate sample crops to LPG.

This is an exact pinned source-document batch, not a universal PDF detector.
Uses source-identified plate samples; maps current/previous versions separately.
Does not issue era or human approvals or create native distribution releases.
"""
from __future__ import annotations
import argparse,hashlib,json,re
from datetime import datetime,timezone
from io import BytesIO
from pathlib import Path
import fitz
from PIL import Image

OFFICIAL_URL='https://www.oregon.gov/odot/Forms/DMV/6726.pdf'
PDF_SHA='56ccdbf8dbbcd39c2803308f255e7374998c1ab418893da8b3577ff2098bdd50'
CACHE_OLD='lpg-current-images-20261011'
CACHE_NEW='lpg-current-images-20261012-or'
MAP={
 'Crater Lake':['LPG-US-OR-00001','LPG-US-OR-00007'],
 'Cultural':['LPG-US-OR-00002','LPG-US-OR-00008'],
 'Golf Oregon':['LPG-US-OR-00009'],
 'Gray Whale':['LPG-US-OR-00010'],
 'OSU Beaver':['LPG-US-OR-00011'],
 'Oregon Trail':['LPG-US-OR-00012'],
 'Oregon Zoo':['LPG-US-OR-00013'],
 'Pacific Wonderland':['LPG-US-OR-00014'],
 'Pollinator Paradise':['LPG-US-OR-00015'],
 'Salmon':['LPG-US-OR-00005','LPG-US-OR-00016'],
 'Smokey Bear':['LPG-US-OR-00017'],
 'Trail Blazers':['LPG-US-OR-00004'],
 'Tree':['LPG-US-OR-00003'],
 'UO Duck':['LPG-US-OR-00018'],
 'Watch for Wildlife':['LPG-US-OR-00019'],
 'Wine Country':['LPG-US-OR-00006']}
CANONICAL_NAMES={'Tree':'Graphic Tree','Trail Blazers':'Portland Trail Blazers'}

def sha(data):return hashlib.sha256(data).hexdigest()
def source_bytes(local):
 if local:return Path(local).read_bytes()
 import requests
 r=requests.get(OFFICIAL_URL,timeout=90,headers={'User-Agent':'LicensePlateGameResearch/0.5 (source attribution)'})
 r.raise_for_status()
 if 'pdf' not in r.headers.get('content-type','').lower() and not r.content.startswith(b'%PDF-'):raise ValueError('Official URL did not return PDF')
 return r.content

def make(root:Path,pdf_data:bytes,source_date:str):
 if sha(pdf_data)!=PDF_SHA:raise ValueError('Official PDF bytes changed; do not silently publish new crops')
 p=fitz.open(stream=pdf_data,filetype='pdf')
 if len(p)!=38:raise ValueError('Manual PDF structure changed')
 source=PDF_SHA
 selected={};records=[];atlas=root/'assets/plates';atlas.mkdir(parents=True,exist_ok=True)
 for pi in range(20,27):
  page=p[pi]
  lines=[]
  for b in page.get_text('dict')['blocks']:
   for l in b.get('lines',[]):
    label=''.join(s['text'] for s in l['spans']).strip()
    lines.append((l['bbox'][1],label))
  lines.sort()
  headings=[]
  for y,label in lines:
   match=re.fullmatch(r'PASSENGER \((.+)\)',label)
   if match:headings.append((y,match.group(1)))
  for idx,(y,label) in enumerate(headings):
   if label not in MAP:continue
   stop=headings[idx+1][0] if idx+1<len(headings) else 760
   ys=[pos for pos,line in lines if y<pos<stop and line.startswith('Issued to (Vehicle Type):')]
   uids=MAP[label]
   if len(ys)!=len(uids):raise ValueError(f'Ambiguous {label} on PDF page {pi+1}: {len(ys)} images for {len(uids)} UIDs')
   for ix,(uid,pos) in enumerate(zip(uids,ys)):
    if uid in selected:raise ValueError('Duplicate '+uid)
    clip=fitz.Rect(85, pos-2,273,pos+94)
    pix=page.get_pixmap(matrix=fitz.Matrix(4.2,4.2),clip=clip,alpha=False)
    img=Image.open(BytesIO(pix.tobytes('png'))).convert('RGB')
    if img.width<600 or img.height<300:raise ValueError('Crop unexpectedly low resolution')
    paths={};hashes={}
    for kind,max_dim in [('display',850),('thumbnail',300)]:
     target=img.copy();target.thumbnail((max_dim,max_dim),Image.Resampling.LANCZOS)
     buf=BytesIO();target.save(buf,'JPEG',quality=88,optimize=True,subsampling=0)
     data=buf.getvalue();out=atlas/f'{uid}-{kind}.jpg';out.write_bytes(data)
     paths[kind]='./assets/plates/'+out.name;hashes[kind]=sha(data)
    official_variant='previous_still_valid' if ix==1 else 'current_or_still_valid'
    entry={'uid':uid,'manual_label':label,'canonical_name':CANONICAL_NAMES.get(label,label)+(' — previous design' if ix==1 else ''),'manual_page':pi+1,'manual_variant':official_variant,'crop_rect_pdf':[round(v,4) for v in (clip.x0,clip.y0,clip.x1,clip.y1)],'source_url':OFFICIAL_URL,'source_document_sha256':PDF_SHA,'source_date':source_date,'match_status':'source_matched','era_status':'unverified','human_approval':False,'display_sha256':hashes['display'],'thumbnail_sha256':hashes['thumbnail']}
    records.append(entry)
    selected[uid]={'name':entry['canonical_name'],'image':paths['display'],'thumbnail':paths['thumbnail'],'source_sha256':PDF_SHA,'source_url':OFFICIAL_URL,'source_date':source_date,'match_status':'source_matched','era_status':'unverified','human_approval':False,'project_use_basis':'owner_directed_fair_use_reference','manual_page':pi+1,'manual_variant':official_variant}
 expected={u for group in MAP.values() for u in group}
 if len(expected)!=19 or set(selected)!=expected:raise AssertionError(f'UID mapping missing: {expected-set(selected)}')
 manifest_path=root/'data/catalog-images.js'
 data=manifest_path.read_text()
 prefix='globalThis.LPG_CATALOG_IMAGES='
 if not data.startswith(prefix):raise ValueError('Manifest format unexpectedly changed')
 old=json.loads(data[len(prefix):].strip().removesuffix(';'))
 if len(old)!=54 or any(uid in old for uid in expected):raise ValueError('Existing catalog-image state changed; stop before overwriting')
 merged={**old,**dict(sorted(selected.items()))}
 if len(merged)!=73:raise ValueError('Expected exactly 73 source-selected images')
 manifest_path.write_text(prefix+json.dumps(merged,ensure_ascii=False,separators=(',',':'))+';\n')
 (root/'database/image-reconciliation-or-20261011.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
 sw=root/'sw.js';s=sw.read_text()
 if s.count(CACHE_OLD)!=1:raise ValueError('Unrecognized old service-worker cache version')
 sw.write_text(s.replace(CACHE_OLD,CACHE_NEW))
 # Keep the existing focused browser regression aligned with the now-expanded cache.
 focused=root/'tests/catalog-images.cjs'
 if focused.exists():
  t=focused.read_text()
  if t.count(CACHE_OLD)!=1 or t.count('assert.equal(cacheCount,108)')!=1 or t.count("assert.equal(await page.locator('#researchResults .catalog-thumb').count(),54);")!=1:
   raise ValueError('Focused browser test changed; inspect before rewriting')
  t=t.replace(CACHE_OLD,CACHE_NEW).replace('assert.equal(cacheCount,108)','assert.equal(cacheCount,146)')
  t=t.replace("assert.equal(await page.locator('#researchResults .catalog-thumb').count(),54);", "assert.equal(await page.locator('#researchResults .catalog-thumb').count(),54);await page.locator('#researchState').selectOption('US-OR');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),19);await page.locator('#researchState').selectOption('US-WA');")
  t=t.replace('PASS: 54 thumbnails,','PASS: 54 WA and 19 OR thumbnails,').replace('108 cached images','146 cached images')
  focused.write_text(t)
 return records,merged

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--pdf',type=Path,help='Offline source for reproducible tests');ap.add_argument('--source-date',default='2026-10-11');args=ap.parse_args()
 records,merged=make(args.root,source_bytes(args.pdf),args.source_date)
 print(json.dumps({'source_pdf_sha256':PDF_SHA,'oregon_matches':len(records),'app_image_total':len(merged),'remaining':1138-len(merged),'status':'source_matched_not_era_or_human_verified'},indent=2))
if __name__=='__main__':main()