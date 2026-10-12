# Process Notes — Oregon source-matched app integration 2026-10-11

## Purpose
Integrate 19 issuing-agency Oregon plate design examples, including distinct previous designs, into the existing LPG UID image presentation without asserting verified issue years or human approval.

## Inputs
Official Oregon DMV Plate Manual, Form 735-6726 revision 7-2026: https://www.oregon.gov/odot/Forms/DMV/6726.pdf. Pinned source SHA-256: 56ccdbf8dbbcd39c2803308f255e7374998c1ab418893da8b3577ff2098bdd50. Existing 1,138 canonical UIDs and 54 Washington source-matched selections. Script tools/integrate_oregon_plate_images.py.

## Step notes
- Step 1: acquired the exact official PDF and rejected any source bytes not matching the verified SHA-256.
- Step 2: identified 16 printed manual design sections and all 19 plate samples on PDF pages 21-27 using headings and structured page layout.
- Step 3: assigned each crop to its one immutable catalog UID, preserving distinct older Crater Lake, Cultural and Salmon designs.
- Step 4: generated 19 enlarged and 19 thumbnail JPEG references with no replacement artwork or new security details.
- Step 5: extended the shared Identify/catalog/collection image manifest from 54 to 73 selected samples, updated the service-worker cache version and focused offline regression expectations.
- Step 6: checked all 38 JPEG paths, SHA-256 hashes, exact source mapping, absence of duplicate UIDs, existing 54 preserved, and Android/web runtime staging.
- Step 7: kept source-matched status independent from issue-year, rights/legal, and human-approval status, and prepared a review branch rather than pushing generated art to main.

## Exceptions / failures
Historic issue years are not independently established for every variant. The source examples are official reference samples but not user-approved final historical artwork. Some source drawings carry proprietary notices; owner-directed fair-use project use does not grant rights or establish a legal conclusion. Physical Android installation and signed stable updater release remain untested.

## Outputs
19 catalog selections (73 cumulative), 38 JPEG derivatives, database/image-reconciliation-or-20261011.json with PDF page and crop provenance, updated data/catalog-images.js, sw.js, and tests/catalog-images.cjs on a generated review branch.

## Final recheck
Checked official source SHA, 19 unique Oregon UIDs, 73 total selections, correct current/prior variant counts, 38 output image hashes, runtime inclusion, syntax, and strict audit before creating the review branch. Browser/native acceptance must still be checked in PR/physical-device tests.

## Completion status
COMPLETE_WITH_EXCEPTIONS
