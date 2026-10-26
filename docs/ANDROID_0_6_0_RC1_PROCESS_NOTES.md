# Process Notes — Android 0.6.0-rc1 candidate for 502 plate images

## Purpose
Produce a genuinely newer native Android APK containing the verified 502-image web runtime and preserved user storage/update mechanisms, signed with the **same private certificate** as the prior versionCode 5 APK so an in-place upgrade is possible. This is a release candidate until real physical-device data-preservation tests pass.

## Inputs
- Main source current 502-match catalog (1,138 immutable IDs, 1,004 display/thumbnail JPEGs).
- Native applicationId `com.thelostharbor.licenseplategame` and previously distributed `versionCode=5`, `0.5.0-alpha`.
- Recovery signing archive in **private Library** `libfile_2e4571ee277c81919b014aaa2cf8785e`, with original certificate SHA-256 `6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b`. It contains a development keystore reused as a fixed distribution signing identity; do not include it in public GitHub or Actions.
- Existing native updater documented in `docs/APP_UPDATES.md`; does not imply a working published latest feed.

## Step notes
1. Bump Android `versionCode` to **6**, `versionName` to `0.6.0-rc1`; keep exact native package identifier and SDK contract.
2. Run strict Trash audit and stage **the entire** 502-image game source in `android-app/app/src/main/assets/www`.
3. Build the full modern native wrapper from Java/Gradle as **unsigned release**, not by repacking the old native shell.
4. On public GitHub Actions runner, verify APK package ID, numeric versionCode 6, build alignment, ZIP readability, and that all **1,004** embedded JPGs match the source SHA-256.
5. Upload only unsigned/aligned APK and Android public `apksigner.jar` build tool to short-retention artifact; no private key/secrets/passwords enter runner or public repository.
6. Locally sign unsigned candidate using separately recovered private keystore, verify final ZIP alignment, Android v2/v3 APK signature and signing certificate matches earlier distribution SHA-256 exactly.
7. Validate/update metadata and candidate availability separately. Stable/latest `update.json` must not be activated before real device acceptance.
8. On phone, install over existing app (never uninstall), verify stored sightings/notebook/photos still present; camera, picker, offline and manual update flows then require physical acceptance. Only after these pass can the signed APK and `update.json` be published as latest stable.

## Exceptions / failures
The previous 0.5 candidate has not been physically installed/accepted in this Chat surface. CI-created debug APKs use ephemeral debug signing and cannot preserve data as a direct upgrade. A successful signed candidate and matching certificate are necessary but **insufficient** evidence for real device behavior. Browser photo data and local storage are not included in any remote APK test package. Candidate `0.6.0-rc1` is not an approved stable release.

## Outputs
New versionCode 6 Android source, separate signed candidate once local signing/verification actually completes, and a bounded GitHub unsigned-release workflow. No private key in GitHub or generated artifacts. No silent removal of user data.

## Rights / privacy notes
Public plate imagery remains source-matched, with historical era and human approval unverified and an owner-directed fair-use project rationale, not a licensing conclusion. Preserve private keystore and passwords outside GitHub. Never embed or print private signing material in source, logs, or user-facing output.

## Final recheck
Before offering APK: verify immutable 1,138 source IDs, 502 source-matched entries, 1,004 images byte-matched in APK, package ID, versionCode > 5, cert SHA, signature and ZIP alignment. Physical update acceptance and stable latest feed remain explicitly separate.

## Actual build receipt and verification
- Source update PR #42 merged at `6f4dfaa38b0b8e4433063c701e4026fd261751bd` after four CI checks passed.
- GitHub Actions unsigned native release runner [40415931961](https://github.com/thestonedcoyote-cell/license-plate-game/actions/runs/40415931961) produced a 0.6.0-rc1 versionCode 6 aligned APK with all 1,004 JPGs byte-matched to repository source, plus the public Android apksigner utility. No private signing material was sent to GitHub.
- Local signing used the **original private recovery keystore**, with one signing certificate and matching previous 0.5.0 APK fingerprint, `6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b`. The appId is unchanged; versionCode advances from 5 to 6. Android APK Signature Scheme v2 and v3 verification PASS; v1 is absent on both prior/new APKs (minimum SDK 26).
- The signed package `license-plate-game-0.6.0-rc1-signed-update.apk` has SHA-256 `1ddc819e98561a1293fa2417d7330a00ee24f6303179116006b335e7a35ccb7d`, size `28389880` bytes, private Library `libfile_4731c410bb5481918f7fc7dac194f66f`.
- A separate validation JSON receipt is Library `libfile_d3e6485dbc0c81918ad2f0223b9457b2`. Package ZIP integrity passes, all 1,004 embedded plate JPEGs retain byte identity from the unsigned APK, and all non-META-INF native/app files are unmodified by signing.
- GitHub latest stable release endpoint was empty at preparation. No `update.json` latest/stable feed was published because physical in-place install/user-data survival are not yet verified.

## User/device acceptance still needed
Install the versionCode 6 APK on top of the existing, same-signer v5 app. **Do not uninstall**. Verify retained sightings, collection, notebook, attached photos, camera, picker, and updater manual check. Confirm no Android signature rejection. Only then publish signed stable latest GitHub release + matching `update.json` so future in-app updates are discoverable.

## Completion status
COMPLETE_WITH_EXCEPTIONS — properly signed, packaged, cryptographically verified, archived **manually installable candidate**. Physical upgrade acceptance and latest/stable in-app distribution remain open.
