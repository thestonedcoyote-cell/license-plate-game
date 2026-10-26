#!/usr/bin/env python3
"""Stage 64 manually inspected California/Wisconsin issuing-agency plate samples.

Only explicitly pinned UID=harvest-file pairs are allowed. Every source image
must still match the original harvested hash and the frozen catalog identity.
This is source-matching, NOT era, license or final human approval.
"""
import argparse,hashlib,io,json,re
from pathlib import Path
from PIL import Image,ImageOps

PREVIOUS="lpg-current-images-20261026-tx"
CURRENT="lpg-current-images-20261026-cawi"
SOURCE_RUN=40386466698
SRC_MAP="data/image-batches/ca-wi-reviewed-map.txt"
SRC_URLS={
 "CA":"https://www.dmv.ca.gov/portal/vehicle-registration/license-plates-decals-and-placards/license-plates/special-interest-special-license-plates/",
 "WI":"https://wisconsindot.gov/Pages/dmv/vehicles/title-plates/special.aspx",
}
ROOT=Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()

def selections(p):
 rows={}
 for line in p.read_text(encoding="utf-8").splitlines():
  line=line.strip()
  if not line or line.startswith("#"):continue
  if line.count("=")!=1:raise ValueError("Invalid reviewed mapping syntax")
  uid,asset=line.split("=")
  if uid in rows or not re.fullmatch(r"LPG-US-(CA|WI)-\d{5}",uid):raise ValueError("Unsafe/duplicate catalog UID")
  if not re.fullmatch(r"asset_\d{4}\.(?:gif|png|jpg|jpeg|webp)",asset):raise ValueError("Unsafe asset name")
  rows[uid]=asset
 if len(rows)!=64 or sum(k.startswith("LPG-US-CA-") for k in rows)!=33 or sum(k.startswith("LPG-US-WI-") for k in rows)!=31:
  raise ValueError("Only the exact inspected 33 CA + 31 WI mapping is permitted")
 if "LPG-US-WI-00007" in rows:raise ValueError("Official WI Civil Air Patrol caption is mismatched and excluded")
 return rows

def source_index(records):
 index={}
 for group in records:
  if group["code"] not in ("CA","WI"):continue
  assert group["status"]=="downloaded"
  for record in group.get("gallery",{}).get("records",[]):
   if record.get("status")!="downloaded":continue
   name=Path(record["file"]).name
   key=(group["code"],name)
   if key in index:raise ValueError(f"Ambiguous source-file basename: {key}")
   if record["source_page_url"].split("?")[0].rstrip("/")!=SRC_URLS[group["code"]].rstrip("/"):
    raise ValueError(f"Unexpected source agency URL: {key}")
   index[key]=record
 return index

def derivative(data,size):
 with Image.open(io.BytesIO(data)) as raw:
  frame=ImageOps.exif_transpose(raw).convert("RGBA")
  if frame.width<90 or frame.height<35 or not 1.35<frame.width/frame.height<3.8:
   raise ValueError(f"Unlikely plate sample geometry: {frame.size}")
  opaque=Image.new("RGBA",frame.size,"white");opaque.alpha_composite(frame)
  im=opaque.convert("RGB")
  im.thumbnail((size,size),Image.Resampling.LANCZOS)
  output=io.BytesIO();im.save(output,format="JPEG",quality=90,optimize=True)
  return output.getvalue(),list(im.size)

def integrate(root,evidence):
 evidence=evidence.resolve()
 archive=json.loads((evidence/"manifest.json").read_text(encoding="utf-8"))
 index=source_index(archive)
 maps=selections(root/SRC_MAP)
 pins={}
 for line in (root/"data/image-batches/ca-wi-original-hashes.txt").read_text(encoding="utf-8").splitlines():
  uid,value=line.split("=")
  if uid in pins or not re.fullmatch("[a-f0-9]{64}",value):raise ValueError("Invalid or duplicate pinned original source hash")
  pins[uid]=value
 if set(pins)!=set(maps):raise ValueError("Reviewed UID and pinned-original manifests differ")
 canonical={r["uid"]:r for r in json.loads((root/"data/image-campaign/manifest.json").read_text(encoding="utf-8"))}
 if len(canonical)!=1138:raise ValueError("Immutable canonical UID baseline changed")
 image_js=root/"data/catalog-images.js";raw=image_js.read_text(encoding="utf-8").strip()
 prefix="globalThis.LPG_CATALOG_IMAGES="
 if not raw.startswith(prefix):raise ValueError("JS manifest format changed")
 existing=json.loads(raw.removeprefix(prefix).rstrip(";"))
 if len(existing)!=306 or any(u in existing for u in maps):raise ValueError("Expected 306 previous sample IDs with no overwrite")
 sw=root/"sw.js";s=sw.read_text(encoding="utf-8")
 if s.count(PREVIOUS)!=1 or CURRENT in s:raise ValueError("Offline cache version mismatch")
 test=root/"tests/catalog-images.cjs";t=test.read_text(encoding="utf-8")
 needle="await page.locator('#researchState').selectOption('US-TX');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),157);"
 if any(t.count(v)!=1 for v in (needle,PREVIOUS,"assert.equal(cacheCount,612)","612 cached images")):
  raise ValueError("Browser regression baseline differs; manual review required")
 outputs={};records=[]
 for uid,asset in sorted(maps.items()):
  code=uid.split("-")[2];source=index.get((code,asset))
  if source is None:raise ValueError(f"Missing harvested source image {uid}: {asset}")
  entry=canonical.get(uid)
  if entry is None or entry["jurisdiction_id"]!="US-"+code:
   raise ValueError(f"Unknown immutable UID {uid}")
  file=(evidence/source["file"].removeprefix("harvest-output/")).resolve()
  if not file.is_relative_to(evidence):raise ValueError("Attempted source file traversal")
  data=file.read_bytes()
  if sha(data)!=pins[uid] or source["sha256"]!=pins[uid]:
   raise ValueError(f"Source hash changed from original October 26 reviewed archive for {uid}")
  label=source.get("alt_text","").strip()
  if not label:raise ValueError(f"No issuing-agency source label for {uid}")
  d_hashes={};d_shapes={}
  for kind,limit in (("display",800),("thumbnail",300)):
   rel=f"assets/plates/{uid}-{kind}.jpg"
   if (root/rel).exists():raise ValueError(f"Existing plate asset would be overwritten {uid}")
   derivative_data,shape=derivative(data,limit)
   outputs[rel]=derivative_data
   d_hashes[kind+"_sha256"]=sha(derivative_data)
   d_shapes[kind+"_size"]=shape
  existing[uid]={
   "name":entry["name"],"image":f"./assets/plates/{uid}-display.jpg",
   "thumbnail":f"./assets/plates/{uid}-thumbnail.jpg",
   "source_sha256":source["sha256"],"source_url":source["source_page_url"],
   "source_asset_url":source["direct_image_url"],"source_label":label,
   "source_date":"2026-10-26","source_run_id":SOURCE_RUN,
   "match_status":"source_matched","era_status":"unverified","human_approval":False,
   "project_use_basis":"owner_directed_fair_use_reference"
  }
  records.append({
   "uid":uid,"name":entry["name"],"jurisdiction_id":"US-"+code,
   "source_page_url":source["source_page_url"],
   "source_asset_url":source["direct_image_url"],"source_label":label,
   "source_file":source["file"],"source_sha256":source["sha256"],
   "source_size":[source["width_px"],source["height_px"]],
   "evidence_method":"explicit_inspected_source_file_map_plus_sha256",
   "match_status":"source_matched","era_status":"unverified","human_approval":False,
   **d_hashes,**d_shapes
  })
 if len(records)!=64 or len(outputs)!=128 or len(existing)!=370:
  raise ValueError("Unexpected candidate totals")
 # All input/provenance checks above precede any writes.
 for rel,data in outputs.items():
  p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 image_js.write_text(prefix+json.dumps(dict(sorted(existing.items())),ensure_ascii=False,separators=(",",":"))+";\n",encoding="utf-8")
 sw.write_text(s.replace(PREVIOUS,CURRENT),encoding="utf-8")
 t=t.replace(needle,needle+"await page.locator('#researchState').selectOption('US-CA');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),33);await page.locator('#researchState').selectOption('US-WI');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),31);")
 t=t.replace(PREVIOUS,CURRENT).replace("assert.equal(cacheCount,612)","assert.equal(cacheCount,740)")
 t=t.replace("157 TX thumbnails","157 TX, 33 CA, 31 WI thumbnails").replace("612 cached images","740 cached images")
 test.write_text(t,encoding="utf-8")
 p=root/"database/image-reconciliation-ca-wi-20261026.json"
 p.write_text(json.dumps({"source_run_id":SOURCE_RUN,"source_archive_status":"originals archived privately; hashes from Actions source manifest",
                          "selected_count":64,"selections":records,
                          "known_exclusion":"WI Civil Air Patrol source alt actually depicts Spay/Neuter plate; excluded",
                          "era_status":"unverified","human_approval":False},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 return {"source_run":SOURCE_RUN,"new_selections":64,"total_selected":370,"gap":768,
         "image_derivatives_added":128,"previous_selection_count":306,
         "status":"source_matched_not_human_or_era_verified"}
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--root",type=Path,default=ROOT)
 a.add_argument("--evidence-dir",type=Path,required=True);args=a.parse_args()
 print(json.dumps(integrate(args.root,args.evidence_dir),indent=2))
