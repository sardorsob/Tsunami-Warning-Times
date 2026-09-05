# Validation Plan

## Source and identity

- Match every modeled and observed record to the same event identity.
- Record retrieval date, version/date, terms, checksum, and exact query or URL.
- Manually cross-check at least three displayed values against authoritative
  records before release.

## Temporal

- Preserve each source's original time field and time standard.
- Normalize to UTC in a derived field only after the source basis is verified.
- Keep rupture, model/forecast issue, modeled arrival, observed first deviation,
  maximum wave, bulletin, public alert, and evacuation times separate.
- Document arrival-pick method, sampling interval, rounding, and precision.

## Spatial and raster

- Assert CRS, coordinate order, extent, resolution, transform, nodata, and datum.
- Test antimeridian behavior and station-to-grid alignment.
- Reconcile input/output features or pixels at every processing stage.
- Quarantine ambiguous or invalid records; never silently drop or repair them.
- Visual-check a representative field and station sample against known geography.

## Analytical

- Define the distance-only baseline before comparison.
- Use the same event origin and timing convention across baseline, model, and
  observations.
- Define residual sign once and test it.
- Report missingness and hard cases; do not summarize away failed stations.
- Quantify uncertainty only where its source and interpretation are documented.

## Cartographic and interaction

- Document projection; distinguish NoData from zero; do not imply amplitude.
- Keep scales and color roles consistent; directly label units and time standard.
- Check thumbnail/squint, grayscale, common color-vision deficiencies, mobile,
  keyboard, touch, reduced motion, and no-WebGL fallback.
- Ensure deterministic and reversible story states and one clock owner.

## Release

- Rebuild data and app from a clean environment.
- Run the full repository gate and inspect CI evidence.
- Confirm source/third-party attribution, originality, public access without login,
  browser behavior, and that the story stands without its abstract.
