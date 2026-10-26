# LPG — Active plate image campaign queue

**Verified checkpoint:** October 26, 2026 (America/Los_Angeles). Refresh GitHub main and Actions results before working; this is not an unattended scheduling system.

## Current truth

- Repository: `thestonedcoyote-cell/license-plate-game`. Frozen app catalog: **1,138 canonical plate UIDs** across 58 jurisdictions.
- Source-matched plate images: **370** = WA 54 + OR 19 + AK 41 + MS 35 + TX 157 + CA 33 + WI 31.
- Remaining original catalog UIDs lacking acquired source images: **768** (67.5%). Runtime image derivatives: **740 JPGs**. Separate original 291 schematic baseline must not be mixed into source-image coverage.
- **All 370 remain `era_status=unverified`, `human_approval=false`.** The owner-directed fair-use reference rationale is separate from original image licenses and from any legal ruling.
- Three historical report-scope plate candidates are not part of the 1,138 runtime IDs.
- **Source discovery leads:** 26 of 58 represented jurisdictions; 32 still need reviewed agency sources.
- GitHub image integration PRs: WA earlier; Oregon [#21](https://github.com/thestonedcoyote-cell/license-plate-game/pull/21), Alaska/Mississippi [#24](https://github.com/thestonedcoyote-cell/license-plate-game/pull/24), Texas [#28](https://github.com/thestonedcoyote-cell/license-plate-game/pull/28), California/Wisconsin [#32](https://github.com/thestonedcoyote-cell/license-plate-game/pull/32).
- California/Wisconsin merged image commit `f08d21b604ccb2bf00336dfd07cc591a0ed1307e` **passed** Pages deployment run `40394284189` and four PR checks (app, cloud, audit, Android debug APK). **No stable signed Android distribution update has been published or physically verified.**

## Archived sources and data

| Artifact | Location / verified identity | Notes |
| --- | --- | --- |
| Washington source evidence | Library `plate-image-evidence-batch01-WA.zip` | Previously saved, supports original 54 matches |
| Oregon 38-page official DMV PDF and evidence | Library `libfile_1c9a2771f7308191b85009db82c688da` | Previously pinned exact source hash |
| Texas/Florida/Alaska/Mississippi harvest | Library `libfile_745e40877fcc8191a3476a2c1bbe2313` | Official Texas guide and AK/MS galleries downloaded; 2026 FL PDF HTTP 403 |
| Texas 157 sample contact-sheet review | Library `libfile_a579570cad5c8191b1b1a39f4c692214` | 157 name/image pairs; 7 unresolved and excluded |
| CA/NV/WI/IN 2026-10-26 original source archive | Library `libfile_01707d71188c819192f9c43b2b535279` | 4 agency source pages, 316 downloaded images, one CA per-asset error; ZIP SHA-256 `9ff45ee8c88571dba1a14f1ea6f817adc7ea03f119d9739b59d87656d2e97e30` |
| Last portable SQLite/images ZIP | Library `libfile_e9eea656eb5081918bc7eeb3e0c56278` | **Historical 149-image state. Needs to be rebuilt to match the current 370 image source manifest.** |

## Highest priority execution

1. **Rebuild source-matched portable SQLite+image archive to 370.** Use current `data/catalog-images.js`, `data/image-campaign/manifest.json`, `assets/plates` and existing scheme with UID stability, asset hashes, selected image records, per-source metadata, 3 separate research-report items if importing older archive. Validate SQLite integrity and foreign keys, full hash inventory and import into app. Archive it durably in Library. Do not treat previous 149-image ZIP as latest.
2. **Recover Florida at scale.** The official 2026 illustrated brochure `https://www.flhsmv.gov/pdf/specialtyplates/Florida%20License%20Plate%20Brochure%20%28Revised%201-2026%29%20reduced%20size.pdf` returned 403 on runner. An official earlier illustrated edition from 10/2025 is a public lead (no binary acquired yet). Search authoritative alternate agency image pages/official samples, not unrelated commercial art. Florida has 132 immutable catalog UIDs; do not mark any matched until sources and era correspond.
3. **Process remaining source archive.** Nevada has **115** downloaded candidate gallery image assets, mostly with absent alt labels; require visual+filename+agency label crosscheck for its 84 catalog designs. Indiana's official page exposed only **two** image assets (one plate example); additional official nested design pages/source retrieval needed for its seven UIDs. California retains 15 unmatched; Wisconsin 18. A Wisconsin official image labeled "Civil Air Patrol" depicted unrelated "Spay, Neuter, Adopt" and must remain excluded pending correction. Do not automatically count official gallery file totals as plate identities.
4. **Expand jurisdiction source coverage.** 32 of 58 represented jurisdictions lack an approved source lead. Prioritize larger gaps by catalog UIDs, beginning AK? (AK already has reviewed sources) and other >10-UID jurisdictions using `data/image-campaign/source-registry.json`; capture explicit licensing statements and year evidence when present.
5. **Iterative integration:** For each bounded batch, review source plate artwork and one-to-one immutable UID, pin original SHA-256, generate non-upscaled thumbnails/display images, update manifest, offline service worker cache and focused browser regression; run strict Trash, web/cloud and Android build CI. Generate a review PR before merging. Preserve original-source archives into Library; GitHub Actions artifacts expire.
6. **Mobile release gate:** Sign with the existing distribution certificate identity, perform **in-place upgrade** on Android without uninstalling (sightings/notebook data must remain), test native photo picker/camera/offline cache update, publish actual APK/release feed only after physical acceptance. A green CI debug APK is not acceptance.

## Failure lessons and protections

- October 26 source harvest recovery run `40386466698` succeeded and original ZIP was preserved to Library.
- TX generator first returned 159 nominal names, where only 157 had been preflight-approved. Enforced an explicit seven-UID exclusion; successful verified Texas run `40390240521`.
- CA/WI original-artifact Actions token received HTTP 401; no source bytes were accepted from an unauthorized job. Workflow was corrected to reacquire issuing-agency pages and check each reviewed image against **independent archived original SHA-256 pins** in `data/image-batches/ca-wi-original-hashes.txt`.
- First reacquisition used a different output-directory name; path normalization fixed via exact output-folder convention. Successful generation run `40393840418`, generated review PR #32 merged and Pages deployment succeeded.
- Never infer legal clearance, issue era, or human visual approval from matching official labels, images, or hashes. Never substitute an unrelated plate design to force complete coverage. Do not place original raw bulk research archives or signing secrets in the public app.

## Exact next step

Produce a refreshed **370-sample portable image/SQLite database** using the live manifest and its 740 JPEG derivatives. If that step cannot be completed in the current surface, continue by acquiring/reconciling the next official gallery evidence while preserving current app source/deployment and all recorded provenance.
