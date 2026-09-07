#!/usr/bin/env python3
"""Harvest reviewed official plate sources on a networked GitHub runner.

Outputs are private research artifacts, not automatically public assets.
PDF extraction preserves source URL, page, xref, hashes, page renders and text.
HTML-gallery extraction preserves source-page URL, direct asset URL, alt text,
host relationship, dimensions when readable, and hashes. It downloads only
assets directly referenced by a reviewed official page; it does not spider the web.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re,time
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse,urljoin
import requests

UA='LicensePlateGameResearch/0.3 (+official-source archival research)'
IMAGE_EXTS={'.png','.jpg','.jpeg','.webp','.gif','.svg','.avif'}

def safe_name(s):
    return re.sub(r'[^A-Za-z0-9._-]+','_',s).strip('_')[:120] or 'source'

def sha(data): return hashlib.sha256(data).hexdigest()

def request(session,url,delay=.45):
    time.sleep(delay)
    r=session.get(url,timeout=75,headers={'User-Agent':UA})
    r.raise_for_status()
    return r

def download(session,url,path,delay=.45):
    r=request(session,url,delay)
    path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(r.content)
    return {'bytes':len(r.content),'sha256':sha(r.content),'content_type':r.headers.get('content-type',''),'final_url':r.url}

def image_dimensions(data,content_type=''):
    if 'svg' in content_type.lower() or data.lstrip().startswith(b'<svg'):
        return None,None
    try:
        from PIL import Image
        with Image.open(BytesIO(data)) as im: return im.width,im.height
    except Exception:
        return None,None

def extract_pdf(pdf_path,out_dir):
    import fitz
    doc=fitz.open(pdf_path); records=[]; seen=set(); out_dir.mkdir(parents=True,exist_ok=True)
    for page_no,page in enumerate(doc,1):
        # Full-page render is essential when plate artwork is vector or composited.
        pix=page.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False)
        page_dest=out_dir/f'page_{page_no:03d}.png'; pix.save(page_dest)
        text=page.get_text('text')
        text_dest=out_dir/f'page_{page_no:03d}.txt'; text_dest.write_text(text,encoding='utf-8')
        records.append({'kind':'page_render','page':page_no,'file':str(page_dest),'bytes':page_dest.stat().st_size,'sha256':sha(page_dest.read_bytes()),'text_file':str(text_dest)})
        for img in page.get_images(full=True):
            xref=img[0]
            if xref in seen: continue
            seen.add(xref); info=doc.extract_image(xref); ext=info.get('ext','bin'); data=info['image']
            dest=out_dir/f'p{page_no:03d}_xref{xref}.{ext}'; dest.write_bytes(data)
            w,h=image_dimensions(data,info.get('ext',''))
            records.append({'kind':'embedded_image','page':page_no,'xref':xref,'file':str(dest),'bytes':len(data),'sha256':sha(data),'width_px':w,'height_px':h})
    return records

def srcset_urls(value):
    urls=[]
    for part in (value or '').split(','):
        first=part.strip().split(' ')[0].strip()
        if first: urls.append(first)
    return urls

def candidate_assets(html,source_url):
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(html,'html.parser'); found=[]
    def add(raw,alt='',context='',via='img'):
        if not raw or raw.startswith(('data:','blob:','javascript:')): return
        u=urljoin(source_url,raw.strip())
        if urlparse(u).scheme not in {'http','https'}: return
        found.append({'url':u,'alt':(alt or '').strip(),'context':(context or '').strip(),'via':via})
    for img in soup.find_all('img'):
        alt=img.get('alt',''); context=' '.join(img.stripped_strings)
        for key in ('src','data-src','data-lazy-src','data-original'):
            add(img.get(key),alt,context,key)
        for key in ('srcset','data-srcset'):
            for u in srcset_urls(img.get(key)): add(u,alt,context,key)
    for source in soup.find_all('source'):
        for u in srcset_urls(source.get('srcset')): add(u,'','picture/source','source-srcset')
    for meta in soup.find_all('meta'):
        if meta.get('property') in {'og:image','og:image:url'} or meta.get('name') in {'twitter:image'}:
            add(meta.get('content'),'','metadata',meta.get('property') or meta.get('name'))
    # Some government CMS pages link image files instead of placing them in <img>.
    for a in soup.find_all('a',href=True):
        href=a['href']; ext=Path(urlparse(href).path).suffix.lower()
        if ext in IMAGE_EXTS: add(href,a.get_text(' ',strip=True),'linked image','anchor')
    # Stable-order de-duplication. Prefer the first occurrence because it often has the best alt text.
    uniq=[]; seen=set()
    for x in found:
        key=x['url'].split('#')[0]
        if key in seen: continue
        seen.add(key); x['url']=key; uniq.append(x)
    return uniq

def harvest_html_gallery(session,source_url,out_dir,max_assets=600):
    from bs4 import BeautifulSoup
    r=request(session,source_url); html=r.text
    out_dir.mkdir(parents=True,exist_ok=True)
    html_dest=out_dir/'source.html'; html_dest.write_text(html,encoding='utf-8',errors='replace')
    soup=BeautifulSoup(html,'html.parser')
    text_dest=out_dir/'source.txt'; text_dest.write_text(soup.get_text('\n',strip=True),encoding='utf-8')
    source_host=urlparse(r.url).hostname or ''
    records=[]; hashes={}
    for idx,c in enumerate(candidate_assets(html,r.url)[:max_assets],1):
        try:
            rr=request(session,c['url'],.18); data=rr.content; ctype=rr.headers.get('content-type','')
            if not (ctype.lower().startswith('image/') or Path(urlparse(rr.url).path).suffix.lower() in IMAGE_EXTS):
                records.append({'kind':'html_asset','status':'skipped_non_image','source_page_url':r.url,'direct_image_url':c['url'],'content_type':ctype,'alt_text':c['alt'],'via':c['via']}); continue
            digest=sha(data)
            if digest in hashes:
                records.append({'kind':'html_asset','status':'duplicate_hash','source_page_url':r.url,'direct_image_url':c['url'],'duplicate_of':hashes[digest],'sha256':digest,'alt_text':c['alt'],'via':c['via']}); continue
            ext=Path(urlparse(rr.url).path).suffix.lower()
            if ext not in IMAGE_EXTS:
                ext={ 'image/png':'.png','image/jpeg':'.jpg','image/webp':'.webp','image/gif':'.gif','image/svg+xml':'.svg','image/avif':'.avif'}.get(ctype.split(';')[0].lower(),'.img')
            dest=out_dir/f'asset_{idx:04d}{ext}'; dest.write_bytes(data); hashes[digest]=str(dest)
            w,h=image_dimensions(data,ctype); asset_host=urlparse(rr.url).hostname or ''
            records.append({'kind':'html_asset','status':'downloaded','source_page_url':r.url,'direct_image_url':rr.url,'requested_image_url':c['url'],'file':str(dest),'bytes':len(data),'sha256':digest,'content_type':ctype,'width_px':w,'height_px':h,'alt_text':c['alt'],'context':c['context'],'via':c['via'],'source_host':source_host,'asset_host':asset_host,'same_host':asset_host==source_host})
        except Exception as e:
            records.append({'kind':'html_asset','status':'error','source_page_url':r.url,'direct_image_url':c['url'],'alt_text':c['alt'],'via':c['via'],'error':repr(e)})
    (out_dir/'assets.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    return {'source_page_url':r.url,'source_html':str(html_dest),'source_text':str(text_dest),'candidates':len(candidate_assets(html,r.url)),'records':records}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--manifest',default='data/harvest_sources.csv')
    ap.add_argument('--output',default='harvest-output')
    ap.add_argument('--codes',default='')
    ap.add_argument('--max-sources',type=int,default=8)
    ap.add_argument('--max-html-assets',type=int,default=600)
    a=ap.parse_args(); wanted={x.strip().upper() for x in a.codes.split(',') if x.strip()}
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True); session=requests.Session(); log=[]; count=0
    with open(a.manifest,newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            code=row.get('code','').upper(); mode=row.get('extraction_mode',''); kind=row.get('source_kind','')
            if wanted and code not in wanted: continue
            supported=mode in {'bulk_pdf','html_gallery'} or kind=='direct_image_asset'
            if not supported: continue
            if count>=a.max_sources: break
            url=row['url']; title=row.get('title','source'); base=out/code/safe_name(title)
            try:
                if mode=='html_gallery':
                    gallery=harvest_html_gallery(session,url,base.parent/(base.name+'_html'),a.max_html_assets)
                    rec={'code':code,'title':title,'url':url,'source_kind':kind,'extraction_mode':mode,'status':'downloaded','gallery':gallery}
                else:
                    ext=Path(urlparse(url).path).suffix.lower() or ('.pdf' if mode=='bulk_pdf' else '.bin')
                    dest=base.with_suffix(ext); meta=download(session,url,dest)
                    rec={'code':code,'title':title,'url':url,'source_kind':kind,'extraction_mode':mode,'file':str(dest),**meta,'status':'downloaded'}
                    if ext=='.pdf' or 'pdf' in meta['content_type'].lower():
                        try: rec['extracted']=extract_pdf(dest,base.parent/(base.name+'_extracted'))
                        except Exception as e: rec['extract_error']=repr(e)
                log.append(rec); count+=1
            except Exception as e:
                log.append({'code':code,'title':title,'url':url,'source_kind':kind,'extraction_mode':mode,'status':'error','error':repr(e)})
    (out/'manifest.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
    ok=sum(x.get('status')=='downloaded' for x in log)
    errors=sum(x.get('status')=='error' for x in log)
    html_assets=sum(sum(1 for a in x.get('gallery',{}).get('records',[]) if a.get('status')=='downloaded') for x in log)
    print(json.dumps({'sources_attempted':len(log),'downloaded_sources':ok,'source_errors':errors,'html_assets_downloaded':html_assets,'output':str(out)},indent=2))
if __name__=='__main__': main()
