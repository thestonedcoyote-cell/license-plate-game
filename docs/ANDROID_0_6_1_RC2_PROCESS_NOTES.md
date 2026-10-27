# Process Notes — signed Android 0.6.1-rc2 source update candidate

## Purpose
Deliver real Nebraska source plate samples and correct attribution/pending-image disclosure to installed LPG Android users while preserving their local data and the original Android signing identity.

## Inputs
- Main app code after #44 and #46: 1,138 frozen catalog IDs, 524 source-matched plate designs, 1,048 JPEGs, source-labeled dialogs and explicitly marked missing-image schematics.
- Previous signed APK: Android 0.6.0-rc1 versionCode 6, private Library `libfile_4731c410bb5481918f7fc7dac194f66f`; certificate SHA-256 `6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b`.
- Signing recovery archive remains private Library `libfile_2e4571ee277c81919b014aaa2cf8785e`.
- Existing native Android updater, per-app installer and all user storage must be retained unchanged.

## Step notes
1. Set versionCode 7 and versionName 0.6.1-rc2, preserving package `com.thelostharbor.licenseplategame`, targetSdk and minSdk.
2. Update the guarded release candidate workflow to stage and verify all **524** exact app image mappings and **1,048** JPEGs.
3. Compile full native unsigned release APK with Gradle; never substitute a repacked legacy APK.
4. Align unsigned candidate and verify package identifier/version plus SHA-256 of every bundled image.
5. Keep keystore and passwords entirely outside GitHub Actions. Locally sign with the preserved private key and verify same cert and APK v2/v3 signature schemes as installed v6.
6. Preserve the exact final signed APK SHA, verification receipt and a private artifact copy if Library storage permits.
7. Require on-phone in-place upgrade acceptance from signed code 6 to code 7 with collection, notebook, photos, search and camera preserved before publishing as stable/latest.

## Exceptions / failures
The user has not yet confirmed physical data preservation after prior v6 upgrade; build/signature checks alone are insufficient. GitHub CI debug APK uses a different signing key. Library storage recently reported its quota full; do not delete existing archives to make room without explicit authorization. All 524 source images are era-unverified and lack human approval.

## Outputs
Android versionCode 7 source and guarded unsigned release build. Signed output exists only after the build, private signing and verification steps actually pass; do not claim this in advance.

## Rights / privacy notes
Private signing data, source originals and end-user device records never enter public GitHub commits. Source image matches are not a copyright license or verified historical issue-year guarantee.

## Final recheck
Verify all 524 original source mappings, 1,048 embedded JPEG hashes, package and versionCode, exact previous certificate, ZIP/signatures and user data on actual Android installation separately.

## Actual build and local signing receipt (2026-10-27)
- Source update PR #48 merged at `0659f38062b457f1d9f370ce14d0a940e54883d0`; Android debug/app/cloud/audit pull-request checks passed.
- [Unsigned native build 40596573704](https://github.com/thestonedcoyote-cell/license-plate-game/actions/runs/40596573704) PASS. Exact Android versionCode 7, versionName `0.6.1-rc2`, 524 selected source image records and 1,048 image JPEGs, each checked against staged source.
- Signed locally using original `lpg-debug.keystore`, **not uploaded to GitHub**, with application ID `com.thelostharbor.licenseplategame`. The signature certificate SHA-256 `6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b` matches the prior signed versionCode 6 APK.
- Final APK `license-plate-game-0.6.1-rc2-signed-update.apk` is **29,459,196 bytes**, SHA-256 `97a3faf395fce771cf9ad28a77a5db612e408c2597f0bdc2b454069ac051c1c6`. Verified APK Signature Scheme v2/v3, intact ZIP structure, 1,048 identical image-file contents and exact 524 selected mappings after signing.
- Signed APK and machine-readable validation report exist as generated conversation attachments, not in the public GitHub repo. A private Library upload was not attempted after the Library reported quota exhaustion earlier in this session; retain prior archives.
- No stable/latest GitHub update release and no user-confirmed device in-place upgrade/data retention tests. The downloadable APK is an **install-over-existing release candidate**, not a proven stable published update.

## Completion status
COMPLETE_WITH_EXCEPTIONS — native v7 update candidate compiled, locally signed and cryptographically verified; real Android upgrade/data preservation and stable/latest distribution remain open.
