# License Plate Game — current plate-image campaign queue

**Verified October 26, 2026.** Refresh GitHub main and library evidence before any new writes. This is an active execution queue, not an unattended task.

## Where we are
- Frozen canonical runtime: **1,138 unique UIDs**, 58 represented jurisdictions.
- **502 source-matched plate design examples** (WA 54, OR 19, AK 41, MS 35, TX 157, CA 33, WI 31, **FL 132**). Coverage **44.1%**; **636** still lack matched official images. **1,004 public display/thumbnail JPEGs** staged for web/offline Android source.
- The Florida integration PR #39 merged `a2e7f921aa7234a7244eb6f285f72af784f537ae`, Pages deploy run **40410709517 PASS**, all four PR CI checks passed. All 132 FL source xrefs/page images/hashes were compared to the official 2026 issuing-agency 27-page brochure.
- All current matches are `source_matched`, **not era-verified or human-approved**, and no independently adjudicated copyright clearance is claimed. Three historical report candidates remain outside canonical runtime.
- Official source-lead coverage remains **26 of 58 jurisdictions**. Other 32 require government source discovery.
- **Signed stable Android release and real in-place upgrade/data-preservation acceptance are still pending.** CI debug builds are not a signed distribution channel.

## Durable checkpoints
- **Current portable SQLite/runtime images:** `LPG_Reference_Image_Snapshot_2026_10_26_502.zip`; private Library `libfile_d3e43441cc2881918db696dde9c0c810`; SHA-256 `cbcd39a71f15a3ed57943c5f4e52d215d8a28175534ba4347ebb187899f8cdc0`; 21,596,295 bytes; ZIP integrity, **1,017** file/hash checks, SQLite integrity and foreign keys PASSED. Tables contain 1,138 canonical catalog rows, 502 selections, 1,004 UID-indexed JPEGs, 501 content-addressed assets, 1,002 derivatives, 1 shared-image issue (TX-00013/TX-00029).
- **Private official Florida raw evidence:** Library `libfile_75203fd8f7c88191945305ea94c0075c`. Official 2026 brochure SHA-256 `d10418d394fe8d95624cdb932627536c258b4f6272786c38bd68a1a04087834a`; 2025 brochure preserved separately in same source archive. This is not distributed with app.
- **Official CA/NV/WI/IN originals:** Library `libfile_01707d71188c819192f9c43b2b535279`. The harvested Nevada gallery contains 115 assets, not yet mapped to design UIDs; official Indiana page exposed just two images, requires supplementary sources.
- **Official Texas/Alaska/Mississippi original harvest:** Library `libfile_745e40877fcc8191a3476a2c1bbe2313`.
- **Official Oregon source archive:** Library `libfile_1c9a2771f7308191b85009db82c688da`.
- **Prior 370 runtime snapshot:** Library `libfile_91645e0e5f8c81919a51f66fe86c79df` (preserved historical state).
- **Prior 149 deep research archive:** Library `libfile_e9eea656eb5081918bc7eeb3e0c56278` (not replaced by runtime-only DB).

## Next executable priorities
1. **P1 Nevada:** Inspect 115 acquired official Nevada image candidates; verify labels/identities through source-page HTML context, official detail pages and individual plate appearance before UID matching. Nevada has 84 frozen catalog UIDs; `115 downloaded assets` does not imply 84 matched plates.
2. **P1 next bulk source batch:** Acquire original government plate brochures and galleries in Minnesota, Nebraska, Alabama and Connecticut. Save GitHub harvest output into private Library immediately before retention expiry. Do not approve plate images automatically.
3. **P1 Indiana/remaining jurisdictions:** Expand reviewed official sources for Indiana's 7 UIDs; discover official sources for the 32 jurisdictions lacking leads, prioritizing highest catalog gaps.
4. **P1 integration:** For each batch, preserve immutable UIDs, source identity/caption, original SHA-256, display/thumbnail hash, status distinctions, and use a generated review PR before web production. Verify offline cache/Identify/catalog/collection and app/cloud/audit/Android CI, then verify Pages deployment.
5. **P2 mobile distribution:** Validate a single stable signed Android identity, in-place update from existing installation, retained local sightings/notebook/photos, camera and native installer; only publish a latest/stable in-app update after physical acceptance.
6. **P3 content audit:** Resolve shared-image Texas pair, historical design variants and original licensing/permission questions; build Find the Differences reviewer separately from basic sourced-image ingestion.

## Hard stop conditions
Do not present agency source download counts as images matched to catalog UIDs. Do not publish image interpretations when ID, design or era conflicts. Do not publish original government source PDFs or private signing credentials to the public repository. Never claim a stable signed update or final artwork approval without a real acceptance result.

## Exact next action
Use the reviewed official source registry to harvest MN, NE, AL and CT as a bounded, source-hashed research batch. Archive the result immediately, then continue with one-to-one review and integration while keeping the 502-image runtime checkpoint intact.
