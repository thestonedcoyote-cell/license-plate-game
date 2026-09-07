# Social / Scoreboard Foundation

Status: **foundation only**. No network account service is live yet.

## Why this exists now

Social play, friends, usernames, regional leaderboards, family groups, and scoreboards will eventually need stable player identity. Creating the local identity schema now avoids coupling a future social system to device-specific browser records or inventing a migration after thousands of sightings exist.

## Local player identity

Every install creates and retains:

- `player_id`: immutable UUID generated locally.
- `username`: optional player-selected handle. Local-only today; it is **not** claimed globally unique until a server validates it.
- `created_at` / `updated_at`.
- `schema_version`.
- `score_version`: identifies the scoring rules used for computed totals.
- `social_sync`: currently `local_only`.

Storage key: `lpg.profile.v1`.

## Future network identity

When accounts are introduced, the server should assign a separate immutable account ID and bind one or more local `player_id` values after explicit user authorization. Never make the visible username the primary key; usernames must be changeable.

Suggested account fields:

- account_id
- username + normalized_username
- display_name (optional)
- created_at
- privacy_level
- home_region (coarse and optional)
- blocked/muted relationships
- local_player_ids / migration receipts

## Score events, not just score totals

Store auditable scoring events so scoring rules can change without corrupting history:

- score_event_id
- account/player ID
- sighting ID
- plate UID
- event_type
- scoring_model_version
- base_value
- rarity/location modifiers
- final_value
- created_at
- verification/confidence state

Leaderboards should normally be computed from accepted score events rather than a mutable integer attached to a user.

## Social surfaces planned

- Friends / family groups.
- Optional public usernames.
- Global, country, state/province, park/trip, and friends-only leaderboards.
- Achievement comparison.
- Recent interesting finds, with exact location hidden by default.
- Challenges such as trip groups, road-trip bingo, or first-to-complete sets.

## Privacy defaults

Exact sighting coordinates and private photos must never become public merely because social features are enabled. Public feeds should use coarse place labels unless the player explicitly chooses otherwise.

## Abuse / fairness foundations

Future scoreboards need:

- duplicate/repeat-sighting controls;
- rate limits;
- impossible-travel checks;
- confidence/verification flags;
- scoring-model versioning;
- appeal/correction records;
- no reward structure that encourages unsafe photography while driving.

The current phone app is passenger-first and should remain so.
