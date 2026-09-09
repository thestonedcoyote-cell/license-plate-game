# Process Notes — image campaign launch

## Purpose
Start real image acquisition, preserve provenance and verify whether the delivered Android candidate supports in-app updates.

## Inputs
Five canonical catalog chunks, existing reference maps, harvest_sources.csv, image campaign plan, native updater source and delivered 0.4 APK.

## Step notes
- Step 1: checked the native updater, in-app entry, permissions and delivered dex. Latest-release endpoint has no published stable release; feature already exists.
- Step 2: decoded/froze all 1,138 UIDs; reconciled 291 existing schematics and 847 missing schematic references. All statuses remain independent and unapproved.
- Step 3: added the Washington issuing-agency gallery and ran a bounded private harvest: 88 archived assets, no source download error.
- Step 4: verified every acquired asset hash and generated conservative name-match candidates for 54 catalog records. Reconciled all 1,138 IDs after mapping.
- Step 5: packaged private raw evidence with portable paths/hash inventory; prepared public metadata and campaign checkpoint.

## Exceptions / failures
Python research dependencies were initially unavailable; installed isolated research dependencies and reran successfully. Global official-source registry is incomplete; Washington is a documented bounded pilot after the catalog freeze, not completion of Phase 1. Some acquired files are site graphics rather than plates. Name matching does not establish era or visual accuracy. No legal/rights or final human approval is implied. No stable updater release was published.

## Outputs
Complete campaign manifest, baseline, source registry, Washington citation/hash index, summary, reusable baseline/mapping scripts, private evidence archive and IMAGE_CAMPAIGN_STATUS.md.

## Final recheck
Rechecked 1,138 unique IDs, no orphan schematic UID, and byte hashes of downloaded assets. Counts reconcile; 54 records have candidates but zero have verified public images or ready human review. Updater support is verified as packaged functionality, not a successful physical installation test.

## Completion status
COMPLETE_WITH_EXCEPTIONS: campaign started and first source batch acquired; full campaign and stable updater release are not complete.
