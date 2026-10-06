# Project Contract

## Objective

Build an original, trustworthy PacificVis 2027 browser story that explains how
one Pacific tsunami produces a bathymetry-shaped arrival field, how selected
observations compare with that field, and why physical travel time is not the
same thing as actionable public warning time.

## Workflow contract

- Execution tier: **Full**, because this is a reproducible competition artifact.
- Primary process: direct Workflow Core route from the user-supplied handoff.
- Primary catastrophe lane: **event forecast/intelligence**, used here for a
  retrospective historical-event product rather than an operational forecast.
- Mode: **research/publishable**.
- Maker: repository contributor assigned in `context/TASKS.md`.
- Checker: independent scientific reviewer when available; otherwise a recorded
  fresh-context checker pass.
- Selected domain skill for repository setup: `geo-data-engineering`.
- Skill rationale: the next evidence gate is authoritative spatial/temporal data
  acquisition with reproducible provenance, CRS, units, datum, and accounting.
- Skill evidence: the source manifest contract, spatial contract, ignored raw
  data layout, provenance validator, and validation plan in this repository.
- Paired delivery skill: `swe-devops-standards` for tests, pinned tools, CI, and
  cross-platform repository behavior.
- Current EDA domain skill: `analyze-data-quality`, applied to T-002D's completed
  missingness and timing-support audit so missing observations, absent timestamps, structural
  not-applicability, quarantine, and source-asset coverage retain separate
  definitions. The script-generated Markdown report remains canonical under
  D-007 and D-008.
- Current visual-story planning skill: `cartography-geoviz`, applied to T-003P
  so projection, antimeridian handling, NoData, comparability, visual hierarchy,
  and accessibility are part of the analytical contract rather than late-stage
  styling. `marimo-notebook` keeps the future notebook a thin view over tested
  modules and generated artifacts. `superpowers:writing-plans` converts the
  accepted T-003P design into T-003I's exact test-first execution and commit
  sequence before implementation begins.

## Decision and lane

| Field | Current contract |
| --- | --- |
| User | PacificVis judges and readers; researchers auditing the evidence |
| Action | Understand and compare physical arrival timing; not make emergency decisions |
| Horizon | One selected historical event from rupture through basin propagation |
| Extent | Pacific basin, narrowed to a small observational and community set |
| Hazard | Tsunami arrival timing; amplitude is out unless supported separately |
| Target unit | Elapsed time and UTC timestamp, definitions source-specific |
| Primary lane | Historical event intelligence |
| Secondary lane | None approved |

The repository has two submission lanes over this shared hazard-data foundation:
a scientific Conference Paper and a materially distinct Visual Data Story. New
story-specific analysis is governed by `context/story/PROJECT.md`; fitted paper
models, paper selection results, and paper figures do not enter the story lane.

## In scope for the first complete version

- one selected historical event and authoritative event metadata;
- one modeled travel-time or arrival field;
- one transparent distance-only reference;
- selected DART and tide-gauge observations with a reproducible arrival pick;
- four to six communities selected for analytical contrast;
- modeled-minus-observed timing residuals with honest precision;
- one authored Pacific projection, synchronized story clock, guided narrative,
  accessible static fallback, and compact methods/data section;
- reproducible Python preprocessing and a static React/TypeScript deployment.

## Out of scope until separately approved

Operational warnings, live feeds, evacuation routing, vulnerability or portfolio
loss, multiple-event comparison, a backend/database, machine learning,
hierarchical Bayesian modeling, 3D/globe work, universal station exploration,
and amplitude visualization without a suitable amplitude product.

## Consequential unknowns

The event, modeled product, observation records, arrival-pick method, community
set, meaning of “warning time,” projection, data licenses/terms, source CRSs,
vertical datums, and travel feasibility are unresolved. The feasibility and data
proof tasks must resolve the applicable fields before production work.

## Smallest useful deliverable

A verified event-feasibility decision followed by a reproducible Tōhoku data
proof covering USGS event metadata, NCEI TTT contours, the NCTR field, four DART
records, and six coastal-gauge candidates. Reusable scripts own the calculations,
a thin marimo notebook exposes the EDA, and Markdown reports preserve the
evidence and decisions. The browser shell is infrastructure, not scientific
evidence.

## Current visual-story planning deliverable

T-003P defines a small fixed diagnostic atlas with evidence-triggered branches.
The accepted T-002C2 build may support preliminary storyboard evidence, while
observed-arrival comparisons and station promotion remain blocked until T-002E
publishes a reviewed shared release. The current distance-versus-arrival thesis
is falsifiable and may be replaced by a stronger supported story. The project
owner accepted the written design on 2026-09-14; T-003I now holds the exact Stage
A implementation plan. The owner selected inline, task-by-task execution on
`main`; T-003A is independently accepted for preliminary diagnostics. On
2026-10-05, T-002D completed the shared adaptive audit and T-002E returned
`revise_arrival_comparison`. The versioned descriptive release does not grant
arrival permission; T-003B stays blocked. Current results and exact run pointer
are `context/EDA_REPORT.md` and `context/EDA_RUN.json`.
