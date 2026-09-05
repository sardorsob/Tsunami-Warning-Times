# Graph Report - Tsunami-Warning-Times  (2026-09-05)

## Corpus Check
- 45 files · ~18,444 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 303 nodes · 306 edges · 37 communities (27 shown, 10 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `76c98919`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- compilerOptions
- validate_manifest
- app/package.json
- devDependencies
- package.json
- App.tsx
- check-build.mjs
- __init__.py
- pacific-tsunami-warning-time
- Handover
- PacificVis 2027 and tsunami-event data feasibility
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
- Project Contract
- Global Constraints
- T-002A — Tōhoku Source-Contract Ledger

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 17 edges
2. `validate_manifest()` - 15 edges
3. `Tōhoku Data Pipeline and EDA Design` - 14 edges
4. `Decision Log` - 12 edges
5. `Tasks` - 12 edges
6. `write_manifest()` - 11 edges
7. `ManifestError` - 10 edges
8. `Handover` - 10 edges
9. `PacificVis 2027 and tsunami-event data feasibility` - 9 edges
10. `Data Card — Feasibility State` - 8 edges

## Surprising Connections (you probably didn't know these)
- `test_manifest_rejects_an_unresolved_spatial_field()` --uses--> `ManifestError`  [INFERRED]
  tests/test_provenance.py → pipeline/provenance.py
- `test_manifest_rejects_duplicate_source_ids()` --uses--> `ManifestError`  [INFERRED]
  tests/test_provenance.py → pipeline/provenance.py
- `test_manifest_rejects_inconsistent_download_state()` --uses--> `ManifestError`  [INFERRED]
  tests/test_provenance.py → pipeline/provenance.py
- `test_manifest_rejects_local_path_traversal()` --uses--> `ManifestError`  [INFERRED]
  tests/test_provenance.py → pipeline/provenance.py
- `test_manifest_requires_extended_iso_access_date()` --uses--> `ManifestError`  [INFERRED]
  tests/test_provenance.py → pipeline/provenance.py

## Import Cycles
- None detected.

## Communities (37 total, 10 thin omitted)

### Community 0 - "compilerOptions"
Cohesion: 0.08
Nodes (25): compilerOptions, allowJs, allowSyntheticDefaultImports, esModuleInterop, forceConsistentCasingInFileNames, isolatedModules, jsx, lib (+17 more)

### Community 1 - "validate_manifest"
Cohesion: 0.18
Nodes (24): parametrize, main(), ManifestError, Path, Validate the project's source-provenance manifest., Run manifest validation from the command line., Raised when the source manifest violates its documented contract., Summary of a successful manifest validation. (+16 more)

### Community 2 - "app/package.json"
Cohesion: 0.11
Nodes (17): dependencies, react, react-dom, engines, node, name, private, scripts (+9 more)

### Community 3 - "devDependencies"
Cohesion: 0.13
Nodes (15): devDependencies, @types/node, @types/react, @types/react-dom, typescript, vite, @vitejs/plugin-react, vitest (+7 more)

### Community 4 - "package.json"
Cohesion: 0.13
Nodes (14): engines, node, name, packageManager, private, scripts, build, check (+6 more)

### Community 5 - "App.tsx"
Cohesion: 0.36
Nodes (4): App(), root, ProjectPhase, ProjectStatus

### Community 10 - "Handover"
Cohesion: 0.08
Nodes (22): graphify, Non-negotiable scientific rules, Project Instructions, Scope and implementation rules, Start here, Verification, Completed, Continue from here (+14 more)

### Community 11 - "PacificVis 2027 and tsunami-event data feasibility"
Cohesion: 0.08
Nodes (20): Source Manifest Contract, Data Card — Feasibility State, Data-proof acquisition set, Known misuse risk, Minimum record contract, Planned grains, Required source classes, Sensitive data and authorization (+12 more)

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

### Community 32 - "Project Contract"
Cohesion: 0.25
Nodes (8): Consequential unknowns, Decision and lane, In scope for the first complete version, Objective, Out of scope until separately approved, Project Contract, Smallest useful deliverable, Workflow contract

### Community 33 - "Global Constraints"
Cohesion: 0.25
Nodes (7): Global Constraints, Task 1: Source-contract ledger and blocked-state validation, Task 2: Atomic, source-independent acquisition core, Task 3: Live source bundle, checksums, and acquisition report, Task 4: Event, contour, and water-level normalization, Task 5: Live data-quality build and requested-phase closure, Tōhoku Data Coverage and Implementation Plan

### Community 34 - "T-002A — Tōhoku Source-Contract Ledger"
Cohesion: 0.29
Nodes (6): Approved contracts — 11 assets, Authoritative evidence and observed smoke checks, Blocked contracts — 4 assets, Contract limits and next steps, Disposition, T-002A — Tōhoku Source-Contract Ledger

## Knowledge Gaps
- **189 isolated node(s):** `name`, `private`, `version`, `type`, `node` (+184 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `name`, `private`, `version` to the rest of the system?**
  _189 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `compilerOptions` be split into smaller, more focused modules?**
  _Cohesion score 0.07692307692307693 - nodes in this community are weakly interconnected._
- **Should `app/package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Should `devDependencies` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `Handover` be split into smaller, more focused modules?**
  _Cohesion score 0.07692307692307693 - nodes in this community are weakly interconnected._
- **Should `PacificVis 2027 and tsunami-event data feasibility` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._