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

**Likely recoverable with a user account and API key.**

The [IOC Sea Level Station Monitoring Facility API](https://api.ioc-sealevelmonitoring.org/)
instructs users to register an account, edit the account, and request membership
in `Access gauges API (gauges_API)` to obtain version 2 API keys. Its
[version 2 documentation](https://api.ioc-sealevelmonitoring.org/v2/doc)
provides the research endpoint
`/v2/research/stations/{code}/sensors/{sensor}/data`, with up to 365 days per
request. The [official Valparaíso catalog record](https://www.ioc-sealevelmonitoring.org/ssc/stationdetails.php?id=SSC-valp)
lists one-minute `prs` and `rad` sensors and research-quality data spanning
1944-01-02 through 2018-12-31, which includes March 2011.

After a key is obtained, test both documented sensor identities for station
`valp` over 2011-03-11 through 2011-03-13. Do not accept the result until its
station identity, sensor, timestamps, sampling, units, datum, missingness, terms,
and checksum have been recorded. Keep the key in an ignored local environment
file or environment variable; never commit it.

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

1. Retry Valparaíso when the requested IOC API access is approved.
2. Email NCTR for the exact event field or complete unit-source package. Continue
   EDA without field-dependent claims unless NCTR supplies a verifiable contract.
