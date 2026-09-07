# Cloud account / web companion foundation

## Goal
Allow the installed mobile PWA and the larger-screen web companion to share one player identity, sightings and Unidentified photos while preserving local-first play for people who never create an account.

## Current state
- Every install already has a stable local `player_id`.
- A mutable local username already exists.
- Sightings/photos are local-first in IndexedDB.
- v11 adds the Research/web companion screen to the same codebase.

## Required backend capabilities
A real cloud release needs:
- authentication: email/password and OAuth (Google first; others optional)
- database: player profile, sightings, plate identifications, score events, achievements, friend relationships
- object storage: private sighting photos
- row/object authorization so one account cannot read another account's private photos or exact GPS
- server-side username uniqueness and abuse controls

## Proposed data objects
### players
- account_id
- public player_id
- username
- display_name (optional)
- created_at / updated_at
- privacy defaults

### devices
- device_id
- player_id
- first_seen / last_seen
- local migration version

### sightings
- sighting_id
- player_id
- plate_uid (nullable while unidentified)
- captured_at
- approximate location fields
- exact coordinates (private by default)
- source: camera/manual/import
- first-sighting flag

### photos
- photo_id
- sighting_id
- private storage key
- thumbnail key
- checksum
- created_at

### score_events
- event_id
- player_id
- sighting_id
- scoring_model_version
- points / rarity components
- created_at

### social
- friendship/follow/group objects
- leaderboard snapshots or query views

## Migration rule
A person must be able to install and play before creating an account. When they later authenticate, the local player ID and local sightings should be linked/migrated rather than discarded.

## Privacy rule
- photos private by default
- exact GPS private by default
- public profile exposes only information the player deliberately shares
- leaderboard entries should not reveal exact sighting locations

## Auth provider note
GitHub Pages is static hosting. Secure password/OAuth login therefore requires a separately provisioned backend/auth provider or API. Do not expose a fake login control until credentials/configuration and authorization rules are actually deployed.

## Final recheck
Before cloud auth is enabled publicly, verify password reset, OAuth redirect rules, account deletion/export, row-level access controls, private photo-object permissions, local-to-cloud migration, duplicate merge behavior, username collision handling and logout/revocation.

## Completion status
INCOMPLETE — client identity and data model foundations exist; backend/auth/storage provisioning remains required.
