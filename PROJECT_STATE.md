# License Plate Game — current project checkpoint

**Recovery starting baseline:** `main` at `27da9d70625117e22a7a6c1ff1fc668a0997c667` (October 11, 2026). This is the input revision, not necessarily the present head after maintenance. Refresh remote main before any further work.

**Android candidate:** 0.5.0-alpha, versionCode **5**, minSdk **26**, package `com.thelostharbor.licenseplategame` (verified in `android-app/app/build.gradle`). The October 11 handoff records a separately signed APK, SHA-256 `aa9913f743bd9df1d4d407bb89a0264dfb75cd79f954d7bd09521f196c99d41b`, signing-certificate SHA-256 `6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b`. Physical install and upgrade acceptance remain **unverified**. No stable/latest release exists; `docs/RELEASE_0_5_UPDATE.json` is prospective metadata only.

**Implemented in source:** vintage lined/glass-covered color tuners; responsive Home with no sliver scroll; centered faint SLR focusing guide; large reference photo with crop/zoom/pan; repeat-sighting counts/history; Mile Markers; editable Road Trip Notebook including photos; first-run offline/account choices and tutorial; camera lifecycle/file picker; native update checks and installer flow. These browser/source claims are not physical Android acceptance. Friendly notebook plate picker, export/backup and end-to-end account service verification remain open.

**Catalog/image status (October 11 continuing checkpoint):** 1,138 immutable runtime UIDs. **149** official source-matched examples displayed across Identify, catalog and collection: 54 Washington + 19 Oregon + 41 Alaska + 35 Mississippi, with **298 JPEG derivatives** in the web/offline runtime. **989** canonical designs still lack acquired matching images. All 149 are `source_matched`, **not** human-approved or universally verified for issue era, and government attribution is not a license. The owner directed a project fair-use rationale, not a legal finding. Three separate report candidates remain outside runtime. The original 291 schematic / 847 unschematized split measures a different category. Current portable database `LPG_Image_Database_2026-10-12_Batch02.zip`, Library ID `libfile_e9eea656eb5081918bc7eeb3e0c56278`, SHA-256 `112cf8aa65ec79662d0c0a282eb5bd31cbfac58dbb1ed79c201089e944293c34` (SQLite integrity, foreign keys, 570 archived file hashes verified). Earlier 73-image database remains preserved separately for comparison. Official Oregon source archive `LPG_OR_Official_Harvest_2026-10-11.zip`, Library ID `libfile_1c9a2771f7308191b85009db82c688da`. Oregon batch PR #21 merged as `af64fe5dde48af0c663ad6aa180d3592108d6f2b`; Alaska/Mississippi 76-image PR #24 merged as `2f1036ef16954ef93bff028c726648cd73f14254`; Pages deployment run `38201004819` PASSED. This is web source/deployment evidence, not native APK upgrade. Read `docs/IMAGE_OR_INTEGRATION_PROCESS_NOTES.md`, `database/image-reconciliation-or-20261011.json`, `docs/IMAGE_CAMPAIGN_STATUS.md`.

**CI:** Android workflow run `38180270926` failed before compilation: the setup-android default package list requested retired SDK package `tools`, resulting in `Warning: Failed to find package 'tools'`. The P0 maintenance workflow supplies only `platform-tools` and retains explicit platform 35/build-tools 35 installation. Pull-request Android CI **passed** on run `38196938500` at commit `8ff855ae371197fbc5e8559ecf8c829ff56b3950`, including compilation, signature/alignment verification and debug APK artifact upload; app validation `38196938531`, Trash audit `38196938504` and cloud validation `38196938503` also passed. These checks do not prove Android physical install, updater acceptance, or distribution signing. Original source baseline passed web validation, Trash audit and GitHub Pages deployment per prior run records; none constitutes Android install acceptance.

**Immediate priority:** P1 source batch `38200139649` finished `COMPLETE_WITH_EXCEPTIONS`: Texas 48-page illustrated official PDF downloaded (209 extracted page/image records), Alaska and Mississippi official galleries downloaded (48 and 307 image assets), Florida illustrated PDF returned HTTP 403. The 76 AK/MS reviewed samples are integrated; next map Texas design pages against its 164 catalog UIDs, obtain alternate official Florida brochure/individual plate images for 132 IDs, and acquire sources for remaining 32 uncovered jurisdictions. Official leads now cover 26/58 jurisdictions, not image completion. P2 real signed Android upgrade/camera/file-picker/updater acceptance and stable update feed; P3 Find the Differences reviewer; P4 bounded app backlog. P0 Android CI repair is complete and verified. Read `docs/CURRENT_IMAGE_CAMPAIGN_QUEUE.md`. Private batch evidence Library `libfile_745e40877fcc8191a3476a2c1bbe2313`.  Do not recommend uninstall to test upgrades; local collection/notebook data may be lost. CI debug signing is not the distribution signing key.

The original product requests below are retained as historical acceptance criteria, not outstanding development work merely because their imperative wording survives. See `HANDOFF.md` for historical implementation details and `docs/APP_UPDATES.md` for the current release mechanism.

## Historical 0.4 requirements (implemented in source; native acceptance outstanding)

### Color tuner redesign

- The current horizontal color tuners look too modern for the road atlas, scrapbook and vintage camera aesthetic.
- Make the controls somewhat larger for easier phone use.
- Present each lined color scale behind a clear glass cover, with period appropriate framing, reflections and wear. Preserve strong color readability in both day and night themes.
- Keep the three controls compact enough that the reference photo, example plate and first results remain useful on a phone screen.
- Preserve direct dragging, accessible labels and the existing matching behavior while changing the visual hardware.

### Road Trip Notebook

- Turn the `Road trip notebook.` title card into an obvious interactive entry point.
- Opening it should show a real notebook or scrapbook for recording unrelated road trip adventures, not just license plate finds.
- An entry should support a date, optional title and location, freeform story or notes, and attached photos styled as Polaroid or 35 mm prints.
- Save entries locally, allow them to be reopened and edited, and present the collection as browsable notebook pages in the established road atlas and scrapbook style.
- License plate sightings may be linked to an entry when useful, but the notebook must also work for any roadside event, stop, discovery or memory.
- Include empty-state guidance and protect saved entries across ordinary app updates.

### Home viewport fit

- The Home screen must fit within the available phone viewport without vertical scrolling. The current few-pixel scroll that reveals only a sliver is a defect.
- Resize and rebalance the title card, action cards, quick-identify area, progress area, gaps and decorative copy as a coordinated layout. Do not merely hide overflow while clipping controls.
- Use responsive height breakpoints so shorter phones reduce decoration and spacing before shrinking tap targets or essential text.
- Acceptance test at representative 360×640, 360×740 and 412×844 CSS-pixel viewports: `scrollHeight <= clientHeight`, bottom navigation remains visible, and every interactive control remains reachable.

### Vintage 35 mm SLR viewfinder

- Replace the current circle-and-line overlay. It reads like a modern phone-camera focus indicator.
- Use a faint rectangular 35 mm focusing-screen overlay centered over the live image, with restrained period details such as a central split-image rangefinder, microprism collar, corner crop marks and a subtle exposure-meter edge.
- Center the plate capture rectangle geometrically within the usable live-image area. The focusing screen may overlap it and should sit above it visually because both are faint guides.
- Keep the live camera image dominant. The overlay must remain visible in bright and dark scenes without obscuring a plate.
- Hide the live focusing overlay from saved photos and the post-capture preview.

### Collection counts and repeat sightings

- Every plate result and collection card must show whether that design has already been collected and the total number of sightings.
- Render the count as pencil-scratched notation on the paper card, such as `found ×3`, rather than as a modern badge.
- A first collection changes the card to collected with count 1. Each later collection increments the count immediately instead of creating an ambiguous duplicate.
- The collection view must expose the same count and provide access to the saved sighting records/photos for that plate.
- Counts must survive restart and ordinary app updates and reconcile with the underlying sightings, rather than being maintained as a separate drifting total.

### Mile Markers achievement system

- Present Mile Markers as an obvious achievement system, not a small text link tucked into a status strip.
- Add a prominent Home entry styled as a stamped travel-passport or roadside milestone card showing unlocked/total progress and the next nearby goal.
- Keep Mile Markers available from More as a secondary route.
- The Mile Markers screen should clearly separate earned and locked achievements, show progress toward incomplete markers, and explain what each one recognizes.
- When a marker unlocks, show a brief scrapbook-style celebration with a direct `View Mile Markers` action. Do not interrupt camera capture.

### First-run welcome, account choice and tutorial

- On first launch, show a welcome flow with clear `Sign in`, `Create account`, and `Continue without account` choices. Local play must remain fully usable without an account.
- Explain in one sentence what signing in adds, particularly backup/sync, without presenting it as required.
- Follow with a short, skippable tutorial covering the fast Camera/Identify choice, collecting and repeat-sighting counts, Mile Markers, and the Road Trip Notebook.
- Keep the tutorial visual and brief, with progress and Back/Next/Skip controls. Do not request camera or location permission until the person invokes the related feature.
- Record completion locally, avoid showing the flow again after app updates, and provide `Account` and `Replay tutorial` from More.
- If account service is unavailable, the offline option must remain immediate and the welcome flow must not trap the user.
