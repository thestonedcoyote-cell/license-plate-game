# LPG — Active Plate Image Campaign Queue

**Checkpoint (2026-10-11, America/Los_Angeles)**

Source repository: `thestonedcoyote-cell/license-plate-game`.
Immutable runtime catalog: **1,138 UIDs** across **58** represented jurisdictions.
Source-matched in web catalog: **73** (54 Washington + 19 Oregon); **1,065 remain without acquired matching images**.
Runtime derivatives: **146 JPEGs**. Historical 291-schematic baseline is not acquired-image coverage.
No current match is a substitute for era/accuracy verification, independent rights assessment, or an actual human review decision.
Three unresolved research/report candidates are **not** additions to the 1,138 runtime designs.

## Where we are
- Washington's issuing-agency gallery supplied 54 source-matched examples. Two incorrect automated pairings were explicitly rejected. Washington historical variants remain unresolved.
- Oregon's July 2026 official 38-page DMV manual supplied **19 individually cropped and inspected examples**, including distinct current/previous Crater Lake, Cultural and Salmon designs. Generator, 38 image derivatives and source hash/mapping record are committed. PR #21 merged at `af64fe5dde48af0c663ad6aa180d3592108d6f2b`; Pages run `38199925236` passed.
- Private, verified portable image/database checkpoint: `LPG_Image_Database_2026-10-12.zip`, Library `libfile_c3bd712da6a48191848af1b34dbb70ad`, SHA-256 `2d725d87d5e3ead8e1151667b36294a833819d3fea82c5a8fb2640ab7dba3549`.
- Oregon source evidence package: `LPG_OR_Official_Harvest_2026-10-11.zip`, Library `libfile_1c9a2771f7308191b85009db82c688da`. The source PDF SHA-256 is `56ccdbf8dbbcd39c2803308f255e7374998c1ab418893da8b3577ff2098bdd50`.
- **26 of 58** catalog jurisdictions now have at least one official source lead (previously 17). A source lead is not an acquired image or an exhaustive gallery.

## Active execution
1. **LPG-P1-BATCH02:** GitHub official-source harvest run [38200139649](https://github.com/thestonedcoyote-cell/license-plate-game/actions/runs/38200139649), `TX,FL,AK,MS`, max 4 sources, source commit `7d41651f96a10161b04386baeb647b929840fdc6`. These states together have **379 existing catalog designs**. At this checkpoint run is **in progress**; source downloads, failures and matching totals must be inspected before claiming success.
2. Once the run finishes, inspect every source record and per-asset failures; download the GitHub artifact **before its 14-day expiration**; verify hashes/ZIP; preserve the raw evidence in private Library with returned ID.
3. Index PDF pages, extracted embedded images and HTML gallery assets against the corresponding catalog UIDs. Identify high-confidence one-to-one designs from official names and layouts; keep ambiguous and historical versions unresolved. Do not promote all PDF images simply because extracted.
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
**P1-A:** Complete archival/assessment of batch 02. **P1-B:** Match its highest-confidence designs and integrate verified-name examples. **P1-C:** Expand next reviewed source tranche and automate conservative candidate intake. **P2:** Native phone acceptance and stable signed update. **P3:** Final human review interface; **P4:** smaller app quality backlog.

## Stop conditions
- If source download fails, retain error evidence and try a documented alternate official source; do not mark source success from the workflow status alone.
- If official text, image and era conflict, preserve the conflicting evidence and park that UID. Never reuse one current image as a prior variant without support.
- Never publicly package raw archival PDFs, private keys or bulk original evidence solely to make a runtime test pass.
- Do not claim an Android installation, user approval, all 1,138 designs filled, or complete rights clearance before actual evidence.

## Next action
Inspect run `38200139649` to completion, retrieve and persist its archive, then issue an honest per-jurisdiction retrieval/mapping receipt.
