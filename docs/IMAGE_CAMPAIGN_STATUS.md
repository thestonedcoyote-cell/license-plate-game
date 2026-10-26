# Image campaign — verified checkpoint October 26, 2026

The game web/Android **source** has **370 source-matched official plate designs**: 54 Washington, 19 Oregon, 41 Alaska, 35 Mississippi, 157 Texas, 33 California, and 31 Wisconsin. Each mapping includes a display and thumbnail JPEG, for **740 offline-staged files**. Acquired source-image coverage is **370 / 1,138 = 32.5%**; **768** canonical designs still lack source-matched examples. Historical 291 schematics / 847 without schematics is a separate artistic-baseline metric.

The October 26 Texas samples came from 161 named examples in the 48-page official TxDMV guide. Seven Texas catalog UIDs remain unresolved and were explicitly excluded; 157 were matched to unique official sections. California/Wisconsin recovered four official agency sources, with 316 gallery images downloaded across CA/NV/WI/IN and one California per-asset failure. Exactly 33 California + 31 Wisconsin designs were visually screened and matched, including an explicit exclusion for Wisconsin Civil Air Patrol, where the issuing-agency image caption points at unrelated Spay/Neuter artwork. Nevada and Indiana source evidence is archived but has **no additional source-matched UIDs** yet.

**Verification:** Merged [Texas image PR #28](https://github.com/thestonedcoyote-cell/license-plate-game/pull/28) and [CA/WI image PR #32](https://github.com/thestonedcoyote-cell/license-plate-game/pull/32) each passed app validation, Trash audit, cloud validation and Android debug-build CI. The CA/WI image revision passed GitHub Pages deployment run `40394284189`. These CI results **do not** constitute physical-device or signed-in-place Android update acceptance. Each of the 370 mapping records remains `source_matched`, `era_status=unverified`, `human_approval=false`; owner-directed fair-use project intent does not certify legal redistribution rights.

**Preserved evidence:** Full CA/NV/WI/IN source archive `LPG_official_harvest_CA_NV_WI_IN_2026-10-26.zip`, Library `libfile_01707d71188c819192f9c43b2b535279`, SHA-256 `9ff45ee8c88571dba1a14f1ea6f817adc7ea03f119d9739b59d87656d2e97e30`. Texas 157-sheet review archive `LPG_Texas_157_Review_2026-10-26.zip`, Library `libfile_a579570cad5c8191b1b1a39f4c692214`. The **portable SQLite ZIP is stale** at 149 samples (Library `libfile_e9eea656eb5081918bc7eeb3e0c56278`); do not substitute its counts for the merged source manifest.

**Next priorities:** Build an updated 370-image portable SQLite evidence package; investigate Florida's official alternative 10/2025 brochure after the 1/2026 PDF returned HTTP 403; match remaining Nevada/Indiana acquisitions or mark unresolved; acquire lead material for the 32 jurisdictions still without reviewed official source pages; continue source-verified image batches; physically test the app's signed upgrade path and data preservation. Details: `docs/CURRENT_IMAGE_CAMPAIGN_QUEUE.md`.

## Original September 9 discovery and calibration checkpoint

## Current checkpoint
Phase 0 passed: 1,138 unique plate UIDs, no missing/duplicate UID, 291 existing schematic references, 847 without a schematic. Existing art is explicitly unverified. Catalog designs span 58 jurisdictions; the original registry had source leads for only 16. Washington's official gallery is now added.

The first bounded Washington pilot archived 88 assets from the issuing agency's gallery. Automatic name/filename matching attached evidence candidates to 54 catalog designs. Assets include non-plate site graphics and duplicate design variants; 88 is not a verified plate count. A name match does not establish design era. Zero images have been marked visually verified, rights-approved or ready for human review.

Official source: https://dol.wa.gov/vehicles-and-boats/vehicles/license-plates/get-custom-plates/special-design-plates

## Durable files
- data/image-campaign/manifest.json: all 1,138 records, independent identity/visual/public-use/safety/review statuses and next actions.
- data/image-campaign/source-registry.json: jurisdiction coverage and outstanding source discovery.
- data/image-campaign/baseline.json: frozen initial totals and catalog hash.
- data/image-campaign/evidence-index-batch01.json: public citation/hash index, no raw production images.
- data/image-campaign/batch01-summary.json: actual pilot totals.
- Private evidence archive: plate-image-evidence-batch01-WA.zip, saved separately. Contains official HTML/text, downloaded assets, portable relative-path index and hash inventory. Never commit this archive or its raw images to the public repo.

## Next execution
1. Finish official-source discovery for uncovered jurisdictions. Registry leads require retrieval, not assumed verification.
2. Resolve Washington candidate mapping conflicts and eras; investigate unmatched catalog entries and newly offered designs without silently changing UIDs.
3. Extract factual visual specifications and element-level public-use questions. Group redundant/irrelevant gallery assets before rendering.
4. Retrieve Oregon's reviewed manual as the next bounded batch; archive/hash evidence and update the canonical manifest without replacing its progress.
5. Build candidates, automated differences and integration rehearsal. Human review remains Phase 9, using the planned Find the Differences interface; that interface is not yet implemented.

Campaign runs are explicit work sessions, not an unattended background job. Start with this checkpoint in a new chat. Historical instruction superseded for the 54 Washington examples now shown in the public app by the owner's direction. Other unmapped examples still require evidence and review.

## Execution exception
The full Phase 1 registry is still incomplete. A bounded Washington acquisition pilot was run after the complete Phase 0 catalog gate to establish a working evidence/mapping pipeline. This does not claim the global source-registry gate or later verification gates passed.

## Updater clarification
The delivered 0.4 APK contains AppUpdates, More → Check for updates, package-install permission, hash/package/version/signature verification and Android installer handling. This was checked in its packaged dex and web assets as well as source. GitHub releases/latest currently returns 404 because no stable release is published. No replacement APK is needed to gain updater support. Future delivery requires a newer signed APK and matching update.json published together to a stable GitHub release. Android asks for installation consent. Physical upgrade acceptance remains required before stable publication.
