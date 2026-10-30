# License Plate Game — current plate-image acquisition queue

**Verified October 29, 2026 (America/Los_Angeles).** Refresh live GitHub main and Actions before working. This project has a daily continuation automation; each run should perform real image intake where possible, with exact source identity checks.

## Current truth
- Frozen catalog: **1,138 immutable UIDs** representing 58 jurisdictions.
- **636 source-matched image selections (55.9%)**, with **502 remaining unmatched**. Exact current selection distribution: Washington 54, Oregon 19, Alaska 41, Mississippi 35, Texas 157, California 33, Wisconsin 31, Florida 132, Nebraska 22, Nevada 84 and Alabama 28. Total web/offline runtime **1,272 JPEGs** (display + thumbnail).
- Two newly merged source-image PRs: [Nevada #51](https://github.com/thestonedcoyote-cell/license-plate-game/pull/51), merger `61a639552ea6b983d622370f561a981dd0db5ba7`; [Alabama #53](https://github.com/thestonedcoyote-cell/license-plate-game/pull/53), merger `a95bdcb7b021df0680d2ea42e528704682deffba`. All four GitHub checks passed on each image PR. The Nevada merge passed subsequent Pages deployment run `40992694492`; confirm latest Alabama Pages build before claiming publication.
- All 636 images are **source-matched illustrations, not era-verified, not human approved, not independently rights-cleared.** The project owner's fair-use rationale is not a legal ruling.
- The current **signed Android 0.6.0-rc1, versionCode 6** still bundles 502 plate reference images. It is not a stable/latest in-app update; an upgrade to source 636 needs another signed versionCode after preserving the same signature and device data acceptance.

## Original source evidence and chain of custody
- Nevada/California/Wisconsin/Indiana original agency archive: private Library `libfile_01707d71188c819192f9c43b2b535279` with ZIP SHA-256 `9ff45ee8c88571dba1a14f1ea6f817adc7ea03f119d9739b59d87656d2e97e30`; Nevada official HTML SHA `b224c08e6fa0c03a4c796cd781c1bfefac76e605719f4e9c9aca27ee6c56bd2d` and image registry SHA `9a30e69e6f20252368d64f66c331a1977e98969eb303dc9cadc30c508439a8f5`. Nevada had 84 UID matches representing 82 unique original artworks; two pairs of design aliases share source images and are recorded in reconciliation.
- Alabama/Nebraska/Minnesota/Connecticut official archive: Library `libfile_07a572791eb481919902b4e16d6ef7ab`; Alabama HTML SHA `322ffe503d3d21c013ec0f006e8b13c3508712bc262398eef3e18f23c62622a0`; image registry SHA `dbb980bf693eaffa267ca1fff1bef183a374c97a1f63e03d75ab5ac55a1a87f9`. Alabama 28 matches, excluding two unclear catalog records. Both original source archives are private; only display/thumbnail derivatives belong in public GitHub.
- Other private source archives: Florida `libfile_75203fd8f7c88191945305ea94c0075c`, Texas/Alaska/Mississippi `libfile_745e40877fcc8191a3476a2c1bbe2313`, Oregon `libfile_1c9a2771f7308191b85009db82c688da`.
- Latest **portable SQLite snapshot currently represents 502 source images**, not 636: Library `libfile_d3e43441cc2881918db696dde9c0c810`, SHA `cbcd39a71f15a3ed57943c5f4e52d215d8a28175534ba4347ebb187899f8cdc0`. Rebuild the portable snapshot to 636 after newly integrated image count is confirmed. Preserve earlier deep-research and original archives.

## Highest-value image gaps (after 636)
| Jurisdiction | Missing | Official source leads |
| --- | ---: | ---: |
| Idaho | 68 | 1; old illustrated government PDF URL returned 404, try official interactive license plate guide or refreshed PDF |
| Ontario, Canada | 39 | 1 |
| New Jersey | 38 | 2 |
| Hawaii | 27 | 0 |
| Michigan | 22 | 3 |
| Wyoming | 21 | 1 |
| Washington | 18 | 1 |
| Wisconsin | 18 | 1 |
| Washington, D.C. | 16 | 1 |
| New Mexico | 16 | 1 |
| California | 15 | 1 |
| Iowa | 13 | 1 |
| Vermont | 13 | 0 |
| Maine | 12 | 0 |
| North Dakota | 12 | 0 |
| Virginia | 11 | 0 |

**Unmatched total across all jurisdictions is 502.** Thirty-two represented jurisdictions still need verified official source leads. The 2026-10-29 source-harvest batch for ID/NJ/MI/WY/ON was launched via main `data/harvest_trigger.json` (Actions `40993449073`) and must be reviewed and its evidence retained before GitHub artifact expiry. Do not count downloaded image files as source-matched designs.

## Next actual actions
1. **Harvest batch 05:** Inspect run `40993449073`, retrieve original image archive, preserve where storage permits, record every source failure and successful page/image SHA. Idaho's 2016 government poster PDF may still be unavailable; never invent substitutes.
2. **Per-UID review:** Cross-check selected source image artwork and exact catalog name against issuer page headings, manually inspect contact sheets, record original SHA-256, source URL, issue-era uncertainty and any deliberate aliases. Generate immutable UID-linked display/thumbnail copies only after review; use a separate generated branch and pass strict app/cloud/Trash/Android CI.
3. **Portable 636 SQLite archive:** Adapt the pinned image package generator from 502 selections to 636, build/validate all 1,272 JPG hashes and SQLite foreign-key integrity, and archive if quota permits.
4. **Expand remaining 32 uncovered jurisdictions:** Research official government registry/brochure/gallery sources, especially HI 27, VT 13, ME 12, ND 12 and VA 11. Preserve source URL reliability and publication date.
5. **Android distribution:** Prepare correctly signed versionCode > 6 update of current web/app source, test actual on-phone data-preserving upgrade, then enable stable GitHub release update.json; do not confuse GitHub debug builds with updateable distribution.

## Hard truth rules
Do not credit an image as matched unless a specific correct plate design is visible, and SHA/source/UID lineage is recorded. Do not substitute generic fleet plates for unrelated named fleet design UIDs, parking placards for license plates, or historical plates for current without proof. Do not announce all 1,138 as complete until each immutable catalog entry has an attributable source-matched image and Pages deployment is verified.
