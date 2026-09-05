# Hazard Event Set

## Contract

The first release will contain exactly one selected historical Pacific tsunami.
The event must have an unambiguous identifier, origin time and location, source
agency, modeled product, observation set, temporal reference, and documented
relationship between all artifacts.

## Current state

No event is frozen. Primary-source screening provisionally recommends the 2011
Tōhoku event for the current physical-propagation thesis, subject to the complete
data-proof gate. The 2025 Kamchatka event is the stronger fallback if the project
is reframed around operational-message timing.

| Candidate | Screening disposition | Unresolved gate |
| --- | --- | --- |
| 2011 Tōhoku | Provisional recommendation | Continuous/raw field access; unshifted series; reproducible picks; warning archive |
| 2010 Maule | Viable runner-up | No demonstrated data or narrative advantage over Tōhoku |
| 2025 Kamchatka | Warning-message fallback | Preliminary model; no verified machine-readable arrival field |

See `docs/research/feasibility.md` for citations and the comparison matrix. The
future freeze decision must record:

| Field | Required value |
| --- | --- |
| Event ID and common name | Source-owned identifier and plain-language label |
| Origin | UTC timestamp, coordinates, depth, and authoritative source |
| Modeled product | Product ID/version, issue/run time, grid semantics, units |
| Observation set | Station IDs, sensor types, time basis, arrival definition |
| Spatial support | Extent, resolution, CRS/coordinate order, antimeridian rule |
| Vertical reference | Bathymetry and water-level datum definitions |
| Uncertainty | Source precision and material methodological uncertainty |
| Terms | Access, reuse, attribution, and redistribution notes |
| Selection evidence | Feasibility score plus completed minimal data proof |

Fame or historical importance alone is not a selection criterion.

## Tōhoku data-proof bundle

The approved attempt covers one USGS event record, NCEI TTT layer 17, one exact
NCTR field/source combination, four DART records, and six coastal-gauge
candidates. This bundle tests availability and analytical fit; it does not alter
the provisional event disposition.

The source and station set can be frozen only when T-002E accepts the upstream
identity, terms, timing, spatial, quality, sensitivity, and reproducibility
evidence. Rejected stations and unavailable assets remain visible in the reports.
