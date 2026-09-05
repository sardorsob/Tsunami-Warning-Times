# Decision Log

## D-001 — Minimal split repository shell

- Date: 2026-09-04
- Status: accepted for setup
- Decision: use a root Python/provenance workspace and an `app/` React,
  TypeScript, and Vite workspace, matching the user's existing project pattern.
- Reason: it separates reproducible scientific preprocessing from the static
  browser artifact without introducing a backend or monorepo framework.
- Revisit when: a verified data format or deployment constraint requires it.

## D-002 — Event selection remains gated

- Date: 2026-09-04
- Status: active
- Decision: no historical event, station, community, or arrival field is encoded
  as selected during repository setup.
- Reason: the handoff requires a data-feasibility comparison rather than fame-led
  selection.
- Revisit when: T-001 has accepted primary-source evidence and T-002 confirms a
  reproducible sample.

## D-003 — Dependencies follow demonstrated need

- Date: 2026-09-04
- Status: active
- Decision: install only React/Vite and quality tooling during setup. Defer D3,
  regl/WebGL helpers, scroll libraries, xarray, rasterio, pandas, GeoPandas, and
  other analytical dependencies until the first code path needs them.
- Reason: source format and rendering needs remain unresolved.
- Revisit when: the data proof or first visual spike begins.

## Open decisions

- Repository license and derived-data redistribution policy.
- Event/product/station/community selection.
- Exact meaning and display label for each warning-time quantity.
- Projection, static fallback format, hosting provider, and attendance feasibility.

## D-004 — Tōhoku is provisional, not frozen

- Date: 2026-09-04
- Status: provisional
- Decision: take the 11 March 2011 Tōhoku event into the minimal data-proof spike.
- Reason: primary-source screening found the strongest combination of a
  machine-queryable NCEI TTT contour layer, mature NOAA/NCTR comparisons, 35
  event-packaged DART records, Pacific tide-gauge comparisons, and reviewed
  source metadata.
- Condition: do not set `selectedEvent`, produce reportable results, or begin the
  full visual story until data-proof steps 1–6 in
  `docs/research/feasibility.md` pass.
- Revisit when: raw model access fails, the distance-versus-arrival discovery does
  not survive calculation, or operational-message timing becomes the main thesis.

## D-005 — Use physical-travel-time wording by default

- Date: 2026-09-04
- Status: active
- Decision: label the comparable quantity “time from earthquake origin to
  observed first arrival.” Use “official message issued X before observed
  arrival” only with a named, timestamped center message.
- Reason: rupture-to-arrival, bulletin issuance, public dissemination, receipt,
  comprehension, and evacuation are different processes with different evidence.
- Revisit when: authoritative local alert and response records support a separate
  warning-system analysis.
