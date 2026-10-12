# License Plate Game — current project checkpoint

**Recovery starting baseline:** `main` at `27da9d70625117e22a7a6c1ff1fc668a0997c667` (October 11, 2026). This is the input revision, not necessarily the present head after maintenance. Refresh remote main before any further work.

**Android candidate:** 0.5.0-alpha, versionCode **5**, minSdk **26**, package `com.thelostharbor.licenseplategame` (verified in `android-app/app/build.gradle`). The October 11 handoff records a separately signed APK, SHA-256 `aa9913f743bd9df1d4d407bb89a0264dfb75cd79f954d7bd09521f196c99d41b`, signing-certificate SHA-256 `6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b`. Physical install and upgrade acceptance remain **unverified**. No stable/latest release exists; `docs/RELEASE_0_5_UPDATE.json` is prospective metadata only.

**Implemented in source:** vintage lined/glass-covered color tuners; responsive Home with no sliver scroll; centered faint SLR focusing guide; large reference photo with crop/zoom/pan; repeat-sighting counts/history; Mile Markers; editable Road Trip Notebook including photos; first-run offline/account choices and tutorial; camera lifecycle/file picker; native update checks and installer flow. These browser/source claims are not physical Android acceptance. Friendly notebook plate picker, export/backup and end-to-end account service verification remain open.

**Catalog/image status:** 1,138 immutable runtime UIDs. 54 Washington designs now have selected official source-matched examples displayed in Identify, catalog and collection; 108 JPEG derivatives are offline staged. Remaining **1,084** designs lack acquired matching source images. Those 54 are `source_matched`, **not** verified for era, human-approved or licensed by the owner of the art. The owner directed fair-use project use, not a legal finding. Three unresolved report entries remain outside runtime. The original 291 schematic / 847 unschematized count is a distinct historical metric. Read `docs/IMAGE_INTEGRATION_PROCESS_NOTES.md` and `docs/IMAGE_CAMPAIGN_STATUS.md`.

**CI:** Android workflow run `38180270926` failed before compilation: the setup-android default package list requested retired SDK package `tools`, resulting in `Warning: Failed to find package 'tools'`. The P0 maintenance workflow supplies only `platform-tools` and retains explicit platform 35/build-tools 35 installation. Pull-request Android CI **passed** on run `38196938500` at commit `8ff855ae371197fbc5e8559ecf8c829ff56b3950`, including compilation, signature/alignment verification and debug APK artifact upload; app validation `38196938531`, Trash audit `38196938504` and cloud validation `38196938503` also passed. These checks do not prove Android physical install, updater acceptance, or distribution signing. Original source baseline passed web validation, Trash audit and GitHub Pages deployment per prior run records; none constitutes Android install acceptance.

**Immediate priority:** P0 current-state documentation and Android CI repair; P1 official-source acquisition and image database reconciliation (Oregon manual is an unresolved lead, not a completed harvest); P2 real Android upgrade/camera/file-picker/updater acceptance before signed stable release; P3 planned Find the Differences reviewer; P4 quality backlog. Do not recommend uninstall to test upgrades; local collection/notebook data may be lost. CI debug signing is not the distribution signing key.

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
