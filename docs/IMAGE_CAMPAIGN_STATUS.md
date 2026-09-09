# Image campaign — started 2026-09-09

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

Campaign runs are explicit work sessions, not an unattended background job. Start with this checkpoint in a new chat. The public app continues to use the prior reference set until new candidates complete all release gates.

## Execution exception
The full Phase 1 registry is still incomplete. A bounded Washington acquisition pilot was run after the complete Phase 0 catalog gate to establish a working evidence/mapping pipeline. This does not claim the global source-registry gate or later verification gates passed.

## Updater clarification
The delivered 0.4 APK contains AppUpdates, More → Check for updates, package-install permission, hash/package/version/signature verification and Android installer handling. This was checked in its packaged dex and web assets as well as source. GitHub releases/latest currently returns 404 because no stable release is published. No replacement APK is needed to gain updater support. Future delivery requires a newer signed APK and matching update.json published together to a stable GitHub release. Android asks for installation consent. Physical upgrade acceptance remains required before stable publication.
