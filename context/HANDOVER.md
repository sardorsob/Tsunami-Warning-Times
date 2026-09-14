# Handover

## Objective and workflow

Prepare the new Pacific Tsunami Warning Time repository for a reproducible,
scientifically defensible PacificVis 2027 project without prematurely selecting
data or overbuilding the application.

The project owner approved the broad Tōhoku acquisition, data-quality, and EDA
design on 2026-09-05 and authorized implementation of T-002A through T-002C on
`main`. T-002A source-contract discovery and T-002B acquisition are accepted;
T-002C normalization/data quality is accepted, and T-002D EDA may now consume
only the accepted analysis-ready data.

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
  evidence. The EDA report stayed intentionally empty through T-002C2 and is now
  populated by the first T-002D slice.

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
- At that gate, the ledger permitted 12 exact assets only for T-002B acquisition
  and kept the continuous NCTR field, Saipan, and Valparaíso visibly blocked. No
  raw data was downloaded in that task, and T-002D was still pending.
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

## T-002C accepted evidence

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
The independent checker reconciled all 15 contracts, raw checksums and sidecars,
both builds, all accounting and table contracts, time/unit/datum semantics,
geometry, missingness, cadence, sentinel-line identity, and the required manual
traces. It approved T-002C after the inventory-hash correction in `d0ef35b` and
spatial-contract correction in `5689f18`.

Final acceptance verification on 2026-09-05 passed Ruff; Pyright with 0 errors,
warnings, or information messages; 77 Python tests; the 15-record provenance
validator; and the complete frontend typecheck, Vitest, and production build.
The final build-directory comparison returned no differences. Graphify rebuilt
the current code graph with 513 nodes, 893 edges, and 43 communities. Raw and
processed data were confirmed ignored and untracked, Serena remained ignored,
and `context/EDA_REPORT.md` remained exactly zero bytes.

## Accepted Saipan source recovery

On 2026-09-08, browser-controlled access reproduced NOAA's HTTP 403 for the
three exact Saipan event links. Internet Archive CDX records exposed preserved
HTTP-200 captures of those same NOAA URLs from 2016-12-22. Acquisition run
`2026-09-09__0142__saipan-recovery__92c438c` downloaded all three without
rewriting them and recorded 12 cached, 3 downloaded, and 2 blocked outcomes
across 17 contracts. The new raw files total 81,117 bytes and their SHA-256
sidecars match.

The header resolves the previously unknown Saipan contract: UHSLC provider,
NTWC archive, meters, UTC, MLLW, nominal one-minute sampling, unfiltered values,
and coordinates `15.2266, 145.742`. Because the source station identifier is
`none`, normalized station ID `saip` follows the archive code and does not assert
CO-OPS ID `1633227`. Reviewed candidate build
`2026-09-08-saipan-reviewed-92c438c` contains 139,383 observations and 108
rejections; `2026-09-08-saipan-reviewed-b-92c438c` is byte-identical. Saipan
contributes 764 event-day observations; all 16 rows belonging to eight
conflicting duplicate timestamps are explicitly quarantined, and the
12:08–23:07 UTC gap remains open.
Days `.071` and `.072` are checksum-gated coverage-only companions. Independent
review reconciled all three raw hashes and sidecars, the exact header contracts,
the 780 = 764 + 16 event-day accounting, and both deterministic builds, then
approved T-002C1 with no remaining blocking findings.

Final verification on 2026-09-08 passed Ruff; Pyright with 0 errors, warnings,
or information messages; 81 Python tests; the 17-record provenance validator;
the frontend typecheck, Vitest, and production build; and `git diff --check`.
Graphify was refreshed. Raw and processed data remain ignored and untracked,
Serena remains ignored, and `context/EDA_REPORT.md` remains exactly zero bytes.

## Completed Valparaíso recovery

T-002C2 is accepted after independent review under D-011. The
IOC API credential is stored only in
macOS Keychain service `org.ioc-sealevelmonitoring.api`, account
`tsunami-warning-times`; repository files and run evidence may record those
identifiers but never the credential. Official IOC documentation confirms
header-based `X-API-KEY` authentication and the research endpoint's sensor,
exclusive-end-date, QC-flag, and filter controls.

Authenticated run `2026-09-09__1838__valparaiso-recovery__9cc448c` downloaded
explicit radar and pressure responses; its rerun reused both checksum-gated
files without network access. The inventory now contains 18 assets: 17 approved
and 1 blocked. Radar contributes 4,272 accepted observations and pressure is a
4,270-row quality companion. Corrected candidate builds
`2026-09-09-valparaiso-reviewed-7576ffb-a` and `-b` have identical checksums,
143,655 observations, 107 rejections, 10 stations, and 4,380 contour parts.
The remaining blocker is the continuous NCTR field. Valparaíso's vertical datum
and horizontal datum remain unknown; all IOC QC flags are preserved.

The first review required three corrections: remove an unsupported source-
preference claim, validate and account for the pressure companion through the
same parser, and replace stale candidate-build references. The corrected
contract selects radar solely because it contains 4,272 timestamps versus
pressure's 4,270, before waveform or residual inspection. Re-review approved
the corrected evidence with no remaining blocking findings. The final gate
passed 88 Python tests, the 18-record provenance validator, Ruff, Pyright, the
frontend typecheck/test/build, Semgrep with no findings, and an independent
Codex Security diff scan with no reportable findings.

## T-002D missingness slice

The first adaptive EDA slice is complete on the accepted T-002C2 build. Clean
implementation commit `7b6d386` adds the reusable typed profiler, thin CLI,
source-supported six-gauge grid configuration, thin marimo notebook, and five
task-owned tests. Run `2026-09-09__1749__missingness__7b6d386` records a
six-file portable evidence bundle and finished local MLflow run
`3ea475f7045e48c9a1a87af913f807e0`; the input fingerprint is
`710dc48719a3f6362635b59cff2663887c43c5484ea9d15f6d3d12a4635d97d4`.

The profiler found 1,049 raw-value blanks among 143,655 observations (0.7302%),
but 2,276 unavailable exact-minute coastal positions among 23,040 (9.8785%).
The sample-density view is 2,156 of 23,040 (9.3576%) because it preserves and
counts 120 valid Saipan off-grid observations without snapping them. Pago Pago
and Saipan dominate continuity risk. All 21,933 coastal fitted/residual blanks
are structural not-applicability, not values to impute. The separate audit also
keeps 90 quarantined DART sentinel records, 1 blocked asset among 18, 10 unknown
horizontal datums, 5 unknown vertical references, and absent TTT labels 71–73
visible.

The notebook passed `marimo check` and a headless HTML execution; the latter is
an ignored smoke artifact. The local MLflow run finished and contains the same
run ID, Git SHA, input fingerprint, metrics, frozen-station tag, and four
generated report/data artifacts. `context/EDA_REPORT.md` is canonical and the
JSON/CSV outputs under `artifacts/eda/missingness/` are script-generated.
Pooled MCAR is not supported; MAR remains only a possible conditional
assumption, and MNAR cannot be excluded without publisher operational evidence.
T-002D remains in progress because gap visualization, DART long-interval review,
arrival-pick sensitivity, spatial/join coverage, NCTR structure, and the
distance-versus-arrival contrast are not complete.

The full repository gate passed with 93 Python tests, 18 validated provenance
records, zero Ruff or Pyright findings, and a successful frontend typecheck,
Vitest run, and production build. A separate source-table recount confirmed
143,655 rows, 1,049 raw blanks, 21,933 coastal rows with structural
fitted/residual blanks, zero retained DART modeled-field blanks, one retained
numeric zero, and rejection reasons 1 blocked / 16 duplicate / 90 sentinel.
Every one of the six normalized-input hashes and four generated-output hashes in
the portable bundle reconciles to the current files.

## Dual-track design checkpoint

The owner approved the dual-track direction on 2026-09-11: one repository, a
Conference Paper as the primary scientific deliverable, and a materially
distinct Visual Data Storytelling entry implemented in `app/`. The reviewed
architecture is recorded in
`docs/superpowers/specs/2026-09-11-dual-track-repository-design.md` and awaits
final owner review before the implementation plan and physical migration.

The design makes the existing top-level data pipeline and analytical files the
shared scientific foundation, adds explicit `paper` and `story` ownership for
new submission-specific work, and defines a semantic originality firewall. The
self-review deliberately keeps completed missingness artifacts, its canonical
Markdown report, and its portable run bundle at their recorded paths so their
checksums and provenance remain valid. It also requires thin Marimo views,
script-backed metrics, lane reports, release manifests, automated import/export
fences, and an AI-assistance disclosure ledger.

Observed for this documentation checkpoint on 2026-09-11: Ruff passed; Pyright
reported 0 errors and 0 warnings; Pytest reported 93 passed; the provenance
validator accepted 18 records; and the frontend typecheck, Vitest test, and
production build passed. `git diff --check` passed, the design contains no TBD,
TODO, FIXME, or XXX placeholders, and the official PacificVis 2027 Conference
Paper, VisNotes, submission-policy, and Visual Data Storytelling pages were
rechecked against the recorded deadlines and originality requirements.

## External track-compatibility guidance

On 2026-09-13, Dr. Angelos Chatzimparmpas replied on behalf of the PacificVis
2027 Visual Data Storytelling Contest co-chairs. The response conditionally
supports the proposed dual-track structure: using the same underlying dataset
is acceptable in principle when the submissions have clearly distinct goals and
contributions and their relationship is fully disclosed. Limited overlap may be
acceptable, but substantial duplication of text, figures, analyses, or other
manuscript content should be avoided.

The co-chairs asked for a later account of the type and approximate extent of
any overlap. No reply was sent during this task. The response remains pending
under X-001 until both contribution statements, the paper methods/analysis
outline, the story thesis/storyboard, preliminary figure inventories, and an
overlap matrix exist. `context/ORIGINALITY.md` holds the detailed paraphrase,
current boundary, and follow-up trigger; D-013 records the decision. The
original email remains in the owner's mailbox rather than the repository. No
Paper/VisNotes co-chair reply was present in the reviewed mail results as of
2026-09-13.

Fresh verification for this correspondence-log checkpoint: Ruff passed;
Pyright reported 0 errors and 0 warnings; Pytest reported 93 passed; the
provenance validator accepted 18 source records; and the frontend typecheck,
Vitest run, and production build passed. A diff scan found no copied email
address, Gmail URL, thread/message identifier, or full private message body in
the new repository record.

## README documentation checkpoint

On 2026-09-13, `README.md` was expanded around the three requested onboarding
surfaces: the source-contract-first dataset gathering process, the current and
planned repository structure, and the originality-preserving split between the
Conference Paper and Visual Data Story. Its organization takes structural
inspiration from the sibling GeoCrop project README without importing that
project's claims or implementation details.

Fresh README verification reconciled 17 approved and 1 blocked source contract,
1 event, 10 stations (6 coastal and 4 DART), 143,655 observations, 4,380 TTT
contour parts, 62,988 vertices, and 107 rejected records against the tracked
manifest and accepted normalized build. All linked repository files exist,
Markdown fences are balanced, and `git diff --check` passed. The full gate also
passed: Ruff; Pyright with 0 errors and 0 warnings; 93 Pytest tests; 18 validated
provenance records; and the frontend typecheck, Vitest run, and production
build.

## Visual-story adaptive EDA planning checkpoint

On 2026-09-14, the project owner approved a story-only visual discovery design:
a fixed diagnostic atlas followed by evidence-triggered branches. The current
distance-versus-arrival concept is now explicitly falsifiable; weak or unstable
evidence triggers a recorded pivot or rejection rather than outcome-driven
station selection.

The written design is
`docs/superpowers/specs/2026-09-14-visual-story-adaptive-eda-design.md`. New
lane context under `context/story/` separates the story question, task ledger,
EDA decision report, and storyboard promotion state from shared and paper work.
The project owner accepted the written specification on 2026-09-14, closing
T-003P. The executable Stage A plan is
`docs/superpowers/plans/2026-09-14-visual-story-stage-a-atlas.md`; T-003I is in
review in that planning checkpoint. The owner subsequently authorized inline,
task-by-task execution on `main`. Task 1 added only the exact GeoPandas 1.1.4 and
Matplotlib 3.11.2 dependency boundary plus package markers. Task 2 added the
separate Natural Earth source contract and manifest; acquired and inspected the
85,352-byte, version 4.1.0, EPSG:4326 coastline; and confirmed its SHA-256 through
an offline cache rerun. Task 3 exposes the shared exact-grid coverage sequence
and separate off-grid samples without snapping; all 6 missingness tests passed
and the existing report writer and generated artifacts remained unchanged. Task
4 adds immutable, source-preserving atlas records, strict reviewed-scope checks,
interpolated 20°E/-340° seam handling, and WGS84 geodesic range rings. Its RED
test failed on the absent atlas module; GREEN passed 6 focused tests, Ruff, and
strict Pyright. A direct accepted-build load reconciled 1 reviewed event, 10
stations, 143,655 observations, 4,380 contour parts, and 6 coastal windows. Task
5 adds a deterministic Pacific evidence-map renderer with explicit Equal Earth,
preliminary-evidence, candidate-station, and published-contour semantics. Its RED
test failed on the absent plot module; GREEN passed all 7 atlas tests, Ruff, and
strict Pyright. A temporary actual-data smoke render wrote valid PNG/SVG outputs
and transformed all 4,514 input line parts into 4,543 seam-safe projected parts.
Task 6 adds deterministic source-window coverage strips whose distinct states
are exact observed value, retained source blank, absent timestamp, and unsnapped
off-grid observation. Its RED test failed on the absent renderer; GREEN passed
14 shared missingness and atlas tests, Ruff, and strict Pyright. A temporary
actual-data render represented 23,040 exact-grid positions and 120 off-grid
observations across all six gauges; lowest-coverage labels are derived from the
supplied metrics. Task 7 adds station-local point panels: coastal raw values and
DART residuals remain distinct, each panel has a local y-scale, and no centering,
smoothing, interpolation, resampling, or gap-bridging line is applied. Its RED
test failed on the absent panel interface; GREEN passed both focused tests, Ruff,
and strict Pyright. A temporary actual-data render contained 10 panels and
24,729 numeric points in the reviewed -6 h to +30 h window: 11,156 coastal and
13,573 DART. Task 8 adds a side-by-side shape diagnostic with identical map
context: six WGS84 geodesic range rings on the left and nine configured published
NCEI contour hours on the right. It accepts no speed or arrival input and assigns
no nearest contour to a station. Its RED test failed on the absent function;
GREEN passed the semantic and byte-determinism test, Ruff, and strict Pyright. A
temporary actual-data render transformed 885 input parts into 916 seam-safe
parts. No canonical story figure, claim, or app export exists yet.

The approved execution boundary has two stages. T-003A may create preliminary
maps and temporal diagnostics from the accepted T-002C2 build, but cannot
promote stations or claims. T-003B remains gated by the frozen arrival method
and a T-002E-promoted shared release. The unavailable NCTR continuous field is
not replaced or inferred; preliminary spatial work uses the published NCEI
contours with their source semantics and limitations.

Fresh planning-package verification passed: Ruff; Pyright with 0 errors and 0
warnings; 93 Pytest tests; 18 validated provenance records; frontend typecheck,
Vitest, and production build; and `git diff --check`. Graphify rebuilt the
repository graph to 760 nodes, 1,279 edges, and 60 communities so the new design
and story context are discoverable. No large data or external service was used.

After written-design acceptance, the implementation-planning checkpoint passed
the same full gate: Ruff; Pyright with 0 errors and 0 warnings; 93 Pytest tests;
18 validated provenance records; frontend typecheck, Vitest, and production
build; placeholder/type-consistency review; and `git diff --check`. Graphify
then refreshed to 781 nodes, 1,299 edges, and 62 communities; a scoped query
returned the Stage A plan, evidence states, fixed/adaptive contracts, and T-003B
gate. The plan contains 11 test-first tasks with separate commits and keeps the
preview, reviewed decision input, canonical clean-tree run, and independent
rebuild distinct.

## Risks and blockers

- The continuous/raw Tōhoku model field and unshifted MOST series are unverified.
- Saipan and Pago Pago have material continuity gaps; reproducible first-arrival
  picks remain unproved for every coastal gauge.
- A comparable primary 2011 warning-message archive was not verified.
- The intended equal-distance versus arrival-time discovery still needs
  calculation; a weak result requires a documented story pivot or event
  reconsideration.
- Per-asset reuse/redistribution terms need review even where Federal open-data
  policy is favorable.
- Conference registration deadlines and remote-presentation options remain
  unpublished; attendance feasibility is an owner decision.
- The storytelling co-chairs still require a concrete overlap description, and
  Paper/VisNotes co-chair guidance remains pending.

## Continue from here

Execute the remaining approved implementation chain in order:

1. Continue the approved inline Stage A plan at Task 9, committing each task
   after its focused verification passes.
2. Continue shared T-002D from the recorded missingness findings: map Pago Pago
   and Saipan gap blocks and inspect DART intervals over 900 seconds.
3. Define the no-interpolation pre-arrival completeness gate, then execute
   arrival-pick sensitivity without model-guided station selection.
4. T-003A may build only the preliminary story diagnostic atlas from the
   accepted T-002C2 candidate build; label every output preliminary.
5. Keep arrival-based T-003B work blocked until T-002E publishes an accepted
   release, then record a promote, revise, pivot, or reject disposition.
6. Keep X-001 pending until both submission concepts are concrete enough to
   quantify overlap; obtain owner authorization before sending the reply.

Do not begin the full wavefront or story app build during the data proof.

## Repository state

The T-000 setup, T-002A source contracts, and T-002B acquisition evidence are on
`main`. Raw and processed data remain ignored and untracked; no deployment or
publication occurred. T-002C, T-002C1, and T-002C2 are accepted; T-002D remains
in progress with its missingness slice complete. Serena and local MLflow state
remain ignored.

## Final disposition

T-000, T-001, T-002P, T-002A, T-002B, T-002C, T-002C1, and T-002C2 are
accepted. T-002D is active but not complete; no event or station set is frozen.
T-003P and T-003I are accepted. T-003A and the root T-003 work are in progress;
Tasks 1–8 are complete and Task 9 is next.
