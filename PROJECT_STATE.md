# License Plate Game checkpoint
Next candidate: 0.3.0-alpha, Android versionCode 3, on release/0.3.0-prep. Main remains the prior scrapbook release.

Implemented: compact radio color tuners; example plate and thumbnail matches; SLR camera styling; large photo-print reference; non-destructive crop, zoom and pan; restored Mile markers; offline atlas fallback. Native updater and camera lifecycle fixes are included.

Read docs/RELEASE_0_3_PROCESS_NOTES.md for checks and limitations, docs/APP_UPDATES.md for release steps. The signed candidate was prepared and delivered separately; its hash is in the notes. Do not publish the prospective metadata alone. Install over scrapbook 0.2 without uninstalling to check upgrade persistence, real permissions, camera capture and pinch/crop on the phone. After acceptance publish APK and update.json together. Earlier APKs need this manual install to gain updater support; subsequent updates still require Android installation consent.

Build with tools/build_android_local.py using Android 35 android.jar, official Android tools and the privately preserved distribution key. Never commit the key. Browser regression is tests/release-ui.cjs, lifecycle regression tests/camera-lifecycle.cjs. Strict trash audit and process-note checker are release gates.

The full plate-image acquisition, reconstruction and verification campaign is specified in `docs/PLATE_IMAGE_CAMPAIGN_PLAN.md`. It audits all 1,138 designs, including the existing 291 public references, and contains the copyable heavy-resource execution prompt.

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
