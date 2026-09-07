# License Plate Game

A passenger-first road-trip collection game for identifying license plates quickly, saving fleeting sightings with the camera, and building a geography-aware collection.

**Status:** v7 alpha, active development. The current catalog contains **1,138 collectible designs**.

## The interaction rule

A sighting may exist for only a second. The first screen therefore has two primary actions: **Camera** and **Identify**. Camera startup and GPS are requested concurrently; capture never waits for location. Manual collection also saves before waiting on GPS.

## Current alpha

- 1,138 collectible designs across the research catalog.
- Dynamic identification questions derived from the visual characteristics currently available.
- Camera capture auto-saves to an Unidentified queue.
- Local-first IndexedDB storage for sightings and photos.
- GPS location attached immediately when available or asynchronously afterward.
- Collection, repeat sightings, achievements, day/night themes, backup/import.
- Origin and where-found maps using Leaflet/OpenStreetMap when online.
- FHWA registration/VMT priors for an experimental rarity estimate; rarity achievements remain disabled.
- Installable PWA deployed through GitHub Pages.

## Privacy

This alpha has no player account, analytics, or server-side sighting upload. Player sightings, photos, and exact coordinates stay in the browser on the device unless explicitly exported. See [PRIVACY.md](PRIVACY.md).

## Images and rights

The public repository does **not** bulk-publish the downloaded official plate-artwork archive. Specialty plates can contain third-party copyrighted/trademarked art. Provenance is kept in the research data and artwork receives a separate rights review before broader redistribution. See [docs/DATA_AND_RIGHTS.md](docs/DATA_AND_RIGHTS.md).

## Development

Run locally:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/`. Real Android camera/GPS/PWA behavior should be tested over HTTPS.

Validate:

```bash
python tools/validate_release.py
node --check app.js
```

## Useful docs

- [Architecture](docs/ARCHITECTURE.md)
- [Moto G Power 5G test checklist](docs/MOTO_TEST.md)
- [Roadmap](docs/ROADMAP.md)
- [Data and image-rights policy](docs/DATA_AND_RIGHTS.md)
- [Security](SECURITY.md)

No open-source license has been selected yet.
