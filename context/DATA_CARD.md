# Data Card — Tōhoku Data-Proof Candidate

## Status

T-002A source contracts, T-002B acquisition, and T-002C normalization have an
accepted baseline. A 2026-09-08 Saipan recovery revision expands the ledger to
17 exact assets: 15 are acquired and checksummed, while the continuous NCTR
field and Valparaíso remain blocked and visible. The revised normalization is
accepted after independent scientific-data review.
Tōhoku remains a data-proof candidate, not a production dataset or operational
warning product.

Raw assets are immutable, checksummed, ignored, and untracked. Reproducible
processed tables are also ignored; their schemas, accounting, output hashes, and
quality metrics are tracked in the run bundle and
`context/DATA_QUALITY_REPORT.md`.

## Required source classes

- authoritative event origin and identity metadata;
- modeled tsunami travel-time or arrival-time field;
- DART station metadata and event time series or authoritative picks;
- coastal tide-gauge metadata and event time series or authoritative picks;
- bathymetry used by, or suitable for explaining, the modeled field;
- openly licensed coastline/boundary context;
- limited authoritative community alert context only if warning-system time is
  shown.

## Data-proof acquisition set

- one reviewed USGS machine event record;
- NCEI TTT layer 17 geometry and metadata;
- one exact NCTR field/source combination with documented coefficients;
- four DART stations selected as two near-field and two far-field records before
  residual inspection;
- six coastal candidates: Saipan, Adak, one Hawaiʻi station, Crescent City,
  Pago Pago, and one Chilean station.

Exact station IDs, deployments, endpoints, windows, and formats are outputs of
T-002A. No candidate becomes analysis-ready merely because it downloads.

## Actual normalized grains

- source outcome: one row per contracted file/API response, including blockers
  and the two Saipan archival companions;
- event: one row for the reviewed USGS event origin;
- travel-time contour: one row per source contour part and `HOURS` value;
- station: one row per selected DART deployment or coastal-gauge identity,
  including blocked candidates;
- observation: one row per accepted station sample, retaining source time;
- arrival pick: one row per station, method configuration, and sensitivity run;
- rejected record: one row per rejected asset, feature, station, or sample.

The NCTR model-field index is absent because no exact continuous field passed the
source gate. Published NCTR scalar source coefficients are coverage-only evidence
and are not a field proxy. Arrival-pick tables are deferred to T-002D.

## Minimum record contract

Each accepted source records publisher, URL, retrieval date, version/date,
license or terms note, checksum, local path, units, time standard, spatial
reference, vertical datum where applicable, missingness, event identity, and all
processing steps. The value `unknown` is explicit and blocks downstream release
when it affects interpretation.

Raw files are immutable and ignored. Normalized files retain source fields and
add derived fields rather than overwriting identity, time, units, or coordinates.
Every stage reconciles input, accepted, rejected, and output counts.

## Current coverage and quality

- one reviewed USGS event row;
- 72 TTT features expanded to 4,380 contour parts and 62,988 vertices;
- four preselected DART stations with 121,722 accepted samples;
- six coastal candidates represented as stations: five with 17,661 observations
  and Valparaíso retained as a blocker;
- 108 rejected records: 2 blocked assets, 90 DART rows containing an
  undocumented `9999` measurement sentinel, and all 16 Saipan rows belonging to
  8 conflicting duplicate timestamps;
- zero duplicate primary keys, zero duplicate station/timestamp pairs, and zero
  null required fields.

CO-OPS raw-value missingness is retained, not imputed. Pago Pago returns only
3,937 of 4,320 requested minute rows, contains 936 null values, and supplies
3,001 usable values (69.468% of the requested window). DART cadence varies by
source; long post-quarantine intervals remain explicit EDA targets. Unknown CRS,
horizontal datum, vertical reference, and time semantics remain `unknown` where
the publisher evidence does not resolve them.

Saipan day `.070` supplies 764 accepted event-day samples in meters relative to
MLLW. Every row at its eight conflicting duplicate timestamps is quarantined,
off-minute source timestamps are retained, and the 12:08–23:07 UTC gap is not
filled. Days `.071` and `.072` remain exact checksummed source companions for
later extended-tail analysis.

## Sensitive data and authorization

The sources are public environmental and geographic records. No PII,
credentials, private data, or user uploads are in scope. Public availability is
not assumed to grant redistribution; terms must be checked per source.

## Known misuse risk

Retrospective data and derived products must not be presented as a real-time
warning service. Station gaps, picked arrivals, and model residuals do not by
themselves measure public warning performance.
