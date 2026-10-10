# Process Notes — LPG database build

## Purpose
Build a real database with saved image files from the supplied research report and existing LPG evidence, using owner-directed fair use as the project basis.

## Inputs
Uploaded research report; current GitHub main 809ce4e627f1e0cca440600d548291d58dcc9dc9; canonical catalog; image campaign manifest; recovered private Washington archive; current Commons description pages and three downloaded originals.

## Step notes
- Step 1: read report and current campaign checkpoint. Identified limited report coverage and inconsistent Puerto Rico mapping.
- Step 2: recovered archived evidence after scratch pruning. Verified hashes rather than assuming files survived.
- Step 3: checked source descriptions, corrected attribution/license records and downloaded all three sample originals. Recorded unverified years as claims.
- Step 4: built normalized SQLite database, actual image files, derivatives, source records, attribution, issues and app-friendly JSON.
- Step 5: verified 1,138 original IDs preserved, 3 separately namespaced report candidates, 91 acquired assets, 164 derivatives and 59 candidate/conflict associations. SQLite integrity, foreign-key and per-file hash checks passed.

## Exceptions / failures
Puerto Rico original initially returned HTTP 429; a later retry succeeded. Report years are unverified, and its Puerto Rico image conflicts with the described 2023 design. No images are falsely marked identity/visually verified. 1,084 canonical designs still lack acquired image links. The existing 291 schematic references remain in the source catalog but are not represented as source photographs. Live app and APK were not updated.

## Outputs
LPG_Image_Database_2026-10-10.zip, database/schema.sql, database/README.md, tools/build_lpg_database.py and tools/fetch_report_images.py.

## Final recheck
Rechecked database integrity, relationship integrity, canonical UID equality, source/image hashes, paths and coverage totals. Saved output is a portable database package, not a claim of complete campaign coverage.

## Completion status
COMPLETE_WITH_EXCEPTIONS: working database package built and validated; full image acquisition, mapping and visual verification remain open.
