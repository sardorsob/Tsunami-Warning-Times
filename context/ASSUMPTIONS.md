# Assumptions and Unknowns

## Working assumptions

- The final artifact will be a static browser deployment with no private data or
  server-side secret.
- Authoritative public sources will be preferred over republished derivatives.
- Internal event timestamps will use UTC after each source time basis is checked.
- The main visual will be Pacific-centered and authored, but its projection is
  not selected.
- A simple interval or residual summary is preferable to a probabilistic model
  unless uncertainty materially changes the explanation.
- Source-supported coastal request windows and cadences may define completeness
  denominators, but they do not authorize timestamp snapping or interpolation.
- DART cadence transitions are treated as sampling-by-design until source or QC
  evidence identifies a true outage.

## Unresolved—do not treat as facts

- historical tsunami event;
- modeled travel-time or forecast product;
- selected DART stations, tide gauges, and communities;
- arrival detection/pick definition and precision;
- whether alert or public-warning timestamps are sufficiently documented;
- CRS, coordinate order, vertical datum, grid nodata convention, and antimeridian
  handling for each source;
- source license/terms and whether any raw or derived file may be redistributed;
- D3 projection, renderer, scroll controller, and hosting provider;
- repository code license;
- feasibility of conference attendance if accepted.
- the upstream cause of each retained blank or timestamp gap; pooled MCAR is not
  supported, MAR is unproved, and MNAR cannot be excluded;
- whether publisher outage, telemetry, maintenance, or QC records can resolve the
  Pago Pago, Saipan, or long-DART-interval mechanisms.
