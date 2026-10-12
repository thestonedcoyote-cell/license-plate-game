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
- Step 3: inspected PDF page index 21 (printed manual page 19). It shows a current Cultural design and a separate earlier Cultural design marked no longer issued but still valid. This corroborates why the catalog's previous-design UIDs must remain distinct.
- Step 4: added an access-check record to the existing official-source registry; left `local_binary_status: remote_only` and `status: leads_need_retrieval` unchanged. No selected image was added, no app runtime asset changed, no current-era claim was promoted.

## Exceptions / failures
Raw official PDF download into the current local sandbox failed, so original source bytes cannot be SHA-256 verified or archived. Browser access to PDF text and an individual rendered page is not equivalent to an archival evidence package. Some incorporated technical drawings have Irwin Hodson Group proprietary reproduction notices. The user's project-use fair-use direction does not grant an image license or establish an adjudicated legal conclusion. The reconciled October 11 database ZIP is not currently retrievable from the available Library listing; the October 10 package has been recovered separately as a historical fallback, not substituted as current.

## Outputs
A traceable Oregon manual access-check and remaining archival gate in `data/image-campaign/source-registry.json`, with 58 jurisdiction entries preserved and Oregon's 19-catalog-UID count unchanged. No source image was added or published.

## Rights / privacy notes
Only evidence metadata was committed. No official plate artwork was reproduced in the repository, no source credits suppressed, and no private credentials or original PDF drawings added.

## Final recheck
Compared before/after jurisdiction counts and preserved the Oregon source URL and `remote_only` state. The raw binary archive/hash, exact mappings, era checks, visual review and rights decision remain pending; this preliminary source preflight cannot count as a completed acquisition batch.

## Completion status
COMPLETE_WITH_EXCEPTIONS — accessibility and document identity checked; private evidence acquisition and image mappings still outstanding.
