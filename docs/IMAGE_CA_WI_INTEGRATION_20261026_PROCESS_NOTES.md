# Process Notes — California and Wisconsin image batch October 26, 2026

## Purpose
Add 64 independently inspected issuing-agency license plate samples to immutable catalog UIDs, preserving original hashes and unresolved matches.

## Inputs
Official CA DMV and WI DOT plate galleries harvested by GitHub run 40386466698, stored as 2026-10-26 private evidence. Exact UID/asset source pairs in data/image-batches/ca-wi-reviewed-map.txt. Prior 306 official sample selections, 1,138 immutable catalog UIDs.

## Step notes
- Step 1: reacquired official agency galleries; every selected original must match a pinned hash from the separately preserved October 26 archive.
- Step 2: enforced exactly 33 CA and 31 WI manually reviewed UID/source-file associations.
- Step 3: verified 64 independent archival original hashes (not just the current reharvest manifest), rejecting modified images, absent/malformed labels and artifacts.
- Step 4: explicitly excluded Wisconsin Civil Air Patrol because its official label points at unrelated Spay/Neuter/Adopt artwork.
- Step 5: created 64 display and 64 thumbnail aspect-preserving JPEGs without upscaling.
- Step 6: expanded the game source image manifest from 306 to 370 examples, offline cache from 612 to 740 JPEGs, and browser regression for California/Wisconsin.
- Step 7: validated all 128 output hashes, 64 unique catalog IDs, web runtime build, offline manifest version, strict Trash audit and JS syntax.
- Step 8: prepared image candidates on a review branch only; main website and signed APK release await separate approval/tests.

## Exceptions / failures
Other California and Wisconsin gallery photos remain excluded when identity or variant is unclear. One original California asset request failed in the harvest, and Nevada (115 downloaded images) and Indiana (2 downloaded images) are not covered by this integration. There is no approval of historical issue era, source license, legal fair-use conclusion, human final visual verification, or signed Android on-device upgrade.

## Outputs
64 new source-matched selections, 128 JPEG derivatives, 370 cumulative image selections, and database/image-reconciliation-ca-wi-20261026.json with source labels/files/original hashes and image derivatives. Private source archive Library libfile_01707d71188c819192f9c43b2b535279.

## Rights / privacy notes
Do not place wholesale original galleries, private credentials, device registrations or raw unrelated material in the public app package. Attribute original government source pages and keep project fair-use basis separately from source-license status.

## Final recheck
Checked 306+64=370 unique selections, 1138-370=768 unmatched UIDs, 740 offline JPEG files, all 128 derivative SHA-256 hashes, no Wisconsin Civil Air Patrol incorrect match, and staged runtime files. Physical Android upgrade and human review remain separate tasks.

## Completion status
COMPLETE_WITH_EXCEPTIONS
