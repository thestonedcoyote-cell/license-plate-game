# License Plate Game — current continuation

**Current version:** 0.5.0-alpha, Android versionCode 5, with recovery starting main `27da9d70625117e22a7a6c1ff1fc668a0997c667` (October 11, 2026). Consult `PROJECT_STATE.md` for the canonical live work queue and verified/pending distinctions, followed by `docs/APP_UPDATES.md` and `docs/IMAGE_CAMPAIGN_STATUS.md`. Refresh the remote revision before mutations.

**Current delivery (October 11):** 149 official source-matched catalog images, 54 Washington, 19 Oregon, 41 Alaska and 35 Mississippi, shared across Identify, research catalog and collection. The web/offline runtime stages 298 JPEG references. Oregon images were merged in PR #21 (`af64fe5dde48af0c663ad6aa180d3592108d6f2b`) and Pages deploy run `38199925236` passed. Acquired-image gap: 989 of 1,138 canonical records. A source match does not mean full design-era verification, legal clearance or human approval. Three unmatched report candidates remain excluded. Current portable database: `LPG_Image_Database_2026-10-12_Batch02.zip`, Library ID `libfile_e9eea656eb5081918bc7eeb3e0c56278` (previous 73-image package preserved). Oregon source archive: `LPG_OR_Official_Harvest_2026-10-11.zip`, Library ID `libfile_1c9a2771f7308191b85009db82c688da`. CI SDK repair PR #18 already merged successfully; physical Android acceptance and stable update feed remain outstanding. Source registry now includes leads for 26 of 58 jurisdictions and official source run `38200139649` retrieved Texas manual and AK/MS galleries, but Florida brochure returned 403; PR #24 integrated reviewed AK/MS 76 images and merged as `2f1036ef16954ef93bff028c726648cd73f14254`, Pages run `38201004819` passed. The source archive is Library `libfile_745e40877fcc8191a3476a2c1bbe2313`; the outstanding next high-yield image mapping is Texas (164 catalog IDs).

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
