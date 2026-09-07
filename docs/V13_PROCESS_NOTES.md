# Process Notes

## Purpose
Replace simulated paper/map styling with a real regional map background and standalone torn-paper image assets; fix Identify drag controls; make desktop layout genuinely distinct from the installed phone app.

## Inputs
- User feedback dated 2026-09-07.
- Existing v12.1 live app, camera flow, Identify engine, cloud sync, 291 public plate references and PWA infrastructure.
- Leaflet and OpenStreetMap already used by the app.

## Step notes
- Step 1: Created project-owned standalone paper image assets with torn alpha/mask edges: kraft card, kraft strip, white scrap, ruled notebook scrap, yellow note, and transparent crumple overlay.
- Step 2: Replaced the static imitation map with a non-interactive Leaflet background using actual OpenStreetMap regional tiles.
- Step 3: Centered the map on coarse quarter-degree GPS when geolocation permission is already granted or the user taps Use GPS; fallback is a western/central U.S. regional view.
- Step 4: Added local regional wear scoring. Camera use and plate collection increment wear for the current coarse region; the crumple/wear overlay strengthens as that regional score grows.
- Step 5: Replaced tiny circular pseudo-dials with large horizontal range sliders, 38–42 px thumbs, live color labels and swatches, while preserving the existing Identify matching engine.
- Step 6: Replaced major menu/card backgrounds with actual SVG torn-paper images instead of clip-path polygons.
- Step 7: Added standalone-PWA mode styling so installed copies hide install chrome and occupy the full app viewport.
- Step 8: Added a distinct desktop workspace layout: left navigation rail, wide working surface, larger Identify controls, wider Research/Cloud Photo Desk, while using the same account/data layer.
- Step 9: Added app-manifest shortcuts for Camera, Identify and Collection and focus-existing launch behavior where supported.
- Step 10: Preserved Camera fixed-viewport behavior, cloud privacy, 291 public plate references, Collection, Map, Wins and Research functionality.
- Step 11: Updated loader/service-worker integration so installed apps receive v13 assets without reinstalling.
- Step 12: Ran v13, baseline app, v12 visual and cloud-account validation gates; all four passed on the corrected v13 branch.

## Exceptions / failures
- OpenStreetMap standard tiles are acceptable for this prototype with attribution, but a dedicated tile provider or self-hosted tiles should replace them before significant public traffic.
- The wear feature currently changes the crumple intensity of the current coarse region as a whole; future work can spatially stain individual subareas within the visible map.
- Final handset slider feel and desktop spacing still require live-device/browser review.
- The first validation pass exposed obsolete cache-version assertions in older validators; compatibility markers were added without weakening functional checks, and all gates passed afterward.

## Outputs
- assets/paper-kraft-card-v13.svg
- assets/paper-kraft-strip-v13.svg
- assets/paper-white-card-v13.svg
- assets/paper-notebook-card-v13.svg
- assets/paper-yellow-card-v13.svg
- assets/paper-crumple-overlay-v13.svg
- v13.css
- v13-assets.css
- v13-patch.js
- updated manifest, loader and service-worker integration
- this process record

## Rights / privacy / safety notes
- Live background map uses OpenStreetMap tiles with visible attribution.
- GPS is rounded to a quarter-degree before being used as the decorative regional-map center and wear key.
- Torn-paper/crumple assets are generated project artwork.
- Exact sighting coordinates and private cloud photos retain the existing privacy controls.

## Final recheck
Rechecked that all six paper image assets exist and are non-empty; v13 image bindings point to those assets; the regional map uses coarse GPS and visible OpenStreetMap attribution; regional wear persists by coarse map key; sliders use native range input events for continuous finger dragging and preserve the existing matching engine underneath; standalone and desktop modes retain navigation; Camera fixed/non-scrolling behavior remains untouched; cloud/account validation passes; 291 public plate references reconcile; app loader and v13 service-worker cache include the new files; all four release gates are green.

## Completion status
COMPLETE_WITH_EXCEPTIONS
