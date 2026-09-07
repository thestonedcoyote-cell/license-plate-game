# Process Notes

## Purpose
Replace the live app's manufactured notebook styling with the generated road-trip mockup as the direct visual target.

## Inputs
- User-approved generated visual mockup from 2026-09-07.
- Existing v11.1 app behavior, cloud account layer, 291 public reference renders, camera workflow, Identify engine, Collection, Research, Map, Wins and Settings.
- Existing update/service-worker infrastructure.

## Step notes
- Step 1: Defined the visual target as the generated mockup itself rather than another abstract style interpretation.
- Step 2: Created an original vintage road-atlas SVG background using factual state/city/route labels and independent vector styling; no copyrighted commercial road-map scan is used.
- Step 3: Added v12 CSS that converts the UI to kraft-paper title strips, taped paper action cards, cream field-note panels, readable sans-serif body text and limited marker-style accent notes.
- Step 4: Reworked Home to three mockup-style cards: Take a picture, Identify a plate, Browse collection.
- Step 5: Added a mockup-style Identify preview to Home while retaining the functional full Identify screen.
- Step 6: Reworked bottom navigation to Home, Identify, Camera, Collection, More. Map and Wins remain available from More.
- Step 7: Restyled the existing functional Identify color dials and labels to Main color, Accent and Letters without replacing its matching logic.
- Step 8: Preserved the no-page-scroll Camera requirement and made post-capture wording explicitly connect the photo to Unidentified and Identify.
- Step 9: Preserved account/cloud/photo-sync functionality and restyled those surfaces rather than removing them.
- Step 10: Updated the PWA loader and service-worker cache so installed copies can receive v12 without reinstalling.
- Step 11: Syntax-checked the new JavaScript patch locally.
- Step 12: Added a dedicated v12 release validator covering visual tokens, atlas asset, loader/cache wiring, typography restrictions and no-page-scroll requirements.
- Step 13: Found and corrected two stale older validators that were tied to prior cache-version strings; both were changed to validate behavior/assets rather than an obsolete version label.
- Step 14: Removed a raw credential literal that had previously been embedded in the public cloud-validation workflow and replaced it with a generic secret-pattern check.
- Step 15: Re-ran all three pull-request gates. Result: Validate app = success, Validate cloud account layer = success, Validate v12 road-trip skin = success.

## Exceptions / failures
- Decorative road-atlas background is an original stylized map layer, not a scan of a 1984 commercial road atlas.
- Exact physical appearance will still vary slightly by handset size and installed system fonts.
- Camera autofocus and Android browser chrome remain handset/browser behavior outside CSS control.
- A credential previously exposed in repository history should still be treated as compromised and rotated; this release removes the literal from the current public workflow but does not rewrite Git history.

## Outputs
- assets/roadmap-v12.svg
- v12.css
- v12-patch.js
- updated app loader and service-worker cache
- corrected version-agnostic baseline/cloud validators
- dedicated v12 validator
- this process record

## Rights / privacy / safety notes
- The map background is independently created vector art using factual geographic labels and does not reproduce a commercial atlas image.
- Existing private cloud-photo rules and opt-in sync behavior are unchanged.
- No official DMV production-image archive is added by this visual release.
- Current client files contain no database password or service-role secret.

## Final recheck
Rechecked that the v12 background, CSS and behavior patch load after v11/cloud layers; Home has exactly three primary action cards; footer order is Home/Identify/Camera/Collection/More; Map and Wins remain reachable from More; Identify retains functional color filtering; Camera remains non-scrolling; cloud account controls remain present; service-worker cache includes all v12 files; the v12 layer contains no script/cursive font stack; the credential literal was removed from the current validator; and all three pull-request validation gates passed before merge.

## Completion status
COMPLETE_WITH_EXCEPTIONS
