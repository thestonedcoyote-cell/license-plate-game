# Take Out the Trash Audit — 2026-09-07

## Purpose
First full cleanup after the screenshot exposed multiple generations of UI code executing simultaneously.

## Inputs
Current `main` runtime, versioned CSS/JS patches, service-worker cache, Pages validators, paper/map assets and release workflows.

## Step notes
- Step 1: Found the loader executing successive v10, v11, v12, v12.1, v13 and v13.0.x UI layers.
- Step 2: Found the static HTML still directly loading an older v8 patch.
- Step 3: Found multiple version-specific validation workflows that were testing obsolete implementation details instead of the current runtime.
- Step 4: Found superseded fake-map assets from v12 still present after the switch to the live regional map.
- Step 5: Collapsed presentation behavior into `ui-current.js` and `ui-current.css`.
- Step 6: Created a single runtime manifest shared by Pages and Android packaging.
- Step 7: Removed obsolete versioned UI layers, old version-specific validators and superseded map assets from the working tree.
- Step 8: Added an automated Trash audit that blocks future releases if those classes of debris return.
- Step 9: Added a native Android packaging project and build workflow using the same runtime manifest.

## Exceptions / failures
Historical process notes remain in `docs/` because they are documentation, not executable runtime. Git history remains the authoritative implementation history.

## Outputs
One current presentation layer, one active runtime manifest, generic release validation, automated Trash gate and Android packaging path.

## Rights / privacy / safety notes
No user data or credentials are introduced by this cleanup. Android packaging uses the same privacy model as the web app.

## Final recheck
Run `python tools/take_out_trash.py --strict`, build the runtime, validate JavaScript syntax, build the web release, then build the Android debug APK. Do not merge if any of those fail.

## Completion status
INCOMPLETE
