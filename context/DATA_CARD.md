# Data Card — Tōhoku Data-Proof Candidate

## Status

T-002A source contracts, T-002B acquisition, and T-002C normalization have an
accepted baseline. The Saipan and Valparaíso recovery revisions expand the
ledger to 18 exact assets: 17 are acquired and checksummed, while only the
continuous NCTR field remains blocked and visible. Independent scientific-data
review accepted the Valparaíso revision after its sensor-selection rationale,
pressure-companion accounting, and build references were corrected.
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

- source outcome: one row per contracted file/API response, including the NCTR
  blocker, two Saipan archival companions, and one Valparaíso sensor-quality
  companion;
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
- six coastal candidates represented as stations with 21,933 observations;
- 107 rejected records: 1 blocked asset, 90 DART rows containing an
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

Valparaíso supplies 4,272 accepted radar samples in metres with UTC source times
and an explicitly unknown vertical datum. Its 4,270-sample pressure response is
retained as a checksummed quality companion rather than normalized as a second
station. All IOC QC flags remain attached; no API filter, mean subtraction, or
timestamp fitting was applied. Forty-eight nominal radar minute positions are
absent, and the sole numeric zero is retained with the publisher's
`out_of_range=T` flag.

## Missingness profile

The reproducible T-002D missingness slice uses six source-supported coastal
windows totaling 23,040 nominal minute positions. Strict exact-grid coverage is
90.1215%: 2,276 positions are unavailable because the exact timestamp is absent
or its retained value is blank. Sample-density coverage is 90.6424%: 2,156
positions are unavailable when Saipan's 120 valid off-grid observations count
without being moved. The two rates intentionally answer different questions.

| Station | Strict coverage | Sample-density coverage | Main evidence |
| --- | ---: | ---: | --- |
| Hilo | 99.3287% | 99.3287% | 29 source blanks |
| Pago Pago | 69.4676% | 69.4676% | 936 blanks and 383 absent tail positions |
| Crescent City | 98.6111% | 98.6111% | 60 source blanks |
| Adak | 99.4444% | 99.4444% | 24 source blanks |
| Saipan | 44.7222% | 53.0556% | 796 exact-grid positions absent; 120 valid off-grid rows |
| Valparaíso | 98.8889% | 98.8889% | 48 positions absent |

The pooled 0.7302% raw-null rate is not a sufficient completeness measure.
Structural not-applicable fields, explicit quarantine, unknown datum metadata,
and the blocked NCTR continuous field use separate denominators. Missingness is
strongly concentrated by station and time, so pooled MCAR is not supported. MAR
is unproved and MNAR cannot be excluded without upstream operational evidence.
No value is imputed.

## Sensitive data and authorization

The sources are public environmental and geographic records. No PII,
credentials, private data, or user uploads are present in repository artifacts.
The IOC access credential remains outside the repository in macOS Keychain.
Public availability is not assumed to grant redistribution; terms must be
checked per source.

## Known misuse risk

Retrospective data and derived products must not be presented as a real-time
warning service. Station gaps, picked arrivals, and model residuals do not by
themselves measure public warning performance.
