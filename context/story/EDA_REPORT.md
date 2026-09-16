# Visual-Story EDA Report

## Run and evidence state

- Run ID: `2026-09-16__0351__story-atlas__6c35d78`
- Git SHA: `6c35d78`
- Command: `uv run python scripts/story/build_story_atlas.py --processed-dir data/processed/tohoku/2026-09-09-valparaiso-reviewed-7576ffb-a --missingness-config config/tohoku-missingness.toml --missingness-summary artifacts/eda/missingness/missingness-summary.json --coastline data/raw/natural-earth/ne_110m_coastline_v4.1.0.zip --config config/story-atlas.toml --decision-input config/story-atlas-decisions.toml --artifact-dir artifacts/eda/story/2026-09-16__0351__story-atlas__6c35d78 --run-dir artifacts/logs/runs/2026-09-16__0351__story-atlas__6c35d78 --report context/story/EDA_REPORT.md --run-id 2026-09-16__0351__story-atlas__6c35d78 --git-sha 6c35d78 --working-tree clean --mlflow-dir .mlflow/mlruns --mlflow-experiment story-tohoku-eda`
- Evidence state: `preliminary_storyboard_evidence`
- Candidate build: `2026-09-09-valparaiso-reviewed-7576ffb-a`

This is story-lane diagnostic evidence. No story claim has been promoted.

## Inputs and source boundary

The atlas consumes one explicit accepted candidate build, the shared missingness
contract and summary, and the separately governed coastline. The continuous NCTR
field is unavailable; published NCEI hourly contours are not a substitute for a
continuous field.

## Fixed diagnostic atlas

- Pacific evidence map: 10 candidate stations and
  4380 published contour parts.
- Observation coverage: 23040 exact-grid
  positions and 120 unsnapped off-grid samples.
- Station time series: 24729 retained numeric
  points. Panels use local scales; amplitudes are not comparable.
- Distance/contour diagnostic: 6 WGS84 distance
  rings and 9 published hour
  classes. The two sides compare shape in different units; no speed conversion
  or station arrival assignment is made.

## Adaptive decision ledger

- **01_pacific_evidence_map — branch:** The corrected Equal Earth map places the reviewed event and all 10 candidate stations without seam-spanning line artifacts, but the event, DART 21418, and nearby labels collide at basin and thumbnail scale. Question: Is the event and candidate observational chain legible at basin scale? Follow-up: Add a reviewed regional inset or small multiple for the crowded Tōhoku cluster while retaining the fixed basin context as diagnostic evidence. Result: The basin context is spatially usable after the force-over seam fix, but local label crowding prevents treating this rendering as a final story scene. Storyboard: No scene is promoted; open a later reviewed regional-context branch without changing candidate stations. Manual QA: Inspected full size and 400 px thumbnail in color, grayscale, deuteranopia, and protanopia simulations; verified the event at 38.297, 142.373, Hilo at 19.7303, -155.0556, and Valparaíso at -33.02767128, -71.62787275; confirmed zero coastline or contour segments over 2,000 km after the seam fix.
- **02_observation_coverage — branch:** Saipan and Pago Pago dominate continuity risk: Hilo has 29 of 4,320 strict positions unavailable, Pago Pago has 1,319 of 4,320, and Saipan has 796 of 1,440 plus 120 unsnapped off-grid observations. Question: Where do distinct availability mechanisms affect the coastal chain? Follow-up: Branch to an observability-first candidate story that explains source blanks, absent timestamps, and off-grid samples before any arrival comparison. Result: The coverage view supports observability as the strongest current story lead; Saipan's 12:07–23:08 UTC observed interval remains visibly open and is not bridged. Storyboard: No scene is promoted; carry the observability-first candidate into a separate reviewed task while the arrival lane remains gated. Manual QA: Inspected full size and 400 px thumbnail in color, grayscale, deuteranopia, and protanopia simulations; reconciled Hilo 99.3287%, Pago Pago 69.4676%, Saipan strict 44.7222% and density 53.0556% to the missingness summary; confirmed distinct observed, source-blank, absent-timestamp, and off-grid encodings.
- **03_station_timeseries — retain:** All 10 station-local panels expose 24,729 retained numeric points, preserve the long Saipan gap, and keep six coastal raw-level panels separate from four DART residual panels. Question: Are retained station signals inspectable without hiding gaps or datums? Follow-up: Retain this as a diagnostic and investigate visible gaps and source-QC outliers through shared data-quality tasks without comparing panel amplitudes. Result: The panels are useful at full size and their macro-patterns survive thumbnail and color-vision checks, but local scales and incompatible vertical references prohibit amplitude comparison. Storyboard: Retain as preliminary diagnostic evidence only; no station, waveform, or scene is promoted. Manual QA: Inspected full size and 400 px thumbnail in color, grayscale, deuteranopia, and protanopia simulations; verified point-only rendering with no gap-bridging line, explicit local-scale labels, the open Saipan interval, and separate coastal raw-value versus DART residual semantics.
- **04_distance_contour_diagnostic — retain:** The six WGS84 range rings remain radial while the nine published contour classes are visibly non-radial across the same Equal Earth projection and extent. Question: How does geodesic range shape differ from published travel-time contours? Follow-up: Retain the shape contrast for the later T-003B gate, where reviewed arrival evidence may test it without assigning a contour or speed-derived arrival to any station. Result: The non-radial shape contrast is strong enough to retain as a candidate, while kilometres and published hours remain explicitly incompatible quantities. Storyboard: No scene is promoted; the distance candidate remains pending T-002E and independent T-003B review. Manual QA: Inspected full size and 400 px thumbnail in color, grayscale, deuteranopia, and protanopia simulations; verified identical panel projection and extent, six ring labels, published hour labels 1, 3, 6, 9, 12, 15, 18, 21, 24, source parts for hours 1, 6, and 24, and the explicit units-differ and no-speed-conversion warning.

## Interpretation

These views test geography, observability, source-preserving
signals, and shape. They do not test an arrival-time claim. The recorded
dispositions are Maker review inputs: `retain` keeps a diagnostic visible,
while `branch` records a new question without promoting a scene or selecting
stations from its result.

## Limitations

No arrival pick, modeled-versus-observed arrival residual comparison, station
promotion, or story claim occurred. Unknown horizontal and vertical datums remain
explicit. Coastal raw levels and DART residual signals are separate quantities.

## Takeaways

The manual review branches the crowded basin context toward a
regional view and the coverage finding toward an observability-first candidate.
It retains the signal and non-radial shape diagnostics as preliminary evidence.
No scene, station, waveform, or arrival claim is promoted.

## Next steps

Hand this preliminary atlas to the independent Checker for scientific and
cartographic review. Keep T-003A in review, carry the regional-context and
observability branches as separately reviewed work, and do not begin
arrival-based Stage B before T-002E.

## Input and output fingerprints

### Inputs

| File | SHA-256 |
| --- | --- |
| `story-atlas.toml` | `1ab3817259a8f47f0e7cfbf413b9419502836d7054e957adfba2dc255db845f2` |
| `tohoku-missingness.toml` | `589156fc620a65f38a0aa981d56d7506ae9cb40076240d967284796a9c1941f2` |
| `event.csv` | `bd1e11e9322f8670f016eeea4820f83ddca811d20fd52395d12405cd86d9ba82` |
| `station.csv` | `d4ad18dafca36e027242095d81a81a3c70ecce59ee3027fbc9f9d077689f5004` |
| `observation.csv` | `9daee574ea2b75c72c8bfb7984a32c248fa8692a2b74ba705ac7848089f52be3` |
| `ttt_contour.csv` | `53f2efd57327e69f196a6ce25417e451ff3366dd3e9f4185ddbe4d764c3caed4` |
| `accounting.json` | `331617e5ed4a9e747ec79364409659e723cd7ece5b20f6cc1b197a40e1abaf83` |
| `missingness-summary.json` | `e18250f621df7e057af450459a4909d40cf74a9a502b702e84e77c60a7961ee6` |
| `ne_110m_coastline_v4.1.0.zip` | `664449b39070027e882abb295974d182afec18ca21107273d17e9e8bf6f64817` |
| `story-atlas-decisions.toml` | `11e27cea2ba1717de52a1d520db4bf4e431c73e9c3928c5f856297e75fca9589` |

### Generated atlas evidence

| File | SHA-256 |
| --- | --- |
| `01_pacific_evidence_map.png` | `a3ec2a5206bc5593dae727a1003e5b1abbe6d49b156543755db454e046426fea` |
| `01_pacific_evidence_map.svg` | `d089a001dda9532ceb874fa42079c7d43971cb1d2ada93bca4cb3d9cf271f407` |
| `02_observation_coverage.png` | `991e4d64bc615388b36949400a423f78c6568e4b30c3a0ef7ed7e6a8c9021dca` |
| `02_observation_coverage.svg` | `306132709fdc3dcbcd5d7c84322cab862e6f131307f8acb4d3ffba4fa98c3d70` |
| `03_station_timeseries.png` | `48fd2793a08f012f9714f3a8ed6b814614cfd1ed2a8dac2aba91b7cd1f5f3482` |
| `03_station_timeseries.svg` | `a8bb88f4878d0d2cbb8eb52fe2d610e29b00b44e15c69630b0bf4f6a001efffe` |
| `04_distance_contour_diagnostic.png` | `9ed1767ab65b425e09fb243cdeabb29dd773a51f07f7a03528aabd7ca55c40a7` |
| `04_distance_contour_diagnostic.svg` | `64d0ac653736f5776d728f9aa87ed2deba2fcfa0dcb16e763f0de46b2ec9684e` |
| `atlas-manifest.json` | `4101db77d8104e8d422fc5ab96f7a5ef2200e1d51db1ddfead6fa10fb52495e1` |
| `decision-ledger.csv` | `a4c1aade238e5696bdeb76a1b20349989b511f5ef101348328e684af77895a62` |
