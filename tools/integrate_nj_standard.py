#!/usr/bin/env python3
"""Source-pinned integration of the NJ MVC standard Garden State plate.

The original is recovered from the private 40993449073 official harvest artifact.
Only JPEG derivatives enter the public repository. Human approval, issue era, and
commercial licensing are not claimed by source matching.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
UID = "LPG-US-NJ-00028"
NAME = "Standard New Jersey"
ORIGINAL = "NJ/New_Jersey_MVC_Standard_Plates_html/asset_0001.jpg"
SOURCE_DIR = "NJ/New_Jersey_MVC_Standard_Plates_html"
PAGE = "https://www.nj.gov/mvc/vehicles/standplates.htm"
ASSET = "https://www.nj.gov/mvc/images/standard.jpg"
ORIGINAL_SHA = "2612d12671decb4702ddd0876ded5a881e1707b9cdadfbc6797593caba712ccd"
REGISTRY_SHA = "cae973d3e18c4cfb80bfecc366f1701cd24a77a9511eeb5d5eeebcead2f41130"
PAGE_SHA = "adc5b136a9adefbee48defc7513d090c4f3e002f6ae3681e35edb579b6a47eaf"
OLD_CACHE = "lpg-current-images-20261029-mion61"
NEW_CACHE = "lpg-current-images-20261102-njstandard1"
PREFIX = "globalThis.LPG_CATALOG_IMAGES="

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def once(s: str, old: str, new: str) -> str:
    if s.count(old) != 1 or (new != old and new in s):
        raise ValueError("Expected exactly one baseline marker: " + old[:100])
    return s.replace(old, new)

def jpeg(raw: bytes, width_limit: int) -> tuple[bytes, list[int]]:
    with Image.open(io.BytesIO(raw)) as origin:
        origin.load()
        im = ImageOps.exif_transpose(origin).convert("RGBA")
        if im.width < 150 or im.height < 70 or not 1.35 <= im.width / im.height <= 3.8:
            raise ValueError("Source does not have credible plate dimensions")
        white = Image.new("RGBA", im.size, "white")
        white.alpha_composite(im)
        rgb = white.convert("RGB")
        rgb.thumbnail((width_limit, width_limit), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        rgb.save(output, "JPEG", quality=90, optimize=True, subsampling=0)
        return output.getvalue(), list(rgb.size)

def integrate(root: Path, evidence: Path) -> dict:
    folder = evidence / SOURCE_DIR
    registry = (folder / "assets.json").read_bytes()
    html = (folder / "source.html").read_bytes()
    if sha(registry) != REGISTRY_SHA or sha(html) != PAGE_SHA:
        raise ValueError("Official issuing-agency page or registry differs from reviewed archive")
    assets = json.loads(registry)
    if len(assets) != 1:
        raise ValueError("NJ standard page's source-asset registry changed")
    entry = assets[0]
    if (entry.get("status"), entry.get("source_page_url"),
        entry.get("direct_image_url"), entry.get("alt_text"), entry.get("sha256"),
        entry.get("file")) != (
            "downloaded", PAGE, ASSET, "Standard Plate Example", ORIGINAL_SHA,
            "harvest-output/" + ORIGINAL):
        raise ValueError("Official asset link, identity label or original hash mismatch")
    if b'<img src="../images/standard.jpg" alt="Standard Plate Example"' not in html:
        raise ValueError("Preserved official page does not link the referenced plate image")
    raw = (evidence / ORIGINAL).read_bytes()
    if len(raw) != 701105 or sha(raw) != ORIGINAL_SHA:
        raise ValueError("NJ MVC original image failed pinned SHA-256/size")
    with Image.open(io.BytesIO(raw)) as im:
        im.verify()
    with Image.open(io.BytesIO(raw)) as im:
        if im.size != (3678,1872):
            raise ValueError("Original image dimensions differ")

    catalog = json.loads((root / "data/image-campaign/manifest.json").read_text())
    if len(catalog) != 1138 or len({x["uid"] for x in catalog}) != 1138:
        raise ValueError("Immutable 1138-design catalog changed")
    canonical = next((x for x in catalog if x["uid"] == UID), None)
    if not canonical or canonical["jurisdiction_id"] != "US-NJ" or canonical["name"] != NAME:
        raise ValueError("NJ UID no longer refers to standard New Jersey")

    manifest = root / "data/catalog-images.js"
    code = manifest.read_text()
    if not code.startswith(PREFIX):
        raise ValueError("Unexpected image manifest structure")
    selected = json.loads(code[len(PREFIX):].strip().removesuffix(";"))
    if len(selected) != 697 or UID in selected:
        raise ValueError("Image baseline changed or NJ standard already selected")
    destinations = {
        kind: root / "assets" / "plates" / f"{UID}-{kind}.jpg"
        for kind in ("display", "thumbnail")
    }
    if any(p.exists() for p in destinations.values()):
        raise ValueError("Refusing to overwrite any existing plate derivative")

    rendered = {}
    for kind, limit in (("display",800),("thumbnail",300)):
        binary, shape = jpeg(raw,limit)
        rendered[kind] = {"bytes": binary, "sha256": sha(binary), "size": shape}
    selected[UID] = {
        "name": NAME,
        "image": f"./assets/plates/{UID}-display.jpg",
        "thumbnail": f"./assets/plates/{UID}-thumbnail.jpg",
        "source_sha256": ORIGINAL_SHA,
        "source_url": PAGE,
        "source_asset_url": ASSET,
        "source_date": "2026-10-29",
        "source_label": "Standard Plate Example (Garden State passenger plate)",
        "match_status": "source_matched",
        "era_status": "unverified",
        "human_approval": False,
        "project_use_basis": "owner_directed_fair_use_reference",
    }
    if len(selected) != 698 or len({x["image"] for x in selected.values()}) != 698:
        raise ValueError("New image selection is not one-to-one")

    worker = root / "sw.js"
    new_worker = once(worker.read_text(), OLD_CACHE, NEW_CACHE)
    testfile = root / "tests/catalog-images.cjs"
    tests = testfile.read_text()
    tests = once(tests, OLD_CACHE, NEW_CACHE)
    tests = once(tests, "assert.equal(cacheCount,1394)", "assert.equal(cacheCount,1396)")
    anchor = "await page.locator('#researchState').selectOption('CA-ON');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),39);"
    tests = once(tests, anchor, anchor + "await page.locator('#researchState').selectOption('US-NJ');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),1);")
    queue = root / "docs/CURRENT_IMAGE_CAMPAIGN_QUEUE.md"
    q = queue.read_text()
    q = once(q,"**Verified October 29, 2026.**","**Verified November 2, 2026.**")
    q = once(q,"**697 / 1,138 source-matched","**698 / 1,138 source-matched")
    q = once(q,"**441 UIDs remain unresolved**","**440 UIDs remain unresolved**")
    q = once(q,"**1,394** public display/thumbnail","**1,396** public display/thumbnail")
    q = once(q,"CA-ON 39.","CA-ON 39, NJ 1.")
    q = once(q,"| New Jersey | 38 |","| New Jersey | 37 |")
    q = once(q,"Remaining **441** distributed","Remaining **440** distributed")
    q = once(q,"## Current truth\n","## Current truth\n- **2026-11-02 NJ standard:** one archived MVC official sample (Garden State) visibly matched to LPG-US-NJ-00028; source SHA-256 pinned, display/thumbnail hashes recorded, era/human approval unverified. This is one source-matched design only, not a rights or era endorsement.\n")

    record = {
        "uid": UID, "catalog_name": NAME, "official_source_page": PAGE,
        "direct_asset_url": ASSET, "original_archive_run": 40993449073,
        "original_archive_artifact": "official-plate-harvest-40993449073",
        "archive_member": ORIGINAL, "official_page_html_sha256": PAGE_SHA,
        "official_asset_registry_sha256": REGISTRY_SHA,
        "source_original_sha256": ORIGINAL_SHA, "original_bytes": len(raw),
        "source_alt_text": "Standard Plate Example",
        "visual_identity_basis": "Source artwork has New Jersey / SAM·PLE / Garden State yellow-gradient passenger design; matches standard catalog design, not a specialty plate",
        "match_status": "source_matched", "era_status": "unverified",
        "human_approval": False, "commercial_rights_approval": False,
        "display_sha256": rendered["display"]["sha256"],
        "thumbnail_sha256": rendered["thumbnail"]["sha256"],
        "display_size": rendered["display"]["size"],
        "thumbnail_size": rendered["thumbnail"]["size"],
        "source_date": "2026-10-29",
    }
    # Only write after source, identity, baseline and unique-path preflight passed.
    for kind, dst in destinations.items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(rendered[kind]["bytes"])
    manifest.write_text(PREFIX + json.dumps(dict(sorted(selected.items())),ensure_ascii=False,separators=(",",":")) + ";\n")
    worker.write_text(new_worker)
    testfile.write_text(tests)
    queue.write_text(q)
    output = root / "database/image-reconciliation-nj-standard-20261102.json"
    if output.exists():
        raise ValueError("Would overwrite existing reconciliation record")
    output.write_text(json.dumps(record,indent=2,ensure_ascii=False) + "\n")
    return {"uid": UID, "newly_integrated": 1, "total": 698, "remaining": 440,
            "source_original_sha256": ORIGINAL_SHA,
            "display_sha256": record["display_sha256"],
            "thumbnail_sha256": record["thumbnail_sha256"]}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--evidence-dir",type=Path,required=True)
    args = p.parse_args()
    print(json.dumps(integrate(args.root,args.evidence_dir.resolve()),indent=2))
