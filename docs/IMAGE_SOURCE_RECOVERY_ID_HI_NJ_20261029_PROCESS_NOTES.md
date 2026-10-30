# Process Notes — Idaho, Hawaii, New Jersey source recovery, 2026-10-29

## Purpose
Continue retrieving authentic plate artwork for the three largest currently unfilled US-state gaps: Idaho 68, New Jersey 38 and Hawaii 27, after the previous Idaho illustrated poster returned HTTP 404.

## Inputs
- Verified current Idaho Transportation Department official license plate information page, interactive specialty plate guide and June 26, 2026 announcement of two new plate designs.
- Hawaii County official vehicle-registration specialty plate index and Hawaii State Office of Veterans' Services benefits/plate examples.
- New Jersey Department of Environmental Protection official Conserve Wildlife plate page.
- Current 697-of-1,138 source-matched runtime checkpoint, 441 unfilled UIDs, source harvest `data/harvest_sources.csv`, reviewed source registry.

## Step notes
1. Verified new issuer URLs by public source discovery, and treated the previous Idaho 2016 poster URL as a recorded HTTP 404 rather than retroactively counting poster artwork.
2. Added six agency/county issuing-source page leads in harvest CSV and `data/image-campaign/source-registry.json`; official image files are not yet downloaded or mapped.
3. Classified Idaho interactive guide as possible browser-dependent material; static HTTP harvest can legitimately find zero plate binaries and should record that failure rather than fake images.
4. Preserved current 697 image selections, immutable 1,138 catalog UIDs, and existing licensing/era/human-review statuses without mutation.
5. Plan next bounded source harvest on main, preserve original bytes/hashes when obtained, then inspect each candidate for exact plate-shaped artwork, catalog identity and variant.

## Exceptions / failures
The old official Idaho illustrated poster remains inaccessible via its former URL. The Idaho official interactive guide depends on JavaScript and may require a supported browser-driven acquisition approach. Hawaii and NJ officials may offer only a subset of historical/organizational designs. These six source pages alone count as **zero** new matched plate images.

## Outputs
Six new source registry/harvest leads, scoped next-step intake of ID/HI/NJ government artwork. No license images or APK released by this PR.

## Rights / privacy notes
Official source locations are not independent artwork redistribution licensing approvals. No private signing key or player data touched.

## Final recheck
Verify literal source URL retrieval and media type, archive original image SHA and issuer page context, then select only one-to-one exact immutable UIDs. Subject generated image branch to independent four PR checks before merging.

## Completion status
COMPLETE_WITH_EXCEPTIONS — source references recorded; images await acquisition and review.
