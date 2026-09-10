# Tōhoku Normalization and Data-Quality Report

## Disposition

T-002C has an accepted 2026-09-05 baseline, and independent scientific-data
review accepted the 2026-09-08 Saipan revision. The current T-002C2 candidate
adds authenticated IOC Valparaíso radar observations plus a checksummed pressure
companion without changing the continuous NCTR-field blocker.

- Run ID: `2026-09-05__1958__quality__5f920f2`
- Build Git SHA: `5f920f2`
- Mode: offline, checksum-gated normalization
- Input inventory:
  `artifacts/logs/runs/2026-09-05__1906__accepted__e602131/outputs.json`
  (`6141ea3f4a49eeb9a98f2a09188fa9b9c7a930e828f1c1897e19ad2a59fef5ca`)
- Contract: `config/tohoku-data-proof.toml`
  (`37d61c3576c4d968e60be3aa408f74124a6a4487f8b0c149ff1872bb104ce1b5`)
- Portable evidence:
  `artifacts/logs/runs/2026-09-05__1958__quality__5f920f2/`

The current candidate uses acquisition inventory
`artifacts/logs/runs/2026-09-09__1923__valparaiso-reviewed__7576ffb/outputs.json`
and build tag `2026-09-09-valparaiso-reviewed-7576ffb-a`. Its raw-data evidence
is portable; its processed tables remain ignored and reproducible from the
tracked contract and parser.

A second build with tag `2026-09-09-valparaiso-reviewed-7576ffb-b` produced the
same seven output checksums; byte comparison of `observation.csv` and
`accounting.json` returned no differences.

The two current build commands used the accepted Valparaíso-rerun inventory,
current contract, repository root, and distinct run tags
`2026-09-09-valparaiso-reviewed-7576ffb-a` and
`2026-09-09-valparaiso-reviewed-7576ffb-b`. Byte comparison returned no
differences.
Opening a build never performs network access, and existing output tags are not
overwritten.

## Source coverage

The current denominator is 18 contracted source assets: 17 are approved and
cached or downloaded (94.4%), and 1 is blocked. Valparaíso radar is the
normalized higher-coverage series; pressure is a coverage-only quality
companion and is not counted as another station. No gauge was substituted.

| Source group | Source IDs | Input SHA-256 / state | Normalized disposition |
| --- | --- | --- | --- |
| USGS event | `usgs-tohoku-origin-csv` | `bcc2a073...8337e` | one event row |
| NCEI TTT | `ncei-ttt-tohoku-layer17-geojson`; `ncei-ttt-tohoku-layer17-metadata` | `77a64b82...7b28`; `0c8f90ca...4a5a5` | 4,380 contour parts; metadata validates identity and CRS |
| NCTR | `nctr-tohoku-source-coefficients`; `nctr-tohoku-model-field` | `f2df0f70...b7ab`; blocked | coefficients retained as coverage-only evidence; continuous field absent |
| DART | `ncei-dart-21413-20110301to20110320`; `21418`; `32401`; `46411` | `6a271680...b007`; `13706104...3333`; `c83bb772...4af`; `7632cfc7...9ea` | four stations; 121,722 accepted observations and 90 quarantined rows |
| CO-OPS | Adak `9461380`; Crescent City `9419750`; Hilo `1617760`; Pago Pago `1770000` | `b4079253...c332`; `6b22f20a...974b`; `f958e362...b143`; `fbac9c7c...c857` | four coastal series; 16,897 rows |
| NTWC/UHSLC Saipan | `ntwc-uhslc-saipan-20110311`; archival companions `20110312`, `20110313` | `42ff98b7...cfe5`; `bc4fcdeb...5f69`; `fc35c8a8...735b0` | 764 accepted event-day observations; all 16 rows at 8 conflicting timestamps quarantined; later days retained coverage-only |
| IOC/SHOA Valparaíso | radar `ioc-valparaiso-rad-20110311to20110314`; pressure companion `ioc-valparaiso-prs-20110311to20110314` | `17abf35d...3233`; `c5098210...717d` | 4,272 radar observations normalized; 4,270 pressure samples retained as checksummed quality evidence |

Full source IDs, complete SHA-256 values, paths, publishers, URLs, units, time
bases, datum notes, and redistribution notes are preserved in the run bundle,
accepted acquisition bundle, source contract, and provenance manifest.

IOC sample accounting is explicit at source grain: radar is
`4,272 input = 4,272 accepted + 0 rejected`, with 4,272 observation outputs;
pressure is `4,270 input = 4,270 accepted + 0 rejected`, with zero observation
outputs because it is a quality companion. Both pass the same pagination,
sensor, timestamp, finite-value, QC-flag, and duplicate-time parser contract.

## Output contract and reconciliation

| Table | Grain | Primary key | Rows | Columns | Duplicate keys | Required-field null rows |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `event.csv` | one reviewed event origin | `event_id` | 1 | 8 | 0 | 0 |
| `ttt_contour.csv` | one source contour part | `contour_id` | 4,380 | 8 | 0 | 0 |
| `station.csv` | one selected station/gauge identity | `station_id` | 10 | 14 | 0 | 0 |
| `observation.csv` | one station sample | `observation_id` | 143,655 | 11 | 0 | 0 |
| `rejected_record.csv` | one rejected source asset or record | `rejection_id` | 107 | 5 | 0 | 0 |

`schemas.json` records the field-level contract. `accounting.json` reconciles
every input at its actual grain: assets, TTT features and parts, station samples,
accepted records, rejected records, and outputs. There are no duplicate
station/timestamp pairs, no source-time nulls, and no within-file time inversions.

| Output | SHA-256 |
| --- | --- |
| `accounting.json` | `331617e5ed4a9e747ec79364409659e723cd7ece5b20f6cc1b197a40e1abaf83` |
| `event.csv` | `bd1e11e9322f8670f016eeea4820f83ddca811d20fd52395d12405cd86d9ba82` |
| `observation.csv` | `9daee574ea2b75c72c8bfb7984a32c248fa8692a2b74ba705ac7848089f52be3` |
| `rejected_record.csv` | `e2d8e86cfead1713036cee2883007a513fc0155d8c6b84f954e757ce72d14310` |
| `schemas.json` | `84cf050ffc0870b262ad0a5daffbd247b7b052632b4c80fa56c45c6d899d0bac` |
| `station.csv` | `d4ad18dafca36e027242095d81a81a3c70ecce59ee3027fbc9f9d077689f5004` |
| `ttt_contour.csv` | `53f2efd57327e69f196a6ce25417e451ff3366dd3e9f4185ddbe4d764c3caed4` |

## Event and contour quality

The event table contains reviewed USGS event
`official20110311054624120_30` at `2011-03-11T05:46:24.120Z`, latitude
38.297, longitude 142.373, depth 29.0 km, and magnitude 9.1 `mww`.

The TTT metadata gate confirms layer `2011/3/11 Tohoku, Japan`, polyline
geometry, and WKID 4326 before the GeoJSON is parsed. All 72 source features are
accepted and expand deterministically to 4,380 parts and 62,988 vertices. The
72 available `HOURS` values are 1 through 70 plus 74 and 75; 71 through 73 are
absent in the source. The normalized extent is longitude
[-179.99999999990004, 180.00000000010004] and latitude
[-77.99997792933794, 87.59715345366902]. Twenty-four parts retain tiny
publisher values just above +180 degrees and are explicitly precision-flagged;
none are silently clamped, none have a segment jump over 180 degrees, and none
are labeled as antimeridian crossings.

## Observation quality

All observation timestamps are normalized to UTC while retaining the exact
source time. The four DART tables cover `2011-03-01T00:00:00Z` through
`2011-03-20T00:00:00Z`. DART raw, fitted, and residual measurements remain in
`m water column`; their vertical reference is explicitly `unknown`. CO-OPS
values remain in meters relative to requested station datum `STND`, with GMT as
the query time basis. DART and coastal values are not combined as if their
vertical references were interchangeable.

The observation table has 1,049 raw nulls (0.7302% overall), all from CO-OPS.
All 21,933 coastal rows—16,897 CO-OPS, 764 Saipan, and 4,272
Valparaíso—correctly have null fitted and residual fields because those
DART-specific fields do not exist in the coastal sources. Saipan keeps the
paired source epoch in `source_extra`. Valparaíso retains one numeric zero with
its publisher QC flag; fixture tests independently prove that valid zero is not
converted to NoData.

| Station | Accepted rows | Raw nulls | Window | Raw range | Cadence / continuity |
| --- | ---: | ---: | --- | --- | --- |
| DART 21413 | 4,151 | 0 | Mar 1 00:00 to Mar 20 00:00 UTC | 5824.28007–5825.87007 | intervals 15, 45, 60, 900, 960 s; 2 over 900 s |
| DART 21418 | 4,958 | 0 | Mar 1 00:00 to Mar 20 00:00 UTC | 5661.43731–5664.31131 | intervals 15, 30, 45, 60, 120, 180, 900, 960, 4500, 8100 s; 15 over 900 s |
| DART 32401 | 3,191 | 0 | Mar 1 00:00 to Mar 20 00:00 UTC | 4798.13994–4799.12291 | intervals 15, 30, 45, 60, 900, 960 s; 2 over 900 s |
| DART 46411 | 109,422 | 0 | Mar 1 00:00 to Mar 20 00:00 UTC | 4259.14838–4260.92811 | intervals 15 and 300 s; none over 900 s |
| Hilo 1617760 | 4,320 | 29 (0.671%) | Mar 11 00:00 to Mar 13 23:59 UTC | -0.123–2.689 m | complete 60 s timestamps; 99.329% usable requested window |
| Pago Pago 1770000 | 3,937 | 936 (23.774%) | Mar 11 00:00 to Mar 13 17:36 UTC | 0.537–2.363 m | 60 s within response; 383-row tail absent; 69.468% usable requested window |
| Crescent City 9419750 | 4,320 | 60 (1.389%) | Mar 11 00:00 to Mar 13 23:59 UTC | -0.396–3.932 m | complete 60 s timestamps; 98.611% usable requested window |
| Adak 9461380 | 4,320 | 24 (0.556%) | Mar 11 00:00 to Mar 13 23:59 UTC | 0.446–3.068 m | complete 60 s timestamps; 99.444% usable requested window |
| Saipan `saip` | 764 | 0 | Mar 11 00:00 to 23:59 UTC | 1.273–2.578 m MLLW | 732 intervals of 60 s; all 16 rows at 8 conflicting timestamps quarantined; 12:08–23:07 absent; 53.056% of event-day minute positions retained |
| Valparaíso `valp` radar | 4,272 | 0 | Mar 11 00:01 to Mar 13 23:55 UTC | 0–6.222 m; datum unknown | unique minute timestamps; 48 of 4,320 nominal positions absent; 98.889% retained; one zero preserved with `out_of_range=T` |

DART has documented mixed reporting cadences, so an interval change is not by
itself called a gap. The table above reports observed post-quarantine intervals;
the longer 4,500 and 8,100 second intervals at 21418 and all intervals over 900
seconds are explicit follow-up targets for adaptive EDA. DART residual identity
checks show a maximum absolute error of about `0.00002` m for
`raw - fitted - residual`, consistent with the source's five-decimal rounded
fields. Per-station residual median/MAD pairs are 21413 `0.02632/0.01474`,
21418 `-0.03392/0.031195`, 32401 `-0.00165/0.00869`, and 46411
`0.01024/0.00834` m; these are quality descriptors, not arrival picks.

## Rejections and adaptive finding

There are 107 explicit rejections: 1 blocked source asset, 90 DART records, and
16 Saipan rows belonging to 8 conflicting duplicate timestamps. The blocked
asset is the continuous NCTR field. DART
rejections by source are 2 at 21413, 67 at
21418, 2 at 32401, and 19 at 46411 (90 of 121,812 input rows; 0.0739%).

Saipan retains valid 1-, 59-, 60-, 61-, 119-, 120-, and 121-second source
intervals rather than rounding them onto a fabricated minute grid. Every source
row at a duplicate UTC timestamp is quarantined with its stable source-row
identity; file order is not used to choose among conflicting water levels. The
long source gap is visible and is not interpolated.

The initial profile exposed exact `9999.00000` values in named DART raw and/or
residual measurement columns while the paired fitted value remained ordinary.
This is physically implausible as meters of water column, but the source
documentation audited for this task does not establish the marker's precise
semantics. The pipeline therefore does not guess that it means null: it
quarantines the entire row as `unexpected_sentinel`, retains the source and line
identity, and excludes it from analysis tables. A fresh deterministic double
build after this change contains zero retained `9999` rows.

## Manual scientific QA

Three TTT parts were traced from raw feature properties and coordinates through
normalization:

- OBJECTID 4 / 1 hour / part 1: 150 vertices, first
  `[139.39765238484972, 34.650624710562]`, last
  `[141.7707211849348, 40.39796390550987]`.
- OBJECTID 8 / 2 hours / part 1: 377 vertices, first
  `[134.19233214541225, 33.234613604534275]`, last
  `[146.3141001097323, 44.47940768191904]`.
- OBJECTID 12 / 3 hours / part 1: 4 vertices, first
  `[128.6821672820945, 27.487274409586405]`, last
  `[128.84517472783148, 27.676710857320245]`.

The first raw and normalized DART rows agree for all four stations: at
`2011-03-01T00:00:00Z`, 21413 retains raw/fitted/residual
`5825.08940/5825.09320/-0.00379`; 21418 retains
`5662.89485/5662.88318/0.01167`; 32401 retains
`4798.96262/4798.97020/-0.00758`; and 46411 retains
`4259.22668/4259.23417/-0.00749` plus unnamed source extra `1.964`.
The source Julian value `60.000000` remains in `source_time`.

The six available coastal records also agree with their respective raw sources:
Hilo `1.309`, Pago Pago `1.647`, Crescent City `2.508`, and Adak `1.113` m.
Their source station IDs and coordinates agree with each raw metadata block.
Saipan begins at `2.239` m MLLW; its exact header states UTC/meters/MLLW and
coordinates `15.2266, 145.742`, while its station identifier is `none`, so the
normalized ID remains the archive code `saip`. Valparaíso radar begins at
`4.462` m at `2011-03-11T00:01:00Z`, preserves the source zero at
`2011-03-12T01:30:00Z` with `out_of_range=T`, and ends at `4.965` m at
`2011-03-13T23:55:00Z`. Its raw and normalized values, UTC timestamps, sensor
identity, and QC flags agree in all three traces.

## Interpretation, limitations, and next steps

Independent review accepted T-002C2, so the revised source subset is
structurally consistent enough for T-002D to inspect TTT contours, four DART
series, and six coastal series. It is not
sufficient for claims requiring the requested continuous NCTR field, direct
cross-datum level comparisons, or complete Pago Pago coverage.

Important limits remain: source horizontal datums are often unknown; DART's
vertical reference is unknown; CO-OPS series use station-specific STND;
redistribution terms still require per-asset review; TTT origin-reference
semantics are not stated in the geometry asset; and this retrospective dataset
is not an operational warning product.

The corrected T-002C2 maker checks reconcile source identity, checksums, accounting, table
contracts, time/unit/datum handling, deterministic output, rejections, and the
manual traces above. The pressure companion shares 4,270 timestamps with radar;
radar has two additional timestamps. Their median absolute-level offset is
1.891 m, which is not interpreted because the vertical datum is unknown.
Independent re-review found no remaining blocking issues. T-002D may begin with
its fixed core profile and branch only from recorded findings. Immediate
evidence-led questions are the DART cadence transitions, Pago Pago missingness,
Valparaíso QC-flag sensitivity, the 24 near-180-degree contour precision flags,
and station-to-contour join completeness. Arrival rules and station inclusion
remain frozen before residual sensitivity is viewed.

## Downstream missingness profile

T-002D run `2026-09-09__1749__missingness__7b6d386` re-read the accepted build
without changing it. It confirms 1,049 retained raw-value blanks, 21,933
structurally inapplicable coastal fitted/residual rows, 2,276 unavailable
exact-minute coastal positions out of 23,040, 90 quarantined DART sentinel rows
out of 121,812 source rows, 17 approved source assets, and 1 blocked asset.

The calculations and exact input/output hashes are in
`scripts/profile_missingness.py`, `pipeline/missingness.py`, the run bundle, and
`context/EDA_REPORT.md`. Five task-owned tests cover the distinctions and the
real local MLflow record. No imputation, timestamp snapping, silent row repair,
or station removal occurs. Pooled MCAR is not supported; upstream cause remains
unknown where publisher outage, maintenance, telemetry, or QC evidence is
absent.
