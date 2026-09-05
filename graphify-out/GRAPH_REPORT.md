# Graph Report - Tsunami-Warning-Times  (2026-09-04)

## Corpus Check
- 40 files · ~11,785 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 253 nodes · 258 edges · 32 communities (22 shown, 10 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b7a67959`
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
- Project Contract
- PacificVis 2027 and tsunami-event data feasibility
- Handover
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

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 17 edges
2. `validate_manifest()` - 14 edges
3. `ManifestError` - 10 edges
4. `write_manifest()` - 10 edges
5. `Handover` - 9 edges
6. `PacificVis 2027 and tsunami-event data feasibility` - 9 edges
7. `Project Contract` - 8 edges
8. `Decision Log` - 7 edges
9. `Tasks` - 7 edges
10. `Validation Plan` - 7 edges

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

## Communities (32 total, 10 thin omitted)

### Community 0 - "compilerOptions"
Cohesion: 0.08
Nodes (25): compilerOptions, allowJs, allowSyntheticDefaultImports, esModuleInterop, forceConsistentCasingInFileNames, isolatedModules, jsx, lib (+17 more)

### Community 1 - "validate_manifest"
Cohesion: 0.20
Nodes (22): parametrize, main(), ManifestError, Path, Validate the project's source-provenance manifest., Run manifest validation from the command line., Raised when the source manifest violates its documented contract., Summary of a successful manifest validation. (+14 more)

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

### Community 10 - "Project Contract"
Cohesion: 0.08
Nodes (20): graphify, Non-negotiable scientific rules, Project Instructions, Scope and implementation rules, Start here, Verification, Consequential unknowns, Decision and lane (+12 more)

### Community 11 - "PacificVis 2027 and tsunami-event data feasibility"
Cohesion: 0.09
Nodes (18): Source Manifest Contract, Data Card — Feasibility State, Known misuse risk, Minimum record contract, Required source classes, Sensitive data and authorization, Status, Data Sources (+10 more)

### Community 12 - "Handover"
Cohesion: 0.22
Nodes (9): Completed, Continue from here, Decisions and assumptions, Final disposition, Handover, Objective and workflow, Repository state, Risks and blockers (+1 more)

### Community 13 - "Decision Log"
Cohesion: 0.25
Nodes (7): D-001 — Minimal split repository shell, D-002 — Event selection remains gated, D-003 — Dependencies follow demonstrated need, D-004 — Tōhoku is provisional, not frozen, D-005 — Use physical-travel-time wording by default, Decision Log, Open decisions

### Community 14 - "Tasks"
Cohesion: 0.25
Nodes (7): T-000 — Prepare the repository, T-001 — Select a feasible event, T-002 — Prove the data path, T-003 — Make the static scientific comparison, T-004 — Test the wavefront mechanism, T-005 — Build and package the story, Tasks

### Community 15 - "Validation Plan"
Cohesion: 0.25
Nodes (7): Analytical, Cartographic and interaction, Release, Source and identity, Spatial and raster, Temporal, Validation Plan

### Community 16 - "Methodology — Draft Contract"
Cohesion: 0.25
Nodes (7): 1. Feasibility, 2. Provenance and data proof, 3. Timing definitions, 4. Baseline and comparison, 5. Visual validation, 6. Reproducibility, Methodology — Draft Contract

### Community 17 - "Historical Event Protocol"
Cohesion: 0.33
Nodes (5): Comparison sequence, Historical Event Protocol, Purpose, Required definitions before execution, Stop conditions

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
Cohesion: 0.50
Nodes (3): Contract, Current state, Hazard Event Set

### Community 24 - "PacificVis Storytelling Benchmark, 2017–2026"
Cohesion: 0.50
Nodes (3): Cross-year criteria for this project, Originality boundary, PacificVis Storytelling Benchmark, 2017–2026

## Knowledge Gaps
- **150 isolated node(s):** `name`, `private`, `version`, `type`, `node` (+145 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Handover` connect `Handover` to `Project Contract`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `ManifestError` (e.g. with `test_manifest_rejects_an_unresolved_spatial_field()` and `test_manifest_rejects_duplicate_source_ids()`) actually correct?**
  _`ManifestError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _150 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `compilerOptions` be split into smaller, more focused modules?**
  _Cohesion score 0.07692307692307693 - nodes in this community are weakly interconnected._
- **Should `app/package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Should `devDependencies` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._