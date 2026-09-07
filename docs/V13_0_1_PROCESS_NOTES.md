# Process Notes

## Purpose
Hotfix v13 so the regional map appears only as the overall background and does not visually bleed through torn-paper UI surfaces.

## Inputs
- User report that the map background appeared to be applied to all assets.
- Live v13 CSS, v13 paper assets, loader and service-worker cache.
- Existing torn-paper SVG assets already present in `assets/`.

## Step notes
- Step 1: Inspected the live v13 stylesheet and confirmed it referenced nonexistent `.webp` paper filenames while the actual assets are the `*-v13.svg` files.
- Step 2: Confirmed `v13-assets.css` attempted to override those filenames, making the paper rendering dependent on stylesheet ordering and leaving the visual layering fragile.
- Step 3: Added `v13.0.1.css` after the v13 asset bindings so the correct paper assets are the final authoritative paper-layer rules.
- Step 4: Added opaque backing colors to kraft, white, notebook and yellow paper surfaces.
- Step 5: Added the matching torn-paper SVG as a CSS alpha mask so the map remains visible only outside the torn edge, never through the paper interior.
- Step 6: Added `isolation:isolate` and explicit z-index separation between the map layers and the application layer.
- Step 7: Corrected the crumple overlay binding to `paper-crumple-overlay-v13.svg`.
- Step 8: Added the hotfix stylesheet to the loader and bumped the PWA cache to `lpg-v13.0.1-2026-09-07`.

## Exceptions / failures
- Exact appearance still depends on browser support for CSS mask images; current Android Chrome and modern desktop Chromium support the properties used, including the `-webkit-` prefixed form.
- This hotfix intentionally changes only layer isolation and does not redesign the regional-map, paper assets, sliders or desktop layout.

## Outputs
- `v13.0.1.css`
- updated `app.js`
- updated `sw.js`
- this process record

## Rights / privacy / safety notes
- No image-rights, location-privacy or cloud-storage behavior changes in this hotfix.
- The live map attribution and coarse regional GPS behavior remain unchanged.

## Final recheck
Recheck that all paper URLs in the hotfix point to existing `*-v13.svg` assets; each paper category has an opaque backing color plus matching mask image; map/wear layers remain below `.app`; `app.js` loads `v13.0.1.css` after v13/v13-assets; `sw.js` caches the hotfix and uses a new cache version; baseline app/cloud/v12/v13 validations remain green; this record contains all required note sections.

## Completion status
INCOMPLETE
