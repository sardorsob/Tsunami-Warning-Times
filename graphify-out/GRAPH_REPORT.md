# Graph Report - Tsunami-Warning-Times  (2026-09-05)

## Corpus Check
- 83 files · ~46,857 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 513 nodes · 893 edges · 43 communities (33 shown, 10 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5689f18a`
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
- EXPERIMENTS.md
- FORECAST_REPORT.md
- MODEL_CARD.md
- STRUCTURE.md
- competition.md
- data/README.md
- acquire_tohoku.py
- Global Constraints
- T-002A — Tōhoku Source-Contract Ledger
- Tōhoku Normalization and Data-Quality Report
- Acquisition run notes
- Acquisition run notes
- test_normalize.py
- Normalization and data-quality run notes
- Acquisition run notes
- Acquisition run notes

## God Nodes (most connected - your core abstractions)
1. `NormalizationError` - 36 edges
2. `build_tables()` - 35 edges
3. `acquire_source()` - 28 edges
4. `SourceContract` - 23 edges
5. `write_run_evidence()` - 20 edges
6. `normalize_ttt()` - 19 edges
7. `sample_contract()` - 19 edges
8. `normalize_dart()` - 18 edges
9. `compilerOptions` - 17 edges
10. `normalize_coastal()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `_contract_record()` --uses--> `SourceContract`  [INFERRED]
  scripts/acquire_tohoku.py → pipeline/acquisition.py
- `_validate_evidence_ids()` --uses--> `SourceContract`  [INFERRED]
  scripts/acquire_tohoku.py → pipeline/acquisition.py
- `write_run_evidence()` --uses--> `SourceContract`  [INFERRED]
  scripts/acquire_tohoku.py → pipeline/acquisition.py
- `offline_fetcher()` --uses--> `ResponseMetadata`  [INFERRED]
  scripts/acquire_tohoku.py → pipeline/acquisition.py
- `_result_record()` --uses--> `AcquisitionResult`  [INFERRED]
  scripts/acquire_tohoku.py → pipeline/acquisition.py

## Import Cycles
- None detected.

## Communities (43 total, 10 thin omitted)

### Community 0 - "compilerOptions"
Cohesion: 0.08
Nodes (25): compilerOptions, allowJs, allowSyntheticDefaultImports, esModuleInterop, forceConsistentCasingInFileNames, isolatedModules, jsx, lib (+17 more)

### Community 1 - "validate_manifest"
Cohesion: 0.18
Nodes (24): main(), ManifestError, Path, ValueError, Validate the project's source-provenance manifest., Run manifest validation from the command line., Raised when the source manifest violates its documented contract., Summary of a successful manifest validation. (+16 more)

### Community 2 - "app/package.json"
Cohesion: 0.06
Nodes (32): dependencies, react, react-dom, devDependencies, @types/node, @types/react, @types/react-dom, typescript (+24 more)

### Community 3 - "test_acquisition.py"
Cohesion: 0.11
Nodes (58): Fetcher, MonkeyPatch, acquire_all(), acquire_source(), AcquisitionResult, _checksum_path(), download_url(), _fetch_with_retries() (+50 more)

### Community 4 - "package.json"
Cohesion: 0.13
Nodes (14): engines, node, name, packageManager, private, scripts, build, check (+6 more)

### Community 5 - "App.tsx"
Cohesion: 0.36
Nodes (4): App(), root, ProjectPhase, ProjectStatus

### Community 10 - "Handover"
Cohesion: 0.05
Nodes (33): graphify, Non-negotiable scientific rules, Project Instructions, Scope and implementation rules, Start here, Verification, Completed, Continue from here (+25 more)

### Community 11 - "Data Card — Tōhoku Data-Proof Candidate"
Cohesion: 0.08
Nodes (21): Source Manifest Contract, Actual normalized grains, Current coverage and quality, Data Card — Tōhoku Data-Proof Candidate, Data-proof acquisition set, Known misuse risk, Minimum record contract, Required source classes (+13 more)

### Community 12 - "Tōhoku Data Pipeline and EDA Design"
Cohesion: 0.13
Nodes (14): Acquisition behavior, Approved choices, Architecture, Canonical records, Commit boundaries, Data flow, Dependencies and deliberate deferrals, EDA contract (+6 more)

### Community 13 - "Decision Log"
Cohesion: 0.15
Nodes (12): D-001 — Minimal split repository shell, D-002 — Event selection remains gated, D-003 — Dependencies follow demonstrated need, D-004 — Tōhoku is provisional, not frozen, D-005 — Use physical-travel-time wording by default, D-006 — Use a broad but source-gated Tōhoku data proof, D-007 — Scripts own calculations; marimo exposes EDA, D-008 — Markdown is the canonical result surface (+4 more)

### Community 14 - "Tasks"
Cohesion: 0.15
Nodes (12): T-000 — Prepare the repository, T-001 — Select a feasible event, T-002A — Resolve source endpoints and contracts, T-002B — Acquire and fingerprint raw assets, T-002C — Normalize and validate analysis tables, T-002D — Run reproducible EDA, T-002E — Review and close the data proof, T-002P — Approve the broad data-proof design (+4 more)

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
Nodes (5): Concept, Discovery sequence, Experience guardrails, Thesis, Visual direction

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

### Community 32 - "acquire_tohoku.py"
Cohesion: 0.13
Nodes (25): ContractError, ValueError, Raised when a source-contract TOML file violates the acquisition contract., _contract_record(), git_short_sha(), main(), offline_fetcher(), datetime (+17 more)

### Community 33 - "Global Constraints"
Cohesion: 0.25
Nodes (7): Global Constraints, Task 1: Source-contract ledger and blocked-state validation, Task 2: Atomic, source-independent acquisition core, Task 3: Live source bundle, checksums, and acquisition report, Task 4: Event, contour, and water-level normalization, Task 5: Live data-quality build and requested-phase closure, Tōhoku Data Coverage and Implementation Plan

### Community 34 - "T-002A — Tōhoku Source-Contract Ledger"
Cohesion: 0.25
Nodes (7): Approved contracts — 12 assets, Authoritative evidence and observed smoke checks, Blocked contracts — 3 assets, Contract limits and next steps, Disposition, T-002A — Tōhoku Source-Contract Ledger, T-002B clean live evidence

### Community 35 - "Tōhoku Normalization and Data-Quality Report"
Cohesion: 0.20
Nodes (9): Disposition, Event and contour quality, Interpretation, limitations, and next steps, Manual scientific QA, Observation quality, Output contract and reconciliation, Rejections and adaptive finding, Source coverage (+1 more)

### Community 37 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 38 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 39 - "test_normalize.py"
Cohesion: 0.07
Nodes (85): build_tables(), BuildResult, _coastal_input_count(), _coordinate_part(), _csv_value(), _dart_input_count(), EventRecord, _feature_reference() (+77 more)

### Community 40 - "Normalization and data-quality run notes"
Cohesion: 0.40
Nodes (4): Adaptive finding, Disposition, Limits, Normalization and data-quality run notes

### Community 41 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

### Community 42 - "Acquisition run notes"
Cohesion: 0.50
Nodes (3): Acquisition run notes, Decision, Limitations

## Knowledge Gaps
- **213 isolated node(s):** `name`, `private`, `version`, `type`, `node` (+208 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_tables()` connect `test_normalize.py` to `acquire_tohoku.py`, `test_acquisition.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `validate_manifest()` connect `validate_manifest` to `test_acquisition.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `SourceContract` connect `test_acquisition.py` to `acquire_tohoku.py`, `test_normalize.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `NormalizationError` (e.g. with `main()` and `test_build_tables_exposes_an_invalid_contract_as_a_normalization_error()`) actually correct?**
  _`NormalizationError` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `build_tables()` (e.g. with `ContractError` and `SourceContract`) actually correct?**
  _`build_tables()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `SourceContract` (e.g. with `build_tables()` and `_load_stations()`) actually correct?**
  _`SourceContract` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _213 weakly-connected nodes found - possible documentation gaps or missing edges._