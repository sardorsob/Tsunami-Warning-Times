# Visual-Story Adaptive EDA Design

Date: 2026-09-14

Status: approved in conversation; written-spec review pending

Lane: story only

## Outcome

Create a small, reproducible diagnostic atlas that uses spatial and temporal
views to decide what the PacificVis Visual Data Story can honestly say. The EDA
tests the current distance-versus-arrival idea as a falsifiable candidate. It may
pivot the storyboard when another finding is stronger or when evidence quality
cannot support the candidate comparison.

This work is exploratory evidence for story design. It is not a paper analysis,
a production story scene, an operational warning product, or a continuous
wavefront reconstruction.

## Approved choices

- Use a fixed visual audit core followed by evidence-triggered branches.
- Generate analyst-facing maps and plots before designing polished story scenes.
- Keep calculations and rendering functions in tested Python modules; use a thin
  Marimo notebook to inspect generated results.
- Save compact figures, tables, metadata, and run evidence under the story lane
  in `artifacts/` and interpret them in Markdown.
- Allow a documented pivot when the distance-versus-arrival contrast is weak,
  unstable, or unsupported.
- Preserve the paper/story originality firewall: no fitted paper model, paper
  feature selection, paper figure, or paper-specific method enters this EDA.
- Defer app exports, animation, WebGL, and polished scene production until a
  static story comparison is accepted.

## Approaches considered

### Fixed diagnostic atlas with adaptive branches — selected

A small common plot set answers integrity and story-value questions. Each
finding has an explicit follow-up rule and disposition. This balances discovery
with reproducibility and makes negative results useful.

### Hypothesis-first storyboard

Plots would be organized around proving that distance alone misleads. This is
faster but makes outcome-driven station selection and narrative lock-in more
likely, so it was rejected.

### Open-ended notebook exploration

An analyst would generate many interactive views and curate the interesting
ones afterward. This is flexible but creates hidden analytical paths and weak
artifact lineage, so it was rejected.

## Evidence boundary

The accepted T-002C2 build is sufficient for preliminary maps of the event,
published NCEI travel-time contours, four DART stations, six coastal gauges,
coverage gaps, and source-preserving time series. These outputs must be labeled
`preliminary_storyboard_evidence`.

The following boundaries remain active:

- the exact continuous NCTR field is unavailable, so the published contours may
  be drawn but may not be presented as a reconstructed continuous wavefront;
- observed-arrival comparisons wait for the shared arrival-pick definition,
  no-interpolation completeness gate, and sensitivity review;
- station or community promotion waits for T-002E and a versioned shared release;
- unknown horizontal or vertical datums remain explicit and block affected
  distance or absolute-level interpretations;
- amplitudes are not compared across stations or datums; and
- physical travel time remains distinct from bulletin, alert, receipt,
  evacuation, and actionable warning time.

## Architecture and ownership

New story-specific work uses these paths:

```text
analysis/story/                     tested metrics, spatial operations, plots
scripts/story/                      thin reproducible entry points
notebooks/story/                    thin Marimo views of generated artifacts
tests/story/                        story EDA and export-boundary checks
artifacts/eda/story/                compact diagnostic figures and tables
artifacts/logs/runs/<run_id>/       portable run evidence with lane = story
context/story/PROJECT.md            story-lane question and boundaries
context/story/TASKS.md              detailed story task ledger
context/story/EDA_REPORT.md         canonical observations and decisions
context/story/STORYBOARD.md         reviewed scene candidates only
```

The shared root pipeline remains the owner of source parsing, normalization,
scientific data quality, arrival definitions, and reviewed releases. Story code
consumes those interfaces and does not duplicate them. The app consumes only
separately reviewed exports under `app/public/data/`, never exploratory files
directly from `artifacts/eda/story/`.

## Two-stage execution

### Stage A — preliminary diagnostic atlas

Stage A may use the accepted T-002C2 build before T-002E because it makes no
station-promotion or final narrative claim. It produces only the first three
required views and, if the spatial contract passes, the fourth:

1. **Pacific evidence map** — event, NCEI travel-time contours, four DART
   stations, and six coastal gauges.
2. **Observation-coverage timelines** — gaps, retained blanks, off-grid samples,
   and source-supported cadence changes.
3. **Station time-series small multiples** — values aligned to earthquake origin
   while preserving source time and separating incompatible datum groups.
4. **Distance-versus-contour diagnostic** — a transparent geodesic-distance
   reference compared with published contour timing, without observed arrivals.

Stage A determines whether the geography is legible, whether the observational
chain is narratively usable, and whether the candidate contrast merits the
reviewed second stage.

### Stage B — reviewed arrival comparison

Stage B starts only after T-002E promotes a versioned shared release. It adds:

5. **Modeled-versus-observed arrival comparison** — intervals or dumbbells with
   the residual sign, timing precision, pick method, and sensitivity visible.
6. **Community contrast sheet** — a human-reviewed shortlist of four to six
   communities using transparent evidence-quality and contrast fields.

Stage B either promotes a static comparison to T-003, revises the atlas, pivots
the story question, or rejects Tōhoku for this story.

## Fixed visual contracts

### Pacific map

- Use a Pacific-centered equal-area or compromise projection suitable for the
  message; do not use Web Mercator for basin-scale comparison.
- Normalize or split geometry at the antimeridian deliberately and record the
  operation and input/output feature counts.
- Preserve source coordinates and perform geodesic rather than planar distance
  calculations in geographic coordinates.
- Use one map for one message. Regional small multiples replace clutter before
  new interaction is considered.
- Label projection, elapsed-time units, source contour semantics, and the
  continuous-field limitation on the figure or adjacent metadata.

### Time-series and coverage views

- Keep source timestamps and verified UTC-derived timestamps distinct.
- Show absent timestamps, retained blank values, quarantined records, off-grid
  values, and designed cadence changes with separate encodings.
- Do not interpolate in the preliminary baseline.
- Use identical extents and scales only where the quantities are comparable;
  otherwise label panels independently.

### Color and accessibility

- Give missing or unavailable data a neutral role distinct from numeric zero.
- Use redundant shape, line style, or annotation where color carries meaning.
- Required checks are thumbnail/squint, grayscale, common color-vision
  deficiencies, legend and units, and a trace of three displayed values.
- Export both PNG for quick review and SVG for inspection when the rendering
  stack produces stable SVG output.

## Adaptive decision ledger

Every required or branched view records one row with:

```text
observation -> question -> follow-up -> result -> disposition -> storyboard implication
```

Allowed dispositions are `retain`, `revise`, `branch`, `promote`, and `reject`.
The report also records input release or candidate-build ID, script command,
artifact paths and hashes, assumptions, limitations, and reviewer state.

Branching rules:

| Trigger | Required response |
| --- | --- |
| Map is illegible at basin scale | Use focused regional small multiples; do not add interaction yet |
| Antimeridian, CRS, or join result is ambiguous | Stop the spatial branch and fix the shared contract |
| Coverage or pick sensitivity is poor | Exclude promotion or make observability the explicit subject |
| Distance contrast is weak | Record the negative result and test a coverage or multi-clock pivot |
| Distance contrast is strong and stable | Promote one static comparison for cartographic review |
| A shared scientific defect appears | Return it to the shared lane and issue a new reviewed release |
| A fitted paper result appears useful | Keep it in the paper lane; do not transfer it into the story |

The fixed core may grow only when the same follow-up recurs across reviewed runs.
Exploration may not change frozen arrival settings or station inclusion after
modeled residuals are inspected.

## Artifact contract

Each run writes a portable bundle and a compact atlas manifest. Every reportable
figure records:

- artifact ID, title, question, and lane;
- generating command and Git SHA;
- input release or candidate-build ID and source checksums;
- projection/CRS, longitude handling, units, and time basis where applicable;
- row, station, feature, and rejection counts;
- output path, media type, dimensions, and SHA-256;
- preliminary or reviewed status;
- finding, limitation, disposition, and storyboard implication; and
- manual QA evidence.

Candidate filenames are numbered by analytical order, not narrative scene:

```text
01_pacific_evidence_map.{png,svg}
02_observation_coverage.{png,svg}
03_station_timeseries.{png,svg}
04_distance_contour_diagnostic.{png,svg}
05_modeled_observed_arrival.{png,svg}
06_community_contrast_sheet.{png,svg}
atlas-manifest.json
decision-ledger.csv
```

Generated files are rebuilt by scripts and never hand-edited. Exploratory
artifacts are not app assets. A separate promotion task may copy only reviewed,
compact exports through a checksummed story-export manifest.

## Marimo contract

`notebooks/story/tohoku_storyboard_eda.py` is a thin reactive atlas viewer. It
may select a run, filter already-generated tables, display figures, and expose
the decision ledger. Unique transformations, metrics, spatial joins, arrival
picks, and figure generation remain in modules or scripts. The notebook must
pass `marimo check` and headless execution.

## Dependency contract

No visualization dependency is added during planning. Stage A may add only the
smallest demonstrated static stack: GeoPandas for spatial table/projection work
and Matplotlib for figures. GeoPandas' installed transitive spatial libraries are
reused; Plotly, Folium, Contextily, Seaborn, D3, WebGL, and a basemap service are
deferred until a reviewed visual requirement cannot be met by the static stack.

Any coastline or boundary layer is a governed source asset with publisher,
license/terms, retrieval date, checksum, CRS, and version. It is not silently
downloaded by a plotting library.

## Verification

Stage A and B each require:

- task-owned tests for calculations, antimeridian behavior, input/output
  accounting, and deterministic artifact metadata;
- deterministic rebuild and checksum comparison;
- `marimo check` and headless notebook execution;
- report-to-manifest and run-bundle reconciliation;
- manual inspection of every figure, including three source-value traces;
- the repository Python, provenance, and frontend gates; and
- `graphify update .` after code changes.

The Checker confirms that the visual conclusion follows from the displayed
evidence, negative findings remain visible, and no paper-only artifact or method
crosses the story boundary.

## Task and commit boundaries

1. Commit this approved design and context package alone.
2. Write and approve an implementation plan before adding dependencies or code.
3. Commit the Stage A test/fixture and minimal static dependency decision.
4. Commit each coherent Stage A visual slice with its tests, artifacts, report,
   and run evidence.
5. Commit Stage B only after T-002E publishes the reviewed release interface.
6. Commit storyboard promotion separately from exploratory evidence.

No push, deployment, dataset download, or external message is part of this
design task.
