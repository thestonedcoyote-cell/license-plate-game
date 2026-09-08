# Process Notes
## Purpose
Address first-grant camera startup and repeated permission symptoms, enlarge the identification reference photo, and add non-destructive cropping. Prepare radio-dial concepts for user selection.
## Inputs
User report from the Moto Android app; existing native wrapper and queued updater branch; current capture/identification integration.
## Step notes
- Step 1: Found overlapping camera/GPS permission requests and unguarded asynchronous camera startup. These are plausible contributors; the reported phone failure has not been reproduced on a physical device.
- Step 2: Queued native runtime permissions, tracked canceled WebView requests, checked actual camera/approximate-location permission state, and limited grants to the local app origin. Start video playback explicitly before asking for GPS; discard late streams after leaving the camera.
- Step 3: Enlarged the reference photo to 150–260px tall with full-width contain sizing and a crop/expand dialog. Added drag-to-select cropping, numeric crop adjustment, full-photo reset, and cancel. Save crop coordinates and a separate cropped blob in the photo record; preserve the original blob. Reload the active stored photo when identifying a saved capture.
- Step 4: Generated three radio concepts: horizontal dashboard tuner, rotary knobs, and transistor-radio gauges. These are proposals and do not alter production color controls.
- Step 5: Native Java compilation, JavaScript syntax checks, runtime staging, strict Trash audit, and tests/camera-lifecycle.cjs passed. Lifecycle tests verify deferred GPS, explicit playback, and stale-stream disposal.
## Exceptions / failures
The Chromium runner crashed with SIGSEGV before opening the app on two attempts. Browser rendering, crop persistence end-to-end, and physical-device permission tests remain pending. No claim is made that the Moto camera bug is resolved on-device. No new APK is released. The next APK must rebuild the native wrapper, not reuse the old compiled shell.
## Outputs
MainActivity.java permission coordination; updated core bundle; photo-editor.js; UI photo integration and sizing; runtime/cache updates; camera lifecycle regression test; this checkpoint. Changes build on the queued in-app updater.
## Final recheck
Verified Java compilation, JavaScript syntax, runtime-file availability, camera lifecycle tests, and strict audit. Recorded the browser failure and outstanding crop/device validation. Hold rollout until those checks pass and the user chooses a dial design.
## Completion status
COMPLETE_WITH_EXCEPTIONS
