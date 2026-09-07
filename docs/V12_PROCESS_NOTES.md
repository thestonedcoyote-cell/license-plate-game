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

## Exceptions / failures
- Decorative road-atlas background is an original stylized map layer, not a scan of a 1984 commercial road atlas.
- Exact physical appearance will still vary slightly by handset size and installed system fonts.
- Camera autofocus and Android browser chrome remain handset/browser behavior outside CSS control.

## Outputs
- assets/roadmap-v12.svg
- v12.css
- v12-patch.js
- updated app loader and service-worker cache
- this process record

## Rights / privacy / safety notes
- The map background is independently created vector art using factual geographic labels and does not reproduce a commercial atlas image.
- Existing private cloud-photo rules and opt-in sync behavior are unchanged.
- No official DMV production-image archive is added by this visual release.

## Final recheck
Recheck that the v12 background, CSS and behavior patch are loaded after v11/cloud layers; Home has exactly three primary action cards; footer order is Home/Identify/Camera/Collection/More; Map and Wins remain reachable from More; Identify retains functional color filtering; Camera remains non-scrolling; cloud account controls remain present; service-worker cache includes all v12 files; process notes include all required sections.

## Completion status
INCOMPLETE
