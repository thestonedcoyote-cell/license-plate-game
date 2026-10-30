# Process Notes — Nevada 84 official license plate artwork integration

## Purpose
Map the entire existing Nevada subsection of the frozen License Plate Game catalog to real sample plate illustrations from the issuing state DMV, using reviewed visual plate artwork, source HTML, exact asset filenames and original binary hashes.

## Inputs
- Nevada DMV official design gallery: `https://dmv.nv.gov/platesmain.htm`; original web harvest run `40386466698`.
- Original preserved private ZIP Library `libfile_01707d71188c819192f9c43b2b535279`, SHA-256 `9ff45ee8c88571dba1a14f1ea6f817adc7ea03f119d9739b59d87656d2e97e30`.
- Archived Nevada `assets.json` SHA `9a30e69e6f20252368d64f66c331a1977e98969eb303dc9cadc30c508439a8f5`; archived source HTML SHA `b224c08e6fa0c03a4c796cd781c1bfefac76e605719f4e9c9aca27ee6c56bd2d`.
- Exact 84-row UID/source-filename mapping in `data/image-batches/nevada-84-reviewed-20261029.json`. Catalog baseline 1,138 unique immutable UIDs and 524 already source-matched designs.

## Step notes
1. Read the issuing-agency source page and archived gallery registry; exclude 20x20 icons and other page decorations.
2. Rendered and inspected four contact sheets covering 94 full-width sample images. Checked visually that the source file for each catalogued Nevada name depicts a license plate, not decorative site artwork.
3. One-to-one mapped all 84 canonical Nevada UIDs to the official gallery plate filenames; two duplicate-content pairings are intentional name aliases: `LPG-US-NV-00002/00006` for Home Means Nevada and `LPG-US-NV-00004/00032` for Agriculture.
4. A fixed-number GitHub Actions job retrieves the original government source from prior harvest and validates exact archived HTML/asset registry SHA before selecting any art.
5. Original image SHA is checked against the source registry; SVGs are rendered at original intrinsic dimensions and JPG/PNG images are converted aspect-preservingly with no speculative plate details.
6. Generator expects exactly 524 existing matches and generates exactly 84 new selected UIDs and 168 display/thumbnail JPEGs, updating the offline service-worker cache and regression assertions to 608/1,138 source-matched.
7. All generated binaries go first to a separate review branch, with an image reconciliation file recording UID, gallery filename/URL, source original SHA, derivative hashes and unverified review statuses. App, cloud, Trash and Android CI review precedes merge.

## Exceptions / failures
Two historical catalog aliases intentionally reference the same official plate artwork, not distinct independently verified plate designs. Every issue-era remains `unverified`, every `human_approval=false`. This produces source-matched reference artwork, not owner inspection/approval of every historical year or a legally cleared commercial redistribution license. Other 530 UIDs still require official artwork after this prospective batch. The currently signed Android `0.6.0-rc1` APK includes the earlier 502 image snapshot, not new Nebraska/Nevada images.

## Outputs
Generator `tools/integrate_nevada_gallery.py`; 84-row reviewed mapping, source-pinned image workflow. Generated review branch contains `database/image-reconciliation-nv-20261029.json`, 168 JPGs, source-selected manifest and offline cache update.

## Rights / privacy notes
The private issuing-agency original archive stays in Library/GitHub temporary artifacts, not in the public source repository. The user's fair-use project rationale is not a legal determination. Never release private signing credentials or use debug key for stable in-place updates.

## Final recheck
Original gallery source HTML/asset manifest SHA; all 84 individually source-SHA matched; 82 distinct source image binaries plus two explicit aliases; 1,138 immutable catalog IDs; 608 selections, 1,216 JPEGs; every generated derivative hash; strict Trash, app, cloud and Android CI; GitHub Pages deployed state after final merge. Physical Android acceptance requires subsequent signed versionCode 7+ build and non-destructive install on a device.

## Completion status
IN_PROGRESS — generation workflow prepared; final CI, image candidate PR, merge and Pages status require actual run verification.
