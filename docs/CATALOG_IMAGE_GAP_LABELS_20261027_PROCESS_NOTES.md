# Process Notes — Catalog source attribution and missing-photo disclosure

## Purpose
Fix incorrect plate source attribution and misleading unlabeled schematic previews observed while 636 of 1,138 plate designs still lack a real official source example in the 0.6.0-rc1 Android candidate.

## Inputs
- Canonical 1,138 plate UIDs; 502 source-matched samples from eight issuing jurisdictions; 636 without source-matched images.
- Exact `data/catalog-images.js` source attribution per selected plate, including agency source URL and reported retrieval date.
- Current shared plate rendering in `ui-current.js`, image-viewer code `catalog-images.js`, and focused regression `tests/catalog-images.cjs`.

## Step notes
1. Found every modal hardcoded to "Official Washington sample" and "Source: Washington Department of Licensing" despite per-record source URLs spanning eight jurisdictions.
2. Resolve display state/issuing agency from the source plate's immutable jurisdiction UID; keep the actual per-image source URL, date and unverified era status in the dialog. Do not invent historical issue years.
3. Label unmapped designs clearly as "source image pending" whether an illustrative schematic exists or no preview drawing exists at all; never label schematic art as a source photograph.
4. Update the research-results summary to show **the source-photo count within the currently selected filters**, rather than always announcing the global 502 photo count.
5. Handle failed modal image loading with a readable message and source link instead of a blank dialog.
6. Bump offline service-worker cache to ensure the corrected catalog viewer and labels replace cached older versions.
7. Add regression coverage for a Florida official source link and title, Nevada pending image disclosure and per-filter count, preserving existing WA full-image and offline tests.

## Exceptions / failures
No missing issuing-agency sample images are fabricated by this fix. 636 original catalog designs still require source acquisition; all 502 source matches remain era-unverified and not human-approved. The separately distributed Android 0.6.0-rc1 APK will not receive repository code changes until a new correctly signed versionCode>6 candidate is built and installed; GitHub website changes alone cannot rewrite an installed APK.

## Outputs
App catalog source viewer and fallback improvements, focused regression assertions, offline cache invalidation. New Android build must be a later versionCode with same original signing key; no stable latest feed or physical test inferred from website CI.

## Rights / privacy notes
Issuing agency URLs are citations, not licenses. No device user data or signing key is modified.

## Final recheck
Verify every source URL still comes from `data/catalog-images.js`, matching agency label and date, all 502 source images preserve unchanged paths, and missing images display clearly as pending. Run PR web, strict audit, cloud and Android debug CI; focused source viewer test separately when browser dependencies are available.

## Completion status
COMPLETE_WITH_EXCEPTIONS — correction prepared for CI and merge, physical Android delivery pending.
