# Data Card — Feasibility State

## Status

No scientific dataset has been approved or downloaded. Tōhoku is authorized for
a broad data-proof attempt, not promoted for production. Candidate sources and
their evidence belong in `docs/research/feasibility.md`; approved machine-readable
records belong in `artifacts/provenance/source-manifest.csv`.

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

## Planned grains

- source asset: one row per retrieved file or API response;
- travel-time contour: one row per source contour part and `HOURS` value;
- model-field index: one row per source variable/grid/time asset;
- station: one row per deployment or gauge identity;
- observation: one row per station sample;
- arrival pick: one row per station, method configuration, and sensitivity run;
- rejected record: one row per rejected asset, feature, station, or sample.

## Minimum record contract

Each accepted source records publisher, URL, retrieval date, version/date,
license or terms note, checksum, local path, units, time standard, spatial
reference, vertical datum where applicable, missingness, event identity, and all
processing steps. The value `unknown` is explicit and blocks downstream release
when it affects interpretation.

Raw files are immutable and ignored. Normalized files retain source fields and
add derived fields rather than overwriting identity, time, units, or coordinates.
Every stage reconciles input, accepted, rejected, and output counts.

## Sensitive data and authorization

The planned sources are public environmental and geographic records. No PII,
credentials, private data, or user uploads are in scope. Public availability is
not assumed to grant redistribution; terms must be checked per source.

## Known misuse risk

Retrospective data and derived products must not be presented as a real-time
warning service. Station gaps, picked arrivals, and model residuals do not by
themselves measure public warning performance.
