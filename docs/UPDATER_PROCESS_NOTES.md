# Process Notes
## Purpose
Prepare an in-app update flow for the next release without publishing a new APK now.
## Inputs
Existing native wrapper, project stable GitHub releases, preserved distribution signing certificate, Android DownloadManager and package installer APIs.
## Step notes
- Step 1: Added native release discovery, explicit download and installation prompts, persistent DownloadManager tracking, retry, and per-app install permission handling.
- Step 2: Added checksum, package identity, minimum SDK, increasing version, and signer checks before opening the Android installer.
- Step 3: Added an Android-only update button under More and startup checks. Added a metadata generator that rejects the wrong distribution key and reads metadata directly from a verified APK.
- Step 4: Compiled all native sources with Java 17 against Android API 35 successfully. Checked JavaScript syntax and the strict Trash audit. Exercised the metadata generator against the existing signed APK and confirmed rejection of a different signer and an unrelated download domain.
- Step 5: Prepared the release runbook, including the one-time manual installation required to receive the updater, full native rebuild requirement, and device acceptance checks.
## Exceptions / failures
No release, update metadata, or new APK has been published. Current installed versions remain unchanged. Physical-device end-to-end testing is pending. Default GitHub CI debug keys must not be used to publish updates for the existing distribution key.
## Outputs
AppUpdates.java, wrapper and manifest integration, Android-only More button, tools/prepare_update.py, docs/APP_UPDATES.md.
## Final recheck
Verified native compilation, JavaScript syntax, metadata generation, negative metadata tests, process notes, and the strict Trash audit. Release rollout remains held for the next update and requires the device checks in APP_UPDATES.md.
## Completion status
COMPLETE_WITH_EXCEPTIONS
