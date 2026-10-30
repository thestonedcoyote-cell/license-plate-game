# Process Notes — 61 Michigan and Ontario official license plate samples

## Purpose
Fill every Michigan and Ontario immutable catalog design using original issuing-agency plate sample graphics, with strict source file SHA and distinct UID matching, without claiming era, rights or human artwork approval.

## Inputs
- Official Michigan SOS standard, special-cause and legacy plate galleries from source harvest run `40993449073`; original issuing-agency URLs and image hashes in archived asset records.
- Official ServiceOntario choose licence plate graphic gallery with 75 downloaded files including 70 licensed plate illustrations and 4 logos, archived from the same run.
- Contact sheets with real visible plate samples reviewed; Michigan 22 unique catalog names, Ontario 39 unique names, including shortened image alt descriptions cross-checked to official HTML page text.
- Exact reviewed map `data/image-batches/mi-on-61-reviewed-20261029.json`, four pinned source HTML/asset-list SHA pairs.
- Prior 636 selected source images, 1,272 display/thumbnail JPGs and original 1,138 immutable catalog UIDs.

## Step notes
1. Crossmatched all 22 Michigan catalog labels to current Michigan Department of State photo samples from official galleries: 19 Michigan fundraising designs, standard Pure Michigan/Mackinac Bridge/Water-Winter Wonderland, and one legacy blue plate.
2. Crossmatched all 39 Ontario catalog labels to Ontario government's official plate graphic list and visible plate examples. The image alt text for Ontario Association of Fire Chiefs says Canadian Association of Fire Chiefs, despite the state source page listing the catalog's name; similarly the snowmobile image alt is shortened, and the Ontario Paramedic Association / Ottawa Redblacks source alt fields are blank. These source-description discrepancies are explicitly retained for later visual/legal review, not silently rewritten as definitive identity/era proof.
3. Explicitly pinned source page HTML and gallery asset registry SHA-256, selected exact indexed original image files, and validated each original against archived image SHA-256.
4. Generated 61 display/thumbnail JPEG pairs with white composition on transparency and aspect-preserving non-upscaled dimensions; no synthesized plate text or security elements.
5. The isolated generated candidate must contain exactly 697 / 1,138 selected examples, 1,394 public/offline JPGs, and every derivative SHA, leaving 441 currently unfilled UIDs.
6. New source photos require independent generated branch review and four GitHub CI checks before merging to public main.

## Exceptions / failures
Historical issue-era remains unverified; human visual approval and legal permission are not assumed. Ontario image captions and source page names have discrepancies for four designs and are flagged as unresolved evidence, not user-approved facts. Idaho official older poster PDF remains HTTP 404; 7/8 new agency source URLs retrieved. No stable signed Android v0.6 update or on-device upgrade/data persistence proof for the newer 697-image catalog.

## Outputs
`tools/integrate_michigan_ontario_gallery.py`, `data/image-batches/mi-on-61-reviewed-20261029.json`, GitHub Actions `.github/workflows/integrate-mi-on-images.yml`; upon successful trigger, 122 JPEGs, source recon JSON, service worker and browser regression generated on review branch.

## Rights / privacy notes
The raw government original research archive stays out of public Github. Official issuing-agency image origin is not independent image rights clearance, and owner fair-use use rationale is not a legal opinion. No private player data, APK signing keys or source credentials are involved.

## Final recheck
Compare the exact four gallery registry/source HTML hashes, 61 original image SHA-256 values, all 122 new derivatives, immutable UID membership/names, 697 manifest records, 1,394 JPEGs, source/era/human flag correctness, four PR checks and Pages deployment after merge. Only count 697 once the image PR is merged.

## Completion status
IN_PROGRESS — pinned mapping/generator prepared, generated image PR and CI pending.
