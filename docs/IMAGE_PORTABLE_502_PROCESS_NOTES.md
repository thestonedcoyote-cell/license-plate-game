# Process Notes — current portable 502-image runtime archive

## Purpose
Regenerate the portable source-matched game image database immediately after Florida's verified source-image integration, without overwriting the prior 370-image snapshot or conflating public reference derivatives with original agency archives.

## Inputs
- GitHub `data/catalog-images.js`: exactly 502 source-matched canonical catalog UIDs; `assets/plates/` holds 1004 runtime JPEGs.
- Immutable 1,138-canonical-UID catalog; `database/schema.sql`; `tools/package_current_images.py`.
- Florida PR #39 merged commit `a2e7f921aa7234a7244eb6f285f72af784f537ae`. Florida official 2026 source PDF and 2025 comparison remain separately archived in private Library `libfile_75203fd8f7c88191945305ea94c0075c`.
- Prior verified 370-image snapshot Library `libfile_91645e0e5f8c81919a51f66fe86c79df` is preserved as historical checkpoint.

## Step notes
- Step 1: reconciled 370 previous source selections with 132 newly source-matched Florida examples, resulting in 502 unique catalog selections.
- Step 2: changed portable builder to require an explicit `--expected-selections` value; accidental catalog drift now aborts output rather than quietly changing the database.
- Step 3: updated GitHub snapshot workflow to require 502 source selections and 1004 JPG files; retain source-image hash strings and user-directed project reference use separately from the published display-image bytes.
- Step 4: preserve canonical UID-to-image paths, content-addressed deduplication and explicit shared identical-image issue records.
- Step 5: produce a new ZIP with a distinct 502-image filename, complete SHA-256 inventory, SQLite runtime selections and without private original PDF archives.
- Step 6: validate ZIP integrity, every included path and SHA-256, SQLite integrity, foreign keys, selection count, historical approval status and duplicate issue records in GitHub Actions.
- Step 7: download and save actual output in the private Library and update durable project checkpoint with exact digest only after verification.

## Exceptions / failures
At this PR stage the 502 ZIP has not yet run; its successful archive/Library transfer must be verified separately. All 502 source matches remain era-unverified, human_approval=false. The old research database includes three non-canonical historical candidates absent from this runtime snapshot. Signed Android physical upgrade/data preservation remains unverified.

## Outputs
`tools/package_current_images.py` generalizes the expected-selection count, the GitHub portable snapshot workflow generates `LPG_Reference_Image_Snapshot_2026_10_26_502.zip` once triggered, and the 370-image ZIP stays intact.

## Rights / privacy notes
All originals and signed keys remain outside the public repository; source-matched official samples and owner fair-use rationale are not independently adjudicated permissions or proven historical issue dates.

## Final recheck
Before completion verify 1,138 UID catalog, 502 unique source-selected UIDs, 1004 runtime paths, exact image hashes, SQLite integrity and foreign key results, archive SHA/bytes, and permanent Library reference. Do not claim a package or app release prior to validated output.

## Completion status
COMPLETE_WITH_EXCEPTIONS — package builder patch prepared, current ZIP has a separate build and upload gate.
