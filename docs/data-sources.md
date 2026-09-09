# Data Sources

The accepted baseline and current Saipan/Valparaíso recovery candidate are documented in
the [primary-source feasibility comparison](research/feasibility.md),
[source-access note](research/source-access-options.md), and
[data card](../context/DATA_CARD.md).

The canonical machine-readable inventory is
[`artifacts/provenance/source-manifest.csv`](../artifacts/provenance/source-manifest.csv).
Its required fields and statuses are documented in the adjacent
[`source-manifest.md`](../artifacts/provenance/source-manifest.md).

Planned source classes include authoritative event metadata, tsunami travel-time
or arrival fields, DART and tide-gauge records, bathymetry, coastline context,
and narrowly scoped public-warning records if the final story makes alert-time
claims. A source appearing in research notes is not approved until its manifest
row is accepted and the data proof passes.

The current ledger contains 18 exact assets: 17 acquired/checksummed and 1
blocked. Saipan day `.070` and Valparaíso radar are normalization inputs;
Saipan `.071`/`.072` and Valparaíso pressure are coverage-only companions. Only
the continuous NCTR field remains blocked.
