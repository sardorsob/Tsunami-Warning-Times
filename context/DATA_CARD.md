# Data Card — Feasibility State

## Status

No scientific dataset has been approved or downloaded. Candidate sources and
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

## Minimum record contract

Each accepted source records publisher, URL, retrieval date, version/date,
license or terms note, checksum, local path, units, time standard, spatial
reference, vertical datum where applicable, missingness, event identity, and all
processing steps. The value `unknown` is explicit and blocks downstream release
when it affects interpretation.

## Sensitive data and authorization

The planned sources are public environmental and geographic records. No PII,
credentials, private data, or user uploads are in scope. Public availability is
not assumed to grant redistribution; terms must be checked per source.

## Known misuse risk

Retrospective data and derived products must not be presented as a real-time
warning service. Station gaps, picked arrivals, and model residuals do not by
themselves measure public warning performance.
