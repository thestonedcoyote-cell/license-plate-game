# Process Notes

## Purpose
Add the first real License Plate Game cloud-account layer using Supabase: email/password authentication, local-player identity migration, opt-in private photo backup, and larger-screen cloud photo review while preserving local-first gameplay.

## Inputs
- Live v11 PWA and existing local player profile (`lpg.profile.v1`).
- Supabase project `ffhsqvhorsyonavahlul`.
- Supabase current Auth/RLS/Storage documentation and security checklist.
- Existing Camera preview/capture flow.
- New database schema with profiles, devices, sightings, sighting_photos, score_events, leaderboard_totals, social_connections and private `sighting-photos` Storage bucket.

## Step notes
- Step 1: Reviewed current Supabase Auth, Data API/RLS, and Storage access-control guidance before implementation.
- Step 2: Created the account/sync database schema with RLS enabled on every exposed table.
- Step 3: Limited ordinary authenticated users to their own profiles, devices, sightings and photo metadata; score-event writes and leaderboard-maintenance writes are not exposed to clients.
- Step 4: Created private Storage bucket `sighting-photos` with per-user folder policies keyed to `auth.uid()`.
- Step 5: Ran Supabase security advisors; result: zero security lints.
- Step 6: Ran performance advisors and added missing covering indexes for score-events and social-connection foreign keys.
- Step 7: Added email/password sign-up/sign-in/sign-out UI using pinned `@supabase/supabase-js@2.115.0` and the project's publishable key. No secret/service-role/database credential is present in client code.
- Step 8: Linked a signed-in account to the app's existing local player ID and username where possible.
- Step 9: Added private photo backup as an explicit opt-in toggle, disabled by default. New Camera captures create a private cloud sighting and private Storage object only when signed in and enabled.
- Step 10: Added a Cloud Photo Desk for larger-screen review using short-lived signed URLs for private Storage objects.
- Step 11: Updated loader and service-worker cache for the cloud layer.

## Exceptions / failures
- Google login is not enabled because the Supabase project still requires Google OAuth client credentials/provider configuration; no nonfunctional Google button is shown.
- The first cloud sync backs up new camera photos after opt-in; it does not yet fully reconcile the historical local IndexedDB sighting database into cloud records.
- Cloud-backed identification updates, cross-device merge conflict handling, score calculation, friends UI and public leaderboards remain later layers.
- The user disclosed a database password in chat; it is not used or stored in the app and should be rotated separately.

## Outputs
- Supabase account/sync database schema and RLS policies.
- Private `sighting-photos` bucket with ownership policies.
- `cloud-sync.js` and `cloud-sync.css`.
- Updated `app.js` loader and `sw.js` cache.
- This process record.

## Rights / privacy notes
Cloud usage is optional. Exact GPS remains out of the first photo-backup path unless explicitly synced later. Photo backup is off by default. Private photos use authenticated RLS-protected Storage paths and signed review URLs. The frontend contains only a Supabase publishable key, never the service role, secret key, or database password.

## Final recheck
Recheck JavaScript syntax; verify cloud files are loaded and cached; verify the frontend contains the publishable key only; verify private photo sync defaults off; verify the Storage bucket is private; verify RLS is enabled on all public app tables; rerun Supabase security advisors; inspect the PR diff for credentials; merge only after GitHub Actions succeeds; verify Pages deployment after merge.

## Completion status
COMPLETE_WITH_EXCEPTIONS
