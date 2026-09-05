# Tōhoku Normalization and Data-Quality Report

## Disposition

T-002C is ready for independent scientific-data review. The candidate is
analysis-ready for the source classes actually acquired, subject to the explicit
limitations below; it is not yet an accepted EDA input and does not supply a
continuous NCTR model field.

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

The two build commands used the accepted inventory, current contract, repository
root, and distinct run tags `2026-09-05-1958-quality-a-5f920f2` and
`2026-09-05-1958-quality-b-5f920f2`. `diff -rq` returned no differences.
Opening a build never performs network access, and existing output tags are not
overwritten.

## Source coverage

The denominator remains all 15 contracted sources: 12 are approved and cached
(80%), and 3 are blocked. No proxy replaced a failed source.

| Source group | Source IDs | Input SHA-256 / state | Normalized disposition |
| --- | --- | --- | --- |
| USGS event | `usgs-tohoku-origin-csv` | `bcc2a073...8337e` | one event row |
| NCEI TTT | `ncei-ttt-tohoku-layer17-geojson`; `ncei-ttt-tohoku-layer17-metadata` | `77a64b82...7b28`; `0c8f90ca...4a5a5` | 4,380 contour parts; metadata validates identity and CRS |
| NCTR | `nctr-tohoku-source-coefficients`; `nctr-tohoku-model-field` | `f2df0f70...b7ab`; blocked | coefficients retained as coverage-only evidence; continuous field absent |
| DART | `ncei-dart-21413-20110301to20110320`; `21418`; `32401`; `46411` | `6a271680...b007`; `13706104...3333`; `c83bb772...4af`; `7632cfc7...9ea` | four stations; 121,722 accepted observations and 90 quarantined rows |
| CO-OPS | Adak `9461380`; Crescent City `9419750`; Hilo `1617760`; Pago Pago `1770000` | `b4079253...c332`; `6b22f20a...974b`; `f958e362...b143`; `fbac9c7c...c857` | four coastal series; 16,897 rows |
| Blocked coastal | Saipan `1633227`; Valparaíso `valp` | not downloaded | station identity and blocker retained; no observations |

Full source IDs, complete SHA-256 values, paths, publishers, URLs, units, time
bases, datum notes, and redistribution notes are preserved in the run bundle,
accepted acquisition bundle, source contract, and provenance manifest.

## Output contract and reconciliation

| Table | Grain | Primary key | Rows | Columns | Duplicate keys | Required-field null rows |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `event.csv` | one reviewed event origin | `event_id` | 1 | 8 | 0 | 0 |
| `ttt_contour.csv` | one source contour part | `contour_id` | 4,380 | 8 | 0 | 0 |
| `station.csv` | one selected station/gauge identity | `station_id` | 10 | 14 | 0 | 0 |
| `observation.csv` | one station sample | `observation_id` | 138,619 | 11 | 0 | 0 |
| `rejected_record.csv` | one rejected source asset or record | `rejection_id` | 93 | 5 | 0 | 0 |

`schemas.json` records the field-level contract. `accounting.json` reconciles
every input at its actual grain: assets, TTT features and parts, station samples,
accepted records, rejected records, and outputs. There are no duplicate
station/timestamp pairs, no source-time nulls, and no within-file time inversions.

| Output | SHA-256 |
| --- | --- |
| `accounting.json` | `ad581a22b900883ce5e35849cb573533d4a4e49d49caa23aedb947319de62413` |
| `event.csv` | `bd1e11e9322f8670f016eeea4820f83ddca811d20fd52395d12405cd86d9ba82` |
| `observation.csv` | `628a9c836f922b17bafb52876b06f7a2df0af12c48fbf85399cf792113a4a7ff` |
| `rejected_record.csv` | `72d93c72ff6d0e9a7e62bf58889f142e5f74e40757616ee5110f501697d03fed` |
| `schemas.json` | `84cf050ffc0870b262ad0a5daffbd247b7b052632b4c80fa56c45c6d899d0bac` |
| `station.csv` | `d88a05b792576ed822616ff8643cc7bc1bf6ba488654ef5f5bbf97824b1f81bb` |
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

The observation table has 1,049 raw nulls (0.7568% overall), all from CO-OPS.
The 16,897 CO-OPS rows correctly have null fitted, residual, and unnamed-extra
fields because those fields do not exist in that source. No normalized zero was
observed in this live bundle, but fixture tests prove that a valid zero is
preserved and is not converted to NoData.

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

There are 93 explicit rejections: 3 blocked source assets and 90 DART records.
The blocked assets are the continuous NCTR field, Saipan observations, and
Valparaíso observations. DART rejections by source are 2 at 21413, 67 at
21418, 2 at 32401, and 19 at 46411 (90 of 121,812 input rows; 0.0739%).

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

The four available coastal records also agree at `2011-03-11T00:00:00Z`:
Hilo `1.309`, Pago Pago `1.647`, Crescent City `2.508`, and Adak `1.113` m.
Their source station IDs and coordinates agree with each raw metadata block.
Saipan remains a station row plus blocked-source rejection after CO-OPS returned
no data and other exact candidates lacked verifiable access/schema. Valparaíso
likewise remains a station row plus blocked-source rejection because the
authoritative historical endpoint requires an API key and alternate exact files
could not be verified. Neither was substituted.

## Interpretation, limitations, and next steps

The accepted source subset is structurally consistent enough for T-002D to
inspect TTT contours, four DART series, and four coastal series while keeping six
coastal candidates in the denominator. It is not sufficient for claims requiring
the requested continuous NCTR field, direct cross-datum level comparisons, or
complete Saipan/Valparaíso/Pago Pago coverage.

Important limits remain: source horizontal datums are often unknown; DART's
vertical reference is unknown; CO-OPS series use station-specific STND;
redistribution terms still require per-asset review; TTT origin-reference
semantics are not stated in the geometry asset; and this retrospective dataset
is not an operational warning product.

If the independent checker accepts T-002C, T-002D should begin with its fixed
core profile and then branch only from recorded findings. Immediate evidence-led
questions are the DART cadence transitions and long intervals, Pago Pago's
missing values and truncated tail, the 24 near-180-degree contour precision
flags, and whether station-to-contour joins are sufficiently complete. Arrival
rules and station inclusion remain frozen before residual sensitivity is viewed.
