# License Plate Game checkpoint
Next candidate: 0.3.0-alpha, Android versionCode 3, on release/0.3.0-prep. Main remains the prior scrapbook release.

Implemented: compact radio color tuners; example plate and thumbnail matches; SLR camera styling; large photo-print reference; non-destructive crop, zoom and pan; restored Mile markers; offline atlas fallback. Native updater and camera lifecycle fixes are included.

Read docs/RELEASE_0_3_PROCESS_NOTES.md for checks and limitations, docs/APP_UPDATES.md for release steps. The signed candidate was prepared and delivered separately; its hash is in the notes. Do not publish the prospective metadata alone. Install over scrapbook 0.2 without uninstalling to check upgrade persistence, real permissions, camera capture and pinch/crop on the phone. After acceptance publish APK and update.json together. Earlier APKs need this manual install to gain updater support; subsequent updates still require Android installation consent.

Build with tools/build_android_local.py using Android 35 android.jar, official Android tools and the privately preserved distribution key. Never commit the key. Browser regression is tests/release-ui.cjs, lifecycle regression tests/camera-lifecycle.cjs. Strict trash audit and process-note checker are release gates.
