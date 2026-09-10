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

## D-006 — Use a broad but source-gated Tōhoku data proof

- Date: 2026-09-04
- Status: approved for implementation planning
- Decision: attempt the NCEI TTT layer, exact NCTR field, four DART records, and
  six coastal-gauge candidates alongside reviewed USGS event metadata.
- Reason: the project owner prefers wider initial evidence, and independent
  source gates prevent an unavailable or ambiguous asset from invalidating the
  rest of the acquisition run.
- Constraint: source inclusion in the attempt is not promotion to analysis-ready
  or production status. T-002A through T-002E must preserve failures and reject
  assets that do not meet identity, terms, time, units, spatial, and quality gates.
- Revisit when: measured access, size, terms, or quality make a source infeasible.

## D-007 — Scripts own calculations; marimo exposes EDA

- Date: 2026-09-04
- Status: approved for implementation planning
- Decision: reusable typed Python modules own acquisition, normalization,
  validation, and analysis; thin CLI scripts invoke them; one marimo notebook
  reads the analysis-ready artifacts and reusable EDA results.
- Reason: this keeps scientific logic testable and command-line reproducible
  while providing a reactive, Git-reviewable exploration surface without hidden
  notebook state.
- Constraint: opening the notebook never downloads data, and the notebook cannot
  contain a transformation or metric unavailable to scripts and tests.
- Revisit when: a demonstrated workflow cannot be expressed cleanly through this
  boundary.

## D-008 — Markdown is the canonical result surface

- Date: 2026-09-04
- Status: accepted
- Decision: acquisition, data-quality, and EDA tasks populate separate Markdown
  reports with evidence, results, interpretation, limitations, takeaways, and
  next steps. Machine-readable metrics and run bundles remain the calculation
  evidence; marimo and figures are supporting views.
- Reason: continuation and scientific review must not depend on notebook state or
  chat history.
- Revisit when: the accepted reports require a derived public-facing format.

## D-009 — Defer DVC and workflow orchestration

- Date: 2026-09-04
- Status: active
- Decision: begin with URL-plus-checksum reconstruction, atomic local downloads,
  ordinary Python CLIs, portable run bundles, and project-local MLflow for the
  substantive EDA run. Do not add DVC or a workflow engine yet.
- Reason: actual source formats, volume, mutability, and collaboration costs have
  not been measured.
- Revisit when: T-002B demonstrates that reconstructing or sharing data from
  authoritative endpoints is too slow, unstable, or large for this approach.

## D-010 — Let evidence branch the EDA

- Date: 2026-09-05
- Status: accepted
- Decision: T-002D begins with a fixed core data-quality and coverage profile,
  then records each observation, question, follow-up check, and disposition in an
  EDA decision ledger. Follow-up analysis is triggered by actual gaps, cadence
  shifts, outliers, geometry behavior, or source conflicts rather than a
  preselected narrative.
- Reason: exploratory analysis should respond to the data while keeping the path
  reproducible and reviewable.
- Constraint: arrival-pick settings and station inclusion rules remain frozen
  before modeled residuals are inspected; adaptive exploration cannot become
  outcome-driven station selection.
- Revisit when: repeated EDA runs show that a stable follow-up check belongs in
  the fixed core profile.

## D-011 — Keep IOC credentials outside the repository and preserve tsunami values

- Date: 2026-09-09
- Status: active
- Decision: store the IOC API key in macOS Keychain under a project-specific
  service/account, resolve it only in memory for an `X-API-KEY` request header,
  and never write it to configuration, URLs, logs, run bundles, or commits. For
  Valparaíso research data, request explicit sensor series with QC flags while
  disabling value-removing QC filters, 30-day mean subtraction, and timestamp
  fitting.
- Reason: the official IOC contract uses header authentication; its documentation
  warns that neighbour and other QC filters can replace tsunami observations
  with missing values. Raw source timestamps, levels, and flags must remain
  inspectable before any arrival analysis.
- Outcome: the explicit radar response is normalized because it has the greater
  timestamp coverage (4,272 versus 4,270 pressure samples); the pressure
  response is a fully validated, checksummed quality companion. This
  pre-residual quality criterion does not inspect tsunami shape or modeled
  residuals. The vertical datum remains unknown, so the inter-sensor
  absolute-level offset is not corrected or interpreted.
- Revisit when: the key is rotated, a platform other than macOS must run live
  acquisition, publisher metadata establishes a sensor-priority rule, or a
  separate filtered derivative is proposed.

## D-012 — Separate missingness mechanisms and do not impute the data proof

- Date: 2026-09-09
- Status: active for T-002D
- Decision: report raw-value blanks, absent source-supported timestamps,
  structurally inapplicable fields, quarantined source records, unknown metadata,
  and unavailable source assets as separate mechanisms with separate
  denominators. Keep strict exact-grid and sample-density coverage distinct for
  off-grid source timestamps. Do not impute or snap timestamps in the data proof.
- Reason: the pooled 0.7302% raw-cell null rate omits absent timestamps and would
  also misclassify 21,933 coastal fitted/residual blanks if structural semantics
  were ignored. Pago Pago and Saipan concentrate the meaningful continuity risk.
- Statistical interpretation: pooled MCAR is not supported. MAR is only a
  possible conditional analysis assumption after station, source, time, and
  reporting mode are represented; MNAR cannot be excluded without publisher
  outage, maintenance, telemetry, or QC evidence.
- Evidence: run `2026-09-09__1749__missingness__7b6d386`, generated from Git SHA
  `7b6d386`, with canonical results in `context/EDA_REPORT.md`.
- Revisit when: publisher outage/QC records resolve causes, a defensible
  gap-handling method is proposed, or sensitivity analysis shows that station
  inclusion or an arrival result changes materially.
