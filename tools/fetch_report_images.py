import concurrent.futures,hashlib,html,json,re,urllib.request,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
import argparse
ap=argparse.ArgumentParser(description='Retrieve the three image leads in the supplied report through their Commons description pages.');ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();root=args.out;root.mkdir(parents=True,exist_ok=True)
seeds=[('AL','2001_Alabama_license_plate_Auburn.jpg','Zul32','CC BY-SA 3.0','https://creativecommons.org/licenses/by-sa/3.0/'),('AR','Arkansas_2011_license_plate.jpg','SuperSonic337','CC0 1.0','https://creativecommons.org/publicdomain/zero/1.0/'),('PR','Puerto_Rico_—_License_plate_"Mayagüez_2010".JPG','Mattes','CC BY 2.0 DE (photograph); public-domain assertion for depicted object','https://creativecommons.org/licenses/by/2.0/de/')]
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'LPG-Image-Database/1.0 (reference research)'})
 with urllib.request.urlopen(req,timeout=45) as r:return r.read(),r.url
def fetch(seed):
 code,title,author,license,url=seed;page='https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(title,safe='')
 item=dict(code=code,title=title,author=author,source_license=license,license_url=url,source_page=page,retrieved_at=datetime.now(timezone.utc).isoformat())
 try:
  body,final=get(page);(root/(code+'.html')).write_bytes(body)
  match=re.search(r'class="fullImageLink"[\s\S]*?<a href="([^"]+)"',body.decode())
  if not match:raise ValueError('No original file URL on source description page')
  image_url=html.unescape(match[1]);data,actual=get(image_url);path=root/(code+'.jpg');path.write_bytes(data)
  from PIL import Image
  with Image.open(path) as im:im.verify()
  with Image.open(path) as im:w,h=im.size
  item.update(status='downloaded',image_url=actual,path=str(path),page_path=str(root/(code+'.html')),sha256=hashlib.sha256(data).hexdigest(),width=w,height=h)
 except Exception as e:item.update(status='failed',error=str(e))
 return item
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:result=list(ex.map(fetch,seeds))
(root/'manifest.json').write_text(json.dumps(result,indent=2,ensure_ascii=False));print(json.dumps(result,indent=2,ensure_ascii=False))
