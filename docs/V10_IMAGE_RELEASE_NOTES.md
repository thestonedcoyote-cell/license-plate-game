# Process Notes

## Purpose
Publish every plate reference image we can currently defend as a clean public app asset without treating possession of an official DMV image as redistribution permission. This record covers the v10 clean-image release cohort.

## Inputs
- Canonical app catalog v7: 1,138 collectible designs.
- 130 records with evidence-backed visual profiles.
- Official production imagery is used as research/verification evidence only unless separately cleared.
- Prior image-rights research and reconstruction classification.

## Step notes
- Step 1: Selected the current evidence-backed visual-profile cohort rather than inventing appearance for records that have not been visually researched yet.
- Step 2: Converted each profile into an LPG-owned compact render specification: background, text color, short slogan, origin code and broad motif family.
- Step 3: Protected logos/characters/sponsor artwork are not traced. The public renderer substitutes original generic symbols for broad concepts such as animal, mountain, water, school, service, flag, vehicle or protected mark.
- Step 4: Public renders use the fictitious serial `LPG 000`, omit validation stickers/security features and include a small `REF` mark.
- Step 5: The app maps renders by immutable plate UID, so the illustration cannot drift to another plate merely because names change.
- Step 6: The public release cohort currently contains 130 plate designs. All other designs retain their non-image fallback until their visual evidence is sufficient for reconstruction or their source art is separately cleared.
- Step 7: Production/source images remain private evidence for comparison and human validation.
- Step 8: Compared the v10 branch to main and confirmed no harvested production JPG/PNG/WebP file is introduced by the release.
- Step 9: Reconciled the public render cohort against canonical app data: 130 visual-profile UIDs, 130 unique UIDs, all present among 1,138 collectible records.
- Step 10: Ran GitHub validation run 34094776819, which successfully syntax-checked the renderer/manifest and asserted exactly 130 unique renders plus the fictitious-serial and `REF` safety markers.

## Exceptions / failures
- This does not claim that 130 renders are pixel-identical reproductions. They are identification references built from verified facts and independently drawn broad visual cues.
- 1,008 collectible designs do not yet have sufficient normalized visual-profile data for this reconstruction path.
- Third-party marks, character art, team/university logos and sponsor artwork are deliberately simplified or omitted even when visible on the production plate.
- Exact source-image reuse remains a separate rights-review path and is not silently folded into this clean cohort.

## Outputs
- `data/reference-renders-v10.js`: 130 plate-UID render specifications.
- `v10-patch.js`: independent SVG renderer and plate-card integration.
- `v10.css`: notebook presentation and reference-render styling.

## Rights / privacy notes
The public app uses LPG-created reference renders, not the harvested official production-image archive. A fair-use theory for exact thumbnails may remain under research, but it is not treated as the clean-release basis for this batch. Reference renders are screen-oriented and intentionally unsuitable as registration credentials. No user photos or locations are introduced by this image release.

## Final recheck
Rechecked the manifest count and uniqueness, canonical UID membership, renderer origin, fictitious `LPG 000` serial, `REF` marker, absence of harvested production-image binaries in the PR, service-worker inclusion, and successful GitHub validation. The public cohort is therefore internally consistent and rights-separated from the private verification archive. Remaining unrendered designs and exact-source-art rights questions are recorded as exceptions rather than represented as completed work.

## Completion status
COMPLETE_WITH_EXCEPTIONS — all 130 currently evidence-backed clean reference renders are staged and validated; 1,008 designs remain pending further visual normalization or separate rights clearance.
