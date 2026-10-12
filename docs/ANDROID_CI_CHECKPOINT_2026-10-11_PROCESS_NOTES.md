# Process Notes — Android CI and checkpoint repair, 2026-10-11

## Purpose
Correct source/documentation drift after 0.5 image integration and remove a reproducible Android CI setup failure without modifying distribution signing, app behavior or the stable update feed.

## Inputs
- Main source commit `27da9d70625117e22a7a6c1ff1fc668a0997c667`.
- GitHub Actions Android run `38180270926`, job `114591149520` and decoded job logs.
- Current `.github/workflows/build-android.yml`, `android-app/app/build.gradle`, `PROJECT_STATE.md`, `HANDOFF.md`, `docs/APP_UPDATES.md`, `docs/IMAGE_CAMPAIGN_STATUS.md`, `docs/IMAGE_INTEGRATION_PROCESS_NOTES.md`, original image-campaign plan, repository image reconciliation manifest.
- Upstream `android-actions/setup-android@v3` action metadata; its default `packages` value is `tools platform-tools`.

## Step notes
- Step 1: verified public remote main head agrees with the October 11 handoff; repository GitHub connection permits branch/file writes.
- Step 2: inspected the failed Android job. `android-actions/setup-android@v3` accepted SDK licenses, then invoked `sdkmanager tools`; the command returned `Warning: Failed to find package 'tools'` and exit code 1, before Gradle and application compilation.
- Step 3: confined remediation to supplying `packages: 'platform-tools'` explicitly on the existing setup action. The existing explicit `sdkmanager 'platforms;android-35' 'build-tools;35.0.0'` step and signature/alignment checks remain.
- Step 4: updated existing canonical project-state/handoff, image status and updater instructions to distinguish 0.5 implementation from obsolete 0.4 instructions; historic feature requirements remain traceable.
- Step 5: PR #18 completed the retest. GitHub Android CI run `38196938500` at `8ff855ae371197fbc5e8559ecf8c829ff56b3950` passed setup, runtime staging, Android SDK platform installation, Gradle debug compilation, APK signing and zip alignment checks, and artifact upload. Web validation `38196938531`, Trash audit `38196938504` and cloud validation `38196938503` all passed.

## Exceptions / failures
The setup failure and successful repair are both verified from GitHub run outcomes. The CI debug APK is not the separately signed distribution artifact. No phone has been controlled or tested from this chat. Latest Library listing did not surface the October 11 signed APK/database ZIP; existence of artifact IDs in the handoff is not proof of current byte access. Private key archive was not accessed. No claim of legal clearance or human era approval is made for Washington samples.

## Outputs
Updated `.github/workflows/build-android.yml`, `PROJECT_STATE.md`, `HANDOFF.md`, `docs/IMAGE_CAMPAIGN_STATUS.md`, `docs/APP_UPDATES.md` on maintenance branch. Maintenance PR #18 and a completed green Android debug APK workflow (artifact ID `11724156028`, not distribution signed).

## Rights / privacy notes
No additional plate imagery, personal records, distribution keys, passwords or private source evidence was added. Existing public image samples remain under user-directed fair-use rationale without legal/era-approval claims.

## Final recheck
GitHub PR #18 diff listed exactly six changed files. Retest at HEAD `8ff855ae371197fbc5e8559ecf8c829ff56b3950` completed Android job successfully, including all signature/alignment steps and artifact upload. All four workflow runs succeeded. Merge and post-merge main SHA remain separate release-control verification tasks. The restored Android CI does not validate physical installation or the distinct distribution identity.

## Completion status
COMPLETE_WITH_EXCEPTIONS — source correction and CI verification completed; PR merge/post-merge main confirmation and external device acceptance remain outstanding.
