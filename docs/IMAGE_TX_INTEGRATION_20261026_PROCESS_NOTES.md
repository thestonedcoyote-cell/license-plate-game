# Process Notes — Texas DMV official plate image integration

## Purpose
Add 157 named examples from the official Texas specialty plate manual to the existing game catalog, with one-to-one immutable IDs, exact source provenance, and distinct review/era/rights states.

## Inputs
Official TxDMV Specialty Plate Guide, revision 12/2025, 48 PDF pages, at https://www.txdmv.gov/sites/default/files/body-files/Special-Plate-Guide.pdf; accepted PDF packaging SHA-256 digests in tools/integrate_texas_manual.py. Existing 1,138 UIDs and 149 source image selections.

## Step notes
- Step 1: downloaded only the official listed PDF and verified its exact SHA-256 against two inspected 48-page source package variants.
- Step 2: parsed the 161 printed plate-name sections and corresponding nearby embedded source artwork, with exactly one plate image per section.
- Step 3: conservatively joined 157 unique printed plate names to 157 immutable Texas catalog IDs, leaving seven unresolved names explicitly excluded.
- Step 4: created 157 display and 157 thumbnail JPEG assets, without upscaling beyond original embedded sample resolution.
- Step 5: expanded the web/Android-source image manifest from 149 to 306 selections; incremented offline image cache from 298 to 612 JPEG files.
- Step 6: verified 157 source-mapped records, all 314 output JPEG hashes, source provenance, page and crop coordinates, staged runtime and exact unresolved UID set.
- Step 7: ran strict repository audit and syntax checks and packaged generated source-image files only to a gated review branch.

## Exceptions / failures
Seven catalog entries remain unresolved and were not silently assigned other designs (Lone Star Texas, Panoramic Texas, St. Mary's University, Texas Parks & Wildlife Roadrunner and Texas Rivers, Texas Reads, The Texas Classic). One exact official source image is used for two Go Texan group variants because the official PDF itself presents the same artwork in both plate-name sections. All examples are source-matched but not separately verified for issue era, public image rights, or final human approval. Physical signed Android upgrade acceptance remains outstanding.

## Outputs
157 additional source-matched UID examples; 314 JPEG derivatives; 306 cumulative web/Android-source selections; database/image-reconciliation-tx-20261026.json with source page, image rectangle, hashes and statuses; updated image manifest, service worker, focused browser regression and generated review branch.

## Rights / privacy notes
Do not publicly commit the raw agency PDF or private signing credentials. Source examples are used on the project's owner-directed fair-use reference rationale, not a claim of public domain, permission, legal adjudication or human final approval.

## Final recheck
Checked the selected total 149+157=306 and remaining 1138-306=832; verified 612 JPEG runtime files, full hash inventory for 314 derivatives, source pin, 157 unique mapped UIDs, exact seven unresolved UIDs and browser test syntax. No stable APK release or device upgrade is implied.

## Completion status
COMPLETE_WITH_EXCEPTIONS
