# LPG — Active Plate Image Campaign Queue

**Checkpoint (2026-10-11, America/Los_Angeles)**

Source repository: `thestonedcoyote-cell/license-plate-game`.
Immutable runtime catalog: **1,138 UIDs** across **58** represented jurisdictions.
Source-matched in web catalog: **149** (54 Washington + 19 Oregon + 41 Alaska + 35 Mississippi); **989 remain without acquired matching images**.
Runtime derivatives: **298 JPEGs**. Historical 291-schematic baseline is not acquired-image coverage.
No current match is a substitute for era/accuracy verification, independent rights assessment, or an actual human review decision.
Three unresolved research/report candidates are **not** additions to the 1,138 runtime designs.

## Where we are
- Washington's issuing-agency gallery supplied 54 source-matched examples. Two incorrect automated pairings were explicitly rejected. Washington historical variants remain unresolved.
- Oregon's July 2026 official 38-page DMV manual supplied **19 individually cropped and inspected examples**, including distinct current/previous Crater Lake, Cultural and Salmon designs. Generator, 38 image derivatives and source hash/mapping record are committed. PR #21 merged at `af64fe5dde48af0c663ad6aa180d3592108d6f2b`; Pages run `38199925236` passed.
- Private, verified portable image/database checkpoint: `LPG_Image_Database_2026-10-12.zip`, Library `libfile_c3bd712da6a48191848af1b34dbb70ad`, SHA-256 `2d725d87d5e3ead8e1151667b36294a833819d3fea82c5a8fb2640ab7dba3549`.
- Oregon source evidence package: `LPG_OR_Official_Harvest_2026-10-11.zip`, Library `libfile_1c9a2771f7308191b85009db82c688da`. The source PDF SHA-256 is `56ccdbf8dbbcd39c2803308f255e7374998c1ab418893da8b3577ff2098bdd50`.
- **26 of 58** catalog jurisdictions now have at least one official source lead (previously 17). A source lead is not an acquired image or an exhaustive gallery.
- Alaska/Mississippi batch: 41 AK + 35 MS inspected source matches, PR #24 merged at `2f1036ef16954ef93bff028c726648cd73f14254`; Pages run `38201004819` passed. Seven ambiguous/missing designs remain excluded. Source archive: Library `libfile_745e40877fcc8191a3476a2c1bbe2313`. Current portable database: `LPG_Image_Database_2026-10-12_Batch02.zip`, Library `libfile_e9eea656eb5081918bc7eeb3e0c56278`, SHA-256 `112cf8aa65ec79662d0c0a282eb5bd31cbfac58dbb1ed79c201089e944293c34`.

## Active execution
1. **LPG-P1-BATCH02:** GitHub official-source harvest run [38200139649](https://github.com/thestonedcoyote-cell/license-plate-game/actions/runs/38200139649) **completed with exceptions**. Texas official Specialty Plate Guide downloaded: 48-page PDF, SHA-256 `9b3fb1a085866fcbe1205e06a76486b76fa7ed2c7346b0b24b871ffd0e9e91ef`, 209 rendered/extracted records. Alaska official gallery: 48 downloaded image files; Mississippi official gallery: 307 downloaded image files. Florida 2026 official brochure returned HTTP 403 (not acquired). Exactly 76 AK/MS UID selections subsequently integrated by PR #24; no Texas/Florida new selections yet.
2. **LPG-P1-BATCH03:** GitHub official harvest run [38201130935](https://github.com/thestonedcoyote-cell/license-plate-game/actions/runs/38201130935) for California, Nevada, Wisconsin and Indiana, with 188 potential existing catalog UIDs. Trigger commit `53584827f18bc87086893dc50c85a6984ee1c4a2`; **in progress** as of this checkpoint. Inspect outcome, preserve the complete original evidence archive in Library and report source errors. No new plate match is assumed merely because pages/images download.
3. Index the retrieved Texas PDF pages, plus the next harvested HTML galleries, against the corresponding catalog UIDs. Identify high-confidence one-to-one designs from official names and layouts; keep ambiguous and historical versions unresolved. Do not promote all PDF images simply because extracted.
4. Generate aspect-preserving display/thumbnail JPEGs only from independently inspected source matches; preserve source URL, page/crop coordinates, original/derivative hashes, status `source_matched`, `era_status=unverified` and `human_approval=false` until further review.
5. Merge source mappings into **one writer's** portable database and into the web `data/catalog-images.js` manifest. Reconcile 1,138 immutable IDs; check foreign keys, UID uniqueness, orphan/missing assets, derivative hashes, offline service-worker cache, Identify/catalog/collection and theme/viewport behavior. Create a review PR and inspect GitHub CI and Pages deployment before calling a web image live.
6. Keep signed Android distribution **separate**. Debug APK CI does not prove signed on-device update/persistence. Real upgrade acceptance is still needed before stable/latest release.

## Scaling after batch 02
- Harvest existing high-yield official manuals/galleries (CA, NV, WI, MN, NE, IN, AL, CT, WV, OK), in jurisdiction-sized, traceable batches, stopping and documenting 403/404/asset failures.
- Expand the registry for **32 remaining catalog jurisdictions lacking confirmed official leads**. Prioritize by existing catalog UID count; do not invent coverage for a source landing page that lacks images.
- Build reusable source-evidence ingestion and candidate-mapping tooling that processes HTML and illustrated PDFs. Expose candidate lists and conflict tickets, never auto-approve matches based on filenames or image similarity alone.
- Publish source-matched batches to the web after UID/provenance and functional checks. Separately maintain an era/visual/rights review queue; the planned Find the Differences tool is for late-stage visual verification, not a blocker to all independent acquisition.
- Save each private evidence/database checkpoint into the Library and record exact artifact ID/hash. Do not rely on temporary Actions artifact retention or mutable scratch folders. Update this queue after each batch rather than starting parallel competing state documents.

## Priority order
**P1-A:** Archive/check batch 03 official sources once its job finishes. **P1-B:** Review Texas PDF's 164 catalog designs; map unambiguous printed-name/plate sample pairs and stage images. **P1-C:** Find an alternate accessible Florida official plate gallery after 403. **P1-D:** Expand the 32 jurisdiction source gaps and reuse conservative inspected-gallery matcher. **P2:** Native phone acceptance and stable signed update. **P3:** Final human review interface; **P4:** smaller app quality backlog.

## Stop conditions
- If source download fails, retain error evidence and try a documented alternate official source; do not mark source success from the workflow status alone.
- If official text, image and era conflict, preserve the conflicting evidence and park that UID. Never reuse one current image as a prior variant without support.
- Never publicly package raw archival PDFs, private keys or bulk original evidence solely to make a runtime test pass.
- Do not claim an Android installation, user approval, all 1,138 designs filled, or complete rights clearance before actual evidence.

## Next action
Inspect run `38201130935` to completion, verify and persist its official-source archive, while staging Texas manual mapping and Florida official-source recovery.
