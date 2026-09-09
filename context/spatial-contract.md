# Spatial Contract

## Current state

The NCEI Tōhoku TTT metadata and GeoJSON contracts are approved. Metadata
identity is `2011/3/11 Tohoku, Japan`, geometry type is polyline, and WKID 4326
is validated before parsing. The GeoJSON request uses output SR 4326 and its
coordinates are stored as longitude, latitude. The accepted normalized contour
extent is longitude [-179.99999999990004, 180.00000000010004] and latitude
[-77.99997792933794, 87.59715345366902].

The 24 contour parts containing publisher coordinates about `1e-10` degrees
above +180 retain those values and carry `longitude_boundary_precision = true`;
they are not silently clamped. A part is marked as crossing the antimeridian only
when adjacent source longitudes jump by more than 180 degrees. The current 4,380
parts contain no such jump.

The USGS event coordinates use the source's WGS84 latitude/longitude contract.
DART and coastal station coordinates retain their source-stated latitude and
longitude order, but their horizontal datums remain unknown. The continuous NCTR
field is blocked, so no NCTR grid, axis order, extent, resolution, nodata value,
cell registration, or field units are project facts. DART vertical reference is
unknown; CO-OPS observations retain station datum `STND` and must not be treated
as a shared vertical datum. The recovered Saipan archive header states MLLW and
coordinates `15.2266, 145.742` in latitude/longitude order, but does not state a
horizontal datum. Saipan values must not be compared as absolute levels with the
CO-OPS `STND` series; later analysis may compare separately detrended anomalies
only under an explicit method.

The IOC real-time station endpoint places Valparaíso `valp` at latitude
`-33.02767128`, longitude `-71.62787275`; its separate catalog record reports
`-33.02730833`, `-71.6259388`. The pipeline retains the real-time endpoint
coordinates and records the discrepancy rather than silently reconciling it.
The research API declares metres but does not establish a vertical or horizontal
datum for the acquired radar and pressure series. Their roughly 1.891 m median
absolute-level offset must not be interpreted or aligned until a source datum
contract is found; later EDA may compare separately centered anomalies under an
explicit method.

## Required per-source fields

- native CRS and coordinate order;
- horizontal datum and vertical datum where applicable;
- axis names, units, grid transform, resolution, bounds, and cell registration;
- nodata/mask semantics and land/ocean treatment;
- longitude domain (`-180..180` or `0..360`) and antimeridian behavior;
- point geometry meaning for stations and communities;
- reprojection/interpolation/resampling method and target CRS;
- input/output feature or pixel counts and rejected-record location.

## Working output rules

- Preserve source CRS and coordinates in the analysis-ready record.
- Use EPSG:4326 only as an interchange/display coordinate system when appropriate;
  do not use it for planar distance.
- Choose the authored Pacific projection after the static scientific figure is
  evaluated, and record its parameters.
- Store a single static raster as a Cloud-Optimized GeoTIFF when georeferenced
  analysis interchange is needed; use NetCDF/Zarr only for a genuinely
  multidimensional source; export a separate compact browser representation.
- Sort vector outputs by a stable identifier and make all transforms idempotent.

Unknown values remain explicit and block the affected output.
