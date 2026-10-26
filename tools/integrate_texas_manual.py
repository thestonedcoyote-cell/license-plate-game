#!/usr/bin/env python3
"""Integrate exactly 157 Texas plate samples from a byte-pinned TxDMV guide.

Automatic candidate identification uses uniquely matching printed plate labels,
their adjacent embedded sample images and the frozen 1,138-entry LPG catalog.
The source's 157 examples were previously reviewed in contact sheets. This tool
does NOT certify plate era, rights, physical-device use, or human final approval.
"""
import argparse,hashlib,io,json,re,unicodedata
from pathlib import Path
import fitz
from PIL import Image,ImageOps

SOURCE_URL="https://www.txdmv.gov/sites/default/files/body-files/Special-Plate-Guide.pdf"
# Two packaging variants inspected Oct 26 have identical 157 embedded sample images.
PDF_SHAS={"9b3fb1a085866fcbe1205e06a76486b76fa7ed2c7346b0b24b871ffd0e9e91ef",
          "bcf40c803c48861215f5e222a90709a7cd7a8e33c8f189d06cd320b2b8d943cb"}
OLD_CACHE="lpg-current-images-20261012-akms"
NEW_CACHE="lpg-current-images-20261026-tx"
EXCLUDED={"LPG-US-TX-00164","LPG-US-TX-00001","LPG-US-TX-00041",
          "LPG-US-TX-00150","LPG-US-TX-00152","LPG-US-TX-00153","LPG-US-TX-00163"}

def sha(b):return hashlib.sha256(b).hexdigest()
def norm(s):
 s=unicodedata.normalize("NFKD",s).lower().replace("’","'")
 return re.sub("[^a-z0-9]+"," ",s).strip()

def extract_labels(page,page_no):
 blocks=page.get_text("dict")["blocks"]
 images=[b for b in blocks if b["type"]==1 and b["bbox"][2]-b["bbox"][0]>=110
         and b["bbox"][3]-b["bbox"][1]>=65]
 labels=[]
 for block in blocks:
  if block["type"]!=0:continue
  lines=[("".join(span["text"] for span in line["spans"]).strip(),line["bbox"])
         for line in block["lines"]]
  for i,(txt,box) in enumerate(lines):
   m=re.match(r"^PLATE NAME\s*:\s*(.*)$",txt,re.I)
   if not m:continue
   name=m.group(1).strip()
   if not name:
    for t,_ in lines[i+1:]:
     if t:name=t;break
   elif i+1<len(lines):
    next_line,next_box=lines[i+1]
    if next_line and not re.search("RTS NAME|Form to Apply",next_line,re.I) and abs(box[0]-next_box[0])<15 and -5<next_box[1]-box[3]<15 and len(name)<45:
     name+=" "+next_line
   if name:labels.append({"name":name,"page":page_no,"y":box[1]})
 labels.sort(key=lambda x:x["y"])
 pairs=[]
 for i,label in enumerate(labels):
  stop=labels[i+1]["y"] if i+1<len(labels) else 699
  candidates=[b for b in images if b["bbox"][1]>=label["y"] and b["bbox"][1]<stop
              and b["bbox"][0]<310]
  if len(candidates)!=1:raise ValueError(f"Ambiguous image region page {page_no}: {label['name']} candidates={len(candidates)}")
  pairs.append((label,candidates[0]))
 return pairs

def source_bytes(local=None):
 if local:return Path(local).read_bytes()
 import requests
 resp=requests.get(SOURCE_URL,timeout=120,headers={"User-Agent":"LicensePlateGameResearch/0.7 (official-source attribution)"})
 resp.raise_for_status()
 return resp.content

def integrate(root,pdf_bytes):
 source_sha=sha(pdf_bytes)
 if source_sha not in PDF_SHAS:raise ValueError("Texas manual PDF bytes changed; manual review required")
 doc=fitz.open(stream=pdf_bytes,filetype="pdf")
 if len(doc)!=48:raise ValueError("Texas manual page count changed")
 catalog=json.loads((root/"data/image-campaign/manifest.json").read_text(encoding="utf-8"))
 texas=[r for r in catalog if r["jurisdiction_id"]=="US-TX"]
 assert len(catalog)==1138 and len(texas)==164
 names={}
 for record in texas:names.setdefault(norm(record["name"]),[]).append(record)
 samples=[]
 for i,page in enumerate(doc,1):
  samples.extend(extract_labels(page,i))
 if len(samples)!=161:raise ValueError(f"Expected 161 unique printed design sections, got {len(samples)}")
 mappings={}; used={};matched_labels=set()
 for label,image in samples:
  name=norm(label["name"]);candidates=names.get(name,[])
  if len(candidates)!=1:continue
  uid=candidates[0]["uid"]
  if uid in mappings:raise ValueError(f"Duplicate catalog name/UID {uid}")
  if id(image) in used:raise ValueError("Reused plate image block")
  mappings[uid]=(label,image);used[id(image)]=uid;matched_labels.add(name)
 if len(mappings)!=157:raise ValueError(f"Expected 157 source-matched names, got {len(mappings)}")
 missing={r["uid"] for r in texas}-set(mappings)
 if missing!=EXCLUDED:raise ValueError(f"Unexpected unresolved Texas IDs {sorted(missing)}")
 marker="globalThis.LPG_CATALOG_IMAGES="
 path=root/"data/catalog-images.js";old=path.read_text(encoding="utf-8").strip()
 if not old.startswith(marker):raise ValueError("Catalog manifest format changed")
 entries=json.loads(old.removeprefix(marker).rstrip(";"))
 if len(entries)!=149 or set(mappings).intersection(entries):raise ValueError("Existing 149 samples changed or Texas UIDs already selected")
 derivative_dir=root/"assets/plates";derivative_dir.mkdir(exist_ok=True,parents=True)
 records=[];seen_hashes={}
 for uid,(label,b) in sorted(mappings.items()):
  raw=b["image"];original_sha=sha(raw)
  with Image.open(io.BytesIO(raw)) as source:
   plate=ImageOps.exif_transpose(source).convert("RGB")
   if not(180<=plate.width<=2500 and 80<=plate.height<=1200 and 1.35<plate.width/plate.height<3.9):
    raise ValueError(f"Not a plausible plate source {uid}: {plate.size}")
   hashes={}
   for role,size in (("display",800),("thumbnail",300)):
    dst=derivative_dir/f"{uid}-{role}.jpg"
    if dst.exists():raise ValueError(f"Would overwrite plate {dst}")
    img=plate.copy();img.thumbnail((size,size),Image.Resampling.LANCZOS)
    img.save(dst,quality=90,optimize=True)
    hashes[role+"_sha256"]=sha(dst.read_bytes())
  entries[uid]={"name":next(r["name"] for r in texas if r["uid"]==uid),
                "image":f"./assets/plates/{uid}-display.jpg",
                "thumbnail":f"./assets/plates/{uid}-thumbnail.jpg",
                "source_sha256":original_sha,"source_document_sha256":source_sha,
                "source_url":SOURCE_URL,"source_date":"2026-10-26","manual_page":label["page"],
                "match_status":"source_matched","era_status":"unverified",
                "human_approval":False,"project_use_basis":"owner_directed_fair_use_reference"}
  records.append({"uid":uid,"source_label":label["name"],"pdf_page":label["page"],
                  "source_bbox":[round(float(z),4) for z in b["bbox"]],
                  "source_image_sha256":original_sha,"source_document_sha256":source_sha,
                  "embedded_width":b["width"],"embedded_height":b["height"],
                  "mapping_basis":"unique_exact_printed_name_and_adjacent_embedded_plate",
                  "match_status":"source_matched","era_status":"unverified",
                  "human_approval":False,**hashes})
 if len(records)!=157 or len(entries)!=306:raise ValueError("Texas image totals disagree")
 path.write_text(marker+json.dumps(dict(sorted(entries.items())),ensure_ascii=False,separators=(",",":"))+";\n",encoding="utf-8")
 target=root/"database/image-reconciliation-tx-20261026.json"
 target.write_text(json.dumps({"source_url":SOURCE_URL,"source_document_sha256":source_sha,"selected":records,
                               "unresolved_uid_list":sorted(missing),
                               "unresolved_count":7},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 sw=root/"sw.js";s=sw.read_text(encoding="utf-8")
 if s.count(OLD_CACHE)!=1:raise ValueError("Service worker cache version unexpected")
 sw.write_text(s.replace(OLD_CACHE,NEW_CACHE),encoding="utf-8")
 test=root/"tests/catalog-images.cjs"
 t=test.read_text(encoding="utf-8")
 needle="await page.locator('#researchState').selectOption('US-MS');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),35);"
 if any(t.count(x)!=1 for x in (needle,OLD_CACHE,"assert.equal(cacheCount,298)","298 cached images")):
  raise ValueError("Focused browser test changed; inspect before automatic update")
 t=t.replace(needle,needle+"await page.locator('#researchState').selectOption('US-TX');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),157);")
 t=t.replace(OLD_CACHE,NEW_CACHE).replace("assert.equal(cacheCount,298)","assert.equal(cacheCount,612)")
 t=t.replace("35 MS thumbnails","35 MS, 157 TX thumbnails").replace("298 cached images","612 cached images")
 test.write_text(t,encoding="utf-8")
 return {"source_sha":source_sha,"source_matches":157,"selected_total":306,"remaining":832,"derivatives_added":314,"unresolved_texas":7}
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--pdf",type=Path);ap.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
 a=ap.parse_args();print(json.dumps(integrate(a.root,source_bytes(a.pdf)),indent=2))
