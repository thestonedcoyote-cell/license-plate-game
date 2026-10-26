# Process Notes — 370-image SQLite completion and Florida acquisition recovery (2026-10-26)

## Purpose
Preserve verified completed work and continue the high-yield official image acquisition campaign into Florida after the current illustrated PDF returned HTTP 403.

## Inputs
- Live GitHub 370-image catalog and successful Actions packaging run `40407467478`.
- Portable runtime SQLite/JPEG ZIP in Library `libfile_91645e0e5f8c81919a51f66fe86c79df`, SHA-256 `cc32ee6cf15250b75babea868cdf9749ec2a00921ef0fa5706196c817a28b251`.
- Historical original research archive `libfile_e9eea656eb5081918bc7eeb3e0c56278` remains preserved.
- Existing `data/harvest_sources.csv` and `data/image-campaign/source-registry.json`.
- Official FLHSMV URLs: 2025 illustrated brochure, standard registration page and specialty plate page. 2026 brochure prior CI failure: HTTP 403.

## Step notes
- Step 1: verified 1,138 canonical UIDs, 370 selected source-matched plates, 740 published JPEG paths and ZIP integrity.
- Step 2: recovered the GitHub-produced ZIP from Actions, validated hashes, and placed the inner portable snapshot (not the wrapper ZIP) into private Library.
- Step 3: verified SQLite integrity, zero foreign-key violations, 370 selected app images, 369 content-unique assets, 738 content-addressed derivatives, and 740 UID-indexed JPEG file rows.
- Step 4: recorded one shared-byte match (Texas `LPG-US-TX-00013` and `LPG-US-TX-00029`) as an unresolved image identity/era review case; neither is human-approved.
- Step 5: added three official Florida alternate source leads after the original 2026 illustrated brochure returned HTTP 403. The 2025 brochure cannot be treated as 2026 image-era proof.
- Step 6: corrected source-of-truth project documents to reference the current runtime snapshot without overwriting older deep-research original archives.
- Step 7: prepared a narrow new Florida harvest (no production image selection until original-source access, names, variants and file hashes are confirmed).

## Exceptions / failures
The new portable 370-image ZIP is a **runtime reference image copy**, not an archival superset of older evidence/SQLite; original source binaries and three independent historical report candidates are external to the snapshot. Florida alternate official pages may also produce HTTP 403. California/Nevada/Wisconsin/Indiana harvested images do not count as matched UIDs until individually mapped; Indiana only exposed two page images in prior batch.

## Outputs
Verified current portable snapshot, updated project checkpoints, three official Florida source leads in reviewed manifest/registry. Florida harvest should be triggered only after its source PR passes CI.

## Rights / privacy notes
Official source pages and published runtime sample derivatives are only evidence under the owner's chosen fair-use reference rationale, not legal copyright clearance, independent issue-era verification, or human art approval. Do not commit raw private research archives or signed Android credentials.

## Final recheck
Checked archive SHA-256, SQLite integrity/foreign keys, table counts, one explicit shared-byte issue, unchanged 1,138 UIDs and 370 selected manifest images. New Florida source rows are leads, not downloaded source images.

## Completion status
COMPLETE_WITH_EXCEPTIONS — durable SQLite snapshot finished; Florida access and unfilled 768 catalog image mappings remain.
