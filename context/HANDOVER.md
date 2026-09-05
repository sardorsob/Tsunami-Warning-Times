# Handover

## Objective and workflow

Prepare the new Pacific Tsunami Warning Time repository for a reproducible,
scientifically defensible PacificVis 2027 project without prematurely selecting
data or overbuilding the application.

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
- Configured Serena for Python and TypeScript. Its shared project configuration
  is intentionally tracked while `.serena/` remains ignored for future local
  state, caches, and overrides.
- Kept D3, regl/WebGL, scroll libraries, geospatial runtime dependencies,
  Playwright, a backend, and modeling tools out until demonstrated need.

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

These are the final fresh gate results for setup task T-000.

## Decisions and assumptions

- The browser product is static and retrospective, never an operational warning
  tool.
- The cross-community default wording is “time from earthquake origin to observed
  first arrival.”
- Tōhoku is only a provisional recommendation. `app/src/project.ts` intentionally
  keeps `selectedEvent` null.
- No repository code license was inferred. The owner must choose one.
- No raw scientific data was downloaded; no reportable scientific result exists.
- `.serena/` predated this setup. Its shared configuration now declares the
  project languages; `project.local.yml` remains local and ignored.

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

Start T-002 and own only its data-proof surface:

1. Read `AGENTS.md`, this file, `context/TASKS.md`,
   `docs/research/feasibility.md`, `context/DATA_CARD.md`,
   `context/spatial-contract.md`, and `context/FORECAST_PROTOCOL.md`.
2. Query NCEI TTT layer 17 as GeoJSON and record exact request, feature count,
   `HOURS`, EPSG:4326 metadata, antimeridian behavior, validity, and missing
   contours.
3. Check NCTR THREDDS/OPeNDAP for a usable raw Tōhoku field and document the
   actual variables, units, grid, time step, longitude convention, coefficients,
   and terms—or narrow the product to authoritative contours.
4. Prove small DART and coastal-gauge samples, freeze the arrival-pick protocol,
   and test the candidate community comparison before changing
   `selectedEvent`.
5. Record every source in the manifest and every transformation/check in the
   task evidence. Stop on ambiguous identity, time, units, CRS/order, datum,
   terms, or material uncertainty.

Do not begin the full wavefront or story build during the data proof.

## Repository state

The T-000 setup is packaged as one project commit on `main`. No push,
deployment, publication, or large download was performed.

## Final disposition

Accepted by the independent repository checker on 2026-09-04. T-000 is complete;
T-002 is the next permitted work surface.
