# License Plate Game — current continuation

**CURRENT signed Android update candidate (October 26, 2026):** Native Android `0.6.0-rc1`, `versionCode=6`, package `com.thelostharbor.licenseplategame`, compiled from current **502 plate images / 1,004 image files**. Signed APK `license-plate-game-0.6.0-rc1-signed-update.apk`, SHA-256 `1ddc819e98561a1293fa2417d7330a00ee24f6303179116006b335e7a35ccb7d`, 28,389,880 bytes, private Library `libfile_4731c410bb5481918f7fc7dac194f66f`; validation receipt Library `libfile_d3e6485dbc0c81918ad2f0223b9457b2`. SHA-256 signing certificate `6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b` confirmed **identical to the previous 0.5.0 distribution APK** using Android apksigner. APK v2/v3 signatures verify (v1 is absent; minSdk 26), all embedded 1,004 JPEGs remain byte-identical to the unsigned native build, APK ZIP integrity passes. GitHub unsigned native build [40415931961](https://github.com/thestonedcoyote-cell/license-plate-game/actions/runs/40415931961) passed staged-image/source/package/versionCode validation; signing key remained outside repository and runner. **Physical in-place upgrade and saved data persistence are not yet tested.** No stable/latest GitHub update feed is published, so this APK is a manually installable *release candidate*, not a completed in-app automated update. **Do not uninstall existing installation.** See `docs/ANDROID_0_6_0_RC1_PROCESS_NOTES.md` and `docs/APP_UPDATES.md`.


**CURRENT verified image checkpoint (2026-10-26):** 502 of 1,138 catalog plate designs have official source-matched examples (WA 54, OR 19, AK 41, MS 35, TX 157, CA 33, WI 31, FL 132), 1,004 runtime JPEG files; 636 unmatched. Florida image PR #39 merged `a2e7f921aa7234a7244eb6f285f72af784f537ae`, Pages deployment run `40410709517` passed. Current portable runtime SQLite and JPEG ZIP: Library `libfile_d3e43441cc2881918db696dde9c0c810`, SHA-256 `cbcd39a71f15a3ed57943c5f4e52d215d8a28175534ba4347ebb187899f8cdc0`, integrity/FK and 1,017 file hashes PASS. Original Florida 2026 official source PDF and 2025 comparison are privately archived as `libfile_75203fd8f7c88191945305ea94c0075c`. All source matches remain era-unverified, human_approval=false; no source license judgment or signed Android in-place upgrade acceptance. Earlier 370/768 counts in the historical paragraphs below are superseded; see `docs/CURRENT_IMAGE_CAMPAIGN_QUEUE.md` for the current next actions.


**Current version:** 0.5.0-alpha, Android versionCode 5, with recovery starting main `27da9d70625117e22a7a6c1ff1fc668a0997c667` (October 11, 2026). Consult `PROJECT_STATE.md` for the canonical live work queue and verified/pending distinctions, followed by `docs/APP_UPDATES.md` and `docs/IMAGE_CAMPAIGN_STATUS.md`. Refresh the remote revision before mutations.

**Current delivery (verified October 26, 2026):** 370 official source-matched design samples across WA54, OR19, AK41, MS35, TX157, CA33, WI31, with 740 JPEG display/thumbnail files in shared Identify/catalog/collection/offline runtime. **768** of 1,138 canonical plate UIDs remain without sourced design artwork. Texas PR #28 merged at `f39bc461f0407e978fb76bda8cac8dca9959a84e`; California/Wisconsin PR #32 merged at `f08d21b604ccb2bf00336dfd07cc591a0ed1307e`, Pages run `40394284189` passed. Source archive for CA/NV/WI/IN Library `libfile_01707d71188c819192f9c43b2b535279` (all 4 official source pages retrieved; 316 image files, 1 CA per-asset error). CA/WI images were independently source-SHA checked, and a WI source-label error was excluded. Texas seven unresolved catalog UIDs remain excluded. **All 370** source selections have unverified design era and no final human approval; no independent legal redistribution clearance is claimed. Current portable runtime SQLite/JPEG snapshot Library `libfile_91645e0e5f8c81919a51f66fe86c79df` (SHA-256 `cc32ee6cf15250b75babea868cdf9749ec2a00921ef0fa5706196c817a28b251`) now includes **370** UID selections and 740 JPEG copies; source evidence originals remain in independent Library archives. Historic full research database Library `libfile_e9eea656eb5081918bc7eeb3e0c56278` is preserved, not replaced. One identical display-byte pair (TX-00013/TX-00029) is flagged in its issue register. Package build Actions run `40407467478` passed. GitHub 0.5.0-alpha debug builds pass, but no stable latest signed distribution release or physical Android update/persistence acceptance is verified. See `docs/CURRENT_IMAGE_CAMPAIGN_QUEUE.md` and `docs/IMAGE_CAMPAIGN_STATUS.md` for next action.

The earlier 0.4 notes below remain **historical**; their candidate/version and rollout language no longer describes the newest candidate. Avoid accidentally repeating implemented work.

## Historical 0.4 checkpoint

# License Plate Game — 0.4 continuation

Start here, then read PROJECT_STATE.md, docs/APP_UPDATES.md and docs/PLATE_IMAGE_CAMPAIGN_PLAN.md. Do not ask the user to reconstruct the old conversation. Update this checkpoint after each release.

## Delivered candidate features
- Bigger vintage tuners, lined glass-covered color scales and day/night styles.
- Home fits short phones without the small unwanted scroll; landscape removes duplicate quick controls while keeping Identify accessible.
- Centered capture rectangle, faint split-prism/microprism SLR viewfinder.
- Prior camera lifecycle fixes, large photo reference and non-destructive crop/zoom/pan retained.
- Road Trip Notebook title opens locally persistent, editable stories/date/place/photo pages. Up to eight photo attachments. Optional plate link currently exposes a UID field; replace with a friendly picker.
- Pencil sighting counts and history/photos; prominent Mile Markers, earned/locked labels and next goal.
- First-launch account/offline choices plus skippable tutorial, replayable under More. Reuses optional cloud photo backup; collection/notebook remain local.
- Android image file chooser, scoped service-worker cache cleanup, correct offline asset failure, safer auth error rendering and version-aware native builder.

## Verification
The earlier 0.4 session passed 28 Chromium viewport/theme cases: 14 sizes spanning 320×568, 360×640, 360×740, 412×844, 360×800, 393×851, 375×667, 390×844, 430×932, 344×882, 768×1024, 820×1180, 1440×1000 and 844×412, each light/dark. Flows included offline welcome/tutorial, notebook save/reload, repeated sightings/history, synthetic camera and crop/zoom. This is browser simulation, not actual Android/iOS operating systems or physical phones. No Safari claim.

A workspace rollback occurred before the source push completed. The signed APK survived in saved files. Exact web source was recovered from its assets; native chooser source and build-version parsing were restored from the retained implementation record. Raw earlier matrix screenshots/results were not retained. The replacement matrix test passed all 28 cases again, including notebook save/reload. Fresh evidence is docs/PHONE_STUDIO_0_4.json. Never describe lost logs as presently available.

## Release state and next action
Candidate 0.4.0-alpha uses Android versionCode 4 and the preserved distribution key. Source update 4c2446465fa540c3365765eba5058f98b3b08bc3 was pushed to main; GitHub Pages deployment, Validate app and Take out the trash succeeded. The final native-only correction also allows JSON backup imports. Public candidate hash is in docs/RELEASE_0_4_UPDATE.json.

Candidate sharing URL after publication:
https://raw.githubusercontent.com/thestonedcoyote-cell/license-plate-game/downloads/0.4.0/downloads/license-plate-game-0.4.0.apk

Stable/latest updater release is held by docs/APP_UPDATES.md until physical upgrade acceptance. The downloads branch does not activate in-app updates. Install over the prior candidate without uninstalling; verify collection persistence, actual permission grant/cancel/retry, immediate camera, crop, file picker, offline use and update installation. Real account login/signup has not been end-to-end verified. Android installation always requires consent.

After acceptance, publish signed APK plus verified update.json together as a stable GitHub release. Metadata in docs is prospective, not a live release asset.

## Outstanding work
1. Real Android upgrade/camera/picker/updater and account acceptance, then stable rollout.
2. Friendly notebook plate picker; notebook/photo export and cloud backup. Uninstall erases local data.
3. Full image campaign: 1,138 designs, 291 simplified references and 847 absent images. Execute the saved plan; automated provenance/image verification first, human side-by-side review near the end.
4. Build the planned Find the Differences review UI: synchronized zoom/pan, overlay/flicker, discrepancy regions and correction tickets. Not implemented in this release.
5. Gradually remove compressed core/layered UI duplication and duplicate catalog loads; investigate unknown color metadata filtering. Passing Trash audit does not prove all redundancies gone.

## Build/recovery
tools/build_android_local.py requires Java 17, Android 35 jar, official Android build tools and APK_STORE_PASSWORD with the private signing key. Do not repack old native dex. Default CI debug signing is not the distribution key.

Certificate SHA-256: 6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b.
Private recovery archive: license-plate-game-private-signing-recovery.zip. Never commit key/password/archive.

Run tests/camera-lifecycle.cjs, tests/phone-studio.cjs, strict Trash audit, process-note checker and native signature/alignment checks. Keep source and this handoff committed so chat limits cannot strand progress.

## Image campaign launch checkpoint
Read docs/IMAGE_CAMPAIGN_STATUS.md first for campaign work. Phase 0 completed; 88 Washington gallery assets privately archived and 54 catalog designs have candidate mappings. Zero images approved. Raw evidence archive is plate-image-evidence-batch01-WA.zip. The current APK already supports More → Check for updates; the feed awaits a stable signed release.

## 2026-10-11 image integration
54 source-matched Washington images now have shared thumbnails/enlarged views across Identify, research catalog and collection. 108 JPEG derivatives are packaged and cached offline. Two incorrect automatic associations were rejected. See database/image-reconciliation-20261011.json and docs/IMAGE_INTEGRATION_PROCESS_NOTES.md. New reconciled package: LPG_Image_Database_2026-10-11.zip. Android source version is 0.5.0-alpha (code 5); use signed distribution build, not CI debug key. Source samples retain era uncertainty and do not imply human approval. 1,084 canonical records still lack acquired image links; three report candidates remain excluded.
