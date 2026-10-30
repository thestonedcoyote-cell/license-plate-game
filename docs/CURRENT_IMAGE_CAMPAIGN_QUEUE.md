# License Plate Game — source-image completion campaign

**Verified October 29, 2026.** 1,138 immutable canonical design UIDs is the goal. The scheduled `LPG Image Completion` automation (task ID `6ae403e314b0819197579d5378fe3987`) will continue daily until all 1,138 have source-matched images and Pages reflects the result. Refresh live GitHub main, not just this note, before changes.

## Current truth
- **697 / 1,138 source-matched plate image examples (61.25%)**. **441 UIDs remain unresolved**. **1,394** public display/thumbnail JPG files, all source SHA links present.
- Image matches by place: WA 54, OR 19, AK 41, MS 35, TX 157, CA 33, WI 31, FL 132, NE 22, NV 84, AL 28, MI 22, CA-ON 39.
- Exact source-image integration PRs: NV [#51](https://github.com/thestonedcoyote-cell/license-plate-game/pull/51), Alabama [#53](https://github.com/thestonedcoyote-cell/license-plate-game/pull/53), Michigan/Ontario [#56](https://github.com/thestonedcoyote-cell/license-plate-game/pull/56), all four PR checks passed and post-merge Pages run `40994709178` passed for the 697 snapshot.
- Some UIDs are legitimate aliases reusing identical physical sample art. Three content-duplicate cases are recorded in portable SQLite issues; **do not call these independent design/era approvals**.
- All 697 image entries remain `match_status=source_matched`, `era_status=unverified`, `human_approval=false`. Issuing-agency artwork origin and owner's project fair-use reference rationale are not a legal licensing decision, and plate issue-era attribution remains open.

## Portable database and original evidence
- **Current SQLite/JPG runtime archive** `LPG_Reference_Image_Snapshot_2026_10_29_697.zip`; private Library `libfile_49cdcafc528c81919e38066a6abda87b`; SHA256 `be2efec2e7cad85a7e315188e645cb6b5a881e3acfd04265b362fdb41a58e4be` (32,404,836 bytes). Integrity checks PASSED: 1,138 canonical catalog IDs, 697 selected images, 1,394 UID-indexed JPEG paths, 694 content-unique published assets, 3 explicitly flagged shared image issues, all SQLite FKs clean, ZIP contents/hashes verified. Does **not** contain original government PDF/HTML/image evidence binaries.
- **New ID/NJ/MI/WY/Ontario official source archive**, Library `libfile_e6ab2311f05c8191a20d6339ba96fa26`, generated from source harvest run `40993449073` (7 of 8 source pages, 174 image files; outdated Idaho government poster URL 404). Source galleries for MI/ON have page HTML/asset-registry SHA pinned in `data/image-batches/mi-on-61-reviewed-20261029.json` and 61 per-original image hashes in `database/image-reconciliation-mi-on-20261029.json`.
- **Nevada/CA/WI/IN original source archive:** Library `libfile_01707d71188c819192f9c43b2b535279`. **AL/NE/MN/CT:** `libfile_07a572791eb481919902b4e16d6ef7ab`. **FL:** `libfile_75203fd8f7c88191945305ea94c0075c`. **TX/AK/MS:** `libfile_745e40877fcc8191a3476a2c1bbe2313`. **OR:** `libfile_1c9a2771f7308191b85009db82c688da`.
- Historic 502 source-image runtime ZIP: `libfile_d3e43441cc2881918db696dde9c0c810`; 149-image deep research archive `libfile_e9eea656eb5081918bc7eeb3e0c56278`. Preserve both instead of overwriting them.

## Highest-value unmatched jurisdictions
| Jurisdiction | Unmatched catalog IDs | Source status |
| --- | ---: | --- |
| Idaho | 68 | Old illustrated state poster URL HTTP 404, official interactive guide at apps.itd.idaho.gov requires scripted browser/deep source retrieval |
| New Jersey | 38 | NJ MVC official dedication index exists but earlier harvest did not capture full plate graphics, follow official dedicated individual subpages and state agency samples |
| Hawaii | 27 | No vetted official gallery registry; county DMV and state veteran/organization plate pages are research leads |
| Wyoming | 21 | Official WYDOT gallery downloaded only a few assets; follow detailed official subpages |
| Washington | 18 | Supplement original issuing-agency DOL plate pages and earlier variants |
| Wisconsin | 18 | Gallery labels include some mismatches; visual review required |
| Washington, DC | 16 | Official government image lead exists |
| New Mexico | 16 | Official government source lead exists |
| California | 15 | Complete older/current era details and specific original source matching |
| Iowa | 13 | Official state source lead exists |
| Vermont | 13 | Agency source discovery needed |
| Maine | 12 | Agency source discovery needed |
| North Dakota | 12 | Agency source discovery needed |
| Virginia | 11 | Agency source discovery needed |

Remaining **441** distributed across more jurisdictions including Texas 7 unresolved, Alabama 2 intentionally excluded, and Indiana 7 after the original two-image official page harvest. All source leads require direct validation; no missing artwork should be fabricated.

## Execution order
1. **P1 Idaho + New Jersey + Hawaii:** Find current issuing-agency galleries or PDFs/interactive source data; do not rely on dead poster links. When available, acquire raw originals, page context and SHA-256 and preserve privately.
2. **P1 Wyoming / Idaho historical gaps:** Check government gallery subpages and older plate variants; pin names, issue-era uncertainty and source hashes. Do not count homepage icons or downloadable assets as completed design matches.
3. **P1 further integration:** Produce bounded one-to-one reviewed UID maps, validate originality/plate aspect and source SHA, generate 800px or original-resolution display and 300px thumbnails, bump offline cache, run browser and app/Trash/cloud/Android CI, merge reviewed image PR and verify Pages.
4. **P2 portable snapshots:** Refresh SQLite only after new checked image batches, keeping complete original catalog and stored source/derivative hash chain, retaining historical archives.
5. **P2 signed Android candidate:** The last signed Android **0.6.0-rc1 versionCode 6** contains only the earlier **502-image** runtime, not the 697-image website. Future signed build must use same preserved certificate, higher versionCode and real physical install/data-preservation acceptance before stable in-app feed.
6. **P3 content accuracy:** Inspect shared-image aliases, catalog names that conflict with official source labels, and historical-era rights/human approval independently of basic sample source-matching.

## Absolute completion criterion
Do not claim all 1,138 plate images completed until `data/catalog-images.js` has 1,138 distinct immutable UIDs, each correctly matched to a verifiable source and original asset SHA, 2,276 valid web/offline image files, successful repository CI and confirmed Pages deployment. Stop the daily completion task only when this is independently verified.
