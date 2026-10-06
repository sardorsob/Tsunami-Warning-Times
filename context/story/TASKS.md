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
  coastal windows without inferred source semantics. Task 5 RED failed on the
  absent plot module; GREEN passed all 7 atlas tests, Ruff, and strict Pyright.
  A temporary real-data render preserved all 4,514 coastline-plus-contour input
  parts as 4,543 seam-safe projected output parts and wrote valid PNG/SVG files.
  Task 6 RED failed on the absent coverage renderer; GREEN passed all 14 shared
  missingness and atlas tests, Ruff, and strict Pyright. Its temporary real-data
  render represented 23,040 exact-grid positions and 120 separate off-grid
  observations across all six gauges; lowest-coverage names are metric-derived.
  Task 7 RED failed on the absent panel interface; GREEN passed both series
  tests, Ruff, and strict Pyright. The actual -6 h to +30 h window yields 10
  locally scaled panels and 24,729 unchanged numeric points: 11,156 coastal raw
  levels and 13,573 DART residuals; missing values remain in the coverage view.
  Task 8 RED failed on the absent diagnostic function; GREEN passed the semantic
  and byte-determinism test, Ruff, and strict Pyright. The actual-data render
  compares six WGS84 range rings with nine configured published contour hours;
  885 input parts become 916 seam-safe parts, with no speed or arrival inference.
  Task 9 RED failed on the absent runner; GREEN passed 10 integration and error-
  path tests plus Ruff and strict Pyright. The runner owns all four figure pairs,
  checksummed manifest and decision ledger, ordered Markdown report, portable
  six-file bundle, project-local MLflow record, output fences, and atomic failure
  cleanup. Task 10 RED failed because the thin notebook did not exist; GREEN
  passed all 3 dependency/boundary tests, `marimo check`, Ruff, and strict
  Pyright. A headless HTML export rendered the explicit no-manifest callout and
  created no repository file; the notebook reads only generated manifests,
  ledgers, and figure paths. The first Task 11 full-size preview exposed false
  horizontal seam segments in both spatial figures, so review stopped. A RED
  regression reproduced PROJ normalizing the exact unwrapped `-340°` endpoint
  to the opposite edge; the typed `force_over` projection fix passed all 12
  atlas tests, Ruff, and strict Pyright. A real-data rerender reduced coastline
  and contour segments over 2,000 km from 9 and 16 to zero; visual inspection
  confirmed the false lines were removed. The first canonical draft then halted
  because its reviewed ledger was paired with stale preview-only interpretation
  and next-step prose. A RED/GREEN runner regression now renders distinct
  preview and reviewed report states; all 10 runner tests, Ruff, and strict
  Pyright pass. Canonical portable run
  `2026-09-16__0351__story-atlas__6c35d78` and local MLflow run
  `a5a576b2c4634a27af6da7655b3e4060` reproduce the four committed decisions:
  branch the crowded basin context and observability lead; retain the signal and
  non-radial shape diagnostics; promote nothing. Figure hashes are map PNG
  `a3ec2a5206bc5593dae727a1003e5b1abbe6d49b156543755db454e046426fea`,
  map SVG
  `d089a001dda9532ceb874fa42079c7d43971cb1d2ada93bca4cb3d9cf271f407`,
  coverage PNG
  `991e4d64bc615388b36949400a423f78c6568e4b30c3a0ef7ed7e6a8c9021dca`,
  coverage SVG
  `306132709fdc3dcbcd5d7c84322cab862e6f131307f8acb4d3ffba4fa98c3d70`,
  series PNG
  `48fd2793a08f012f9714f3a8ed6b814614cfd1ed2a8dac2aba91b7cd1f5f3482`,
  series SVG
  `a8bb88f4878d0d2cbb8eb52fe2d610e29b00b44e15c69630b0bf4f6a001efffe`,
  diagnostic PNG
  `9ed1767ab65b425e09fb243cdeabb29dd773a51f07f7a03528aabd7ca55c40a7`,
  and diagnostic SVG
  `64d0ac653736f5776d728f9aa87ed2deba2fcfa0dcb16e763f0de46b2ec9684e`.
  Independent verification run
  `2026-09-16__0351__story-atlas-verify__6c35d78` with local MLflow run
  `bfe3efe1d5714f4e92577b8f5a03d346` matched all eight figure bytes, all four
  decision rows, metrics hash
  `33f265b1a79ec2b52e7dfc638e51e3f890bd9139e7b2eb5f48ffd1b1a2ed687a`,
  configuration hash
  `ba83d20051b69c41c73864cddc946a025e8136dc15111b0dde163fa1d3ceba05`,
  input fingerprint
  `e9805ae16527145c0030da7b4a7711989997296e02815253b84e7c426eff2b5b`,
  input records, and all stable manifest fields. Final Maker gate: Ruff passed;
  Pyright reported 0 errors and 0 warnings; all 122 Python tests passed; the
  shared and story provenance validators accepted 18 and 1 records; the Marimo
  notebook check passed; frontend typecheck, Vitest, and production build
  passed; and
  `git diff --check` passed. Graphify refreshed to 990 nodes, 1,910 edges, and
  76 communities and returned the Stage A inputs, story modules, generated
  evidence, preliminary branches, and T-003B gate without paper-lane imports.
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-14 — inline Stage A execution started with the minimal
  pinned static geospatial dependency boundary; 2026-09-14 — governed coastline
  acquisition and offline checksum rerun passed with source precision preserved;
  2026-09-14 — exposed exact-grid coverage states by reusing the shared CSV and
  UTC validators without changing the existing missingness writer; 2026-09-14 —
  added immutable source-preserving atlas records, strict Stage A scope checks,
  interpolated Pacific seam splits, and WGS84 distance rings; 2026-09-14 —
  added the deterministic Pacific evidence map with explicit projection,
  preliminary-state, candidate-marker, and non-continuous-field labels;
  2026-09-14 — added source-window coverage strips with separate observed,
  source-blank, absent-timestamp, and unsnapped off-grid encodings; 2026-09-14 —
  added source-honest station point panels with no centering, smoothing,
  interpolation, resampling, shared y-scale, or gap-bridging line; 2026-09-14 —
  added the side-by-side geodesic-range/published-contour shape diagnostic with
  explicit incompatible units and nearest-contour prohibition; 2026-09-16 —
  added the preview/review-aware reproducible runner with overwrite refusal,
  story-lane fences, checksum reconciliation, and no-partial-output tests;
  2026-09-16 — added the read-only reactive atlas viewer and verified its empty
  state without loading normalized tables, plotting, tracking, or writing;
  2026-09-16 — stopped the first real-atlas review on a visible seam defect,
  traced it to exact-boundary longitude normalization, and fixed the root cause
  with a typed projection regression and real-data spatial rerender;
  2026-09-16 — rejected the first canonical report's stale preview prose and
  added tested state-specific interpretation, takeaways, and next steps;
  2026-09-16 — generated the corrected clean-SHA canonical atlas, executed the
  thin notebook, and independently reproduced stable scientific and visual
  evidence byte-for-byte; the full repository gate and Graphify query passed,
  and the Maker result was submitted for independent review; 2026-10-05 —
  independent Checker reproduced all eight figure files and traced inputs and
  outputs. Fixed blank populated notebook rendering with a RED/GREEN visible-
  export regression. Checker accepts preliminary diagnostic scope; public-scene
  label collisions, contour contrast and small-width typography remain explicit
  follow-ups in `docs/reviews/2026-10-05-stage-a-checker.md`.
- Status: done

## T-003B — Complete the reviewed arrival comparison

- ID: T-003B
- Title: Test and promote the visual-story contrast
- Depends on: T-003A done and a shared release explicitly grants arrival-comparison permission
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
- Evidence: T-002E completed with `revise_arrival_comparison`; the descriptive
  release sets `arrival_comparison_allowed=false`. A file's existence is not
  promotion. First resolve observed-onset validation and a modeled-arrival
  product, or separately approve a story pivot that does not need that comparison.
- Attempts / Max: 0 / 3
- Attempt log: not started
- Status: blocked (scientific arrival-comparison gate)
