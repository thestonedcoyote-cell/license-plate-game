# Process Notes — Portable 370-image runtime source snapshot (2026-10-26)

## Purpose
Produce a traceable portable SQLite/JSON/JPEG snapshot from the **currently deployed** LPG image selection manifest (370 source-matched plates), not the obsolete 149-image October 12 research archive.

## Inputs
- Canonical runtime catalog: `data/catalog.part0.b64` through `part4.b64`, exactly 1,138 unique original catalog IDs.
- `data/catalog-images.js`, 370 source-matched examples: WA 54, OR 19, AK 41, MS 35, TX 157, CA 33, WI 31.
- `assets/plates/*-display.jpg` and `*-thumbnail.jpg`, 740 public runtime JPEGs.
- Existing `database/schema.sql`, current checked-in source URL and source hash metadata, GitHub revision and CLI `tools/package_current_images.py`.
- Historic 149-image research database `LPG_Image_Database_2026-10-12_Batch02.zip` remains preserved privately under Library ID `libfile_e9eea656eb5081918bc7eeb3e0c56278`.

## Step notes
- Step 1: check current catalog UID uniqueness, number of selected app images and manifest membership.
- Step 2: verify all 370 selected images remain `source_matched`, `era_status=unverified` and `human_approval=false`.
- Step 3: check, hash and copy all current 370 enlarged and 370 thumbnail public JPEGs byte-for-byte from the GitHub checkout into an isolated package.
- Step 4: build a portable SQLite database using original schema with an added `app_image_selections` table; record issuing-agency source URLs, original-image SHA-256 references and published-image hashes independently.
- Step 5: retain all 1,138 existing canonical IDs, no extraneous catalog UIDs, and explicitly omit the three separate non-canonical historical report entries. Do not claim this is a superset of the prior research-only archive.
- Step 6: export current source/provenance metadata, catalog, app selection manifest, SQLite tables, README and complete file hash inventory, and ZIP the directory.
- Step 7: verify SQLite integrity, foreign keys, totals and image SHA-256 hashes, then verify ZIP file integrity in CI.
- Step 8: preserve the Actions artifact in the user's private Library before artifact retention expires; record the verified final Library reference and archive SHA-256 in the next project checkpoint.

## Exceptions / failures
The current public repository **does not contain all the agency source-original binaries**; those remain separately archived in private source-evidence ZIPs. This is a runtime reference-image snapshot. The inherited legacy schema column `assets.original_path` points to a *published display derivative* for this snapshot, explicitly labelled `asset_role=published_runtime_display_derivative_not_original`. The original SHA-256 in `app_image_selections.source_asset_sha256` is provenance metadata, **not a hash of an included original source asset**. Historical research-only entities/claims/issues from prior portable database are not silently imported into this app-focused snapshot.

## Outputs
`LPG_Reference_Image_Snapshot_2026_10_26.zip` with new SQLite/JSON/JPEG snapshot, README, validation and checksums; no original source binary, signing keys, or legal/era approval. CI workflow `.github/workflows/package-current-images.yml`.

## Rights / privacy notes
All selected image samples carry user-directed fair-use reference context; this does not grant original artwork licenses. Only existing public in-app reference JPEGs enter the package. No GPS, user sightings, private recordings, device storage, credentials or signing keys included.

## Final recheck
Check ZIP `testzip`, every listed file/hash, 1,138 canonical records, 370 selected images, 740 JPEG derivatives, foreign key references and SQLite integrity. Browser and physical Android testing remain separate, and no updated stable APK release is produced.

## Completion status
COMPLETE_WITH_EXCEPTIONS — source-specific originals are external to this portable runtime snapshot, and the final generated artifact/Library archival checks remain to be verified after CI execution.
