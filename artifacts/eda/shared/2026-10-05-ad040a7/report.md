# Tōhoku shared EDA — timing support audit

Run `2026-10-05-ad040a7` · implementation `ad040a7` · frozen protocol `2026-10-05-v1`.

## Scope and disposition

This completes the shared descriptive/sensitivity audit, not physical-arrival validation. The data proof needs **revision for arrival comparisons**. Descriptive coverage and preliminary story diagnostics are usable; community timing selection and modeled-minus-observed claims remain blocked.

Verified 143,655 accepted observations, 10 stations, 4,380 contour parts and 62,988 vertices against accepted hashes. All 17 acquired raw assets reconcile. The 18th asset, the continuous NCTR field, remains blocked.

## All-station sensitivity results

Eight frozen event settings and eight disjoint pre-origin controls per station. Coastal raw-water-level runs are unsupported controls, never arrival estimates. The spread is across successful settings only; failed settings remain visible and prevent promotion.

| Station | Field | Detect / 8 | Control crossings / 8 | Unevaluable controls / 8 | Spread (s) | Screen |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1617760 | raw | 8 | 0 | 0 | 21960.0 | fail |
| 1770000 | raw | 8 | 0 | 0 | 6600.0 | fail |
| 21413 | residual | 8 | 0 | 0 | 1635.0 | fail |
| 21418 | residual | 8 | 0 | 0 | 15.0 | pass, unvalidated |
| 32401 | residual | 8 | 0 | 0 | 210.0 | fail |
| 46411 | residual | 8 | 0 | 0 | 60.0 | pass, unvalidated |
| 9419750 | raw | 8 | 0 | 0 | 5100.0 | fail |
| 9461380 | raw | 8 | 4 | 0 | 5640.0 | fail |
| saip | raw | 0 | 0 | 8 | unknown | fail |
| valp | raw | 8 | 0 | 0 | 78420.0 | fail |

Even a passing screen would require independent onset validation. No physical-arrival or modeled-arrival timestamp is released. No maximum-wave, public-alert, evacuation or actionable-warning time is calculated.

## Adaptive evidence ledger

Observation → question → follow-up → decision; frozen detector settings were not retuned.

- **Hilo**: 0 intervals exceed the declared cadence limit; 0 retained source-QC flags. Follow-up: inspect the exact endpoints in `gaps.csv` and all candidate ±15-minute source windows in `candidate-windows.csv`; 0/8 controls cross and 0/8 are unevaluable. Decision: unsupported_raw_water_level; do not use the threshold timestamp as a physical arrival.
- **Pago Pago**: 0 intervals exceed the declared cadence limit; 0 retained source-QC flags. Follow-up: inspect the exact endpoints in `gaps.csv` and all candidate ±15-minute source windows in `candidate-windows.csv`; 0/8 controls cross and 0/8 are unevaluable. Decision: unsupported_raw_water_level; do not use the threshold timestamp as a physical arrival.
- **DART 21413**: 2 intervals exceed the declared cadence limit; 0 retained source-QC flags. Follow-up: inspect the exact endpoints in `gaps.csv` and all candidate ±15-minute source windows in `candidate-windows.csv`; 0/8 controls cross and 0/8 are unevaluable. Decision: unvalidated; do not use the threshold timestamp as a physical arrival.
- **DART 21418**: 15 intervals exceed the declared cadence limit; 0 retained source-QC flags. Follow-up: inspect the exact endpoints in `gaps.csv` and all candidate ±15-minute source windows in `candidate-windows.csv`; 0/8 controls cross and 0/8 are unevaluable. Decision: unvalidated; do not use the threshold timestamp as a physical arrival.
- **DART 32401**: 2 intervals exceed the declared cadence limit; 0 retained source-QC flags. Follow-up: inspect the exact endpoints in `gaps.csv` and all candidate ±15-minute source windows in `candidate-windows.csv`; 0/8 controls cross and 0/8 are unevaluable. Decision: unvalidated; do not use the threshold timestamp as a physical arrival.
- **DART 46411**: 0 intervals exceed the declared cadence limit; 0 retained source-QC flags. Follow-up: inspect the exact endpoints in `gaps.csv` and all candidate ±15-minute source windows in `candidate-windows.csv`; 0/8 controls cross and 0/8 are unevaluable. Decision: unvalidated; do not use the threshold timestamp as a physical arrival.
- **Crescent City**: 0 intervals exceed the declared cadence limit; 0 retained source-QC flags. Follow-up: inspect the exact endpoints in `gaps.csv` and all candidate ±15-minute source windows in `candidate-windows.csv`; 0/8 controls cross and 0/8 are unevaluable. Decision: unsupported_raw_water_level; do not use the threshold timestamp as a physical arrival.
- **Adak**: 0 intervals exceed the declared cadence limit; 0 retained source-QC flags. Follow-up: inspect the exact endpoints in `gaps.csv` and all candidate ±15-minute source windows in `candidate-windows.csv`; 4/8 controls cross and 0/8 are unevaluable. Decision: unsupported_raw_water_level; do not use the threshold timestamp as a physical arrival.
- **Saipan**: 4 intervals exceed the declared cadence limit; 0 retained source-QC flags. Follow-up: inspect the exact endpoints in `gaps.csv` and all candidate ±15-minute source windows in `candidate-windows.csv`; 0/8 controls cross and 8/8 are unevaluable. Decision: unsupported_raw_water_level; do not use the threshold timestamp as a physical arrival.
- **Valparaíso**: 4 intervals exceed the declared cadence limit; 140 retained source-QC flags. Follow-up: inspect the exact endpoints in `gaps.csv` and all candidate ±15-minute source windows in `candidate-windows.csv`; 0/8 controls cross and 0/8 are unevaluable. Decision: unsupported_raw_water_level; do not use the threshold timestamp as a physical arrival.

## Distribution, fit, geometry, and join checks

`profiles.csv` retains raw/fitted/residual extrema, medians, zeros, blanks and cadence histograms. Extremes are described, not silently trimmed; source-QC exclusions affect the detector only. Raw minus fitted is compared with the publisher residual using a 0.00002 m rounding tolerance.

- DART 21413: maximum |raw − fitted − residual| 2e-05 m; 8 rows exceed tolerance.
- DART 21418: maximum |raw − fitted − residual| 2.0000001e-05 m; 8 rows exceed tolerance.
- DART 32401: maximum |raw − fitted − residual| 2e-05 m; 3 rows exceed tolerance.
- DART 46411: maximum |raw − fitted − residual| 2.0000001e-05 m; 212 rows exceed tolerance.

Contour audit: 24 boundary-roundoff vertices; 0 unsplit >180° jumps. No geometry repaired, CRS overwritten, or datum inferred. Observation IDs and station–UTC keys are unique; station joins and source/unit/vertical-reference semantics reconcile.

WGS84 source distances are descriptive approximations because all station horizontal datums are unknown. The DART timing-versus-distance figure shows candidate ranges, not travel speeds or modeled residuals. Hourly contours cannot supply a defensible station-arrival value; the continuous NCTR field remains unavailable, so its internal structure cannot be inspected.

## Missingness remains part of this audit

The existing missingness profiler is rerun on these exact inputs. See this run's `missingness-report.md` and `missingness/` tables for denominators, per-station continuity and the original adaptive ledger. Structural coastal fitted/residual blanks are not imputed. Upstream missing values, absent timestamps, quarantined sentinels and inaccessible assets remain distinct. MCAR/MAR/MNAR mechanisms are not identified from these records alone.

## Takeaways and next steps

1. Keep the preliminary atlas for source geography and coverage, with its existing chart-review caveats.
2. Resolve an observed-onset method for the coastal tidal series and independently validate DART picks; do not choose stations by attractive agreement.
3. Obtain an arrival-capable modeled product or approve a separately validated extraction method. Do not substitute nearest contours for the blocked field.
4. Only after a new scientific review grants arrival-comparison permission should Stage B select communities and draft a timing-discrepancy story. Paper modeling stays separate.

## Reproduction and evidence

Run `scripts/run_tohoku_eda.py --help`. `meta.json` records the command, Git SHA, no-randomness policy and protocol; `inputs.json` anchors source/processed bytes; `outputs.json` hashes all stable outputs. `sensitivity.csv` includes every outcome and sampling bracket. Figures are diagnostics with CSV alternatives; the Marimo notebook only displays these outputs.
