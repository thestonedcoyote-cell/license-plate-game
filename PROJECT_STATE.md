# License Plate Game checkpoint
Current candidate: 0.4.0-alpha, Android versionCode 4. Read HANDOFF.md first for implemented features, tests, recovery and remaining release gates. Historical requirements below remain for traceability.

Implemented: compact radio color tuners; example plate and thumbnail matches; SLR camera styling; large photo-print reference; non-destructive crop, zoom and pan; restored Mile markers; offline atlas fallback. Native updater and camera lifecycle fixes are included.

Read docs/RELEASE_0_3_PROCESS_NOTES.md for checks and limitations, docs/APP_UPDATES.md for release steps. The signed candidate was prepared and delivered separately; its hash is in the notes. Do not publish the prospective metadata alone. Install over scrapbook 0.2 without uninstalling to check upgrade persistence, real permissions, camera capture and pinch/crop on the phone. After acceptance publish APK and update.json together. Earlier APKs need this manual install to gain updater support; subsequent updates still require Android installation consent.

Build with tools/build_android_local.py using Android 35 android.jar, official Android tools and the privately preserved distribution key. Never commit the key. Browser regression is tests/release-ui.cjs, lifecycle regression tests/camera-lifecycle.cjs. Strict trash audit and process-note checker are release gates.

The full plate-image acquisition, reconstruction and verification campaign is specified in `docs/PLATE_IMAGE_CAMPAIGN_PLAN.md`. It audits all 1,138 designs, including the existing 291 public references, and contains the copyable heavy-resource execution prompt. Human side-by-side review is the final substantive image gate and will use a Find the Differences interface with synchronized zoom/pan, split/overlay/flicker comparison, clickable discrepancy regions and automatic correction tickets.

## Next update requirements

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
