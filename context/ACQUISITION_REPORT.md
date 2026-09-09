# T-002A — Tōhoku Source-Contract Ledger

## Disposition

Source discovery recorded an accepted 15-asset baseline on 2026-09-05. After
the Saipan and Valparaíso recovery revisions, the current ledger records 18
exact assets: 17 are approved and locally checksummed, while only the NCTR
continuous field remains blocked. The clean committed baseline
evidence bundles `2026-09-05__1906__accepted__e602131` and
`2026-09-05__1906__accepted-rerun__e602131` each recorded 12 `cached` and 3
`blocked` outcomes totaling 12,386,361 bytes. Both have Git SHA `e602131`,
`working_tree: clean`, and `evidence_disposition: ready-for-review`; every
outcome's byte count and checksum is identical between the two bundles. The
machine-readable ledger is
`artifacts/provenance/source-manifest.csv`; exact contracts are in
`config/tohoku-data-proof.toml`.

## Valparaíso recovery evidence

The authorized IOC credential is held in macOS Keychain and is added only as an
`X-API-KEY` header for the exact IOC API hostname. It is absent from URLs,
configuration, run bundles, command output, and Git. Live run
`2026-09-09__1838__valparaiso-recovery__9cc448c` recorded 15 cached, 2
downloaded, and 1 blocked outcomes. The two downloaded IOC responses total
1,893,995 bytes. Cache rerun
`2026-09-09__1838__valparaiso-recovery-rerun__9cc448c` recorded 17 cached and 1
blocked outcome with the same 14,361,473-byte inventory and identical hashes.

The source-preferred one-sensor response selected radar for the full window, so
the explicit `rad` response is the normalized series. The explicit `prs`
response is a checksummed quality companion. Both cover the exclusive-end
request `2011-03-11` through `2011-03-14`, report metres, contain one sensor
identity and unique UTC timestamps, and preserve publisher QC flags. The API
requests disable 30-day mean subtraction, timestamp fitting, and every
value-removing QC filter. The vertical datum and horizontal datum remain
`unknown`.

## Saipan recovery evidence

The browser-controlled click on NOAA's exact `.070` link reproduced HTTP 403;
a separate request with the event page as referrer also returned 403. The
Internet Archive CDX index exposed HTTP-200 captures from 2016-12-22 for the
same three NOAA URLs. Live acquisition run
`2026-09-09__0142__saipan-recovery__92c438c` recorded 12 cached, 3 downloaded,
and 2 blocked outcomes: 17 total assets and 12,467,478 bytes. The three new raw
files total 81,117 bytes and have matching `.sha256` sidecars.

The files self-identify as Saipan/UHSLC continuous NGWLMS observations via GOES,
in meters, UTC, nominal one-minute cadence, MLLW, NTWC, and unfiltered. They give
coordinates `15.2266, 145.742` and pair Unix epoch seconds with
`YYYYMMDDhhmmss`. The source station identifier is `none`, so the contract uses
archive code `saip` and does not claim CO-OPS ID `1633227`. Day `.070` is the
normalization input; `.071` and `.072` are checksummed archival companions.

## T-002B clean live evidence

Command: `uv run python scripts/acquire_tohoku.py --config
config/tohoku-data-proof.toml --root . --run-tag accepted`

- Accepted bundle: `2026-09-05__1906__accepted__e602131`; 12 `cached`, 3
  `blocked`, 12,386,361 total bytes, config SHA-256
  `4d253132699d07417206827e65528cf342cff558d3b254f9be99c740ad33b979`.
- Cache proof command: `uv run python scripts/acquire_tohoku.py --config
  config/tohoku-data-proof.toml --root . --run-tag accepted-rerun`
- Accepted-rerun bundle: `2026-09-05__1906__accepted-rerun__e602131`; 12
  `cached`, 3 `blocked`, with every output byte count and SHA-256 identical to
  the accepted bundle. Blocked contracts were not fetched.

Each portable bundle contains `meta.json`, `config.json`, `inputs.json`,
`outputs.json`, `metrics.json`, and `notes.md`. Independent data-quality review
accepted the bundle/manifest/raw/sidecar reconciliation, verified that all raw
assets remain ignored and untracked, and confirmed that blocked sources were not
replaced with proxies. T-002B is accepted and T-002C may proceed.

Manual source identity checks on the acquired raw cache found:

- USGS `official20110311054624120_30`: origin
  `2011-03-11T05:46:24.120Z`, latitude `38.297`, longitude `142.373`, depth
  `29 km`, magnitude `9.1 mww`.
- NCEI TTT GeoJSON begins with `OBJECTID`/`HOURS` pairs `4/1`, `8/2`, and
  `12/3`; each is a `MultiLineString` named `2011 Japan`.
- DART first records identify the selected source files and their row counts:
  21418 (5,025), 21413 (4,153), 46411 (109,441), and 32401 (3,193). The raw
  records retain the source's unnamed eleventh token.
- CO-OPS JSON metadata identifies Adak Island 9461380 (`51.8606`, `-176.6376`),
  Hilo 1617760 (`19.7303`, `-155.0556`), Crescent City 9419750 (`41.7456`,
  `-124.1844`), and Pago Pago 1770000 (`-14.28`, `-170.69`), with 4,320,
  4,320, 4,320, and 3,937 rows respectively.

## Authoritative evidence and observed smoke checks

- [USGS FDSN CSV](https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&eventid=official20110311054624120_30), [service version](https://earthquake.usgs.gov/fdsnws/event/1/version), [ComCat terms](https://earthquake.usgs.gov/data/comcat/data-eventterms.php), [citation](https://doi.org/10.5066/F7MS3QZH), and [USGS copyright policy](https://www.usgs.gov/faqs/are-usgs-reportspublications-copyrighted): reviewed one CSV record for `official20110311054624120_30`, origin `2011-03-11T05:46:24.120Z`, `38.297`, `142.373`, depth `29 km`, magnitude `9.1 mww`, update `2026-08-15T23:03:39.669Z`. The compact CSV, rather than GeoJSON, is the T-002B contract.
- [NCEI layer metadata](https://gis.ngdc.noaa.gov/arcgis/rest/services/ttt_contours/MapServer/17?f=pjson), [ordered GeoJSON](https://gis.ngdc.noaa.gov/arcgis/rest/services/ttt_contours/MapServer/17/query?where=1%3D1&outFields=OBJECTID%2CHOURS%2CName%2CIndex&returnGeometry=true&outSR=4326&orderByFields=OBJECTID%20ASC&f=geojson), [feature count](https://gis.ngdc.noaa.gov/arcgis/rest/services/ttt_contours/MapServer/17/query?where=1%3D1&returnCountOnly=true&f=json), [travel-time semantics](https://www.ncei.noaa.gov/products/natural-hazards/tsunamis-earthquakes-volcanoes/tsunamis/travel-time-maps), and [archive policy](https://www.ncei.noaa.gov/archive): observed layer `2011/3/11 Tohoku, Japan`, WKID 4326, 72 LineString/MultiLineString features, `HOURS` 1–70, 74, and 75, and non-contiguous `OBJECTID`. Twenty-four vertices about `1e-10` degrees over +180 are retained as source boundary precision; no segment jumps over 180 degrees.
- [NCEI DART event page](https://www.ngdc.noaa.gov/hazard/dart/2011honshu_dart.html) says its real-time records were extracted from NDBC. The [NDBC Web Data Guide](https://www.ndbc.noaa.gov/docs/ndbc_web_data_guide.pdf) defines its `YYYY MM DD hh mm ss` examples as UTC, establishing the calendar-field time basis for the selected records; Julian day is retained as a separate source field. Source-defined near-field stations are 21418 and 21413. Pre-residual geographic far-field stations are 46411 (northeast Pacific) and 32401 (southeast Pacific). The documented ten-field layout conflicts with an observed eleventh token in sampled rows; it is retained as an unnamed source extra and is not interpreted.
- [CO-OPS Data API contract](https://api.tidesandcurrents.noaa.gov/api/prod/): exact one-minute-water-level queries request `STND`, `gmt`, and metric units for 2011-03-11 through 2011-03-13. Observed rows were Adak 9461380: 4320, Hilo 1617760: 4320, Crescent City 9419750: 4320, and Pago Pago 1770000: 3937; Pago Pago missingness is material. Raw values are preliminary and meters relative to station datum.
- [IOC Valparaíso station metadata](https://www.ioc-sealevelmonitoring.org/ssc/stationdetails.php?id=SSC-valp), [IOC API documentation](https://api.ioc-sealevelmonitoring.org/v2/doc), and the [official API guide](https://github.com/SLSMF/API-Documentation/blob/main/API_description.md): the `valp` station endpoint identifies SHOA and coordinates `-33.02767128, -71.62787275`; the authenticated research responses contain 4,272 radar and 4,270 pressure rows. The OpenAPI declares metres for `slevel`, an exclusive `timestop`, and CC BY 4.0. The official example interprets `stime` as UTC.
- Exact NOAA event links for [Saipan `.070`](https://www.tsunami.gov/previous.events/03-11-11_Honshu/Data/saip_A_2011.070), [`.071`](https://www.tsunami.gov/previous.events/03-11-11_Honshu/Data/saip_A_2011.071), and [`.072`](https://www.tsunami.gov/previous.events/03-11-11_Honshu/Data/saip_A_2011.072) still return HTTP 403, but preserved copies of those exact URLs supplied verifiable headers and bytes. The analogous Valparaíso PTWC links remain inaccessible, but they are no longer a coverage blocker because the official IOC research API supplied the contracted series directly.
- [NCTR event page](https://nctr.pmel.noaa.gov/honshu20110311/), [model comparison/source page](https://nctr.pmel.noaa.gov/honshu20110311/honshu20110311-modeldata.html), and [propagation database access page](https://nctr.pmel.noaa.gov/propagation-database-access.html): the event page publishes the scalar source weights recorded below, but no current stable HTTPS continuous event-specific machine-readable field, grid/time metadata, unit-source combination, or unshifted coastal series was found.

## Approved contracts — 17 assets

| Class | Exact assets | Contract notes |
| --- | --- | --- |
| Event | USGS FDSN CSV | One reviewed event record; latitude/longitude are WGS84; depth reference remains unknown. |
| Modeled contours | NCEI layer 17 metadata JSON and ordered GeoJSON | Preserve geometry and antimeridian boundary precision; asset-specific terms and derivation details remain unknown. |
| Model source | NCTR scalar coefficients | Publishable source-page weights: `4.66*kiszb24 + 12.23*kiszb25 + 26.31*kisza26 + 21.27*kiszb26 + 22.75*kisza27 + 4.98*kiszb27`. Units are unstated; unit-source parameters are in NOAA PMEL Technical Memorandum 139. |
| DART observations | 21418, 21413, 46411, 32401 | Selection precedes residual inspection. NCEI traces real-time records to NDBC, whose guide defines the calendar fields as UTC; Julian day remains separate source data. Water-column series are meters. |
| Coastal observations | Adak 9461380, Hilo 1617760, Crescent City 9419750, Pago Pago 1770000, Saipan `saip` `.070`, and Valparaíso `valp` radar | CO-OPS sources request `one_minute_water_level`, `STND`, `gmt`, metric JSON. Saipan is source-declared UTC/meters/MLLW. IOC Valparaíso is source-declared UTC/metres with unknown datum and retains all QC flags. |
| Coastal archival companions | Saipan `saip` `.071` and `.072` | Exact preserved NOAA event files; checksummed and retained for possible extended-tail EDA, not normalized in the event-day proof. |
| Coastal quality companion | Valparaíso `valp` pressure | Exact IOC response retained for sensor-quality comparison; not normalized as a second station series. |

## Blocked contracts — 1 asset

| Requested asset | Blocker | Required treatment |
| --- | --- | --- |
| NCTR model field | No stable event-specific machine-readable HTTPS field, units, grid/time metadata, or source combination | Keep blocked; images and shifted plots are not proxies. |

## Contract limits and next steps

The ledger uses source-owned values only. It does not infer a CRS, horizontal or
vertical datum, coordinate order, source-time basis, or units where a publisher
does not state them. `unknown` therefore remains a release blocker for the
affected interpretation. The NCEI contour product lacks asset-specific
authorship/terms, exact epicenter, TTT version, bathymetry version, and
derivation parameters. DART's eleventh token must remain unparsed unless its
publisher names it.

Each contract also records a conservative, whitespace-tolerant response prefix
for T-002B identity checks. This is only an acquisition guard; the full parser
and row-level validation remain T-002C responsibilities. An explicit `reason`
is present on every contract: `not applicable` for approved assets and the
source-specific access/contract blocker for blocked assets.

The baseline T-002B run acquired 12 approved exact assets. The Saipan and
Valparaíso recovery runs bring the local checksum-gated cache to 17 approved
assets and record actual byte counts, checksums, safe response headers, and
response counts. They did not download the blocked NCTR asset or replace it with
a proxy. Independent review of T-002C2 is the remaining gate before T-002D.
