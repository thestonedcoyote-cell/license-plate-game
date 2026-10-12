# Process Notes — Alaska and Mississippi official image integration

## Purpose
Add 76 independently inspected official plate samples by one-to-one canonical UID while retaining unverified era/human approval and unresolved cases.

## Inputs
GitHub reviewed harvest run 38200139649, action artifact official-plate-harvest-38200139649, with AK 48 and MS 307 downloaded agency-page assets. Immutable 1,138 catalog IDs and existing 73 source selections. Reviewed source URL/hashes in data/image-batches/ak-ms-reviewed.json.

## Step notes
- Step 1: recovered exact reviewed harvest artifact from Actions without uncontrolled crawling and checked source manifest status.
- Step 2: applied 35 unique exact official-label Mississippi matches and 41 visually inspected named Alaska image assignments, rejecting ambiguous/excluded records.
- Step 3: verified SHA-256 of all 76 original official source files before generating thumbnails or changing app state.
- Step 4: produced 76 enlarged and 76 thumbnail JPEG derivatives, preserving aspect ratio and not upscaling government source images.
- Step 5: expanded shared app image mapping from 73 to 149; updated service worker cache to 298 images for offline availability and adjusted focused image regression.
- Step 6: checked all 76 immutable UIDs, images and derived SHA-256 values against runtime staging, retained existing source mappings and strict Trash audit.
- Step 7: prepared generated assets on an independent review branch and kept Android stable/latest feed untouched.

## Exceptions / failures
Five Alaska UIDs and two Mississippi UIDs remain excluded for insufficient source/design mapping. The larger harvest also returned a Florida 403; it is not an image-match success. All 76 are source-matched only: historical issue years and human approval remain unverified. The owner's fair-use project-use direction does not establish a license or legal ruling. True Android device upgrade/testing remains separate.

## Outputs
76 new UID-selected source references, 152 JPEG derivatives, combined 149 source matches, database/image-reconciliation-ak-ms-20261011.json, updated JS image mapping and service worker cache, and process notes on a generated review branch.

## Rights / privacy notes
Public runtime receives limited plate example JPEG derivatives, not wholesale original gallery archives or private credentials. Preserve agency URLs/hashes, explicit owner-directed project-use classification and no unsupported legal approval.

## Final recheck
Checked source metadata, unique existing UIDs, SHA-256 of all 76 originals, every derived JPEG hash, exactly 298 staged images, web JS syntax, runtime and strict audit. Browser, real Android upgrade and human final visual/rights reviews remain independent acceptance gates.

## Completion status
COMPLETE_WITH_EXCEPTIONS
