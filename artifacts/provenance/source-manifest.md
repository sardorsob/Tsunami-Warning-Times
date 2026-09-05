# Source Manifest Contract

The machine-readable inventory is `source-manifest.csv`. Validate it with:

```bash
uv run python -m pipeline.provenance artifacts/provenance/source-manifest.csv
```

Every cell is explicit: use `unknown`, `not applicable`, or `not-downloaded`
instead of a blank. Spatial sources explicitly record spatial reference,
horizontal/vertical datum, coordinate order, temporal reference, units,
processing level, and missingness. `candidate` means the source may be useful but
is not approved for analysis. Only `approved` sources may feed reportable output.
`rejected` and `superseded` rows remain in the ledger with a reason.

For downloaded assets, replace `not-downloaded` with a repository-relative local
path and a lowercase SHA-256 digest. The manifest records source facts, not a
claim that public availability permits redistribution.
