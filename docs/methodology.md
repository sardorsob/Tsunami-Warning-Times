# Methodology — Draft Contract

No scientific analysis has yet been executed. This document defines the order in
which it may proceed.

## 1. Feasibility

Compare candidate events using authoritative modeled-field availability, DART
and tide-gauge records, event metadata, source terms, formats, and useful
community contrasts. Select on evidence availability, not fame.

## 2. Provenance and data proof

Freeze source URLs/queries, versions, retrieval dates, terms, and checksums. Load
one modeled field and two observations. Verify event identity, time standard,
units, CRS/order, vertical datum, nodata, missingness, and station coordinates.
Log every record/pixel count and rejected record. Rerun to confirm idempotence.

## 3. Timing definitions

Preserve and label these as different quantities:

- event origin or rupture time;
- model/forecast run or bulletin issue time;
- modeled arrival time;
- observed first deviation or other documented arrival pick;
- maximum-wave time;
- public alert or evacuation-message time.

“Physical travel time” is modeled or observed arrival minus event origin.
“Public warning lead time” requires an authoritative public alert timestamp and a
clearly defined arrival endpoint. Neither automatically measures time available
for a person to act.

## 4. Baseline and comparison

Define a transparent distance-only reference without consulting residuals. Use
one event origin and timing convention across the reference, modeled field, and
observations. Extract modeled values at stations with a documented interpolation
rule. Define residual sign and precision before calculating comparisons.

## 5. Visual validation

Make a static figure before animation. Document projection and antimeridian
handling; distinguish NoData from zero; keep extent, scale, labels, units, and
color roles consistent. Check three displayed values manually. Only then test a
data-derived animated threshold and its static fallback.

## 6. Reproducibility

All transformations run from terminal-invokable Python modules, use typed public
interfaces and `pathlib`, log accounting, and write generated outputs outside
source code. Reportable artifacts retain source IDs, configuration, Git SHA, and
checksums. The browser consumes compact static exports and no secrets.
