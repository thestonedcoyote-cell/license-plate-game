# Process Notes

## Purpose
Increase fidelity to the approved generated mockup by restoring a visibly crumpled road-atlas background, stronger torn/ripped paper treatment, and direct touch-drag color dials.

## Inputs
- User-approved generated License Plate Game mockup from 2026-09-07.
- Existing v12 live app and v11.1 cloud/account foundation.
- Existing functional Identify color matching engine and fixed Camera workflow.

## Step notes
- Step 1: Identified the gap between the mockup and live app as loss of physical texture rather than wrong basic palette/layout.
- Step 2: Created a compact original crumpled road-atlas WebP from the project's independent map artwork, adding paper grain, fold shading, wrinkles, aging and edge wear.
- Step 3: Added irregular torn-edge clipping to kraft/paper controls rather than the cleaner geometric v12 edges.
- Step 4: Reworked Home Identify and full Identify paper surfaces to read as ripped ruled notebook paper with a ragged left edge, punched-hole cues, blue rules and red margin line.
- Step 5: Reworked the three Identify color controls into visible circular color wheels.
- Step 6: Added Pointer Events so dragging a finger around each dial continuously selects color sectors; mouse/stylus dragging works through the same path.
- Step 7: Suppressed the old tap-to-next behavior on the dial face while retaining arrow buttons as accessible alternate controls.
- Step 8: Updated app loader ordering so v12.1 loads after v12 without disturbing camera, photo, catalog, research or cloud logic.
- Step 9: Updated the PWA service-worker cache so installed apps receive the new map, CSS and drag-control JavaScript without reinstalling.

## Exceptions / failures
- The crumpled map is independent app artwork, not a scan of a commercial 1980s atlas. It is intentionally designed to evoke the physical road-map experience rather than reproduce a specific copyrighted map.
- Paper tearing remains responsive CSS rather than a unique raster tear for every card, so exact edge shape repeats by component class.
- Final finger feel depends on actual handset size and must still be tested on the Moto.

## Outputs
- assets/roadmap-crumpled-v12.1.webp
- v12.1.css
- v12.1-patch.js
- updated app.js loader
- updated sw.js cache
- this process record

## Rights / privacy / safety notes
- Map artwork is independently generated from project-owned vector styling and factual geographic labels.
- No DMV production-image rights status changed in this release.
- Cloud photo privacy, authentication and opt-in backup behavior are unchanged.

## Final recheck
Recheck that the crumpled WebP exists and is non-empty; v12.1 CSS references it; ripped-paper styling is present; dial CSS uses touch-action:none; v12.1 JavaScript uses pointerdown/pointermove and preserves arrow-button fallback; app.js loads both v12.1 files after v12; sw.js caches the new map/CSS/JS; baseline app and cloud validation remain green; this record contains all required note sections.

## Completion status
INCOMPLETE
