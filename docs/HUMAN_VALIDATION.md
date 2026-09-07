# Human Show-and-Tell Validation

Human reviewers should spend their time on judgment, not catalog mechanics.

## Standard review screen

Each item should show:

- the proposed canonical plate name;
- the proposed image/reconstruction;
- when useful, the authoritative production-reference image beside it;
- source/provenance summary;
- machine confidence/match score when available;
- three large decisions: **Looks right**, **Wrong / needs correction**, **Unsure**;
- an optional note field.

The reviewer should not have to rename files, find official pages, edit database IDs, or understand the ingestion pipeline.

## Review types

### Mapping validation
Question: **Does this image belong to this plate name?**

Use this after automatic PDF position/name matching.

### Reconstruction validation
Question: **Is the independently reconstructed reference image visually accurate enough to identify the real plate?**

Show reconstruction and production reference side-by-side. Reviewers should flag meaningful differences in background, text color, major layout, slogan, motif, logo position, or overall recognizability. Tiny anti-counterfeit/security differences are expected and should not be recreated.

### Visual-tag validation
Question: **Do these coarse attributes match the plate?**

Useful attributes: background color, text color, motif, broad visual style, readable slogan/words.

## Notes requirement

A reviewer note is optional for **Looks right** but expected for **Wrong**. The review tool must always preserve the decision, reviewer/session identifier if supplied, timestamp, plate UID, source/reference identifier, and any written note.

## Completion rule

A review batch is complete only after:

1. every item has a decision or is explicitly marked unresolved;
2. exported review data has been generated;
3. counts of correct / wrong / unsure reconcile to total reviewed items;
4. notes for wrong items are present where possible;
5. a final recheck confirms no items silently disappeared from the queue.

## Privacy / rights

Production reference art used for internal validation should remain in private/local review packages unless separately cleared for public redistribution. A self-contained local HTML review package is preferred because it can show reference images without publishing them on the app website.
