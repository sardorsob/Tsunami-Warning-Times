# Blocked-source access options

Access checked against official sources on 2026-09-08. A blocked contract means
the automated proof could not establish an exact, reproducible source contract;
it does not necessarily mean that the data can never be obtained.

## Scope clarification

Tōhoku names the earthquake and source region in northeastern Honshū. The
project's observational and modeled scope is Pacific-wide: its accepted TTT
contours cover the Pacific basin, while DART and coastal stations include Japan,
Alaska, Hawaiʻi, American Samoa, California, and the southeast Pacific.

## Valparaíso (`valp`)

**Recovered on 2026-09-09 through the official authenticated research API.**

The [IOC Sea Level Station Monitoring Facility API](https://api.ioc-sealevelmonitoring.org/)
instructs users to register an account, edit the account, and request membership
in `Access gauges API (gauges_API)` to obtain version 2 API keys. Its
[version 2 documentation](https://api.ioc-sealevelmonitoring.org/v2/doc)
provides the research endpoint
`/v2/research/stations/{code}/sensors/{sensor}/data`, with up to 365 days per
request. The [official Valparaíso catalog record](https://www.ioc-sealevelmonitoring.org/ssc/stationdetails.php?id=SSC-valp)
lists one-minute `prs` and `rad` sensors and research-quality data spanning
1944-01-02 through 2018-12-31, which includes March 2011.

The credential is stored in macOS Keychain under the project-specific service
`org.ioc-sealevelmonitoring.api` and account `tsunami-warning-times`. The
acquisition client reads it only in memory, sends it only in `X-API-KEY` to the
exact IOC HTTPS hostname, and refuses authenticated redirects. The credential
does not appear in configuration, URLs, logs, run evidence, or Git.

Explicit `rad` and `prs` requests cover `2011-03-11` through the exclusive
`2011-03-14` endpoint in one page. They disable 30-day mean subtraction,
timestamp fitting, and all value-removing QC filters while requesting QC flags.
The full-window source-preferred response selected radar, so its 4,272 unique
timestamps are normalized. The 4,270-row pressure response is checksummed as a
quality companion. The two sensors share 4,270 timestamps; radar has two
additional timestamps. The source declares metres and the official example
interprets `stime` as UTC, but no verified vertical datum or horizontal datum is
assigned. The approximately 1.891 m median inter-sensor level offset is therefore
recorded but not interpreted as an error or a common-datum comparison.

## Saipan

**Recovered on 2026-09-08 from preserved copies of the exact NOAA event files.**

The [NOAA/NWS 2011 Honshu event archive](https://www.tsunami.gov/previous.events/?p=03-11-11_Honshu)
lists Saipan and links exact `.070`, `.071`, and `.072` event files. A browser
click and a separate HTTP request both reproduced the server's HTTP 403 response,
so browser authentication was not the missing piece. The Internet Archive CDX
index records 2016-12-22 HTTP-200 captures of those exact NOAA URLs. Their raw
captures were downloaded and checksummed without rewriting the source bytes.

The headers identify `Saipan,_USA`, UHSLC, continuous NGWLMS observations,
coordinates `15.2266, 145.742`, meters, UTC, nominal one-minute sampling, MLLW,
NTWC, unfiltered data via GOES, and paired Unix-epoch/calendar timestamps. The
NOAA event page independently reports a 09:04 UTC observed arrival and 74 cm
peak amplitude. NOAA's current
[one-minute CO-OPS request page](https://opendap.co-ops.nos.noaa.gov/axis/webservices/waterlevelrawonemin/plain/index.jsp)
does not list station `1633227` among supported one-minute stations, and the
exact 2011 CO-OPS query returned no data. The recovered source header says its
station identifier is `none`; the pipeline therefore uses the archive code
`saip` and does not relabel the series as CO-OPS station `1633227` or substitute
Guam.

Day `.070` is normalized for the event-day proof. Days `.071` and `.072` are
checksummed coverage-only companions until extended-tail EDA needs them. The
event-day file has 780 source samples and eight duplicate timestamps whose 16
conflicting rows are all quarantined, leaving 764 accepted samples. It also has
a material 12:08–23:07 UTC gap; no interpolation is authorized.

## NCTR continuous event field

**Not a key problem; no ready event-specific machine-readable field is currently
published through the verified route.**

The [NCTR 2011 Honshu event page](https://nctr.pmel.noaa.gov/honshu20110311/)
publishes graphics, animations, model/data comparison plots, and the six scalar
unit-source weights. It does not link a continuous event field with a verified
grid, time axis, units, and source combination. NCTR's
[Forecast Propagation Database access page](https://nctr.pmel.noaa.gov/propagation-database-access.html)
describes OpenDAP access to unit-source netCDF files, but its published catalog
URL currently resolves to a missing page over HTTPS.

Ask NCTR at `oar.pmel.tsunami-webmaster@noaa.gov` for either the exact continuous
MOST field used for the 2011 Honshu result or the precise unit-source netCDF
assets, versions, grid metadata, units, and combination instructions needed to
reconstruct it from the published weights. Reconstruction would be a new,
validated processing decision rather than a direct replacement download; event
images or shifted comparison plots must not be used as proxies.

## Recommended order

1. Email NCTR for the exact event field or complete unit-source package. Continue
   EDA without field-dependent claims unless NCTR supplies a verifiable contract.
