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
- Evidence: Core implementation review and independent acquisition data-quality
  review are **APPROVED**. The acquisition core's 33 tests (42 repository tests
  total), focused Ruff, and focused Pyright passed. Review fixes required an
  explicit safe response-header value allowlist, pre-write evidence-ID
  reconciliation, sibling-temporary all-or-nothing bundle publication with
  cleanup/retry tests, and `total_outcomes` metrics. Clean committed bundles
  `2026-09-05__1906__accepted__e602131` and
  `2026-09-05__1906__accepted-rerun__e602131` each report 12 `cached`, 3
  `blocked`, 12,386,361 bytes, `working_tree: clean`, and
  `ready-for-review`; all output checksums and byte counts are identical. The
  reviewer reconciled both bundles, the manifest, the 12 ignored raw files, and
  their 12 ignored checksum sidecars with no proxy substitution.
- Attempts / Max: 3 / 3
- Attempt log: 2026-09-05 — implemented the Task 2 core and thin CLI; 2026-09-05
  — review round 1 corrected no-clobber, cache-truth, containment, and retry
  safety gaps; pending reviewer acceptance and separately authorized live
  acquisition/checksum run; 2026-09-05 — review round 2 added malformed-sidecar
  isolation, owned-sidecar rollback, and raw/sidecar namespace collision guards;
  2026-09-05 — final transport review added bounded retry and sibling isolation
  for incomplete HTTP response reads; fresh final review added NUL-path contract
  rejection plus defensive per-source `ValueError` isolation; 2026-09-05 — core
  implementation review APPROVED; review fixes added safe header-value
  serialization, atomic temporary-bundle publication, input/output ID checks,
  and failure-cleanup tests; 2026-09-05 — clean committed accepted and
  accepted-rerun bundles reconcile; independent data-quality review APPROVED.
- Status: done

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
- Evidence: deterministic offline builds
  `2026-09-05-1958-quality-a-5f920f2` and
  `2026-09-05-1958-quality-b-5f920f2` are byte-identical: 1 event, 4,380 TTT
  parts, 10 stations, 138,619 observations, and 93 visible rejections. The
  portable run bundle is `2026-09-05__1958__quality__5f920f2`; the complete
  profile and manual source traces are in `context/DATA_QUALITY_REPORT.md`.
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-05 — typed offline normalization, schema/accounting
  outputs, fixture tests, and deterministic builder completed; correctness
  review resolved metadata, accounting, empty-source, containment, and unit
  contract findings; adaptive profiling then found 90 undocumented DART `9999`
  measurement rows, which were quarantined before the final double build;
  independent review found and resolved one incorrect inventory-hash reference
  and one stale spatial-contract statement, then APPROVED all identity, checksum,
  accounting, schema, time/unit/datum, geometry, missingness, rejection,
  determinism, and manual-trace gates
- Status: done

## T-002C1 — Recover and normalize Saipan event data

- ID: T-002C1
- Title: Recover the exact NOAA Saipan files without substituting another gauge
- Depends on: T-002C done
- Owner (Maker): data-pipeline contributor
- Checker: scientific data reviewer
- Phase: source recovery and data quality
- Data refs: NOAA/NWS 2011 Honshu event page; preserved captures of the exact
  `.070`, `.071`, and `.072` NOAA URLs
- Scientific refs: `docs/research/source-access-options.md`;
  `context/spatial-contract.md`; source headers
- Statistical notes: preserve gaps, duplicates, off-minute timestamps, units,
  and datum; do not interpolate or tune arrival logic
- Scope: reproduce direct-access behavior, recover exact archived source bytes,
  fingerprint all three days, normalize the event-day file, retain later days as
  explicit archival companions, and revise coverage/provenance reports
- Artifacts to produce: three ignored immutable raw files and sidecars, acquisition
  run bundle, parser and tests, revised manifest/contracts/reports, deterministic
  candidate normalized tables
- Acceptance criteria: source identity, UTC, meters, MLLW, coordinates, row
  counts, checksums, duplicates, gaps, and blocked-source denominator reconcile;
  no claim that archive code `saip` is CO-OPS station `1633227`
- Verification commands: parser RED/GREEN tests, focused acquisition/normalization
  suite, provenance validator, double-build comparison, full repository gate,
  and independent source/data-quality review
- Manual QA: compare all three headers and hashes; trace the first Saipan sample;
  compare NOAA event-page arrival and peak metadata without treating them as
  computed picks
- Evidence: acquisition run
  `2026-09-09__0142__saipan-recovery__92c438c` has 12 cached, 3 downloaded, and
  2 blocked outcomes across 17 contracts; the three Saipan files total 81,117
  bytes. Reviewed candidate build `2026-09-08-saipan-reviewed-92c438c` contains
  139,383 observations and 108 rejections; the `-b-` rebuild is byte-identical.
  Saipan supplies 764 accepted event-day rows; all 16 rows belonging to 8
  conflicting duplicate timestamps are quarantined.
- Attempts / Max: 2 / 3
- Attempt log: 2026-09-08 — Chrome-controlled link click and referrer-bearing HTTP
  probe both reproduced NOAA HTTP 403; exact 2016-12-22 Internet Archive captures
  were located and downloaded; source headers resolved UTC/meters/MLLW and
  coordinates; parser and dispatch behavior were implemented through observed
  RED/GREEN tests; reviewer-requested all-row duplicate quarantine was added and
  deterministically rebuilt; 81 Python tests, Ruff, Pyright, 17-record
  provenance validation, frontend checks/build, and `git diff --check` passed;
  independent review reconciled source bytes, accounting, hashes, and reports
  and APPROVED with no remaining blocking findings
- Status: done

## T-002C2 — Recover and normalize Valparaíso research data

- ID: T-002C2
- Title: Use authorized IOC access to recover the Valparaíso event series
- Depends on: T-002C1 done
- Owner (Maker): data-pipeline contributor
- Checker: scientific data reviewer
- Phase: authenticated acquisition and data quality
- Data refs: IOC SLSMF v2 OpenAPI contract; official SLSMF API manual; station
  `valp`; pressure `prs` and radar `rad` research series
- Scientific refs: `docs/research/source-access-options.md`;
  `context/spatial-contract.md`; D-011
- Statistical notes: sensor coverage and QC flags may guide a documented source
  choice, but observed tsunami shape or model residuals may not
- Scope: store the credential outside Git, authenticate via `X-API-KEY`, acquire
  the exact event window for both documented sensors without value-removing API
  filters, fingerprint raw responses, validate station/sensor/time/unit/datum
  semantics, normalize the accepted series or keep ambiguity visible, and revise
  coverage/provenance reports
- Artifacts to produce: Keychain entry, ignored immutable raw files and sidecars,
  non-secret run evidence, tested credential-aware acquisition and normalization,
  revised contracts/manifest/reports, and deterministic normalized candidates
- Acceptance criteria: no secret reaches repository files, command output, run
  evidence, or Git; official identity and endpoint parameters are recorded;
  source rows, accepted rows, rejections, sensors, timestamps, missingness, QC
  flags, units, and datum reconcile; no API filter silently removes a tsunami
  value; Valparaíso leaves blocked status only if the full contract passes
- Verification commands: secret scan, credential-loader and parser RED/GREEN
  tests, two-run raw checksum comparison, deterministic normalized rebuild,
  provenance validator, full repository gate, and independent scientific review
- Manual QA: trace both sensor headers/metadata, first/event-window/last samples,
  QC-flagged points, station coordinates, and three raw-to-normalized values
- Evidence: Keychain entry stored and length-validated without displaying the
  credential; official OpenAPI and API manual confirm `X-API-KEY`, meter-valued
  `slevel`, exclusive `timestop`, sensor selection, and QC/filter semantics;
  authenticated run `2026-09-09__1838__valparaiso-recovery__9cc448c` downloaded
  4,272 radar and 4,270 pressure rows; cache rerun reproduced both hashes;
  deterministic builds `2026-09-09-valparaiso-reviewed-7576ffb-a` and `-b`
  produced 143,655 observations and 107 rejections with identical checksums
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-09 — authorized IOC credential received; planning and
  credential containment completed; both explicit sensor responses acquired and
  reconciled; radar selected by greater timestamp coverage before any residual
  or waveform inspection and pressure retained as a fully validated quality
  companion; first review found three accounting/documentation gaps, the maker
  corrected all three, and independent re-review approved the source contract,
  companion accounting, deterministic builds, and reporting with no remaining
  blocking findings
- Status: done

## T-002D — Run reproducible EDA

- ID: T-002D
- Title: Profile the broad Tōhoku data proof with scripts and marimo
- Depends on: T-002C, T-002C1, and T-002C2 done
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
- Evidence: missingness run
  `2026-09-09__1749__missingness__7b6d386` profiles the accepted T-002C2 build,
  records a six-file portable bundle and finished project-local MLflow run
  `3ea475f7045e48c9a1a87af913f807e0`, and produces the canonical Markdown,
  JSON, and CSV evidence. The reusable profiler has five task-owned tests; the
  thin marimo view passes static validation and headless execution. Remaining
  adaptive EDA scope is still pending.
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-09 — completed the first test-driven T-002D slice on a
  clean committed implementation; it separates raw nulls, absent expected
  timestamps, structural not-applicable fields, deliberate quarantine, metadata
  unknowns, and blocked source assets without imputation or timestamp snapping;
  the complete T-002D task remains active
- Status: in-progress

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

## T-003P — Approve the adaptive visual-story EDA design

- ID: T-003P
- Title: Define the visual discovery and artifact contract
- Depends on: accepted T-002C2 build and approved dual-track design
- Owner (Maker): project coordinator
- Checker: project owner
- Phase: story planning
- Data refs: accepted T-002C2 analysis-ready artifacts and shared missingness run
- Scientific refs: spatial contract, validation plan, and D-010 through D-014
- Statistical notes: design only; no result or station selection
- Scope: fixed visual audit core, adaptive branches, evidence states, scientific
  gates, artifact lineage, story/paper boundary, and implementation sequence
- Artifacts to produce: dated design specification and story context package
- Acceptance criteria: written design matches the approved discussion, permits
  an evidence-led pivot, and keeps implementation and unsupported claims out
- Verification commands: link and consistency checks plus `git diff --check`
- Manual QA: project owner reviews the written specification
- Evidence: project owner approved the design discussion and written
  specification on 2026-09-14; design commit `335948d`
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-14 — approved a fixed diagnostic atlas with adaptive
  branches and a falsifiable distance-versus-arrival candidate; 2026-09-14 —
  project owner accepted the written specification
- Status: done

## T-003I — Plan the Stage A diagnostic atlas implementation

- ID: T-003I
- Title: Convert the approved story design into an executable Stage A plan
- Depends on: T-003P done
- Owner (Maker): project coordinator
- Checker: project owner
- Phase: story planning
- Data refs: accepted T-002C2 build and shared missingness evidence; planned
  governed Natural Earth coastline context
- Scientific refs: approved story design, spatial contract, validation plan,
  originality firewall, and D-010 through D-014
- Statistical notes: planning only; no result or candidate selection
- Scope: exact test-first tasks for the static geospatial stack, governed map
  context, reusable coverage/geometry interfaces, four preliminary diagnostics,
  run evidence, adaptive review input, and thin Marimo view
- Artifacts to produce:
  `docs/superpowers/plans/2026-09-14-visual-story-stage-a-atlas.md`
- Acceptance criteria: the plan covers Stage A without crossing into arrival-
  based Stage B, paper analysis, app export, or an inferred NCTR field; each
  coherent task has verification and a commit boundary
- Verification commands: specification-coverage, placeholder, naming, and type-
  consistency review; `git diff --check`; repository gate; Graphify refresh
- Manual QA: project owner chooses the task-by-task execution approach
- Evidence: 11-task implementation plan prepared after written-design approval;
  full repository gate passed with 93 Python tests and 18 provenance records;
  Graphify refreshed to 781 nodes, 1,299 edges, and 62 communities and returned
  the Stage A/T-003B boundary in a scoped query
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-14 — prepared the exact Stage A implementation, evidence,
  adaptive-review, and handoff sequence; 2026-09-14 — project owner authorized
  inline execution with review after each task commit
- Status: done

## T-003 — Run adaptive visual-story EDA and make the static comparison

- ID: T-003
- Title: Discover and validate the visual-story comparison
- Depends on: T-003I done; T-002E promote
  required before arrival-based evidence or station promotion
- Owner (Maker): story analysis/visualization contributor
- Checker: scientific, cartographic, and originality reviewer
- Phase: story EDA and static visual proof
- Data refs: accepted T-002C2 build for preliminary evidence; one explicitly
  accepted T-002E release for reviewed evidence
- Scientific refs: story EDA design, accepted source and method documentation,
  spatial contract, validation plan, and originality firewall
- Statistical notes: descriptive visual comparison; define geodesic distance,
  propagation assumption, residual sign, timing precision, and pick sensitivity
- Scope: a preliminary Pacific evidence map, coverage timelines, station small
  multiples, and distance-versus-contour diagnostic; after the shared gate,
  modeled-versus-observed arrival comparison, community contrast sheet, and an
  explicit promote, revise, pivot, or reject disposition
- Artifacts to produce: generated figures, atlas manifest, decision ledger,
  portable run evidence, story EDA report, and at most one promoted static proof
- Acceptance criteria: projection and antimeridian behavior documented; NoData
  distinct; no amplitude or actionable-warning-time claim; negative findings
  visible; paper artifacts absent; three displayed values checked; the notebook
  contains no unique calculation or rendering logic
- Verification commands: deterministic rebuild, task-owned tests, `marimo check`,
  headless notebook execution, manifest/report reconciliation, full repository
  gate, and Graphify update
- Manual QA: full-size and thumbnail review, grayscale and color-vision checks,
  source-value traces, and paper/story overlap audit
- Evidence: detailed subtasks and current state live in `context/story/TASKS.md`;
  Task 1 resolved the two exact static visualization dependencies and passed its
  focused dependency and strict-type gates; Task 2 added the separately governed
  Natural Earth coastline, one-record story manifest, lane-tagged acquisition
  evidence, and an exact offline checksum rerun; Task 3 added a tested shared
  exact-grid/off-grid timeline interface without changing recorded missingness;
  Task 4 added immutable atlas inputs, strict reviewed-scope validation,
  interpolated Pacific seam handling, and WGS84 distance rings, then validated
  all 10 stations, 143,655 observations, 4,380 contour parts, and 6 coastal
  windows against the accepted build; Task 5 added a deterministic Pacific map
  renderer and smoke-rendered 4,514 input line parts into 4,543 seam-safe parts;
  Task 6 added deterministic source-window coverage strips and smoke-rendered
  23,040 exact-grid positions plus 120 unsnapped off-grid observations; Task 7
  added separately scaled point panels for 11,156 coastal raw values and 13,573
  DART residuals in the reviewed -6 h to +30 h window; Task 8 added the
  side-by-side six-ring/nine-contour shape diagnostic without speed or arrival
  inference and smoke-rendered 885 input parts as 916 seam-safe parts
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-14 — Stage A inline execution began at the approved
  dependency boundary; 2026-09-14 — the governed basin-context source passed
  contract, geometry, provenance, ignore, and idempotence checks; 2026-09-14 —
  coverage-state exposure passed 6 missingness tests, Ruff, and strict Pyright;
  2026-09-14 — atlas-core RED/GREEN passed 6 focused tests, Ruff, strict Pyright,
  and a direct accepted-build scope load; 2026-09-14 — evidence-map RED/GREEN
  passed all 7 atlas tests, Ruff, strict Pyright, and an actual-data temporary
  PNG/SVG render; 2026-09-14 — coverage-plot RED/GREEN passed 14 shared and
  story tests, Ruff, strict Pyright, and an actual six-gauge temporary render;
  2026-09-14 — station-series RED/GREEN passed focused semantics and byte-
  determinism tests plus an actual ten-panel temporary render; 2026-09-14 —
  distance-diagnostic RED/GREEN passed its semantic/byte gate, Ruff, strict
  Pyright, and an actual-data temporary render
- Status: in-progress

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

## X-001 — Close the dual-track compatibility follow-up

- ID: X-001
- Title: Describe the paper/story overlap and obtain final chair guidance
- Depends on: approved dual-track migration; stable contribution statements,
  paper methods/analysis outline, story thesis/storyboard, and figure inventories
- Owner (Maker): project owner with project coordinator support
- Checker: independent originality reviewer
- Phase: cross-track governance
- Data refs: shared release manifests and the named source inventory
- Scientific refs: official track policies; `context/ORIGINALITY.md`; D-013
- Statistical notes: disclose shared source-factual analysis without transferring
  fitted paper-model results into the story
- Scope: quantify the expected overlap by data, preprocessing, analysis, figures,
  and prose; prepare the requested factual response; reconcile any Paper/VisNotes
  guidance; and update the originality firewall
- Artifacts to produce: reviewed overlap matrix, owner-approved response, chair
  disposition, and updated originality ledger
- Acceptance criteria: both contributions are concrete; permitted overlap is
  bounded; prohibited duplication is explicit; all related work is disclosed;
  the response is not sent before owner authorization
- Verification commands: cross-document consistency and final artifact/figure
  inventory checks
- Manual QA: compare the response against both submissions and the original
  chair correspondence
- Evidence: 2026-09-13 storytelling co-chair reply conditionally permits the
  same dataset and requests the type and approximate extent of expected overlap
- Attempts / Max: 0 / 3
- Attempt log: waiting for enough paper and story context to answer accurately
- Status: pending
