# Process Notes — Alabama official gallery, 28 source-matched designs

## Purpose
Add high-confidence issuing-agency image references to the Alabama portion of the frozen License Plate Game catalog without fabricating two unresolved designs.

## Inputs
- Official Alabama Department of Revenue license plate archive/gallery `https://www.revenue.alabama.gov/license-plates/`.
- Original AL/MN/NE/CT agency harvest, GitHub Actions run `40411922074`, privately saved Library `libfile_07a572791eb481919902b4e16d6ef7ab`.
- Archived Alabama HTML SHA-256 `322ffe503d3d21c013ec0f006e8b13c3508712bc262398eef3e18f23c62622a0`; asset registry SHA-256 `dbb980bf693eaffa267ca1fff1bef183a374c97a1f63e03d75ab5ac55a1a87f9`.
- 28 exact UID/source file mappings in `data/image-batches/alabama-28-reviewed-20261029.json`, baseline 608 source-matched UIDs of 1,138 canonical UIDs, before this batch.

## Step notes
1. Inspected two Alabama government sample-image contact sheets to establish which gallery assets depict actual license plates and belong to existing catalog names.
2. Selected 28 one-to-one plate assets, using the highest matching original image resolution available per design, with original URL, archived filename and SHA-256 match at integration.
3. Explicitly **excluded** Alabama `LPG-US-AL-00017` Disability Access Parking because the source offers parking placards, not a plate, and `LPG-US-AL-00020` FORT Fleet because the source only establishes a generic `FLEET` plate, not the catalog's more specific identifier.
4. Added a reproducible on-demand GitHub Actions batch that restores the old official harvest, validates HTML and gallery SHA, independently checks every selected original asset SHA, generates width-limited display/thumbnail JPEGs and retains immutable catalog IDs.
5. Expected selection count after exact 28 integration is 636 / 1,138, 1,272 total offline-staged JPG files, leaving 502 canonical IDs without source-matched images.
6. Generated binary artwork is committed to a separate review-only branch and requires normal repository app/cloud/Trash/Android CI before merging; current 0.6.0-rc1 signed Android installation does **not** auto-update.

## Exceptions / failures
Source-image matching does not establish original issue year, final human review, source-specific commercial redistribution licenses or physical mobile app upgrade acceptance. The two omitted Alabama UIDs remain unresolved and must not be counted as matched.

## Outputs
`tools/integrate_alabama_gallery.py`, exact 28-UID official gallery map `data/image-batches/alabama-28-reviewed-20261029.json`, review-only generator workflow `.github/workflows/integrate-alabama-images.yml`. Generated review branch will carry JPEGs, manifest, source reconciliation and offline cache revisions.

## Rights / privacy notes
Raw official source archives remain in private Library / short-lived Actions workspaces and are not committed to public GitHub. The owner-directed fair-use reference rationale is separate from legal authorization and historical verification. Signing keys are not part of this acquisition.

## Final recheck
Official archive asset/HTML hashes; 28 individual original image SHA matches; 56 generated derivative hashes; no overwrite of previous images; 636 selected UID records; 1,272 runtime JPGs; pinned exception list; web/browser/Android build CI and Pages deployment after merge.

## Completion status
IN_PROGRESS — source review and code prepared, generated assets still require actual CI and review PR merge.
