# Process Notes — 22 Nebraska DMV source plate examples (2026-10-27)

## Purpose
Recover official sample plate artwork missing from 22 frozen Nebraska catalog IDs, without substituting ambiguous art.

## Inputs
Nebraska DMV's 26-page 2023–2029 illustrated plate manual, https://dmv.nebraska.gov/sites/dmv.nebraska.gov/files/doc/dvr/plates/2023_Series_Plates.pdf; PDF SHA-256 `33ad4b77beeef9349b1747aeaf451502548fc08771953b0e08e3c657c2de6f82`; source evidence GitHub run `40411922074` and private Library `libfile_07a572791eb481919902b4e16d6ef7ab`. Before integration: 1,138 fixed catalog records, 502 source-matched examples, 1,004 JPEGs.

## Step notes
1. Inspected 2023–2029 DMV table pages and associated original embedded image xrefs with the same-row printed source captions.
2. Bound 22 distinct existing immutable catalog IDs to exact PDF pages, xrefs and source-image SHA-256 hashes in `data/image-batches/nebraska-2023-reviewed-20261027.json`.
3. Explicitly excluded `LPG-US-NE-00023`, whose canonical name “Vets Get Pets” differs from the manual's “Pets for Vets” design.
4. Pinned input document SHA, page count, caption presence and each source image content hash; reject silent PDF/extraction drift.
5. Reproducible generator converts no-upscaled plate source pixels to 22 display and 22 thumbnail JPEGs.
6. Before integration to production, independently verify exact 524 selected images, 1048 staged JPEG paths, service-worker cache invalidation, original UID/name invariants, the strict Trash audit and Android/web CI.
7. Generate images on separate branch `generated/nebraska-22-official-plate-images-20261027` for a final review/merge PR. Do not release an Android APK automatically.

## Exceptions / failures
Only 22 of Nebraska's 23 canonical names are matched. The original source PDF is privately archived, not committed to the public game repo. Era/status/human approval remain unverified; agency sample evidence does not grant a redistribution license. Existing 0.6.0-rc1 signed APK will not auto-update from GitHub source changes.

## Outputs
Reviewed one-to-one Nebraska mapping, reproducible image integration generator and GitHub Actions review-branch workflow; ultimately 44 new JPEGs and 22 new source examples after successful second PR/CI gate.

## Rights / privacy notes
No private keystore, user photographs, raw survey data or source-original PDFs enter public commits. Maintain source attribution and a separately documented project-use rationale.

## Final recheck
Test PDF identity, 22 xref SHA values, frozen UID/name consistency, asset output hashes, precise offline cached count, app/browser, audit and Android CI before merging generated image binaries.

## Completion status
COMPLETE_WITH_EXCEPTIONS — reviewed source mapping and generator prepared; actual image build and production app merge remain separate.
