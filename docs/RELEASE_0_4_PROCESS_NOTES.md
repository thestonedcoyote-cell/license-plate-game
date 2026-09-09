# Process Notes — 0.4 candidate

## Purpose
Apply queued usability notes, test phone layouts, clean release paths, publish a signed candidate and prepare continuation.

## Inputs
Prior 0.3 source, PROJECT_STATE.md, APP_UPDATES.md, Trash protocol, image campaign plan and saved signed 0.4 APK.

## Step notes
- Step 1: implemented the features listed in HANDOFF.md. Earlier session passed 28 viewport/theme cases and notebook/collection/synthetic camera/crop flows.
- Step 2: corrected compact Home overflow, inactive landscape screen display and nine-pixel guide offset during those tests.
- Step 3: after workspace rollback, recovered exact web source from the saved APK and restored native chooser/build changes. Earlier raw test logs were lost; do not represent them as retained artifacts.
- Step 4: recheck runtime packaging, syntax, camera lifecycle, strict Trash audit and native build before publishing. Exclude unrelated font-license line-ending changes.

## Exceptions / failures
Browser simulation does not establish physical Android or iOS compatibility. Device installation, real camera/picker, account flows and update persistence remain unverified. Stable/latest is held pending physical acceptance. Image campaign and difference-review tool remain planned. Compressed legacy core still contains duplication.

## Outputs
Signed 0.4 candidate, exact recovered web source, restored native source, phone test, prospective update metadata and HANDOFF.md.

## Final recheck
Verified candidate recovery and checked source packaging against its assets. Fresh recovery recheck: 28/28 viewport/theme cases pass, notebook save/reload passes, camera lifecycle passes, syntax and strict Trash audit pass, native compile/signature/alignment and 34 packaged assets pass. Fresh matrix evidence is docs/PHONE_STUDIO_0_4.json. GitHub main source push, Pages deployment, app validation and Trash workflow succeeded. Final native chooser correction supports JSON backup imports as well as images; native compile/signature/alignment rechecked after that correction. Physical gate remains separate.

## Completion status
COMPLETE_WITH_EXCEPTIONS: candidate features complete; stable updater rollout, physical checks and broader image work remain outstanding.
