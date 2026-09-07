# Process Notes

## Purpose
Replace simulated paper/map styling with a real regional map background and raster torn-paper UI assets; fix Identify drag controls; make desktop layout genuinely distinct from the installed phone app.

## Inputs
- User feedback dated 2026-09-07.
- Existing v12.1 live app, camera flow, Identify engine, cloud sync, 291 public plate references and PWA infrastructure.
- Leaflet and OpenStreetMap already used by the app.

## Step notes
- Step 1: Created project-owned raster paper assets with alpha torn edges: kraft card, kraft strip, white scrap, ruled notebook scrap, yellow note, and transparent crumple overlay.
- Step 2: Replaced the static imitation map with a non-interactive Leaflet background using actual OpenStreetMap regional tiles.
- Step 3: Centered the map on coarse quarter-degree GPS when geolocation permission is already granted or the user taps Use GPS; fallback is a western/central U.S. regional view.
- Step 4: Added local regional wear scoring. Camera use and plate collection increment wear for the current coarse region; the crumple/wear overlay strengthens as that regional score grows.
- Step 5: Replaced tiny circular pseudo-dials with large horizontal range sliders, 38–42 px thumbs, live color labels and swatches, while preserving the existing Identify matching engine.
- Step 6: Replaced major menu/card backgrounds with actual raster torn-paper images instead of clip-path polygons.
- Step 7: Added standalone-PWA mode styling so installed copies hide install chrome and occupy the full app viewport.
- Step 8: Added a distinct desktop workspace layout: left navigation rail, wide working surface, larger Identify controls, wider Research/Cloud Photo Desk, while using the same account/data layer.
- Step 9: Preserved Camera fixed-viewport behavior, cloud privacy, 291 public plate references, Collection, Map, Wins and Research functionality.
- Step 10: Prepared loader/service-worker changes so installed apps receive v13 assets without reinstalling.

## Exceptions / failures
- OpenStreetMap standard tiles are acceptable for this prototype with attribution, but a dedicated tile provider or self-hosted tiles should replace them before significant public traffic.
- The wear feature currently changes the crumple intensity of the current coarse region as a whole; future work can spatially stain individual subareas within the visible map.
- Final handset slider feel and desktop spacing still require live-device/browser review.

## Outputs
- assets/paper-kraft-card.webp
- assets/paper-kraft-strip.webp
- assets/paper-white-card.webp
- assets/paper-notebook-card.webp
- assets/paper-yellow-card.webp
- assets/paper-crumple-overlay.png
- v13.css
- v13-patch.js
- loader/service-worker integration
- this process record

## Rights / privacy / safety notes
- Live background map uses OpenStreetMap tiles with visible attribution.
- GPS is rounded to a quarter-degree before being used as the decorative regional-map center and wear key.
- Torn-paper/crumple assets are generated project artwork.
- Exact sighting coordinates and private cloud photos retain the existing privacy controls.

## Final recheck
Pending release validation: verify all raster assets are non-empty; v13 CSS uses the raster assets; regional map uses coarse GPS and visible OSM attribution; wear score persists by regional key; sliders emit input/change continuously and keep the existing matching engine in sync; standalone and desktop modes both preserve navigation; Camera remains non-scrolling; cloud/account layer and 291 references still validate; service worker caches all v13 assets.

## Completion status
INCOMPLETE
