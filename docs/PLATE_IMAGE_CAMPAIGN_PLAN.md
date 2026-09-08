# Plate Image Accuracy Campaign

## Objective

Produce the most visually accurate, legally defensible, screen-oriented reference available for every one of the 1,138 cataloged plate designs. Audit the existing 291 public references as well as the 847 designs without public reference art.

The campaign must track three independent facts for every design:

1. **Identity established** — the source image and catalog record refer to the same plate design and era.
2. **Visual accuracy verified** — the public reference preserves the features a person needs to recognize the plate.
3. **Public use decided** — the exact source asset or reconstructed result has an explicit use classification.

No status implies either of the other two.

## Definition of complete

The campaign is complete when:

- all 1,138 immutable plate UIDs have one manifest row;
- every row has a current disposition: verified public image, verified reconstruction, safe abstraction, permission/legal review, source unresolved, or catalog correction required;
- every visual claim is tied to retained source evidence;
- every public image has passed mapping, visual, rights, and credential-safety gates;
- every unresolved item records sources attempted and the next useful action;
- totals reconcile to 1,138 with no duplicate or silently dropped UID;
- the app, research view, and identification metadata use the same approved UID mapping.

Completion does not require pretending that an uncertain plate is solved. A documented unresolved result is valid; an unsupported approximation is not.

## Canonical record for each plate

Create one `plate-image-record.json` entry per UID with:

- UID, jurisdiction, canonical name, category, issue years and active/retired state;
- aliases and official source terminology;
- plate dimensions/aspect family;
- source-page URLs, direct-asset URLs, retrieval date, archive/hash, source authority and source type;
- source image dimensions, crop bounds and whether it is a sample, photograph, brochure render or production diagram;
- background and lettering colors, preferably sampled in CIELAB plus display sRGB/hex;
- border, bands, gradients, serial position, jurisdiction text, slogans and other readable text;
- motif description, placement and visual weight;
- logo, seal, sponsor, character, university/team and other protected-mark flags;
- reconstruction spec and renderer version;
- identity confidence, visual confidence, human decision and notes;
- public-use class A/B/C/D and credential-safety decision;
- final public asset path or explicit unresolved reason.

Store raw official/reference assets in private research artifacts. Commit only cleared public assets, render specifications, citations and non-sensitive review results.

## Evidence standard

Use the strongest available evidence in this order:

1. issuing-agency statute, regulation, adopted plate specification or manufacturing drawing;
2. current issuing-agency plate manual, brochure, order page or official gallery;
3. issuing-agency archived page or official press release tied to a date;
4. authorized sponsor or rights-holder page linked by the issuing agency;
5. two or more independent real-world photographs that agree on the design and era;
6. specialist collector/archive material used only when stronger evidence is unavailable and marked accordingly.

For a **verified** identity, require one authoritative official source or two independent agreeing secondary references. Search-result thumbnails, auction listings and unsourced social posts may locate leads but cannot establish a final mapping alone.

Record design years carefully. A plate name reused for a redesign is a separate visual version and must not overwrite the earlier UID or inherit its image.

## Public image decision

Choose the first viable route for each design:

1. **Cleared exact asset** — use an official or authorized image only when terms, license, permission or source-specific review supports it.
2. **High-fidelity independent reconstruction** — reconstruct factual layout, colors and text from specifications; use the production image only for comparison.
3. **Reconstruction with cleared/separable mark** — reconstruct the base and use a cleared mark, or replace the protected element with a labeled neutral indicator.
4. **Identification abstraction** — preserve the distinctive palette, layout, words and broad motif while avoiding protected creative expression.
5. **Private reference only** — show no exact public art until permission or review resolves it.

All public assets use a fictitious serial, omit current stickers and security features, remain screen sized, and carry the existing reference/non-endorsement treatment.

## Execution phases

### Phase 0 — Freeze and audit the catalog

- Decode the five canonical catalog chunks and export a working manifest of all 1,138 UIDs.
- Reconcile duplicate names, aliases, reused designs, issue years and retired-but-still-seen variants.
- Reconcile the 291 existing render UIDs against the manifest.
- Assign every row an initial status and jurisdiction batch.
- Produce a baseline dashboard whose totals equal 1,138.

Gate: no harvesting begins until every catalog UID appears exactly once in the baseline.

### Phase 1 — Build the official-source registry

- Expand `data/harvest_sources.csv` to cover every jurisdiction represented in the catalog.
- Record current gallery/manual, archived official material, technical/specification sources, sponsor pages and known access barriers.
- Prioritize high-yield official sources already identified: Oregon, California, Nevada, Texas, Florida, Minnesota, Wisconsin, Nebraska, Indiana, Alabama, Connecticut, West Virginia and Oklahoma. Refresh broken or blocked Idaho, Massachusetts and New Hampshire sources.
- Assign source freshness, expected plate count, historical coverage, access difficulty and extraction method.

Gate: every jurisdiction has an official source or a documented official-source failure and fallback search path.

### Phase 2 — Harvest private evidence

- Run jurisdiction-sized harvests from reviewed source pages; do not perform uncontrolled web crawling.
- Preserve source HTML/PDF, extracted text, page renders, embedded images, direct images, retrieval metadata and SHA-256 hashes.
- Deduplicate exact and near-duplicate assets while retaining every source relationship.
- Render difficult PDFs at sufficient resolution for text and motif inspection.
- Log errors, redirects, blocks, missing pages and date ambiguity.

Gate: each acquired asset is reproducible from its manifest record and hash. Acquired evidence remains private by default.

### Phase 3 — Map evidence to plate UIDs

- Generate candidate mappings from official names, alt text, nearby page text, OCR, issue years, jurisdiction and catalog aliases.
- Use image similarity only to group candidates, never as the sole identity proof.
- Assign confidence: high, medium, low or conflict.
- Send medium, low and conflicting mappings to the review queue.
- Detect official designs absent from the catalog and catalog entries absent from official sources; route these to catalog review rather than silently adding or deleting records.

Gate: high-confidence mappings have authoritative support; every other mapping is explicitly queued or unresolved.

### Phase 4 — Extract visual specifications

- Normalize geometry, broad color regions, text, border, bands, serial field, slogan, motifs and mark placement.
- Sample colors from several clean areas, discounting compression, glare, plate reflectivity and photography white balance. Record ranges where official examples disagree.
- Separate factual structure from protected expressive artwork.
- Compare multiple examples for active plates to distinguish design from lighting, frames, stickers and vehicle reflections.
- Preserve a structured spec rather than a prose-only description.

Gate: a reconstruction cannot begin until its minimum recognition features and uncertain elements are identified.

### Phase 5 — Produce candidate public references

- Upgrade the renderer to support accurate gradients, image masks, landscape layers, side graphics, emblems, typographic zones and plate aspect families.
- Render at a controlled master size, then generate the small in-app thumbnail and enlarged research view.
- Keep source art and renderer output separate so a renderer update can regenerate all derivatives.
- Rebuild the existing 291 from their evidence records when the new spec is more accurate.
- Use explicit placeholders or safe abstractions for uncleared marks; never let a missing protected element appear to be verified.

Gate: asset schema, fictitious serial, safety treatment, dimensions and UID filename must validate automatically.

### Phase 6 — Two-stage visual review

Stage A is a mechanical comparison: plate name, UID, years, aspect, dominant colors, text, layout, required elements and source freshness.

Stage B is a human side-by-side review showing the candidate beside the best authoritative production reference. The decision is **Looks right**, **Wrong / needs correction**, **Unsure**, or **Legal review needed**. Wrong decisions require a note when possible.

High-complexity scenic, character, tribal, university, sports, sponsor and cause plates require a second review pass after correction. Minimal standard plates may pass with one authoritative source and one human review.

Gate: every public candidate has a recorded human decision; no bulk “approve all” action is accepted.

### Phase 7 — Rights and safety review

- Apply public-use classes A/B/C/D per element and per final asset.
- Keep exact-thumbnail fair-use analysis source-specific and outside automated approval.
- Check protected art, logos, seals, marks, sponsor terms and implied endorsement separately.
- Confirm fictitious serial, absence of security/validation details, screen-oriented resolution and reference labeling.

Gate: only `public_use=approved` and `credential_safety=approved` assets enter the public manifest.

### Phase 8 — Integration and reconciliation

- Generate the UID-to-asset manifest and visual-filter metadata from approved records.
- Run catalog membership, duplicate UID, orphan asset, missing asset, source citation and cache/runtime checks.
- Test thumbnails and enlarged views in day/night themes and on phone/desktop layouts.
- Produce final counts by disposition, jurisdiction, source class, confidence and review status.
- Package private evidence, public assets, review exports, process notes and a machine-readable unresolved queue separately.

Gate: all counts reconcile to 1,138 and each user-facing image resolves to the intended UID.

## Work batching

Use jurisdiction batches so official terminology, design families and source context stay together. A batch should normally contain 25–80 designs; split very large catalogs by standard, specialty, organizational and historical groups.

Within each batch, keep responsibilities separate:

- source discovery and archival;
- catalog mapping;
- visual extraction;
- rendering;
- visual review;
- rights/safety decision;
- final reconciliation.

Workers may write only their stage output. One coordinator merges stage results and maintains the canonical manifest. This prevents concurrent work from silently changing UIDs, names or statuses.

Recommended order:

1. Washington and the existing 291 references, to calibrate quality against familiar material;
2. high-yield official manuals/galleries already in the source registry;
3. remaining states/provinces with straightforward official galleries;
4. blocked, dynamic or poorly archived jurisdictions;
5. conflict, rights and historical-version queues;
6. final full-catalog recheck.

## Accuracy scoring and release rule

Use component scores to reveal weak areas rather than hide them in one average:

- identity and era: 0–3;
- geometry/layout: 0–3;
- palette: 0–3;
- wording/serial field: 0–3;
- motif recognizability: 0–3;
- source authority/freshness: 0–3;
- human verification: 0–2.

A standard verified public reference needs no zero component, identity/era 3, and human verification 2. A score does not grant rights clearance. Safe abstractions should be labeled as abstractions even when they score well for recognition.

## Campaign outputs

- canonical `plate-image-manifest.json` for all 1,138 UIDs;
- expanded official-source registry;
- private hashed evidence packages by jurisdiction;
- structured reconstruction specifications;
- versioned renderer and deterministic public derivatives;
- local side-by-side review packages and exported decisions;
- public image manifest and visual-filter metadata;
- catalog-correction queue, source-unresolved queue and rights-review queue;
- campaign dashboard and process notes with final reconciliation.

## Heavy-resource execution prompt

Use the following as the launch instruction for the dedicated campaign:

> Execute the License Plate Game Plate Image Accuracy Campaign in `docs/PLATE_IMAGE_CAMPAIGN_PLAN.md`. Work through every phase and persist checkpoints after each jurisdiction batch. Audit all 1,138 catalog UIDs, including the existing 291 references; do not treat current artwork as automatically verified. Use authoritative official evidence first, retain raw production imagery only in private research artifacts unless separately cleared, and keep identity verification, visual accuracy, public-use clearance and credential safety as independent statuses. Use parallel workers for source discovery, mapping, visual extraction and rendering, but allow only the coordinator to modify the canonical manifest. Build local side-by-side human-review packages and place uncertain, conflicting or rights-sensitive items in explicit queues. Do not invent missing plate details or silently drop records. Continue until every UID has a reconciled disposition, all approved assets pass automated and human gates, and final counts equal 1,138. Save source code and public manifests to the project repository; save private evidence and review packages only in approved private storage. Produce process notes, a final coverage dashboard, unresolved queues and a release-ready public asset bundle. Do not publish or deploy the resulting bundle until the user has reviewed the final dashboard and representative samples.

