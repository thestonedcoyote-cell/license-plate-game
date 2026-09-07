# Process Notes

## Purpose
Repair the Android/browser UI shown in the user-provided screenshot by removing legacy visual artifacts, restoring readable opaque paper surfaces, and rebuilding Home/footer after older patches have run.

## Inputs
- User-provided screenshot from 2026-09-07 showing map bleed, washed-out paper, clipped title text, ghosted legacy copy, and incomplete footer rendering.
- Existing v13 regional-map, paper assets, slider controls, cloud/account layer, camera workflow, collection, research, map, wins and PWA infrastructure.

## Step notes
- Step 1: Treated the screenshot as ground truth rather than inferring from CSS alone.
- Step 2: Identified that multiple generations of visual CSS/DOM patches remained active simultaneously.
- Step 3: Added a final screenshot-driven stylesheet that loads last and explicitly owns paper opacity, text contrast, sizing, navigation and mobile layout.
- Step 4: Removed CSS masks from UI parents and kept the torn-paper SVG as the paper background image itself.
- Step 5: Forced readable dark ink on light paper and removed inherited opacity/mix-blend/text-shadow effects.
- Step 6: Rebuilt the Home DOM from scratch after legacy patches finish, removing ghosted v9/v10 presentation content.
- Step 7: Rebuilt the footer into Home, Identify, Camera, Collection, More and restored Map/Wins under More.
- Step 8: Preserved the regional live map as the only map layer beneath the UI.
- Step 9: Preserved Identify sliders, camera behavior, collection data, cloud sync and existing reference-render data.
- Step 10: Bumped the service-worker cache and added the v13.0.3 CSS/JS to the cached core list.

## Exceptions / failures
- This fixes the specific class of Android rendering failure visible in the screenshot. Final visual confirmation still requires loading the new build on that browser/phone.
- Older visual files remain in the repository for compatibility, but v13.0.3 loads last and replaces their visible Home/footer presentation.

## Outputs
- v13.0.3.css
- v13.0.3-patch.js
- updated app.js
- updated sw.js
- this process record

## Rights / privacy / safety notes
- No location/privacy behavior changed.
- No official DMV production imagery or new third-party visual assets were added.
- Existing OpenStreetMap attribution remains visible for the regional map background.

## Final recheck
Recheck that v13.0.3 CSS and patch load after all older visual layers; Home is rebuilt after legacy patches; paper surfaces use project paper SVGs with no parent mask; dark text is forced on light paper; footer has five complete items; Map and Wins remain reachable; v13 regional map remains behind the app; service-worker cache version is v13.0.3 and contains both new files.

## Completion status
COMPLETE_WITH_EXCEPTIONS
