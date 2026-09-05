# Source Manifest Contract

The machine-readable inventory is `source-manifest.csv`. Validate it with:

```bash
uv run python -m pipeline.provenance artifacts/provenance/source-manifest.csv
```

Every cell is explicit: use `unknown`, `not applicable`, or `not-downloaded`
instead of a blank. Spatial sources explicitly record spatial reference,
horizontal/vertical datum, coordinate order, temporal reference, units,
processing level, and missingness. `candidate` means the source may be useful but
is not approved for analysis. `approved` means the exact asset is eligible for
the separately gated acquisition task, not that it is analysis-ready or
reportable. `blocked` means the requested asset has a recorded access or contract
blocker and cannot feed an acquisition run. `rejected` and `superseded` rows
remain in the ledger with a reason.

The T-002A ledger has one row per exact source asset. Its accompanying contract
file, `config/tohoku-data-proof.toml`, records expected format/signature,
planned local path, source-owned units and temporal/spatial semantics, and
station metadata. It is an acquisition allowlist, not a download log.

For downloaded assets, replace `not-downloaded` with a repository-relative local
path and a lowercase SHA-256 digest. The manifest records source facts, not a
claim that public availability permits redistribution.
