# Tōhoku Missingness EDA

## Run and scope

- Run ID: `2026-09-09__1749__missingness__7b6d386`
- Git SHA: `7b6d386`
- Command: `uv run python scripts/profile_missingness.py --processed-dir data/processed/tohoku/2026-09-09-valparaiso-reviewed-7576ffb-a --config config/tohoku-missingness.toml --artifact-dir artifacts/eda/missingness --run-dir artifacts/logs/runs/2026-09-09__1749__missingness__7b6d386 --report context/EDA_REPORT.md --run-id 2026-09-09__1749__missingness__7b6d386 --git-sha 7b6d386 --working-tree clean --mlflow-dir .mlflow/mlruns --mlflow-experiment tohoku-eda`
- Scope: the first, missingness-focused slice of T-002D; no arrival pick, model
  residual, or station promotion decision is made here.

The accepted table contains **143,655 station samples**.
There are **1,049 missing raw values
(0.7302%)**, but that pooled cell rate hides missing
timestamps and strong station concentration. The six coastal windows have
**2,276 unavailable exact-minute
positions out of 23,040
(9.8785%)**. A sample-density view,
which allows valid off-grid observations to count without snapping them to a
minute, gives 9.3576%
unavailable.

## Checks performed

- separated blank raw measurements from absent expected timestamps;
- separated source missingness from structurally inapplicable columns;
- retained zero as a numeric observation;
- measured exact-grid and sample-density coastal coverage separately;
- summarized DART cadence without imposing a false uniform grid;
- counted explicit source-record quarantine and whole-asset unavailability;
- exposed unknown datum metadata separately from missing observations; and
- inspected the TTT hour-label sequence without assuming absent labels were
  intended publisher outputs.

## Coastal completeness

| Station | Accepted | Expected | Source blanks | Absent timestamps | Off-grid | Strict unavailable | Strict coverage | Longest observed gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hilo | 4,320 | 4,320 | 29 | 0 | 0 | 29 | 99.3287% | 60 s |
| Pago Pago | 3,937 | 4,320 | 936 | 383 | 0 | 1,319 | 69.4676% | 60 s |
| Crescent City | 4,320 | 4,320 | 60 | 0 | 0 | 60 | 98.6111% | 60 s |
| Adak | 4,320 | 4,320 | 24 | 0 | 0 | 24 | 99.4444% | 60 s |
| Saipan | 764 | 1,440 | 0 | 796 | 120 | 796 | 44.7222% | 39,660 s |
| Valparaíso | 4,272 | 4,320 | 0 | 48 | 0 | 48 | 98.8889% | 1,560 s |

Saipan's off-grid rows are valid source observations, not errors. They remain at
their original timestamps. Pago Pago and Saipan are the material continuity
risks; the other four coastal series have high requested-window coverage.

## Missingness mechanisms

| Mechanism | Count | Denominator | Rate | Interpretation |
| --- | ---: | ---: | ---: | --- |
| `source_blank_value` | 1,049 | 143,655 | 0.7302% | upstream value missing at a retained timestamp; exact cause unknown |
| `structural_not_applicable` | 21,933 | 143,655 | 15.2678% | coastal sources do not publish DART fitted/residual fields |
| `coastal_strict_grid_unavailable` | 2,276 | 23,040 | 9.8785% | expected timestamp absent or exact-grid value blank |
| `dart_sentinel_quarantine` | 90 | 121,812 | 0.0739% | ambiguous 9999 measurement row deliberately excluded |
| `source_asset_unavailable` | 1 | 18 | 5.5556% | whole contracted asset unavailable; not row-level missingness |

The **21,933** coastal rows with empty
`fitted_value` and `residual_value` are not missing observations: those
DART-specific quantities do not exist in the coastal sources. They must not be
imputed. All DART rows retained for analysis have populated raw, fitted, and
residual fields; unexpected retained DART modeled-field null rows:
**0**.

## DART cadence

| DART station | Accepted | Observed intervals (s) | >900 s | Maximum interval |
| --- | ---: | --- | ---: | ---: |
| 21413 | 4,151 | 15, 45, 60, 900, 960 | 2 | 960 s |
| 21418 | 4,958 | 15, 30, 45, 60, 120, 180, 900, 960, 4500, 8100 | 15 | 8,100 s |
| 32401 | 3,191 | 15, 30, 45, 60, 900, 960 | 2 | 960 s |
| 46411 | 109,422 | 15, 300 | 0 | 300 s |

DART reporting changes among source-supported cadences, so cadence transitions
are sampling-by-design until evidence shows otherwise. Intervals over 900
seconds remain follow-up gaps rather than being silently treated as ordinary
cadence.

## Statistical interpretation

**Pooled MCAR is not supported.** Missingness is strongly concentrated by
station and contiguous time window. Some analyses may assume MAR after
conditioning on station, time, source, and reporting mode, but the current data
do not prove that assumption. MNAR cannot be ruled out because an outage could
be related to unobserved sea conditions. Distinguishing MAR from MNAR requires
publisher telemetry, maintenance, or quality-control logs that are not present
in this bundle.

This is not primarily century-scale technology missingness. The 2011 sources
already recorded minute- and second-scale values. The observed patterns are
more consistent with localized source, telemetry, QC, or archival interruption,
but the exact causes remain unknown unless publisher evidence resolves them.

## Other incompleteness

- Source assets: 17 approved and
  1 blocked out of 18;
  the blocked NCTR continuous field is asset-level unavailability, not a row
  null rate.
- Station metadata: 10 of
  10 horizontal datums and
  5 of 10
  vertical references remain explicitly `unknown`.
- TTT contours: source hour labels 71, 72, 73 are absent inside the
  1-through-75 sequence. That
  is an upstream sequence gap with unknown intent, not proven local data loss.

## Adaptive EDA decision ledger

- **Pooled null rate hides absent rows:** reconstruct source-supported coastal
  grids. This check now belongs in the fixed core profile.
- **Pago Pago and Saipan dominate unavailability:** map their gap blocks and
  test arrival-pick sensitivity without interpolation before promotion.
- **Saipan contains valid `:59` timestamps:** keep strict-grid and
  sample-density coverage separate; preserve source time rather than snapping.
- **DART cadence is mixed by source design:** inspect intervals above documented
  cadence before labeling gaps; long intervals remain open checks.
- **Outage metadata is absent:** seek publisher telemetry/QC evidence if causal
  classification affects conclusions; MAR/MNAR remain unresolved.

## Limitations, takeaways, and next steps

Tests and deterministic calculations establish where missingness appears and
whether it came from local filtering. They do not establish the upstream causal
mechanism. The pipeline introduced no imputation and keeps rejected rows and the
blocked asset visible.

Next, T-002D should visualize gap blocks, inspect DART intervals over 900
seconds, define pre-arrival completeness gates, and run arrival-pick sensitivity
with an explicit no-interpolation baseline. Station inclusion remains frozen
until those checks are reviewed.

## Input and output fingerprints

The portable run bundle records these same fingerprints as JSON. The
source manifest remains authoritative for the 18 contracted source assets.

### Normalized inputs

| File | SHA-256 |
| --- | --- |
| `tohoku-missingness.toml` | `589156fc620a65f38a0aa981d56d7506ae9cb40076240d967284796a9c1941f2` |
| `accounting.json` | `331617e5ed4a9e747ec79364409659e723cd7ece5b20f6cc1b197a40e1abaf83` |
| `observation.csv` | `9daee574ea2b75c72c8bfb7984a32c248fa8692a2b74ba705ac7848089f52be3` |
| `rejected_record.csv` | `e2d8e86cfead1713036cee2883007a513fc0155d8c6b84f954e757ce72d14310` |
| `station.csv` | `d4ad18dafca36e027242095d81a81a3c70ecce59ee3027fbc9f9d077689f5004` |
| `ttt_contour.csv` | `53f2efd57327e69f196a6ce25417e451ff3366dd3e9f4185ddbe4d764c3caed4` |

### Generated machine-readable outputs

| File | SHA-256 |
| --- | --- |
| `coastal-missingness.csv` | `07e0b87515f10c21d203b35e4e043ecf7d49d08fd202d8cb4eb540b2b3748ac5` |
| `missingness-mechanisms.csv` | `c305400a1f8d823293199a80985a33ec68b63e88646d5a0fa28c573500d373a3` |
| `missingness-summary.json` | `e18250f621df7e057af450459a4909d40cf74a9a502b702e84e77c60a7961ee6` |
