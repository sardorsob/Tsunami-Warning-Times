# Visual-Story Source Notes

## Natural Earth coastline context

- Source ID: `natural-earth-coastline-110m-v4.1.0`
- Publisher: Natural Earth
- Asset: 1:110m coastline, version 4.1.0
- URL: `https://naturalearth.s3.amazonaws.com/110m_physical/ne_110m_coastline.zip`
- Source page checked: 2026-09-14
- Terms checked: 2026-09-14; Natural Earth states that its raster and vector
  map data are in the public domain.
- Intended use: neutral, generalized Pacific coastline context only.
- Known limitation: the 1:110m theme includes major islands but omits lower-rank
  minor-island detail and is not suitable for local positional interpretation.
- Acquisition state: downloaded by the governed contract in immutable run
  `2026-09-14__2157__story-map-context__df0ef32`.
- Idempotence check: offline run
  `2026-09-14__2158__story-map-context-rerun__df0ef32` reused the checksummed
  cache with status `cached`, the same 85,352 bytes, and the same SHA-256.
- Retrieval result: 85,352-byte ZIP with SHA-256
  `664449b39070027e882abb295974d182afec18ca21107273d17e9e8bf6f64817`.
- Embedded identity: version `4.1.0`; the source `.prj` declares WGS84 and
  GeoPandas resolves it to `EPSG:4326`.
- Geometry inspection: 134 `LineString` features; bounds
  `(-180.0, -85.60903777459774, 180.00000044181039, 83.64513)`.
- Boundary precision: the observed maximum longitude is approximately
  `4.42e-7` degrees above +180. The source value is preserved and stays within
  the project's explicit `1e-6` boundary-precision tolerance; no coordinate was
  silently clamped or repaired.
- Acquisition command:
  `uv run python scripts/acquire_tohoku.py --config config/story-map-context.toml --root . --run-tag story-map-context --lane story`.

The coastline does not supply travel time, bathymetry, station metadata, or an
NCTR field. It cannot repair or override any scientific source geometry.
