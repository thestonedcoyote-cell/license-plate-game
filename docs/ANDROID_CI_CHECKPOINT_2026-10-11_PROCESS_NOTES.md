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
- Step 5: opened a maintenance branch for PR checks, not a stable release. CI verdict to be filled after the PR job result is observed.

## Exceptions / failures
The setup failure is verified from the log; the proposed remedy is not yet verified by a new GitHub runner. The CI debug APK is not the separately signed distribution artifact. No phone has been controlled or tested from this chat. Latest Library listing did not surface the October 11 signed APK/database ZIP; existence of artifact IDs in the handoff is not proof of current byte access. Private key archive was not accessed. No claim of legal clearance or human era approval is made for Washington samples.

## Outputs
Updated `.github/workflows/build-android.yml`, `PROJECT_STATE.md`, `HANDOFF.md`, `docs/IMAGE_CAMPAIGN_STATUS.md`, `docs/APP_UPDATES.md` on maintenance branch. One maintenance PR/check receipt to follow.

## Rights / privacy notes
No additional plate imagery, personal records, distribution keys, passwords or private source evidence was added. Existing public image samples remain under user-directed fair-use rationale without legal/era-approval claims.

## Final recheck
Workflow contents, branch HEAD, PR workflow result and changed-file list must be independently re-read after CI. Do not mark the failure resolved until the observed workflow no longer fails at the obsolete `tools` package installation. Continue P1 independently if CI remains externally blocked.

## Completion status
INCOMPLETE — source patch and documentation prepared; new CI observation and final recheck pending.
