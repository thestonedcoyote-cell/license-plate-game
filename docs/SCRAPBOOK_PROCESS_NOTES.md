# Process Notes
## Purpose
Bring the actual app toward the user's uploaded road-trip scrapbook mockup, preserving camera and collection functions and producing a signed update to the repaired APK.
## Inputs
- Base GitHub commit d7275b8db94a1b1ddd2cd76d56c3bf2e2b5a0f4c.
- User mockup: file_000000000ae881fdad2e3e3837a3e1cd.png. Actual-app screenshot: Screenshot_20260907-163504.png.
- Original native shell and private signing key recovered in the installation-repair session.
## Step notes
- Step 1: Compared supplied images. Replaced emoji launch illustrations, corrected SVG aspect-ratio stretching and colored noise, condensed title typography, and replaced the viewport-filling home panel with a compact notebook layout.
- Step 2: Added generated vintage camera art and a bundled decorative atlas background, editable SVG plate illustrations, paper-only grayscale texture, navigation icons, and brighter named night color indicators. Real regional map tiles become visible after location is acquired; the separate functional map remains available in More.
- Step 3: Connected home color selectors to actual filters. Preserved original bound identification controls in a hidden integration container so existing capture/resolve/render handlers keep their references. Routed new navigation through the original camera lifecycle handler. Corrected result buttons to invoke the existing collection handler.
- Step 4: Browser checked day/night at 412x844 and 360x740 and desktop at 1440x1000. Home fits without scrolling at 412x844; smaller devices can scroll the home content without moving navigation. Checked all launch artwork loaded, camera receives a simulated stream, photo saves to Unidentified, Identify attaches that photo, manual collection addition works, and both counts survive reload. No page JavaScript errors were recorded.
- Step 5: Updated cache manifest and Android versionCode to 2 / versionName 0.2.0-alpha. Packaged the original compiled native shell with current web runtime using tools/repack_android.py, which uses official zipalign and apksigner. Added signature and alignment checks to the Gradle CI workflow.
## Exceptions / failures
- This is an implementation inspired closely by the supplied image, not a pixel-identical extraction. Typography, paper edges, map details, and responsive sizing differ.
- Initial browser download timed out; direct official Chrome-for-Testing download succeeded.
- Initial edited JavaScript failed syntax validation and was corrected before browser testing.
- No physical Android installation or on-device camera/GPS test was performed. Browser camera tests use a synthetic camera stream.
- The compiled native shell is reused, not freshly compiled. For native changes, use android-app and its Gradle workflow.
- GitHub CI still uses its own debug signing key. The distributed APK uses the privately saved recovery key; never distribute a CI debug APK as its update without explicitly using the same key. No automatic updater has been added.
## Rights / privacy notes
Camera and atlas illustrations were generated using the built-in image tool, with the user's mockup as the style reference. Prompts requested only a vintage SLR camera on paper and only a worn Rocky Mountain/Great Plains atlas page, respectively. The generated atlas is decorative, not a navigation aid. Other new illustrations are repository-native SVG artwork. Oswald font is distributed under the SIL Open Font License; see docs/OSWALD-LICENSE.txt, also bundled in the app. The signing key is private and is not part of the repository.
## Outputs
- Updated ui-current.js/css and existing paper SVG artwork.
- New camera-art.svg, road-plate.svg, collection-art.svg, atlas-art.svg.
- Version 2 APK signed with certificate SHA-256 6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b, same as installation-repair APK.
- Browser screenshots show rendered working app, not a generated UI mockup.
## Final recheck
Verified runtime manifest, JavaScript syntax, browser interactions, and the signed APK's v2/v3 signatures, alignment, manifest version, and packaged runtime integrity. Rechecked release audit after changes: COMPLETE. Physical device installation and user visual acceptance remain unverified.
## Completion status
COMPLETE_WITH_EXCEPTIONS
