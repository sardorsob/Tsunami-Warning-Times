# Tasks

## T-000 — Prepare the repository

- ID: T-000
- Title: Prepare a minimal, reproducible project shell
- Depends on: none
- Owner (Maker): Codex primary agent
- Checker: independent repository checker assigned after Maker gate
- Phase: setup
- Data refs: no scientific data acquired
- Scientific refs: user handoff; Catastrophe Modeling & GeoAI profile
- Statistical notes: no model or result is in scope
- Scope: repository instructions, context contracts and retention, provenance
  validation, Python/Node tooling, browser status shell, Graphify, tests, CI,
  and handover
- Artifacts to produce: the tracked repository scaffold described in
  `context/STRUCTURE.md`
- Acceptance criteria: setup is installable; checks pass; unresolved scientific
  choices remain explicit; no large data, secret, backend, or unsupported claim
  is introduced; prior `.serena/` content is preserved
- Verification commands: full gate in `AGENTS.md`; Graphify query/explain;
  clean-tree review limited to newly created files
- Manual QA: read README links and browser shell copy; inspect ignored data paths
- Evidence: Maker environment, lint, type, test, build, audit, manifest, and
  browser checks recorded in `context/HANDOVER.md`; independent checker accepted
  the corrected repository on 2026-09-04
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-04 — Maker setup complete; checker-requested provenance
  path/state validation and Node engine alignment corrected; re-check accepted
- Follow-up: 2026-09-04 — retained all context placeholders, removed Serena from
  the tracked tree, and initialized a verified code-only Graphify graph
- Status: done

## T-001 — Select a feasible event

- ID: T-001
- Title: Verify competition rules and compare candidate tsunami events
- Depends on: T-000 repository locations
- Owner (Maker): source-feasibility research agent
- Checker: Codex primary agent
- Phase: feasibility
- Data refs: primary-source pages linked in `docs/research/feasibility.md`
- Scientific refs: authoritative competition, NOAA, NCEI/NDBC, and national
  agency documentation only
- Statistical notes: availability screening, not model evaluation
- Scope: two or three candidate events; modeled fields; DART; tide gauges;
  metadata; terms; community-comparison potential; timing definitions
- Artifacts to produce: `docs/research/feasibility.md`; accepted decision entries
- Acceptance criteria: every material claim has a primary citation; unknowns are
  visible; recommendation is traceable; timing concepts are separated
- Verification commands: link and claim audit; no dataset download
- Manual QA: scientific reviewer checks event identity and recommendation logic
- Evidence: 97-line primary-source note reviewed; official contest, registration,
  NCEI TTT layer, NCTR event page, and NCEI DART page sampled independently on
  2026-09-04; recommendation remains conditional on the documented data proof
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-04 — research completed and accepted with conditional recommendation
- Status: done

## T-002P — Approve the broad data-proof design

- ID: T-002P
- Title: Approve the Tōhoku acquisition and EDA work package
- Depends on: accepted T-001 recommendation
- Owner (Maker): Codex primary agent
- Checker: project owner
- Phase: planning
- Data refs: candidate rows in `artifacts/provenance/source-manifest.csv`
- Scientific refs: `docs/research/feasibility.md`; approved workflow profiles
- Statistical notes: design only; no source is promoted and no result is estimated
- Scope: source coverage, task boundaries, data flow, validation, reporting,
  run tracking, failure behavior, and intentionally empty report placeholders
- Artifacts to produce: approved design specification and updated context contracts
- Acceptance criteria: tasks are independently checkable; every requested source
  is owned; scripts remain the source of calculations; marimo remains a thin EDA
  consumer; Markdown is the canonical result surface
- Verification commands: link/placeholder/consistency review and repository gate
- Manual QA: project owner reviews the committed specification before T-002A
- Evidence: design approved in chat and reaffirmed by the project owner on
  2026-09-05; specification and context package passed the full repository gate;
  three report placeholders verified at zero bytes
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-04 — planning package prepared for owner review;
  2026-09-05 — project owner approved the design and authorized T-002A through
  T-002C execution on `main`
- Status: done

## T-002A — Resolve source endpoints and contracts

- ID: T-002A
- Title: Resolve the exact Tōhoku model and observation assets
- Depends on: T-002P done
- Owner (Maker): data-pipeline contributor
- Checker: scientific reviewer
- Phase: source discovery
- Data refs: provisional source manifest plus authoritative source metadata
- Scientific refs: `docs/research/feasibility.md`; source-owned documentation
- Statistical notes: inventory only; do not select stations from desired residuals
- Scope: verify machine endpoints and terms for USGS event metadata, NCEI TTT
  layer 17, the NCTR field and coefficients, four DART records, and six coastal
  gauges; resolve exact station IDs, coordinates, time windows, and formats
- Artifacts to produce: updated source manifest and
  `context/ACQUISITION_REPORT.md`
- Acceptance criteria: every asset has a stable URL or documented access blocker,
  publisher, version/date, terms, expected schema, units, spatial/time basis, and
  planned local path; station selection rule is independent of observed residuals
- Verification commands: authoritative metadata/link audit and manifest validator
- Manual QA: reconcile station names/IDs and three map locations with source pages
- Evidence: 2026-09-05 — 15 exact asset contracts recorded in
  `config/tohoku-data-proof.toml` and the source manifest: 12 acquisition-approved
  and 3 explicitly blocked. The blocked status has RED/GREEN provenance-test
  evidence; no raw data was downloaded. Maker verification is recorded in the
  T-002A report; a fresh final scientific reviewer approved the four-commit
  range after three correction rounds with no material findings.
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-05 — authoritative endpoint and contract audit started;
  2026-09-05 — exact source-contract ledger completed with NCTR field and
  Saipan and Valparaíso retained as blocked, while the published NCTR scalar
  coefficients were approved with their units explicitly unstated; submitted
  for independent scientific review;
  2026-09-05 — review round 1 added NCEI-to-NDBC UTC evidence, corrected the
  coefficient HTML contract, and aligned downstream acquisition/normalization
  plans to `approved` contracts and USGS FDSN CSV;
  2026-09-05 — review round 2 aligned the downloader interface exactly to the
  TOML field names, added explicit blocker reasons, and corrected the byte-prefix
  encoding contract;
  2026-09-05 — final interface check added the previously omitted narrative
  content-signature field to the planned downloader dataclass;
  2026-09-05 — fresh final reviewer approved the exact contracts, source/time
  evidence, manifest symmetry, downstream interface, and blocked-source handling
- Status: done

## T-002B — Acquire and fingerprint raw assets

- ID: T-002B
- Title: Download the approved Tōhoku source bundle reproducibly
- Depends on: T-002A done
- Owner (Maker): data-pipeline contributor
- Checker: data-quality reviewer
- Phase: acquisition
- Data refs: approved T-002A manifest rows only
- Scientific refs: source-owned schemas and terms accepted in T-002A
- Statistical notes: acquisition accounting only; no inferential result
- Scope: idempotent downloads for the event record, TTT contours, NCTR field,
  four DART stations, and six coastal gauges; immutable raw cache; checksums;
  retry/timeout behavior; per-source success or quarantine
- Artifacts to produce: reusable acquisition module, thin CLI, raw checksums,
  source inventory, run bundle, and populated `context/ACQUISITION_REPORT.md`
- Acceptance criteria: reruns do not corrupt or silently replace assets; byte
  counts and checksums reconcile; unavailable or ambiguous sources fail
  independently and never masquerade as successful downloads
- Verification commands: unit fixtures, opt-in live smoke checks, two-run checksum
  comparison, provenance validator, and raw-file accounting
- Manual QA: open representative files and compare headers/identity with source
- Evidence: 2026-09-05 — source-independent acquisition core has fixture RED/GREEN
  evidence for atomic writes, cache reuse, immutable conflict quarantine,
  bounded transient-failure isolation in source-ID order, blocked no-fetch, TOML
  contract-field preservation, and bounded prefix inspection. Focused suite
  passed (24 tests); Ruff and Pyright passed; CLI help and an isolated offline
  run bundle were exercised. Review correction adds hard-link no-clobber
  finalization, sidecar-backed cache verification, local I/O containment,
  symlink-root containment, strict duplicate/blank contract rejection, and
  transient HTTP retry classification. No live request or raw scientific data
  download occurred.
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-05 — implemented the Task 2 core and thin CLI; 2026-09-05
  — review round 1 corrected no-clobber, cache-truth, containment, and retry
  safety gaps; pending reviewer acceptance and separately authorized live
  acquisition/checksum run; 2026-09-05 — review round 2 added malformed-sidecar
  isolation, owned-sidecar rollback, and raw/sidecar namespace collision guards;
  2026-09-05 — final transport review added bounded retry and sibling isolation
  for incomplete HTTP response reads.
- Status: in progress

## T-002C — Normalize and validate analysis tables

- ID: T-002C
- Title: Produce analysis-ready model and observation tables
- Depends on: T-002B done
- Owner (Maker): data-pipeline contributor
- Checker: scientific data reviewer
- Phase: data quality
- Data refs: checksummed T-002B raw assets
- Scientific refs: `context/DATA_CARD.md`; `context/spatial-contract.md`;
  `context/FORECAST_PROTOCOL.md`
- Statistical notes: preserve source precision and missingness; no model-guided
  tuning of observation picks
- Scope: normalize schemas, timestamps, coordinates, CRS, units, station metadata,
  TTT contours, NCTR dimensions, and water-level series; quarantine invalid or
  ambiguous records; log input/output/rejection counts
- Artifacts to produce: typed reusable transformations, compact processed tables,
  schemas, rejected-record output, run bundle, and populated
  `context/DATA_QUALITY_REPORT.md`
- Acceptance criteria: explicit grain/key for every table; UTC derivation retains
  source time; zero differs from NoData; geometry/grid and antimeridian rules pass;
  no unexplained row, feature, sample, or station loss
- Verification commands: task-owned tests, schema checks, count reconciliation,
  coordinate/geometry validation, and deterministic rebuild comparison
- Manual QA: inspect three contours, four DART records, and six coastal records
- Evidence: pending
- Attempts / Max: 0 / 3
- Attempt log: not started
- Status: pending

## T-002D — Run reproducible EDA

- ID: T-002D
- Title: Profile the broad Tōhoku data proof with scripts and marimo
- Depends on: T-002C done
- Owner (Maker): analysis contributor
- Checker: independent analytical reviewer
- Phase: EDA
- Data refs: accepted T-002C analysis-ready artifacts only
- Scientific refs: data, spatial, forecast, and validation contracts
- Statistical notes: descriptive and sensitivity analysis; exploratory findings
  remain distinct from frozen production claims
- Scope: reusable analysis functions, a thin marimo notebook, data inventory,
  missingness/cadence/distribution checks, spatial coverage, NCTR structure,
  arrival-pick sensitivity, join coverage, and distance-versus-arrival contrasts;
  maintain a decision ledger whose follow-up checks are triggered by observed
  quality findings rather than a fixed list of preferred results
- Artifacts to produce: analysis module, marimo notebook, compact tables/figures,
  file run bundle, project-local MLflow run, and populated
  `context/EDA_REPORT.md`
- Acceptance criteria: notebook contains no unique transformation logic; all
  calculations are reproducible from scripts; Markdown records results, evidence,
  interpretations, limitations, takeaways, and next steps; failed sources remain
  visible in denominators and coverage statements
- Verification commands: task-owned tests, `marimo check`, headless notebook run,
  report regeneration, MLflow/run-bundle reconciliation, and selected-value checks
- Manual QA: inspect all figures/tables and compare at least three values with data
- Evidence: pending
- Attempts / Max: 0 / 3
- Attempt log: not started
- Status: pending

## T-002E — Review and close the data proof

- ID: T-002E
- Title: Decide whether Tōhoku is ready for the static comparison
- Depends on: T-002D done
- Owner (Maker): project coordinator
- Checker: independent scientific reviewer
- Phase: data-proof review
- Data refs: accepted T-002A through T-002D evidence
- Scientific refs: all task-owned reports and authoritative source records
- Statistical notes: freeze definitions only after sensitivity and hard-case review
- Scope: audit source identity, terms, reproducibility, data quality, arrival
  definitions, uncertainty, selection bias, and the proposed community contrast
- Artifacts to produce: checker disposition, updated decisions/data card/handover,
  and either a frozen event/observation set or an explicit revise/reject decision
- Acceptance criteria: every upstream criterion has evidence; unsupported assets
  are excluded; known blockers cannot reverse the recommendation; T-003 receives
  an explicit versioned interface or remains blocked
- Verification commands: clean rerun, independent report/code review, checksum
  comparison, full repository gate, and Graphify update
- Manual QA: scientific reviewer traces three reported findings to raw sources
- Evidence: pending
- Attempts / Max: 0 / 3
- Attempt log: not started
- Status: pending

## T-003 — Make the static scientific comparison

- ID: T-003
- Title: Compare a distance-only ring with the modeled arrival field
- Depends on: T-002E done with a promote disposition
- Owner (Maker): analysis/visualization contributor
- Checker: scientific and cartographic reviewer
- Phase: analysis
- Data refs: versioned T-002 outputs only
- Scientific refs: accepted source and method documentation
- Statistical notes: define distance metric, propagation assumption, residual sign,
  and timing precision
- Scope: one static Pacific figure and one or two explanatory comparisons
- Artifacts to produce: generated figure, table, method note, and provenance entry
- Acceptance criteria: projection documented; NoData distinct; no amplitude claim;
  same extent/scale; labels and units readable; three displayed values checked
- Verification commands: deterministic rebuild and task-owned tests
- Manual QA: squint/thumbnail, grayscale, and color-vision review
- Evidence: pending
- Attempts / Max: 0 / 3
- Attempt log: not started
- Status: pending

## T-004 — Test the wavefront mechanism

- ID: T-004
- Title: Render one data-derived animated threshold with a static fallback
- Depends on: accepted T-003 figure and visual grammar
- Owner (Maker): frontend visualization contributor
- Checker: frontend and scientific reviewer
- Phase: prototype
- Data refs: compact, versioned T-002/T-003 web asset
- Scientific refs: accepted field semantics and visual bandwidth definition
- Statistical notes: animation threshold must not imply amplitude or precision the
  source does not contain
- Scope: one renderer spike, one clock owner, one deterministic state transition,
  reduced-motion/static fallback, and performance measurement
- Artifacts to produce: isolated spike or minimal integrated vertical slice
- Acceptance criteria: geometry is data-derived; pause/scrub works; WebGL failure
  retains meaning; keyboard/touch path works; tests and build pass
- Verification commands: frontend gate plus targeted manual browser checks
- Manual QA: desktop, mobile portrait, reduced motion, and WebGL-disabled paths
- Evidence: pending
- Attempts / Max: 0 / 3
- Attempt log: not started
- Status: pending

## T-005 — Build and package the story

- ID: T-005
- Title: Complete, validate, and package the guided entry
- Depends on: accepted T-004 vertical slice and storyboard approval
- Owner (Maker): project contributor
- Checker: independent scientific, accessibility, and competition reviewers
- Phase: production
- Data refs: accepted, versioned pipeline outputs only
- Scientific refs: accepted method, source, and validation records
- Statistical notes: uncertainty shown only when defined and decision-relevant
- Scope: five guided scenes, four to six communities, methods/data, optional
  post-story scrubber, stable static deployment, abstract, and demo plan
- Artifacts to produce: production browser build, final reports, 150-word abstract,
  deployment evidence, and demonstration-video plan
- Acceptance criteria: all scientific, cartographic, interaction, accessibility,
  competition, attribution, and originality gates pass
- Verification commands: full CI, browser matrix, link check, static fallback,
  clean install/build, and public-URL smoke check after deployment authorization
- Manual QA: end-to-end story without hover, sound, motion, or abstract
- Evidence: pending
- Attempts / Max: 0 / 3
- Attempt log: not started
- Status: pending
