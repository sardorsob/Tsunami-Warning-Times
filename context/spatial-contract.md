# Spatial Contract

## Current state

No spatial source is approved, so no CRS, coordinate order, extent, grid,
resolution, nodata value, or vertical datum is yet a project fact.

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
