# Process Notes — new jurisdiction official-source leads, October 11, 2026

## Purpose
Expand the image-acquisition source registry beyond its previous 17 of 58 jurisdictions without conflating source discovery with acquired or visually matched plate images.

## Inputs
Existing `data/harvest_sources.csv`, `data/image-campaign/source-registry.json` at main `ad92c1a9381f9d2b10d628db91947da1d99e325b`; independently retrieved issuing-agency pages from AK, MS, NJ, MI, WY, DC, NM, IA and Ontario via public search and page inspection.

## Step notes
- Step 1: counted 58 runtime jurisdictions and 17 with official lead entries.
- Step 2: independently found 12 official page leads spanning nine previously uncovered jurisdictions, representing 248 immutable catalog designs in aggregate, with no implication every design is currently pictured there.
- Step 3: appended 12 source rows to the reviewed harvest CSV and recorded them in the jurisdiction registry. The source registry now has 26 of 58 jurisdictions with at least one lead.
- Step 4: marked these jurisdictions `official_leads_discovered_not_harvested`, not downloaded or matched. Subpage-only New Jersey/Wyoming and potentially non-image Ontario program references remain flagged.
- Step 5: extended harvest-record metadata to carry an explicit `jurisdiction_id`, while preserving US-XX fallback for older input lists. Matching can now distinguish CA-ON from nonexistent US-ON.
- Step 6: left all existing 1,138 catalog UIDs, 54 Washington mappings, and Oregon integration review state unchanged.

## Exceptions / failures
No new image files were acquired as part of this discovery-only patch. Many pages display only current designs; historical IDs may need archives or independent references. The HTML harvesting tool only follows images directly embedded on reviewed source pages and not nested unreviewed links. No human approval or licensing conclusion can be inferred from a government source's existence.

## Outputs
12 official page leads across nine jurisdictions (AK, MS, NJ, MI, WY, DC, NM, IA, CA-ON); 31 total rows in source CSV; 26 of 58 catalog jurisdictions with leads; explicit-jurisdiction mapping compatibility in existing harvester and evidence mapper.

## Rights / privacy notes
Only publicly available URLs, government attribution and retrieval leads were recorded; no private data, third-party original art or credentials included in these source-only changes.

## Final recheck
Checked the catalog-region counts (58), source rows (31), new-source total (12), and lead-jurisdiction count (26) after write. The 248 designs describe potential coverage pool, not completed acquisitions or trustworthy mapped images. Original catalog IDs remain unchanged; further network harvest and mapping are required.

## Completion status
COMPLETE_WITH_EXCEPTIONS — source discovery complete for these nine jurisdictions; retrieval and image matching pending.
