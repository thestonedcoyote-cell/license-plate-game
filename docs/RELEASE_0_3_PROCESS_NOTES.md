# Process Notes
## Purpose
Prepare version 0.3.0-alpha (versionCode 3) with the approved vintage identification design and restored Mile markers.
## Inputs
Camera/crop branch commit 356fec36807c87952a8d54112d136b6b933900b1 includes queued native updater and camera permission repair. Approved concept: compact lined-gradient radio tuners, example plate, thumbnail results, SLR camera, photo prints, crop/zoom.
## Step notes
- Step 1: Implemented three compact tuners, example color preview, print-framed reference and result thumbnails, SLR controls and offline atlas background.
- Step 2: Added pinch zoom, pan, select crop and precise crop values while retaining original photo blobs. Browser testing found controls available before image decode; controls now wait for decoding and handler initialization.
- Step 3: Restored achievements as Mile markers on Home and under More; all 11 existing badges remain available.
- Step 4: Browser regression passed at phone and desktop sizes: catalog entry, fake-camera capture, crop dimensions, zoom dimensions, original preservation, saved counts and crops after reload, 11 Mile markers, zero page errors. Screenshots reviewed. Camera lifecycle test passed permission ordering, explicit playback and stale stream cleanup.
- Step 5: Built full native APK with official Android tools, including AppUpdates.java; verified v2/v3 signatures, preserved distribution certificate, alignment and all 32 embedded runtime files. Strict trash audit passed.
## Exceptions / failures
No physical Android device test performed: installer, real camera/GPS permission flow and physical pinch gestures still need confirmation. Browser camera used a synthetic test stream. Reference thumbnails are catalog illustrations. Java compilation reports deprecated API usage. The release is prepared, not published; update metadata URL is prospective and must not be treated as live. Browser testing ran offline with external requests blocked.
## Outputs
- releases/license-plate-game-0.3.0-candidate.apk (delivered separately)
- tools/build_android_local.py: full native build, never reuses stale dex
- tests/release-ui.cjs: Playwright regression; set LPG_RUNTIME, LPG_TEST_OUTPUT and optionally CHROME_BIN
- docs/RELEASE_0_3_UPDATE.json: verified metadata for prospective release
APK SHA-256: d81c4b6d026e6b2edb26c6132c345c73d330594bee91264750e7a4735251a7d1
## Rights / privacy notes
No private photos, locations or signing key committed. Tests use synthetic camera frames and local browser storage.
## Final recheck
Source changes, browser regression, lifecycle regression, strict audit, runtime staging, signed native build and metadata validation completed. Candidate certificate matches scrapbook 0.2. Phone testing remains explicitly outstanding. Publish only after phone acceptance, using APP_UPDATES.md; no current stable release was changed.
## Completion status
COMPLETE_WITH_EXCEPTIONS
