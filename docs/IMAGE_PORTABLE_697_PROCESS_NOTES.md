# Process Notes — portable 697-image source-reference database (2026-10-29)

## Purpose
Refresh the portable reference database after merging Nevada 84, Alabama 28, Michigan 22 and Ontario 39 official sample plates, without changing immutable catalog UIDs or confusing source-matched examples with approved historical/rights evidence.

## Inputs
GitHub main after MI/ON image PR #56, expected 1,138 catalog UIDs, 697 source-matched app image references and 1,394 public display/thumbnail JPEGs. Existing robust byte-hashed `tools/package_current_images.py` and `database/schema.sql`. The 502-image portable ZIP in Library `libfile_d3e43441cc2881918db696dde9c0c810` remains a historical app state; source archives remain separate.

## Step notes
1. Require explicit `--expected-selections 697` with the current checked-in manifest to prevent silent future drift.
2. Copy all 1,394 runtime display/thumbnail JPGs byte-for-byte; index original source SHA strings and issuing agency URLs separately.
3. Retain unique content-addressed stored assets while preserving per-UID image files and explicit duplicate source-image cases.
4. Build SQLite with original immutable UIDs and all 697 source-selected records; prohibit human-approved or era-verified status changes.
5. Verify archive ZIP structure, SHA-256 for every file, SQLite integrity, foreign keys, 697 app image selections and 1,394 UID-indexed JPG records.
6. Archive generated ZIP for portable use. GitHub Actions artifact is temporary; privately store in Library only if current user quota permits, without deleting existing evidence.

## Exceptions / failures
Current Library storage may be full. The official issuing-agency original binary archives remain distinct from this public runtime reference copy. Historical design era, human approval, rights clearance, stable signed Android update and physical data-preservation tests are not satisfied by this package.

## Outputs
`LPG_Reference_Image_Snapshot_2026_10_29_697.zip` from GitHub Actions workflow `.github/workflows/package-current-images.yml`.

## Rights / privacy notes
No recovered signing keystore, GPS sightings, player notes, private photos or original government PDFs are included; owner fair-use reference rationale is separate from legal permission.

## Final recheck
Check exactly 1,138 canonical UIDs, 697 source selections, 1,394 per-UID JPG paths, all file hash inventory records, no FK errors or unapproved status promotion. Keep historical snapshots intact.

## Completion status
IN_PROGRESS — workflow and acceptance values prepared, final package and permanent archival verification pending.
