# Visual Story Tasks

## T-003P — Approve the adaptive visual-story EDA design

- ID: T-003P
- Title: Define the visual discovery and artifact contract
- Depends on: approved dual-track repository design and accepted T-002C2 build
- Owner (Maker): project coordinator
- Checker: project owner
- Phase: story planning
- Data refs: accepted T-002C2 analysis-ready artifacts and shared missingness run
- Scientific refs: spatial contract, validation plan, dual-track design, and
  cartographic guidance
- Statistical notes: design only; the candidate narrative remains falsifiable
- Scope: visual questions, fixed diagnostic core, adaptive branches, artifact
  lineage, scientific gates, story/paper boundary, and commit sequence
- Artifacts to produce: dated design specification and updated story context
- Acceptance criteria: the written design matches the approved discussion,
  distinguishes preliminary from reviewed evidence, allows an honest pivot,
  and introduces no implementation or story claim
- Verification commands: link check, context consistency review,
  `git diff --check`, and documentation-sensitive repository checks
- Manual QA: project owner reviews the written specification
- Evidence: project owner approved the proposed design in conversation and the
  written specification on 2026-09-14; design commit `335948d`
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-14 — selected a fixed diagnostic atlas with adaptive
  branches and authorized a pivot if the distance-versus-arrival idea is weak;
  2026-09-14 — project owner accepted the written specification
- Status: done

## T-003I — Plan the Stage A diagnostic atlas implementation

- ID: T-003I
- Title: Convert the approved story design into an executable Stage A plan
- Depends on: T-003P done
- Owner (Maker): project coordinator
- Checker: project owner
- Phase: story planning
- Data refs: accepted T-002C2 build; shared missingness run; governed Natural
  Earth coastline contract planned but not yet acquired
- Scientific refs: approved adaptive visual-story EDA design, spatial contract,
  validation plan, and cartographic guidance
- Statistical notes: implementation planning only; no result, arrival pick,
  station promotion, or narrative selection
- Scope: exact files and interfaces, test-first steps, fixed four-plot Stage A
  atlas, adaptive review input, deterministic evidence, thin Marimo viewer,
  frequent commit boundaries, and the T-002E fence around Stage B
- Artifacts to produce:
  `docs/superpowers/plans/2026-09-14-visual-story-stage-a-atlas.md`
- Acceptance criteria: every design requirement maps to an executable step;
  preview and canonical runs have truthful Git state; manual review is a
  validated input; no Stage B, paper, app-export, or NCTR proxy work enters the
  plan
- Verification commands: design-to-plan coverage review; placeholder and type-
  consistency scans; `git diff --check`; full repository gate; Graphify refresh
- Manual QA: project owner chooses inline or delegated task-by-task execution
- Evidence: comprehensive 11-task plan prepared after written-design approval;
  full repository gate passed with 93 Python tests and 18 provenance records;
  Graphify refreshed to 781 nodes, 1,299 edges, and 62 communities and returned
  the plan, evidence states, and T-003B gate in a scoped query
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-14 — decomposed Stage A into dependency, source,
  missingness, geometry, four plot, evidence-runner, notebook, and reviewed-run
  commits with explicit scientific stop conditions; 2026-09-14 — project owner
  authorized inline execution with review after each task commit
- Status: done

## T-003A — Build the preliminary diagnostic atlas

- ID: T-003A
- Title: Generate story-only spatial and temporal discovery views
- Depends on: T-003I done
- Owner (Maker): story analysis contributor
- Checker: scientific and cartographic reviewer
- Phase: story EDA
- Data refs: accepted T-002C2 build; no arbitrary processed-file discovery
- Scientific refs: visual-story design, spatial contract, and validation plan
- Statistical notes: descriptive visual checks only; no arrival residual or
  station-promotion decision
- Scope: tested story analysis functions, thin script, thin Marimo atlas view,
  Pacific evidence map, coverage timelines, station small multiples, and a
  distance-versus-contour diagnostic only if spatial checks pass
- Artifacts to produce: PNG/SVG figures, atlas manifest, decision ledger,
  portable run bundle, and generated `context/story/EDA_REPORT.md`
- Acceptance criteria: every figure is deterministic and source-traceable;
  missingness and NoData are explicit; paper artifacts are absent; all outputs
  are labeled `preliminary_storyboard_evidence`
- Verification commands: task-owned tests, deterministic rebuild, report and
  manifest reconciliation, `marimo check`, headless notebook execution, full
  repository gate, and Graphify update
- Manual QA: inspect every figure at full and thumbnail size, grayscale, and
  common color-vision simulations; trace three displayed values
- Evidence: Task 1 RED failed on missing GeoPandas and `analysis`; GREEN resolved
  exactly GeoPandas 1.1.4 and Matplotlib 3.11.2, passed 2 focused tests, and
  reported zero Pyright errors. Task 2 RED failed on the missing map contract,
  manifest, and run lane; GREEN passed 39 tests and added one validated source
  record. Live run `2026-09-14__2157__story-map-context__df0ef32` downloaded the
  85,352-byte Natural Earth 4.1.0 ZIP with SHA-256
  `664449b39070027e882abb295974d182afec18ca21107273d17e9e8bf6f64817`;
  offline rerun `2026-09-14__2158__story-map-context-rerun__df0ef32` reused it
  exactly. Inspection found EPSG:4326 and 134 `LineString` features; raw ZIP and
  sidecar are ignored. Task 3 RED failed on the missing timeline records; GREEN
  passed all 6 missingness tests plus Ruff and strict Pyright. The public timeline
  preserves observed, source-blank, absent-timestamp, and off-grid states without
  snapping, and the existing generated missingness artifacts were unchanged.
  Task 4 RED failed on the absent atlas module; GREEN passed 6 atlas tests, Ruff,
  and strict Pyright. A direct load of the accepted build validated the reviewed
  event, 10 stations, 143,655 observations, 4,380 contour parts, and all 6
  coastal windows without inferred source semantics
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-14 — inline Stage A execution started with the minimal
  pinned static geospatial dependency boundary; 2026-09-14 — governed coastline
  acquisition and offline checksum rerun passed with source precision preserved;
  2026-09-14 — exposed exact-grid coverage states by reusing the shared CSV and
  UTC validators without changing the existing missingness writer; 2026-09-14 —
  added immutable source-preserving atlas records, strict Stage A scope checks,
  interpolated Pacific seam splits, and WGS84 distance rings
- Status: in-progress

## T-003B — Complete the reviewed arrival comparison

- ID: T-003B
- Title: Test and promote the visual-story contrast
- Depends on: T-003A done and T-002E promotes a versioned shared release
- Owner (Maker): story analysis contributor
- Checker: independent scientific, cartographic, and originality reviewer
- Phase: story EDA review
- Data refs: one explicitly accepted shared release manifest
- Scientific refs: frozen arrival method, completeness gate, uncertainty notes,
  story design, and originality firewall
- Statistical notes: descriptive comparison with documented pick sensitivity;
  no fitted paper result
- Scope: modeled-versus-observed arrival view, transparent candidate-community
  contrast sheet, adaptive pivot or rejection decision, and promotion of at most
  one static comparison into the storyboard
- Artifacts to produce: reviewed atlas additions, final decision ledger, updated
  story EDA report, storyboard disposition, and provenance evidence
- Acceptance criteria: arrival definitions and residual sign are explicit;
  station selection predates residual inspection; negative results remain
  visible; the promoted comparison survives scientific and cartographic review
- Verification commands: task-owned tests, clean deterministic rebuild, release
  checksum validation, full repository gate, and Graphify update
- Manual QA: compare three values with authoritative or normalized sources and
  audit paper/story figures and methods for overlap
- Evidence: pending
- Attempts / Max: 0 / 3
- Attempt log: not started
- Status: pending
