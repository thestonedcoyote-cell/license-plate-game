#!/usr/bin/env python3
"""Download reviewed official plate sources on a networked GitHub runner.

Outputs are research artifacts, not automatically public assets. PDF extraction
preserves the source URL, page number, xref, hashes, and page renders for later
matching/reconstruction/rights review.
"""
import argparse,csv,hashlib,json,re,time
from pathlib import Path
from urllib.parse import urlparse
import requests

UA='LicensePlateGameResearch/0.2 (+official-source archival research)'

def safe_name(s):
    return re.sub(r'[^A-Za-z0-9._-]+','_',s).strip('_')[:120] or 'source'

def sha(data): return hashlib.sha256(data).hexdigest()

def download(session,url,path,delay=.6):
    time.sleep(delay)
    r=session.get(url,timeout=75,headers={'User-Agent':UA})
    r.raise_for_status(); path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(r.content)
    return {'bytes':len(r.content),'sha256':sha(r.content),'content_type':r.headers.get('content-type','')}

def extract_pdf(pdf_path,out_dir):
    import fitz
    doc=fitz.open(pdf_path); records=[]; seen=set(); out_dir.mkdir(parents=True,exist_ok=True)
    for page_no,page in enumerate(doc,1):
        # Full-page render is essential when plate artwork is vector or composited.
        pix=page.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False)
        page_dest=out_dir/f'page_{page_no:03d}.png'; pix.save(page_dest)
        text=page.get_text('text')
        (out_dir/f'page_{page_no:03d}.txt').write_text(text,encoding='utf-8')
        records.append({'kind':'page_render','page':page_no,'file':str(page_dest),'bytes':page_dest.stat().st_size,'sha256':sha(page_dest.read_bytes())})
        for img in page.get_images(full=True):
            xref=img[0]
            if xref in seen: continue
            seen.add(xref); info=doc.extract_image(xref); ext=info.get('ext','bin'); data=info['image']
            dest=out_dir/f'p{page_no:03d}_xref{xref}.{ext}'; dest.write_bytes(data)
            records.append({'kind':'embedded_image','page':page_no,'xref':xref,'file':str(dest),'bytes':len(data),'sha256':sha(data)})
    return records

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--manifest',default='data/harvest_sources.csv')
    ap.add_argument('--output',default='harvest-output')
    ap.add_argument('--codes',default='')
    ap.add_argument('--max-sources',type=int,default=8)
    a=ap.parse_args(); wanted={x.strip().upper() for x in a.codes.split(',') if x.strip()}
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True); session=requests.Session(); log=[]; count=0
    with open(a.manifest,newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            code=row.get('code','').upper(); mode=row.get('extraction_mode',''); kind=row.get('source_kind','')
            if wanted and code not in wanted: continue
            if mode!='bulk_pdf' and kind!='direct_image_asset': continue
            if count>=a.max_sources: break
            url=row['url']; title=row.get('title','source'); base=out/code/safe_name(title)
            try:
                ext=Path(urlparse(url).path).suffix.lower() or ('.pdf' if mode=='bulk_pdf' else '.bin')
                dest=base.with_suffix(ext); meta=download(session,url,dest)
                rec={'code':code,'title':title,'url':url,'source_kind':kind,'extraction_mode':mode,'file':str(dest),**meta,'status':'downloaded'}
                if ext=='.pdf' or 'pdf' in meta['content_type'].lower():
                    try: rec['extracted']=extract_pdf(dest,base.parent/(base.name+'_extracted'))
                    except Exception as e: rec['extract_error']=repr(e)
                log.append(rec); count+=1
            except Exception as e:
                log.append({'code':code,'title':title,'url':url,'status':'error','error':repr(e)})
    (out/'manifest.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
    ok=sum(x.get('status')=='downloaded' for x in log)
    print(json.dumps({'sources_attempted':len(log),'downloaded':ok,'output':str(out)},indent=2))
if __name__=='__main__': main()
