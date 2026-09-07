# Process Notes

## Purpose
Repair the v13.0.1 Android rendering regression shown in the user-provided screenshot, where the live regional map bled through torn-paper UI surfaces and text/controls became translucent or unreadable.

## Inputs
- User screenshot from 2026-09-07 showing the broken live layout.
- Live v13.0.1 CSS, paper SVG assets, app loader and PWA service worker.
- Existing regional map, slider, desktop and cloud functionality.

## Step notes
- Step 1: Inspected the screenshot and identified that the map was visible through paper interiors and that text/content inside those elements had reduced opacity.
- Step 2: Inspected v13.0.1.css and confirmed the hotfix applied CSS `mask-image` directly to container elements.
- Step 3: Determined that CSS masks apply to the entire element including its children, so the paper mask also masked text, icons and controls. This explains both the map bleed and faded content in the screenshot.
- Step 4: Added v13.0.2.css loaded after v13.0.1 to remove all parent `mask-image` properties.
- Step 5: Kept torn edges in the standalone SVG background artwork itself rather than masking the parent DOM element.
- Step 6: Forced full opacity, normal blend mode and explicit dark-ink text colors on paper surfaces and their functional content.
- Step 7: Reinforced stacking order so the map and wear layers remain behind the app.
- Step 8: Added mobile sizing repairs for the title and three home action cards observed clipping in the screenshot.
- Step 9: Updated app.js so v13.0.2.css loads after all earlier visual layers.
- Step 10: Bumped the PWA service-worker cache to v13.0.2 and added the new CSS to the precache list.
- Step 11: Added a release validator specifically checking that the parent-mask regression cannot return silently.

## Exceptions / failures
- Final visual verification still requires the live Android browser/PWA because CSS/SVG rasterization can differ between browser engines.
- The app still contains historical visual layers from earlier versions; v13.0.2 deliberately overrides them rather than attempting a risky same-day stylesheet consolidation.

## Outputs
- v13.0.2.css
- updated app.js loader
- updated sw.js cache
- .github/workflows/validate-v13-0-2.yml
- docs/V13_0_2_SCREENSHOT_DIAGNOSIS.md
- this process record

## Rights / privacy / safety notes
- No location, account, cloud-photo, map-source or image-rights behavior changed in this hotfix.
- OpenStreetMap attribution remains visible.

## Final recheck
Rechecked that v13.0.2 explicitly removes parent masks, restores full opacity and readable dark ink, keeps torn edges in the SVG paper backgrounds, remains loaded after v13.0.1, is included in the v13.0.2 PWA cache, and does not modify camera, cloud, location or plate-image logic. Live handset visual verification remains the final external check.

## Completion status
COMPLETE_WITH_EXCEPTIONS
