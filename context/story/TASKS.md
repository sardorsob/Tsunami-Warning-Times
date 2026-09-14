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
- Evidence: project owner approved the proposed design in conversation on
  2026-09-14; written specification prepared for review
- Attempts / Max: 1 / 3
- Attempt log: 2026-09-14 — selected a fixed diagnostic atlas with adaptive
  branches and authorized a pivot if the distance-versus-arrival idea is weak
- Status: in-review

## T-003A — Build the preliminary diagnostic atlas

- ID: T-003A
- Title: Generate story-only spatial and temporal discovery views
- Depends on: T-003P done and its implementation plan approved
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
- Evidence: pending
- Attempts / Max: 0 / 3
- Attempt log: not started
- Status: pending
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
