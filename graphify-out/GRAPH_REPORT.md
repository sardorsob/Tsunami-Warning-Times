# Graph Report - Tsunami-Warning-Times  (2026-10-05)

## Corpus Check
- 166 files · ~756,770 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1064 nodes · 2064 edges · 80 communities (66 shown, 14 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 69 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7b87d6dc`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- compilerOptions
- validate_manifest
- app/package.json
- test_acquisition.py
- package.json
- App.tsx
- check-build.mjs
- __init__.py
- pacific-tsunami-warning-time
- Handover
- Data Card — Tōhoku Data-Proof Candidate
- Tōhoku Data Pipeline and EDA Design
- Decision Log
- Tasks
- Validation Plan
- Methodology — Draft Contract
- Historical Event Protocol
- Problem
- Concept
- Scope
- Spatial Contract
- Assumptions and Unknowns
- Hazard Event Set
- PacificVis Storytelling Benchmark, 2017–2026
- artifacts/README.md
- Experiment Ledger
- FORECAST_REPORT.md
- MODEL_CARD.md
- STRUCTURE.md
- competition.md
- data/README.md
- PacificVis 2027 Dual-Track Repository Design
- Global Constraints
- T-002A — Tōhoku Source-Contract Ledger
- Tōhoku Normalization and Data-Quality Report
- Tōhoku Missingness EDA
- Acquisition run notes
- Acquisition run notes
- test_normalize.py
- Normalization and data-quality run notes
- Acquisition run notes
- Acquisition run notes
- Acquisition run notes
- Acquisition run notes
- Acquisition run notes
- missingness.py
- Project Contract
- Project Instructions
- Pacific Tsunami Warning Time
- Acquisition run notes
- tohoku_missingness.py
- 2026-09-09__1749__missingness__7b6d386/notes.md
- Visual-Story Adaptive EDA Design
- Originality and Track Compatibility Ledger
- Visual Story Contract
- Visual-Story EDA Report
- Visual Storyboard
- Visual Story Tasks
- File Structure
- analysis/__init__.py
- plots.py
- build_story_atlas.py
- Acquisition run notes
- Acquisition run notes
- Visual-Story Source Notes
- test_story_atlas_cli.py
- AtlasError
- test_atlas.py
- build_series_panels
- tohoku_storyboard_eda.py
- test_eda.py
- Dataset gathering
- 2026-09-16__0351__story-atlas__6c35d78/notes.md
- Global constraints
- Independent Stage A Checker review
- Tōhoku timing audit protocol
- test_notebook_render.py

## God Nodes (most connected - your core abstractions)
1. `AtlasError` - 49 edges
2. `NormalizationError` - 41 edges
3. `build_tables()` - 40 edges
4. `load_atlas_inputs()` - 28 edges
5. `acquire_source()` - 28 edges
6. `_run()` - 28 edges
7. `SourceContract` - 23 edges
8. `write_run_evidence()` - 21 edges
9. `plot_distance_contour_diagnostic()` - 20 edges
10. `Handover` - 20 edges

## Surprising Connections (you probably didn't know these)
- `main()` --uses--> `AtlasError`  [INFERRED]
  scripts/story/build_story_atlas.py → analysis/story/atlas.py
- `test_atlas_loader_rejects_unflagged_longitude_outside_precision_tolerance()` --uses--> `AtlasError`  [INFERRED]
  tests/story/test_atlas.py → analysis/story/atlas.py
- `test_decision_input_rejects_incomplete_or_promoting_review()` --uses--> `AtlasError`  [INFERRED]
  tests/story/test_story_atlas_cli.py → analysis/story/atlas.py
- `_rejection_count()` --uses--> `AtlasInputs`  [INFERRED]
  scripts/story/build_story_atlas.py → analysis/story/atlas.py
- `validate_stage_a_scope()` --uses--> `ExpectedWindow`  [INFERRED]
  analysis/story/atlas.py → pipeline/missingness.py

## Import Cycles
- None detected.

## Communities (80 total, 14 thin omitted)

### Community 0 - "compilerOptions"
Cohesion: 0.08
Nodes (25): compilerOptions, allowJs, allowSyntheticDefaultImports, esModuleInterop, forceConsistentCasingInFileNames, isolatedModules, jsx, lib (+17 more)

### Community 1 - "validate_manifest"
Cohesion: 0.16
Nodes (26): main(), ManifestError, Path, ValueError, Validate the project's source-provenance manifest., Run manifest validation from the command line., Raised when the source manifest violates its documented contract., Summary of a successful manifest validation. (+18 more)

### Community 2 - "app/package.json"
Cohesion: 0.06
Nodes (32): dependencies, react, react-dom, devDependencies, @types/node, @types/react, @types/react-dom, typescript (+24 more)

### Community 3 - "test_acquisition.py"
Cohesion: 0.06
Nodes (99): HTTPRedirectHandler, MonkeyPatch, acquire_all(), acquire_source(), AcquisitionResult, _checksum_path(), ContractError, download_url() (+91 more)

### Community 4 - "package.json"
Cohesion: 0.13
Nodes (14): engines, node, name, packageManager, private, scripts, build, check (+6 more)

### Community 5 - "App.tsx"
Cohesion: 0.36
Nodes (4): App(), root, ProjectPhase, ProjectStatus

### Community 10 - "Handover"
Cohesion: 0.10
Nodes (20): Accepted Saipan source recovery, Completed, Completed Valparaíso recovery, Continue from here, Decisions and assumptions, Dual-track design checkpoint, External track-compatibility guidance, Final disposition (+12 more)

### Community 11 - "Data Card — Tōhoku Data-Proof Candidate"
Cohesion: 0.06
Nodes (28): Source Manifest Contract, Actual normalized grains, Current coverage and quality, Data Card — Tōhoku Data-Proof Candidate, Data-proof acquisition set, Known misuse risk, Minimum record contract, Missingness profile (+20 more)

### Community 12 - "Tōhoku Data Pipeline and EDA Design"
Cohesion: 0.13
Nodes (14): Acquisition behavior, Approved choices, Architecture, Canonical records, Commit boundaries, Data flow, Dependencies and deliberate deferrals, EDA contract (+6 more)

### Community 13 - "Decision Log"
Cohesion: 0.12
Nodes (16): D-001 — Minimal split repository shell, D-002 — Event selection remains gated, D-003 — Dependencies follow demonstrated need, D-004 — Tōhoku is provisional, not frozen, D-005 — Use physical-travel-time wording by default, D-006 — Use a broad but source-gated Tōhoku data proof, D-007 — Scripts own calculations; marimo exposes EDA, D-008 — Markdown is the canonical result surface (+8 more)

### Community 14 - "Tasks"
Cohesion: 0.12
Nodes (17): T-000 — Prepare the repository, T-001 — Select a feasible event, T-002A — Resolve source endpoints and contracts, T-002B — Acquire and fingerprint raw assets, T-002C1 — Recover and normalize Saipan event data, T-002C2 — Recover and normalize Valparaíso research data, T-002C — Normalize and validate analysis tables, T-002D — Run reproducible EDA (+9 more)

### Community 15 - "Validation Plan"
Cohesion: 0.22
Nodes (8): Acquisition and accounting, Analytical, Cartographic and interaction, Release, Source and identity, Spatial and raster, Temporal, Validation Plan

### Community 16 - "Methodology — Draft Contract"
Cohesion: 0.25
Nodes (7): 1. Feasibility, 2. Provenance and data proof, 3. Timing definitions, 4. Baseline and comparison, 5. Visual validation, 6. Reproducibility, Methodology — Draft Contract

### Community 17 - "Historical Event Protocol"
Cohesion: 0.29
Nodes (6): Comparison sequence, Data-proof sequencing, Historical Event Protocol, Purpose, Required definitions before execution, Stop conditions

### Community 18 - "Problem"
Cohesion: 0.33
Nodes (5): Decision value, Problem, Question, Success, What would mislead

### Community 19 - "Concept"
Cohesion: 0.33
Nodes (5): Candidate discovery sequence, Candidate thesis, Concept, Experience guardrails, Visual direction

### Community 20 - "Scope"
Cohesion: 0.40
Nodes (4): Deferred, Feasibility gate, First complete version, Scope

### Community 21 - "Spatial Contract"
Cohesion: 0.40
Nodes (4): Current state, Required per-source fields, Spatial Contract, Working output rules

### Community 22 - "Assumptions and Unknowns"
Cohesion: 0.50
Nodes (3): Assumptions and Unknowns, Unresolved—do not treat as facts, Working assumptions

### Community 23 - "Hazard Event Set"
Cohesion: 0.40
Nodes (4): Contract, Current state, Hazard Event Set, Tōhoku data-proof bundle

### Community 24 - "PacificVis Storytelling Benchmark, 2017–2026"
Cohesion: 0.50
Nodes (3): Cross-year criteria for this project, Originality boundary, PacificVis Storytelling Benchmark, 2017–2026

### Community 32 - "PacificVis 2027 Dual-Track Repository Design"
Cohesion: 0.08
Nodes (24): Commit boundaries, Conference paper, Confirmed targets and dates, Data and experiment flow, Deliberate deferrals, Failure and change handling, Originality firewall, Outcome (+16 more)

### Community 33 - "Global Constraints"
Cohesion: 0.25
Nodes (7): Global Constraints, Task 1: Source-contract ledger and blocked-state validation, Task 2: Atomic, source-independent acquisition core, Task 3: Live source bundle, checksums, and acquisition report, Task 4: Event, contour, and water-level normalization, Task 5: Live data-quality build and requested-phase closure, Tōhoku Data Coverage and Implementation Plan

### Community 34 - "T-002A — Tōhoku Source-Contract Ledger"
Cohesion: 0.20
Nodes (10): Approved contracts — 17 assets, Authoritative evidence and observed smoke checks, Blocked contracts — 1 asset, Contract limits and next steps, Disposition, Downstream missingness reconciliation, Saipan recovery evidence, T-002A — Tōhoku Source-Contract Ledger (+2 more)

### Community 35 - "Tōhoku Normalization and Data-Quality Report"
Cohesion: 0.18
Nodes (10): Disposition, Downstream missingness profile, Event and contour quality, Interpretation, limitations, and next steps, Manual scientific QA, Observation quality, Output contract and reconciliation, Rejections and adaptive finding (+2 more)

### Community 36 - "Tōhoku Missingness EDA"
Cohesion: 0.14
Nodes (13): Adaptive EDA decision ledger, Checks performed, Coastal completeness, DART cadence, Generated machine-readable outputs, Input and output fingerprints, Limitations, takeaways, and next steps, Missingness mechanisms (+5 more)

### Community 37 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 38 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 39 - "test_normalize.py"
Cohesion: 0.06
Nodes (103): build_tables(), BuildResult, _coastal_input_count(), _coordinate_part(), _csv_value(), _dart_input_count(), EventRecord, _feature_reference() (+95 more)

### Community 40 - "Normalization and data-quality run notes"
Cohesion: 0.40
Nodes (4): Adaptive finding, Disposition, Limits, Normalization and data-quality run notes

### Community 41 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 42 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 43 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 44 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 45 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 46 - "missingness.py"
Cohesion: 0.08
Nodes (59): build_coastal_coverage_timelines(), CoastalWindowProfile, CoveragePosition, DartCadenceProfile, ExpectedWindow, _load_accounting(), load_expected_windows(), _mechanism_rows() (+51 more)

### Community 47 - "Project Contract"
Cohesion: 0.22
Nodes (9): Consequential unknowns, Current visual-story planning deliverable, Decision and lane, In scope for the first complete version, Objective, Out of scope until separately approved, Project Contract, Smallest useful deliverable (+1 more)

### Community 48 - "Project Instructions"
Cohesion: 0.29
Nodes (6): graphify, Non-negotiable scientific rules, Project Instructions, Scope and implementation rules, Start here, Verification

### Community 49 - "Pacific Tsunami Warning Time"
Cohesion: 0.20
Nodes (10): Current status, Evidence and reporting, License, Local setup, Pacific Tsunami Warning Time, PacificVis 2027 — Conference Paper + Visual Data Storytelling Contest, Paper and visual-story separation, Project at a glance (+2 more)

### Community 50 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 52 - "tohoku_missingness.py"
Cohesion: 0.39
Nodes (8): artifact_selector(), coastal_table(), headline_metrics(), imports(), interpretation(), load_summary(), cell, title()

### Community 54 - "Visual-Story Adaptive EDA Design"
Cohesion: 0.09
Nodes (22): Adaptive decision ledger, Approaches considered, Approved choices, Architecture and ownership, Artifact contract, Color and accessibility, Dependency contract, Evidence boundary (+14 more)

### Community 55 - "Originality and Track Compatibility Ledger"
Cohesion: 0.25
Nodes (7): Correspondence received 2026-09-13, Current disposition, Evidence history, Originality and Track Compatibility Ledger, Pending response, Purpose, Working overlap boundary

### Community 56 - "Visual Story Contract"
Cohesion: 0.25
Nodes (7): Contribution boundary, Evidence states, First deliverable, Governing design, Question, Status, Visual Story Contract

### Community 57 - "Visual-Story EDA Report"
Cohesion: 0.15
Nodes (12): Adaptive decision ledger, Fixed diagnostic atlas, Generated atlas evidence, Input and output fingerprints, Inputs, Inputs and source boundary, Interpretation, Limitations (+4 more)

### Community 58 - "Visual Storyboard"
Cohesion: 0.33
Nodes (5): Candidate discovery questions, Preliminary branches, Promotion rule, Status, Visual Storyboard

### Community 59 - "Visual Story Tasks"
Cohesion: 0.33
Nodes (5): T-003A — Build the preliminary diagnostic atlas, T-003B — Complete the reviewed arrival comparison, T-003I — Plan the Stage A diagnostic atlas implementation, T-003P — Approve the adaptive visual-story EDA design, Visual Story Tasks

### Community 60 - "File Structure"
Cohesion: 0.11
Nodes (18): Create, File Structure, Generated by the implementation, Global Constraints, Modify, Stage A Completion Gate, Task 10: Add the thin Marimo atlas viewer, Task 11: Run the real atlas and record adaptive findings (+10 more)

### Community 63 - "plots.py"
Cohesion: 0.10
Nodes (45): AtlasInputs, project_line_parts(), Shift a longitude into the Pacific display domain [-340, 20)., Split linework at 20°E while retaining an endpoint on each seam side., Project unwrapped Pacific linework without normalizing its seam endpoints., Validated normalized inputs for preliminary story diagnostics., shift_longitude(), split_at_display_seam() (+37 more)

### Community 64 - "build_story_atlas.py"
Cohesion: 0.13
Nodes (36): DecisionRecord, display_path(), load_decision_input(), _png_dimensions(), preview_decisions(), Path, Inspectable evidence artifacts for the preliminary visual-story atlas., Write stable human-readable JSON. (+28 more)

### Community 65 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 66 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 68 - "test_story_atlas_cli.py"
Cohesion: 0.35
Nodes (16): main(), Run the fixed Stage A atlas and write reconstructable evidence., _cli_args(), parametrize, Path, _replace_arg(), _sha256(), _stage_cli_fixture() (+8 more)

### Community 69 - "AtlasError"
Cohesion: 0.14
Nodes (27): AtlasConfig, AtlasError, _boolean(), _coordinate(), _finite(), geodesic_range_ring(), _integer_tuple(), load_atlas_config() (+19 more)

### Community 70 - "test_atlas.py"
Cohesion: 0.20
Nodes (23): ContourRecord, EventRecord, load_atlas_inputs(), ObservationRecord, Load normalized inputs while preserving source semantics and explicit unknowns., Reviewed event identity and origin., Source-stated station location and measurement semantics., One observation with source time kept separate from verified UTC. (+15 more)

### Community 71 - "build_series_panels"
Cohesion: 0.33
Nodes (6): build_series_panels(), One retained numeric value positioned relative to earthquake origin., A station-local series whose y-scale must not be shared., Build station-local point series without smoothing, centering, or resampling., SeriesPanel, SeriesPoint

### Community 72 - "tohoku_storyboard_eda.py"
Cohesion: 0.36
Nodes (9): decision_ledger(), discover_manifests(), evidence_boundary(), generated_figures(), imports(), load_manifest(), cell, require_manifest() (+1 more)

### Community 73 - "test_eda.py"
Cohesion: 0.11
Nodes (46): Any, audit(), fingerprint(), Path, Checksummed, descriptive shared EDA; no arrival or story-selection promotion., Record bytes and a portable repository-relative path., Require rectangular CSV records, including for provenance inputs., Describe retained values and gaps without dropping outliers or imputing. (+38 more)

### Community 74 - "Dataset gathering"
Cohesion: 0.40
Nodes (5): Collection and validation rules, Data flow, Dataset gathering, Reproducing the pipeline, Source inventory

### Community 76 - "Global constraints"
Cohesion: 0.22
Nodes (8): Global constraints, Review focus, Shared EDA and scientific closure implementation plan, Task 1: Freeze diagnostic protocol and task boundaries, Task 2: Implement shared audit and sensitivity core, Task 3: Add report runner and thin notebook, Task 4: Execute and follow findings, Task 5: Independently review and close with an explicit disposition

### Community 77 - "Independent Stage A Checker review"
Cohesion: 0.29
Nodes (6): Commands and results, Independent Stage A Checker review, R1 independent recheck and final disposition, R1 — Populated notebook renders no visible content, Rendered-image review and chart checker, Reproducibility and provenance

### Community 78 - "Tōhoku timing audit protocol"
Cohesion: 0.40
Nodes (4): Adaptive sequence and acceptance, Frozen rules, Measurement contract, Tōhoku timing audit protocol

### Community 79 - "test_notebook_render.py"
Cohesion: 0.50
Nodes (3): Path, Verify visible notebook output, not just successful execution., test_populated_atlas_notebook_displays_figures_and_decisions()

## Knowledge Gaps
- **373 isolated node(s):** `name`, `private`, `version`, `type`, `node` (+368 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SourceContract` connect `test_acquisition.py` to `test_normalize.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `load_contracts()` connect `test_acquisition.py` to `validate_manifest`, `test_normalize.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `build_tables()` connect `test_normalize.py` to `test_acquisition.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `AtlasError` (e.g. with `main()` and `test_atlas_loader_rejects_unflagged_longitude_outside_precision_tolerance()`) actually correct?**
  _`AtlasError` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `NormalizationError` (e.g. with `main()` and `test_build_tables_exposes_an_invalid_contract_as_a_normalization_error()`) actually correct?**
  _`NormalizationError` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `build_tables()` (e.g. with `ContractError` and `SourceContract`) actually correct?**
  _`build_tables()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _373 weakly-connected nodes found - possible documentation gaps or missing edges._