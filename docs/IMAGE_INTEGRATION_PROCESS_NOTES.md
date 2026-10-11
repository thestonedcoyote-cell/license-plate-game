# Process Notes — catalog image integration 2026-10-11

## Purpose
Reconcile database evidence with LPG identifiers and display source images in Identify, research catalog, collection and an enlarged reference view.

## Inputs
LPG_Image_Database_2026-10-10; existing 1,138 canonical IDs; 56 Washington candidate associations covering 54 designs. Owner-directed fair-use reference basis remains in force.

## Step notes
- Step 1: visually inspected all 56 candidate associations against names/source samples. Rejected Seahawks artwork under generic Throwback and Breast Cancer artwork under Square Dancer. Kept the independently matching images for those designs.
- Step 2: selected one official source sample for each of 54 canonical designs. Retained era uncertainty and no claim of human approval. Left all three unmatched report records out of runtime.
- Step 3: added local thumbnails and enlarged views with issuing-agency source, saved date and issue-year caveat. Collection uses the same UID mapping. Missing imagery retains existing fallback behavior.
- Step 4: included all 108 derived JPEG files in runtime staging and service-worker precache. Changed cache version. Source registry works in both window and service-worker scope.
- Step 5: reconciled a copied database package: app_image_selections records 54 source-matched selections, and two incorrect associations are marked conflict. Historical report candidates remain separate.

## Exceptions / failures
Initial browser assertion raced the dialog close event; corrected the test to wait for removal. These official samples are source-matched, not a claim that every issue-year variant is identical. 1,084 canonical designs still lack acquired matching images. No human visual approval was invented. Three report samples remain excluded because their exact canonical mapping is unresolved. Android installer testing remains a physical-device gate.

## Outputs
54 selected source references, 108 packaged JPEG derivatives, UID manifest, image UI, reconciled database, focused browser regression and Android 0.5 source version.

## Final recheck
Browser checks passed: 54 thumbnails load, full image/source dialog opens and closes, collected plate uses the same image, Identify displays the selected design, all 108 files are cached and offline reload displays images. Runtime stages 145 files. Distribution build/publishing status is reported separately after tool completion.

## Completion status
COMPLETE_WITH_EXCEPTIONS: image integration and browser/offline verification complete; remaining image coverage and physical installer acceptance are open.
