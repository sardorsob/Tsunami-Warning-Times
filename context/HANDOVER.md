# Handover

## Objective and workflow

Prepare the new Pacific Tsunami Warning Time repository for a reproducible,
scientifically defensible PacificVis 2027 project without prematurely selecting
data or overbuilding the application.

The project owner approved the broad Tōhoku acquisition, data-quality, and EDA
design on 2026-09-05 and authorized implementation of T-002A through T-002C on
`main`. T-002A source-contract discovery and T-002B acquisition are accepted;
T-002C normalization/data quality has a deterministic candidate in independent
review, and EDA remains gated on accepted analysis-ready data.

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
- Populated the acquisition and data-quality reports from their task-owned
  evidence. The EDA report remains intentionally empty until T-002D.

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

## T-002A verification evidence

Observed on 2026-09-05 for the source-contract ledger:

- The required RED test failed with `unsupported status 'blocked'`; after the
  minimal validator change, its GREEN rerun passed.
- The final provenance suite passed 9 tests; the source-manifest validator
  accepted 15 exact assets; Ruff passed; Pyright reported 0 errors; the source
  contract TOML parsed with Python 3.12; and `git diff --check` passed.
- The ledger permits 12 exact assets only for T-002B acquisition and keeps the
  continuous NCTR field, Saipan, and Valparaíso visibly blocked. No raw data was
  downloaded and T-002D remains pending.
- `graphify update .` rebuilt the tracked graph after the provenance and contract
  changes: 304 nodes, 307 edges, and 38 communities.
- Review round 1 added the NCEI-to-NDBC UTC evidence chain for DART calendar
  fields, corrected the NCTR coefficient HTML contract, and aligned downstream
  planning to `approved` contracts and USGS FDSN CSV. The Task 1 gate reran with
  15 manifest records, 9 passing provenance tests, clean Ruff, and 0 Pyright
  errors.
- Later review rounds aligned the downloader dataclass exactly to the TOML,
  added explicit reasons and byte-prefix validation, and restored the narrative
  content-signature field. A fresh final reviewer approved the complete range
  with no material findings.

## Decisions and assumptions

- The browser product is static and retrospective, never an operational warning
  tool.
- The cross-community default wording is “time from earthquake origin to observed
  first arrival.”
- Tōhoku is only a provisional recommendation. `app/src/project.ts` intentionally
  keeps `selectedEvent` null.
- No repository code license was inferred. The owner must choose one.
- The accepted T-002B raw bundle exists locally as ignored, immutable,
  checksummed files. No EDA result or production claim exists.
- `.serena/` predated this setup and remains intact locally, but the entire
  directory is ignored and absent from the current tracked tree.

## T-002B accepted clean evidence

Clean committed evidence bundles `2026-09-05__1906__accepted__e602131` and
`2026-09-05__1906__accepted-rerun__e602131` each report 12 `cached` outcomes,
3 `blocked` outcomes, and 12,386,361 total bytes. Both record Git SHA `e602131`,
`working_tree: clean`, and `evidence_disposition: ready-for-review`; all output
checksums and byte counts match. Source inspection confirmed
the USGS event identity, the first three TTT contours, all four DART files, and
all four available CO-OPS metadata blocks. The manifest now records the raw
paths and SHA-256 values.

The implementation review and independent data-quality review are approved. The
reviewer reconciled both bundles, the manifest, all 12 raw assets, and all 12
checksum sidecars; confirmed that raw data remains ignored and untracked; and
found no proxy substitution. T-002B is done and T-002C may proceed.

## T-002C candidate evidence

At Git SHA `5f920f2`, two offline checksum-gated builds with tags
`2026-09-05-1958-quality-a-5f920f2` and
`2026-09-05-1958-quality-b-5f920f2` produced byte-identical outputs: 1 event,
4,380 TTT contour parts, 10 station rows, 138,619 accepted observations, and 93
rejections. The tracked portable bundle is
`2026-09-05__1958__quality__5f920f2`; the processed tables remain ignored.

Core correctness review is approved after fixes for source-metadata identity,
grain accounting, empty-source handling, output containment, units, and strict
geometry types. A later adaptive profile found 90 exact `9999` values in DART
measurement fields. Because publisher semantics were not verified, the pipeline
now quarantines those rows as `unexpected_sentinel` instead of guessing a null
meaning; tests and the final double build confirm no retained sentinel rows.
T-002C awaits its final independent scientific-data disposition.

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

Execute the remaining approved implementation chain in order:

1. Complete the independent T-002C review of identity, accounting, units/time,
   datum handling, deterministic outputs, manual traces, and rejections.
2. Resolve any material finding and rerun the full repository gate before
   accepting T-002C.
3. Keep T-002D adaptive: run a fixed core profile, record each finding in an EDA
   decision ledger, and add follow-up checks only when observed evidence warrants
   them.

Do not begin the full wavefront or story build during the data proof.

## Repository state

The T-000 setup, T-002A source contracts, and T-002B acquisition evidence are on
`main`. Raw and processed data remain ignored and untracked; no deployment or
publication occurred. T-002C is in review, and T-002D remains pending.

## Final disposition

T-000, T-001, T-002P, T-002A, and T-002B are accepted. T-002C is in review, and
T-002D is not yet active.
