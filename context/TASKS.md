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
- Scope: repository instructions, context contracts, provenance validation,
  Python/Node tooling, browser status shell, tests, CI, and handover
- Artifacts to produce: the tracked repository scaffold described in
  `context/STRUCTURE.md`
- Acceptance criteria: setup is installable; checks pass; unresolved scientific
  choices remain explicit; no large data, secret, backend, or unsupported claim
  is introduced; prior `.serena/` content is preserved
- Verification commands: full gate in `AGENTS.md`; clean-tree review limited to
  newly created files
- Manual QA: read README links and browser shell copy; inspect ignored data paths
- Evidence: Maker environment, lint, type, test, build, audit, manifest, and
  browser checks recorded in `context/HANDOVER.md`; independent checker accepted
  the corrected repository on 2026-09-04
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-04 — Maker setup complete; checker-requested provenance
  path/state validation and Node engine alignment corrected; re-check accepted
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

## T-002 — Prove the data path

- ID: T-002
- Title: Reproduce one modeled field and two observed station records
- Depends on: accepted T-001 recommendation
- Owner (Maker): data-pipeline contributor
- Checker: scientific reviewer
- Phase: data proof
- Data refs: approved rows in `artifacts/provenance/source-manifest.csv`
- Scientific refs: source documentation accepted in T-001
- Statistical notes: define arrival pick and precision before residuals
- Scope: acquire a minimal sample; validate identity, UTC basis, units, CRS,
  vertical datum, nodata, geometry/grid, missingness, and licensing; log counts
- Artifacts to produce: source records, schemas, validation output, rejected-record
  report, reproducible script, and two manually cross-checked observations
- Acceptance criteria: idempotent rerun; no unexplained record loss; exact source
  lineage; observed and modeled times remain separate
- Verification commands: task-owned tests plus a rerun and checksum comparison
- Manual QA: inspect the field and station locations against source records
- Evidence: pending
- Attempts / Max: 0 / 3
- Attempt log: not started
- Status: pending

## T-003 — Make the static scientific comparison

- ID: T-003
- Title: Compare a distance-only ring with the modeled arrival field
- Depends on: accepted T-002 data proof
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
