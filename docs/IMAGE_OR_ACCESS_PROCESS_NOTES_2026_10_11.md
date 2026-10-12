# Process Notes — Oregon official manual source preflight (2026-10-11)

## Purpose
Progress the next source lead for the License Plate Game image campaign without pretending that a web-accessible PDF has been archived, hashed, mapped or approved.

## Inputs
- Main commit `fc52d3a69162bfbfcc52e5e053c90fcf69d79cab`.
- `data/image-campaign/source-registry.json`: Oregon / US-OR has 19 canonical catalog entries, and the current manual lead is `https://www.oregon.gov/odot/Forms/DMV/6726.pdf`.
- Live issuing-agency PDF accessed October 11, 2026; 38 pages; `Form 735-6726 (REV 7-2026)`.
- Canonical `data/image-campaign/manifest.json`, 19 immutable `LPG-US-OR` UIDs, including distinct previous variants.
- `docs/PLATE_IMAGE_CAMPAIGN_PLAN.md` source/identity/rights/visual-review separation.

## Step notes
- Step 1: recovered the Oregon record from the live source registry and counted 19 catalog UIDs without editing canonical UIDs.
- Step 2: opened the exact Oregon DMV official PDF. Its introduction says it lists currently issued plates plus still-valid plates no longer issued. Identified `Form 735-6726` revision `7-2026` and 38 PDF pages.
- Step 3: inspected PDF page indexes 20, 21 and 24 (printed manual pages 18, 19 and 22). Each shows a current design and a separate earlier still-valid but no-longer-issued design for Crater Lake, Cultural and Salmon, respectively. The catalog's current/previous pairs must remain distinct: `LPG-US-OR-00001` / `LPG-US-OR-00007`, `LPG-US-OR-00002` / `LPG-US-OR-00008`, and `LPG-US-OR-00005` / `LPG-US-OR-00016`. These are source-page observations, not complete era-dating or final image approval.
- Step 4: added an access-check record to the existing official-source registry; left `local_binary_status: remote_only` and `status: leads_need_retrieval` unchanged. No selected image was added, no app runtime asset changed, no current-era claim was promoted.
- Step 5: extended Library recovery beyond the project folder and located both October 11 files at the Library root. Materialized the reconciled database ZIP and distribution APK. Database ZIP integrity and SQLite integrity/foreign-key checks passed; selected app images = 54, plate records = 1,141 (1,138 canonical + 3 separate research candidates), jurisdiction registry = 101. APK SHA-256 matches handoff and ZIP structure tests pass.

## Exceptions / failures
Raw official PDF download into the current local sandbox failed, so original source bytes cannot be SHA-256 verified or archived. Browser access to PDF text and an individual rendered page is not equivalent to an archival evidence package. Some incorporated technical drawings have Irwin Hodson Group proprietary reproduction notices. The user's project-use fair-use direction does not grant an image license or establish an adjudicated legal conclusion. The initial project-folder Library list omitted the October 11 root-level artifacts; a subsequent recursive global Library inventory found them. This retrieval correction does **not** remove the independent raw-Oregon-PDF archive blocker.

## Outputs
A traceable Oregon manual access-check and remaining archival gate in `data/image-campaign/source-registry.json`, with 58 jurisdiction entries preserved and Oregon's 19-catalog-UID count unchanged. No source image was added or published. Recovered Library artifacts (not repo commits): `LPG_Image_Database_2026-10-11.zip` SHA-256 `a3e98edc1de43e1c14fb2b76373f97ef4d3a5f6fc66bb2e973510b26f09a1558`, and `license-plate-game-0.5.0.apk` SHA-256 `aa9913f743bd9df1d4d407bb89a0264dfb75cd79f954d7bd09521f196c99d41b`.

## Rights / privacy notes
Only evidence metadata was committed. No official plate artwork was reproduced in the repository, no source credits suppressed, and no private credentials or original PDF drawings added.

## Final recheck
Compared before/after jurisdiction counts and preserved the Oregon source URL and `remote_only` state. Verified both recovered ZIP containers, current database `PRAGMA integrity_check` and `foreign_key_check`, and recorded the exact APK hash. The raw **Oregon PDF** archive/hash, Oregon mappings, era checks, visual review and rights decision remain pending; this preliminary source preflight cannot count as a completed acquisition batch.

## Completion status
COMPLETE_WITH_EXCEPTIONS — accessibility and document identity checked; private evidence acquisition and image mappings still outstanding.
