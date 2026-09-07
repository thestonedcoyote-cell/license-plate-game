# Plate Image Reconstruction Policy

## Goal

License Plate Game needs accurate visual references without assuming that an image published by a DMV or a plate sponsor may be freely redistributed.

The preferred public-image strategy is therefore **independent reconstruction from facts and legal/technical specifications**, with production images used as reference material for human accuracy verification rather than as the source file being republished.

This is a product/research policy, not legal advice.

## Legal premise under investigation

Copyright protects original expression, not facts, systems, methods, concepts, familiar symbols, typeface, or mere variations of lettering/coloring. Government edicts such as legislation, administrative rulings, regulations, and similar official legal materials are not copyrightable. State and local government publications outside that category may still be copyrighted. Separately, logos, sponsor artwork, seals, trademarks, and other third-party elements may have copyright, trademark, statutory, or endorsement restrictions even when the plate's factual layout is public information.

Therefore, an independently created plate reference should be decomposed into source elements rather than treated as one indivisible picture.

## Reconstruction evidence ladder

Use the highest available source for each element:

1. statute or enacted legislation defining plate content;
2. administrative rule/regulation or legally adopted specification;
3. official technical/manufacturing specification;
4. official written description of required content;
5. official production/sample image used only to verify the independent rendering;
6. multiple real-world photographs used only to verify accuracy where official references are insufficient.

A production/sample image is **verification evidence**, not proof that the image file itself is redistributable.

## Per-element provenance

Every reconstructed plate should record, where applicable:

- plate UID;
- dimensions/aspect ratio source;
- background-color source;
- text-color source;
- required state/province/country wording;
- required slogans or short phrases;
- serial-layout specification;
- borders/bands/field layout;
- legally specified familiar symbols;
- creative illustration/artwork required;
- third-party logos/marks required;
- government seal/insignia required;
- source URLs and citations;
- renderer/version used;
- human verification reference(s);
- human verification status;
- public-use status;
- residual legal-risk notes.

## Public-use classes

### A — factual/spec reconstruction

Built only from uncopyrightable facts/specifications and our own rendering choices. No protected logo, sponsor art, seal, or copied illustration. Candidate for public distribution after human accuracy review.

### B — reconstruction with separable mark

Base plate can be reconstructed from facts/specifications, but one or more logos, seals, sponsor marks, or artistic elements require a separate rights determination. Publish only the cleared elements; use a neutral placeholder for uncleared elements.

### C — creative design dependence

The plate's identity depends materially on original illustration/artwork for which specifications do not define the expression. Do not publish an accurate copied/redrawn version merely because we traced or recreated it independently. Seek permission/license, find a public-domain/authorized source, or use a deliberately non-infringing identification abstraction after legal review.

### D — private/reference only

Official or real-world imagery may be stored privately as research/verification evidence but not included in the public build.

## Human verification

A human reviewer compares the generated representation with at least one authoritative production/sample image and checks:

- overall composition;
- relative placement;
- colors;
- required wording;
- motif identity;
- omissions/additions;
- whether the reconstruction accidentally copied protectable creative expression beyond what the factual/specification sources require.

The reviewer records **accurate**, **needs adjustment**, or **legal review needed**. Accuracy approval is not itself a legal clearance.

## Non-endorsement

The app should state that plate images are reference representations for identification and that License Plate Game is not affiliated with or endorsed by issuing governments, universities, sports teams, nonprofits, or plate sponsors.

## Current implementation direction

The research database and harvesting pipeline should add a reconstruction track alongside direct-image acquisition. Official images remain evidence; public artwork is selected per plate based on provenance and rights status.
