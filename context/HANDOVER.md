# Handover

## Objective and workflow

Prepare the new Pacific Tsunami Warning Time repository for a reproducible,
scientifically defensible PacificVis 2027 project without prematurely selecting
data or overbuilding the application.

The project owner approved the broad Tōhoku acquisition, data-quality, and EDA
design on 2026-09-05 and authorized implementation of T-002A through T-002C on
`main`. T-002A source-contract discovery is active; EDA remains gated on accepted
analysis-ready data.

- Tier: Full
- Primary process: direct Workflow Core route from the supplied handoff
- Primary lane: retrospective event forecast/intelligence
- Project mode: research/publishable
- Setup domain skill: `geo-data-engineering`
- Delivery skill: `swe-devops-standards`

## Completed

- Read the full project handoff and the Core, Data Science, and Catastrophe
  Modeling & GeoAI profiles.
- Inspected comparable user repositories and retained their split Python plus
  `app/` frontend convention without copying their project content.
- Verified current competition requirements and corrected the handoff's overly
  narrow description of the initial submission formats.
- Compared 2011 Tōhoku, 2010 Maule, and 2025 Kamchatka from primary sources.
  Tōhoku is the conditional data-proof candidate, not a frozen event.
- Defined honest timing labels and separated modeled, observed, bulletin, public
  alert, first-deviation, and maximum-wave concepts.
- Added project instructions, scope/decision/scientific contracts, provenance
  inventory and validation, ignored data stages, pinned Python/Node environments,
  a minimal React/Vite status shell, tests, and immutable-SHA CI actions.
- Kept Serena entirely local: `.serena/` is ignored and absent from the current
  tracked tree while its existing files remain available in this workspace.
- Initialized Graphify's project instructions, local Codex hook, and AST graph.
  The durable graph is tracked; machine-specific roots, manifests, and caches
  remain ignored.
- Kept D3, regl/WebGL, scroll libraries, geospatial runtime dependencies,
  Playwright, a backend, and modeling tools out until demonstrated need.
- Designed the T-002P through T-002E work package: exact-source discovery,
  source-gated acquisition, normalization/data quality, script-backed marimo
  EDA, Markdown reporting, and independent scientific closure.
- Added intentionally empty acquisition, data-quality, and EDA report files.
  Their task-owned scripts will populate them when work begins.

## Verification evidence

Observed during the setup session on 2026-09-04:

- `uv sync`: Python 3.12.13 environment created; 11 packages resolved; pinned
  pytest, Ruff, and Pyright installed.
- `npm install`: 49 packages added; audit reported zero vulnerabilities.
- Python gate after corrections: the lock check and Ruff passed; Pyright reported
  0 errors; Pytest reported 8 passed; the provenance validator accepted 6 records.
- Frontend gate after corrections: TypeScript passed; Vitest reported 1 passed;
  Vite 8.2.2 built 17 modules and emitted a 191.65 kB JavaScript bundle
  (60.47 kB gzip).
- Browser QA: correct document title and heading hierarchy; expected feasibility
  copy and definition list present; no console warnings/errors; no horizontal
  overflow at default or mobile test viewport; mobile layout remained readable.
- Clean `npm ci`: 50 packages added; zero vulnerabilities. The optional macOS
  `fsevents` install script remains unapproved because the build does not need it.
- `npm audit --omit=dev`: zero vulnerabilities.
- Independent re-check: accepted after confirming paired provenance download
  state, safe repository-relative paths, Node 24.18.0 alignment, and no
  fix-induced regression.
- Graphify 0.9.50 initialization and incremental rebuild: the current graph has
  253 nodes, 258 edges, and 32 communities; `query`, `explain`, `god-nodes`, and
  multigraph diagnostics completed successfully.

These are the final fresh gate results for setup task T-000.

## T-002P verification evidence

Observed on 2026-09-04 for the planning/context package:

- Ruff passed; Pyright reported 0 errors; Pytest reported 8 passed; the
  provenance validator accepted 6 source records.
- TypeScript passed; Vitest reported 1 passed; Vite built 17 modules and verified
  both required build outputs.
- `git diff --check` passed and the changed planning surface contained no
  `TBD`, `TODO`, `FIXME`, or `XXX` placeholders.
- `ACQUISITION_REPORT.md`, `DATA_QUALITY_REPORT.md`, and `EDA_REPORT.md` were
  each verified at zero bytes and remain intentionally empty until their owning
  tasks run.

## Decisions and assumptions

- The browser product is static and retrospective, never an operational warning
  tool.
- The cross-community default wording is “time from earthquake origin to observed
  first arrival.”
- Tōhoku is only a provisional recommendation. `app/src/project.ts` intentionally
  keeps `selectedEvent` null.
- No repository code license was inferred. The owner must choose one.
- No raw scientific data was downloaded; no reportable scientific result exists.
- `.serena/` predated this setup and remains intact locally, but the entire
  directory is ignored and absent from the current tracked tree.

## Risks and blockers

- The continuous/raw Tōhoku model field and unshifted MOST series are unverified.
- Raw coastal-gauge continuity, datums, and reproducible first-arrival picks are
  unproved.
- A comparable primary 2011 warning-message archive was not verified.
- The intended equal-distance versus arrival-time discovery still needs
  calculation; the event must change if that result is weak.
- Per-asset reuse/redistribution terms need review even where Federal open-data
  policy is favorable.
- Conference registration deadlines and remote-presentation options remain
  unpublished; attendance feasibility is an owner decision.

## Continue from here

Execute the approved data-coverage and implementation chain in order:

1. Resolve exact authoritative endpoints, formats, station IDs/deployments,
   windows, units, terms, and expected schemas for the approved source bundle.
2. Record stable assets or explicit blockers in the source manifest and
   `context/ACQUISITION_REPORT.md`.
3. Select the four DART stations from documented near/far coverage before
   inspecting model residuals.
4. Independently review T-002A before downloading the approved source bundle or
   choosing format-driven dependencies.
5. Complete tested, source-independent acquisition and then normalization/data
   quality as T-002B and T-002C. Commit each accepted task or meaningful subtask.
6. Keep T-002D adaptive: run a fixed core profile, record each finding in an EDA
   decision ledger, and add follow-up checks only when observed evidence warrants
   them.

Do not begin the full wavefront or story build during the data proof.

## Repository state

The T-000 setup is on `main`. The planning package is a separate documentation
commit for project-owner review. No data download, implementation, deployment,
or publication was performed in this planning step.

## Final disposition

T-000, T-001, and T-002P are accepted. T-002A is active. T-002B and T-002C are
authorized but remain dependency-gated in that order; T-002D is not yet active.
