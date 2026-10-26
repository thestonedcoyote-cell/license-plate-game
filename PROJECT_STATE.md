# License Plate Game — current project checkpoint

**Recovery starting baseline:** `main` at `27da9d70625117e22a7a6c1ff1fc668a0997c667` (October 11, 2026). This is the input revision, not necessarily the present head after maintenance. Refresh remote main before any further work.

**Android candidate:** 0.5.0-alpha, versionCode **5**, minSdk **26**, package `com.thelostharbor.licenseplategame` (verified in `android-app/app/build.gradle`). The October 11 handoff records a separately signed APK, SHA-256 `aa9913f743bd9df1d4d407bb89a0264dfb75cd79f954d7bd09521f196c99d41b`, signing-certificate SHA-256 `6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b`. Physical install and upgrade acceptance remain **unverified**. No stable/latest release exists; `docs/RELEASE_0_5_UPDATE.json` is prospective metadata only.

**Implemented in source:** vintage lined/glass-covered color tuners; responsive Home with no sliver scroll; centered faint SLR focusing guide; large reference photo with crop/zoom/pan; repeat-sighting counts/history; Mile Markers; editable Road Trip Notebook including photos; first-run offline/account choices and tutorial; camera lifecycle/file picker; native update checks and installer flow. These browser/source claims are not physical Android acceptance. Friendly notebook plate picker, export/backup and end-to-end account service verification remain open.

**Catalog/image status (verified October 26, 2026):** **370 / 1,138** immutable catalog UIDs have official source-matched design examples: **54 WA, 19 OR, 41 AK, 35 MS, 157 TX, 33 CA and 31 WI**. The runtime contains **740** source-linked display/thumbnail JPEGs (offline cache updated); **768** canonical designs remain without matching source images. Previous simplified schematic counts remain a separate metric. All image selections retain `match_status=source_matched`, `era_status=unverified`, `human_approval=false`; issuing-agency provenance is not a redistribution license, nor is the owner's project fair-use rationale an adjudicated legal conclusion. Three report research candidates remain outside the 1,138 catalog. TX image PR #28 merged as `f39bc461f0407e978fb76bda8cac8dca9959a84e`; CA/WI image PR #32 merged as `f08d21b604ccb2bf00336dfd07cc591a0ed1307e` and GitHub Pages run `40394284189` **passed**. Exact source/derivative hashes and exclusions are in `database/image-reconciliation-tx-20261026.json` and `database/image-reconciliation-ca-wi-20261026.json`. Private source archive `LPG_official_harvest_CA_NV_WI_IN_2026-10-26.zip` is Library `libfile_01707d71188c819192f9c43b2b535279`, SHA-256 `9ff45ee8c88571dba1a14f1ea6f817adc7ea03f119d9739b59d87656d2e97e30`. **Current portable runtime snapshot:** `LPG_Reference_Image_Snapshot_2026_10_26.zip`, Library `libfile_91645e0e5f8c81919a51f66fe86c79df`, SHA-256 `cc32ee6cf15250b75babea868cdf9749ec2a00921ef0fa5706196c817a28b251`. GitHub packaging run `40407467478` passed ZIP and SQLite validations: 1,138 catalog IDs, 370 app selections, 740 published display/thumbnail copies, 101 jurisdiction registry rows, 7 source URL records; 369 unique display-content asset hashes (one byte-identical shared image pair), 738 content-addressed derivatives, and 740 UID-specific runtime image file records; SQLite integrity and foreign keys PASS. Shared-byte pair `LPG-US-TX-00013`/`LPG-US-TX-00029` remains flagged for review. This ZIP contains public runtime image derivatives, **not** private original source images. The earlier 149-image research archive Library `libfile_e9eea656eb5081918bc7eeb3e0c56278` remains preserved separately with research-only candidates. Signed stable Android release and physical upgrade remain unverified.

**CI:** Android workflow run `38180270926` failed before compilation: the setup-android default package list requested retired SDK package `tools`, resulting in `Warning: Failed to find package 'tools'`. The P0 maintenance workflow supplies only `platform-tools` and retains explicit platform 35/build-tools 35 installation. Pull-request Android CI **passed** on run `38196938500` at commit `8ff855ae371197fbc5e8559ecf8c829ff56b3950`, including compilation, signature/alignment verification and debug APK artifact upload; app validation `38196938531`, Trash audit `38196938504` and cloud validation `38196938503` also passed. These checks do not prove Android physical install, updater acceptance, or distribution signing. Original source baseline passed web validation, Trash audit and GitHub Pages deployment per prior run records; none constitutes Android install acceptance.

**Immediate priority:** P1 continue image capture/matching for **768** unmatched canonical designs. Recover Florida's official illustrated brochure (original 2026 source returned HTTP 403, alternative official 10/2025 illustrated PDF lead exists); inspect/match Nevada's 115 acquired gallery assets with missing alt text, Indiana's two image assets, unresolved historic/current variants in TX/CA/WI, and expand government sources for the 32/58 catalog jurisdictions without leads. Reuse exact-UID and source-SHA review gates. P2 create a refreshed portable SQLite/image archive representing all 370 selections, then test stable-signature, in-place Android update and saved-user-data preservation before publishing a latest APK. P3 implement Find the Differences/human-review audit. P0 Android CI has passed; a successful debug APK job is not physical upgrade acceptance. No user approval/era/rights acceptance is claimed.

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
