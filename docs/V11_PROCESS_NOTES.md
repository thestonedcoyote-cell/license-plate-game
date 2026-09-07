# Process Notes

## Purpose
Implement the v11 app changes requested from real Moto use: remove the faux binder-hole treatment, make the app read as ruled paper with rough kraft-paper controls, eliminate whole-screen scrolling, rebuild Identify around three color controls, add a desktop-friendly Research catalog, integrate the pending Texas clean-reference tranche, and preserve account/social foundations without faking cloud authentication.

## Inputs
- Live v10 PWA on GitHub Pages.
- User feedback from installed Moto G Power 5G (2023).
- Canonical compressed catalog: 1,138 collectible designs.
- v10 public reference-render set: 130 designs.
- Texas clean-reference tranche: 161 UID-mapped renders derived from private official-image coarse palettes and canonical metadata.
- Existing local player ID / username foundation in `v8-patch.js`.
- Existing camera/photo-to-Identify flow and local IndexedDB sighting/photo storage.

## Step notes
- Step 1: Created `v11-notebook-identify-web` from the pending Texas-render branch so the unfinished 161-image tranche is completed rather than abandoned.
- Step 2: Removed the left-side faux binder-hole visual treatment and replaced the app background with mild ruled paper plus a notebook margin line.
- Step 3: Reworked top/bottom navigation and major controls as rough-edged kraft-paper scraps using offline CSS textures, uneven clip paths, paper shadows and subtle tack/tape cues.
- Step 4: Enforced a fixed app viewport. Main screens do not scroll the document; collection, settings, achievements, Identify candidates and Research results use bounded internal scrolling areas.
- Step 5: Rebuilt Identify independently from the old dynamic question wall. The new surface uses three rotary color controls: main background, second/accent color and lettering color, plus optional text/state/motif clues.
- Step 6: Suppressed unfiltered candidate output. Until a clue is selected, Identify shows a calm instruction instead of hundreds of matches. Filtered results are capped to the best 80 and scroll only inside their result space.
- Step 7: Preserved photo-assisted identification by retaining the `pendingPhotoBanner` target used by the v10 photo flow so a captured or reopened Unidentified photo can remain visible while matching.
- Step 8: Added a Research screen built from the same catalog chunks used by the game. It supports search, place and category browsing and is accessible from Home and More; on larger screens it naturally expands into the web-companion research surface.
- Step 9: Wired the 161 Texas clean-reference render specifications into the public loader after the existing 130-render cohort, raising expected public visual references to 291 unique plate UIDs.
- Step 10: Updated the service-worker cache plan so existing installed PWAs receive v11 and the Texas render asset without reinstalling.
- Step 11: Preserved the current local profile foundation: stable player ID, mutable username and local-only social identity. Cloud password/Google authentication is not exposed as functional until a real auth/backend project exists.

## Exceptions / failures
- Cloud account login and multi-device photo sync cannot be securely completed from the current static GitHub Pages deployment without provisioning an authentication/database/storage backend. Client/data foundations are preserved; backend provider setup remains a separate deployment step rather than a fake UI control.
- Auto-identification from camera imagery is not yet implemented. The photo now has a usable manual-identification path; OCR/color/motif-assisted ranking remains a future computer-vision stage.
- Many catalog rows still lack normalized visual colors/motifs. The three color controls can only be as complete as visual metadata; image-harvest/normalization work continues.
- The 291 public reference renders are identification artwork, not production-credential replicas and not exact redistributed DMV artwork.
- Final handset verification is still required for v11 viewport fit, internal scrolling and color-dial usability on the Moto.

## Outputs
- `v11.css` — ruled-paper / kraft-paper interface and fixed viewport/internal-scroll rules.
- `v11-patch.js` — color-first Identify, Research screen and v11 app integration.
- Updated `app.js` loader — v10 + Texas render cohort + v11 UI.
- Updated `sw.js` — v11 cache and installed-PWA update path.
- Existing `data/reference-renders-tx-v10.1.js` completed as a live app input.
- This process record and cloud-sync foundation documentation.

## Rights / privacy notes
Public visual coverage uses LPG-created reference renders. The official/production reference imagery that informed visual extraction remains private research evidence unless separately cleared. Exact GPS and captured photos remain local-first in the current release. A future cloud account must make photo/location sync opt-in and protect exact coordinates by default.

## Final recheck
Before merge, verify JavaScript syntax for v8/v10/v11 patches, loader and service worker; verify the two public render files combine to exactly 291 unique UIDs; verify `v11.css`, `v11-patch.js` and the Texas render file are cached by the v11 service worker; verify whole-page scrolling is disabled outside Camera while required content wells have internal overflow; verify Identify includes three color dials and hides matches before a clue; verify Research loads from all five catalog chunks; verify photo target `pendingPhotoBanner` remains present; verify process notes pass the repository note checker; inspect the PR diff for unintended production-image binaries; merge only after GitHub Actions succeeds; then verify Pages deployment succeeds.

## Completion status
INCOMPLETE — implementation is staged on the v11 branch; automated validation, PR review, merge, live Pages publication and Moto confirmation remain.
