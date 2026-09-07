# Process Notes

## Purpose
Turn the current phone alpha into a more integrated notebook-like road game, make the camera a fixed no-scroll capture surface, make saved photos visibly flow into identification, and publish every currently defensible clean reference image.

## Inputs
- v9 installed PWA and user phone feedback from Moto G Power 5G (2023).
- Canonical catalog: 1,138 collectible designs.
- 130 evidence-backed visual profiles.
- Existing IndexedDB photo/sighting workflow, Unidentified collection, camera and Identify screens.
- Existing process-note/recheck standard and image-rights research.

## Step notes
- Step 1: Reframed the UI as one notebook sheet rather than independent manufactured cards/windows. Added ruled-paper background, red notebook margin, binder-hole visual cue, handwritten/marker-like system fonts, paper tabs, scribbled underlines and integrated controls.
- Step 2: Increased base text to 19px, with an 18px small-phone floor, and enlarged result names, metadata and controls so the phone does not require close-up reading.
- Step 3: Converted Camera into a fixed 100dvh viewport. While Camera is active, normal header/navigation and page scrolling are removed; preview/video fills the viewport; the frame guide is centered; shutter controls stay above the safe-area bottom edge.
- Step 4: Made photo state explicit. A captured photo is labeled as saved in Collection → Unidentified and offers a direct Saved photos route.
- Step 5: Renamed the primary post-capture action to `Identify this photo →` and carry the visible captured image onto Identify as an attached-photo strip so the user can compare it while narrowing candidates.
- Step 6: Added the same attachment behavior when an Unidentified photo is reopened for identification from Collection.
- Step 7: Generated 130 public LPG reference-render specs from evidence-backed visual profiles. Protected logos/characters/sponsor art are simplified to original broad motif symbols rather than traced or copied.
- Step 8: Added a client-side SVG renderer keyed by immutable plate UID. Public renders use verified colors/slogans/broad motif family, fictitious `LPG 000` serials and a visible `REF` marker.
- Step 9: Kept harvested official production images out of the public tree unless separately cleared. State-site copyright/reuse research continues to show that publicly viewable graphics are not uniformly free to redistribute, particularly sponsor and third-party artwork.
- Step 10: Updated the app loader and service-worker cache so the installed PWA receives v10 assets through the existing update mechanism.

## Exceptions / failures
- 1,008 collectible designs still lack sufficient normalized visual-profile data for clean reconstruction and therefore retain the non-image fallback.
- The 130 public renders are identification references, not pixel-identical replicas; protected creative elements are intentionally simplified.
- Exact official image redistribution is not being treated as clean where site terms or third-party ownership remain ambiguous.
- Final device behavior still requires post-deployment confirmation on the Moto because browser simulation cannot prove Android camera viewport/safe-area behavior.

## Outputs
- `v10.css` — integrated notebook interface and fixed camera viewport.
- `v10-patch.js` — clean reference render integration and photo-to-identify flow.
- `data/reference-renders-v10.js` — 130 public reference render specifications.
- Updated `app.js` loader and `sw.js` cache manifest.
- `docs/V10_IMAGE_RELEASE_NOTES.md` and this process record.

## Rights / privacy notes
Captured user photos and precise location remain local to the device under the current local-first model. Public reference renders are newly generated LPG artwork from factual/verified characteristics and are intentionally non-credential-like. Production/reference images remain research evidence unless separately cleared.

## Final recheck
Before merge: run JavaScript syntax validation; verify the render manifest has exactly 130 unique UIDs and all are canonical catalog records; verify no harvested production image was added to the public tree; verify `LPG 000` and `REF` appear in the public renderer; verify v10 files appear in the service-worker cache; run the repository release/process-note checks; inspect the PR diff for unintended changes; and verify the Pages deployment after merge.

## Completion status
INCOMPLETE — implementation is staged; repository checks, PR review, merge and live deployment remain.
