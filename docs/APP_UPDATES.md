# App update delivery

Included in the 0.3 and 0.4 native candidates. Stable/latest publication still requires the physical upgrade checks below.

## Player flow
The native wrapper checks GitHub's latest stable release on launch, at most once per day after a successful check. More → Check for updates always checks immediately. A dismissed release is not automatically offered again, but remains available from the manual check. Offline checks are quiet unless requested manually.

The player chooses Download. Android DownloadManager downloads in the background, and the download ID and metadata survive app restarts. Failed downloads can be retried. Before offering Install, the app verifies SHA-256, application ID, increasing versionCode, supported Android version, and exact equality with the installed signing certificate set. Android still performs its own APK verification and asks the player to confirm installation. If necessary, the app opens Android's per-app installation permission screen first.

## Next release requirements
1. Merge the updater branch when the next release is ready. Increase versionCode above 2 and bump the web service-worker cache.
2. Build the full native wrapper with Gradle. **Do not use tools/repack_android.py:** the old native shell has no updater or install permission.
3. Sign with the preserved private distribution key. Its certificate SHA-256 is `6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b`. Recovery archive: `license-plate-game-private-signing-recovery.zip`. Never commit this archive or key. Default GitHub CI debug signing does not use this key.
4. Run the Trash audit and runtime build, validate the APK with apksigner/zipalign, and device-test an upgrade from the last delivered APK. Confirm that the collection survives. Test the permission screen, cancellation, offline mode, retry, and a later signed version.
5. Generate `update.json` with `python tools/prepare_update.py APK --build-tools SDK_BUILD_TOOLS --url HTTPS_GITHUB_RELEASE_ASSET_URL --notes 'User-facing changes' --output update.json`. The script reads version and minimum SDK from the APK, computes its hash, and rejects a different signing key.
6. Create a draft GitHub release with both the APK and `update.json` attached. The URL must use `https://github.com/thestonedcoyote-cell/license-plate-game/releases/download/TAG/FILENAME.apk`. Verify both assets before marking the release stable/latest. Do not publish test metadata.
7. Existing installations need one manual installation of the updater-enabled APK. Later stable releases can be discovered inside the app. This is not silent installation or Google Play delivery.

## Metadata contract
`applicationId`, integer `versionCode`, `versionName`, integer `minSdk`, HTTPS release-asset `url`, 64-character `sha256`, and plain-text `notes`. The native check finds the asset named `update.json` on GitHub's latest non-prerelease release. No credentials are required for this public repository.

## Verification remaining
Physical device and installer tests are required before rollout. Native compilation and metadata-generator tests cannot establish that installation works on the user's phone.
