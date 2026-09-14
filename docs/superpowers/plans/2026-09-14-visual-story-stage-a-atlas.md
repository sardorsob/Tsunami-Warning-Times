# Visual-Story Stage A Diagnostic Atlas Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build four reproducible, preliminary visual-story diagnostics from the accepted Tōhoku candidate tables without making arrival-pick, station-promotion, or public story claims.

**Architecture:** Story-specific code loads explicit normalized inputs into typed immutable records, reuses shared missingness definitions for coverage, and renders deterministic static figures through GeoPandas and Matplotlib. A thin CLI owns run evidence and Markdown generation; a thin Marimo notebook reads the generated atlas manifest. The accepted shared pipeline remains the source of scientific records and the app receives no exploratory output.

**Tech Stack:** Python 3.12, GeoPandas 1.1.4, Matplotlib 3.11.2, PyProj/Shapely/Pandas through GeoPandas, Marimo 0.24.0, MLflow Skinny 3.16.0, Pytest 9.1.1, Ruff, and Pyright strict mode.

**Spec:** `docs/superpowers/specs/2026-09-14-visual-story-adaptive-eda-design.md`

## Global Constraints

- This plan implements Stage A only and labels every output `preliminary_storyboard_evidence`.
- Use only an explicitly supplied accepted T-002C2 processed directory; never discover the newest directory.
- Keep the exact NCTR continuous field blocked and do not interpolate a field from NCEI contours.
- Keep modeled arrival, observed first deviation, maximum wave, bulletin, public alert, and evacuation times separate.
- Do not calculate observed arrivals, model residuals, station promotion, or community selection in this plan.
- Do not import from `analysis/paper`, read `artifacts/eda/paper`, or export to `app/public/data`.
- Preserve source timestamps, zeros, blank values, off-grid observations, quarantine, units, CRS, coordinate order, and datum labels.
- Plot DART published residual values and coastal raw values in separately labeled panels; do not compare amplitudes across panels.
- Use the Pacific-centered Equal Earth CRS `+proj=eqearth +lon_0=-160 +datum=WGS84 +units=m +no_defs +type=crs`.
- Split linework at the display seam before projection and record input/output part counts.
- Use Natural Earth 1:110m coastline version 4.1.0 only as governed context; keep its raw ZIP ignored and checksummed.
- Add only `geopandas==1.1.4` and `matplotlib==3.11.2` as direct visualization dependencies.
- Produce PNG and SVG with deterministic metadata; generated files are script-owned and never hand-edited.
- Record a portable run bundle, project-local MLflow run with `lane=story`, atlas manifest, decision ledger, and canonical Markdown report.
- Keep every file below `context/`, including an empty file if a later step intentionally leaves one empty.
- Commit each task separately on `main`; do not push, deploy, send messages, or download any source outside the approved contract.

## File Structure

### Create

- `analysis/__init__.py` — marks the analysis namespace.
- `analysis/story/__init__.py` — exports the Stage A public interfaces.
- `analysis/story/atlas.py` — typed input loading, validation, Pacific seam handling, coverage-facing records, and geodesic range rings.
- `analysis/story/plots.py` — deterministic rendering for the four diagnostic figures.
- `analysis/story/artifacts.py` — atlas manifest, decision ledger, Markdown, run bundle, and MLflow recording.
- `scripts/story/build_story_atlas.py` — thin Stage A command-line entry point.
- `notebooks/story/tohoku_storyboard_eda.py` — thin reactive viewer over the generated manifest and figures.
- `config/story-map-context.toml` — exact Natural Earth coastline acquisition contract.
- `config/story-atlas.toml` — reviewed projection, time window, contours, and range-ring settings.
- `config/story-atlas-decisions.toml` — observed manual-review findings used to regenerate the canonical report.
- `artifacts/provenance/story-source-manifest.csv` — story-only source ledger for map context.
- `context/story/SOURCES.md` — map-context identity, terms, checksum, and limitations.
- `tests/story/test_dependencies.py` — direct dependency and namespace smoke checks.
- `tests/story/test_map_context.py` — map-context contract and story-manifest checks.
- `tests/story/test_atlas.py` — loader, coverage, seam, geodesic, and plot behavior.
- `tests/story/test_story_atlas_cli.py` — artifact, report, run-bundle, and lane-fence integration checks.

### Modify

- `pyproject.toml:9-36` — pin direct dependencies and include `analysis` in strict type checking.
- `uv.lock` — lock the geospatial stack.
- `scripts/acquire_tohoku.py:253-388` — add a validated run-lane field while preserving `shared` as the default.
- `tests/test_acquisition.py:71-130` — prove lane recording and invalid-lane rejection.
- `pipeline/missingness.py:35-230` — expose exact-grid coverage positions and off-grid samples without changing existing profile semantics.
- `tests/test_missingness.py:258-330` — reconcile timeline status counts with the accepted missingness definitions.
- `.github/workflows/ci.yml:28-34` — validate the story source manifest.
- `artifacts/README.md:1-16` — document the story atlas and its evidence states.
- `context/STRUCTURE.md` — change implemented Stage A paths from planned to active.
- `context/story/PROJECT.md` — record the implementation state.
- `context/story/TASKS.md` — move T-003A through Maker and Checker states using observed evidence.
- `context/story/EDA_REPORT.md` — script-generated results, interpretations, limitations, takeaways, and next branches.
- `context/story/STORYBOARD.md` — retain “no promotion” unless the later T-003B review authorizes one.
- `context/HANDOVER.md` — exact commands, checks, artifacts, blockers, and continuation.
- `graphify-out/graph.json`, `graphify-out/graph.html`, and `graphify-out/GRAPH_REPORT.md` — refreshed project graph.

### Generated by the implementation

- `artifacts/eda/story/$STORY_RUN_ID/01_pacific_evidence_map.png`
- `artifacts/eda/story/$STORY_RUN_ID/01_pacific_evidence_map.svg`
- `artifacts/eda/story/$STORY_RUN_ID/02_observation_coverage.png`
- `artifacts/eda/story/$STORY_RUN_ID/02_observation_coverage.svg`
- `artifacts/eda/story/$STORY_RUN_ID/03_station_timeseries.png`
- `artifacts/eda/story/$STORY_RUN_ID/03_station_timeseries.svg`
- `artifacts/eda/story/$STORY_RUN_ID/04_distance_contour_diagnostic.png`
- `artifacts/eda/story/$STORY_RUN_ID/04_distance_contour_diagnostic.svg`
- `artifacts/eda/story/$STORY_RUN_ID/atlas-manifest.json`
- `artifacts/eda/story/$STORY_RUN_ID/decision-ledger.csv`
- `artifacts/logs/runs/$STORY_RUN_ID/{meta,config,inputs,outputs,metrics}.json`
- `artifacts/logs/runs/$STORY_RUN_ID/notes.md`

---

### Task 1: Add the minimal static geospatial stack

**Files:**

- Create: `analysis/__init__.py`
- Create: `analysis/story/__init__.py`
- Create: `tests/story/test_dependencies.py`
- Modify: `pyproject.toml:9-36`
- Modify: `uv.lock`

**Interfaces:**

- Consumes: Python `>=3.12,<3.14` and the existing `dev` dependency group.
- Produces: importable `analysis.story`; exact GeoPandas 1.1.4 and Matplotlib 3.11.2 dependencies; strict type checking over `analysis`.

- [x] **Step 1: Write the failing dependency test**

```python
from importlib.metadata import version


def test_static_story_geospatial_dependencies_are_exact() -> None:
    assert version("geopandas") == "1.1.4"
    assert version("matplotlib") == "3.11.2"


def test_story_analysis_namespace_imports() -> None:
    import analysis.story

    assert analysis.story.__doc__ == "Story-only descriptive analysis."
```

- [x] **Step 2: Run the test and observe the missing dependency/package failure**

Run: `uv run pytest tests/story/test_dependencies.py -q`

Expected: FAIL because the story analysis package and geospatial dependencies do not exist.

- [x] **Step 3: Add the package markers and exact dependencies**

`analysis/__init__.py`:

```python
"""Submission-specific analysis packages."""
```

`analysis/story/__init__.py`:

```python
"""Story-only descriptive analysis."""
```

Run:

```bash
uv add --group dev geopandas==1.1.4 matplotlib==3.11.2
```

Change the Pyright include list to:

```toml
include = ["analysis", "pipeline", "scripts", "tests"]
```

- [x] **Step 4: Verify the environment and lockfile**

Run:

```bash
uv lock --check
uv run pytest tests/story/test_dependencies.py -q
uv run pyright
```

Expected: lock check succeeds, 2 tests pass, and Pyright reports zero errors.

- [x] **Step 5: Commit the dependency boundary**

```bash
git add analysis/__init__.py analysis/story/__init__.py tests/story/test_dependencies.py pyproject.toml uv.lock
git commit -m "build(story): add static geospatial stack"
```

### Task 2: Add governed Pacific coastline context

**Files:**

- Create: `config/story-map-context.toml`
- Create: `artifacts/provenance/story-source-manifest.csv`
- Create: `context/story/SOURCES.md`
- Create: `tests/story/test_map_context.py`
- Modify: `scripts/acquire_tohoku.py:253-388`
- Modify: `tests/test_acquisition.py:71-130`
- Modify: `.github/workflows/ci.yml:28-34`

**Interfaces:**

- Consumes: `pipeline.acquisition.load_contracts`, `pipeline.acquisition.acquire_all`, `scripts.acquire_tohoku.write_run_evidence`, and `pipeline.provenance.validate_manifest`.
- Produces: source ID `natural-earth-coastline-110m-v4.1.0`; ignored raw ZIP `data/raw/natural-earth/ne_110m_coastline_v4.1.0.zip`; acquisition evidence with `lane="story"`; a one-record story source manifest.

- [x] **Step 1: Write failing contract and lane tests**

Add to `tests/story/test_map_context.py`:

```python
from pathlib import Path

from pipeline.acquisition import load_contracts
from pipeline.provenance import validate_manifest


def test_story_map_context_is_one_exact_public_domain_asset() -> None:
    contracts = load_contracts(Path("config/story-map-context.toml"))

    assert len(contracts) == 1
    contract = contracts[0]
    assert contract.source_id == "natural-earth-coastline-110m-v4.1.0"
    assert contract.url == (
        "https://naturalearth.s3.amazonaws.com/110m_physical/"
        "ne_110m_coastline.zip"
    )
    assert contract.local_path.as_posix() == (
        "data/raw/natural-earth/ne_110m_coastline_v4.1.0.zip"
    )
    assert contract.expected_prefix == "PK"


def test_story_source_manifest_is_valid() -> None:
    result = validate_manifest(Path("artifacts/provenance/story-source-manifest.csv"))
    assert result.records == 1
```

Extend `tests/test_acquisition.py` so the existing fixture call passes
`lane="story"`, expects `"lane": "story"` in `meta.json`, and adds:

```python
def test_write_run_evidence_rejects_an_unknown_lane(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unsupported run lane"):
        write_run_evidence(
            root=tmp_path,
            run_tag="bad-lane",
            config_path=tmp_path / "missing.toml",
            contracts=(),
            results=(),
            command="fixture",
            mode="offline",
            lane="unknown",
        )
```

- [x] **Step 2: Run the tests and confirm the missing files/interface**

Run:

```bash
uv run pytest tests/story/test_map_context.py tests/test_acquisition.py::test_write_run_evidence_writes_an_immutable_portable_bundle tests/test_acquisition.py::test_write_run_evidence_rejects_an_unknown_lane -q
```

Expected: FAIL because the story contract/manifest and `lane` parameter do not exist.

- [x] **Step 3: Add the validated run lane**

Add `Literal` to the imports in `scripts/acquire_tohoku.py`, then change the writer signature and metadata:

```python
def write_run_evidence(
    *,
    root: Path,
    run_tag: str,
    config_path: Path,
    contracts: Sequence[SourceContract],
    results: Sequence[AcquisitionResult],
    command: str,
    mode: str,
    lane: Literal["shared", "paper", "story"] = "shared",
    now_utc: Callable[[], datetime] = utc_now,
    git_sha: Callable[[], str] | None = None,
    working_tree: Callable[[], str] | None = None,
) -> Path:
    if lane not in {"shared", "paper", "story"}:
        raise ValueError(f"unsupported run lane {lane!r}")
```

Add `"lane": lane` to `meta.json`. Add the CLI argument and pass it to the writer:

```python
parser.add_argument("--lane", choices=("shared", "paper", "story"), default="shared")
```

- [x] **Step 4: Create the exact source contract**

Create `config/story-map-context.toml`:

```toml
contract_version = "2026-09-14"

[assets.natural_earth_coastline]
source_id = "natural-earth-coastline-110m-v4.1.0"
source_class = "coastline context"
availability = "approved"
reason = "not applicable"
url = "https://naturalearth.s3.amazonaws.com/110m_physical/ne_110m_coastline.zip"
local_path = "data/raw/natural-earth/ne_110m_coastline_v4.1.0.zip"
format = "ESRI Shapefile ZIP"
publisher = "Natural Earth"
expected_content_signature = "Natural Earth 1:110m coastline version 4.1.0; major islands included."
expected_prefix = "PK"
units = "degrees in source coordinates"
crs = "expected WGS84 from source .prj; verify after acquisition"
horizontal_datum = "expected WGS84 from source .prj; verify after acquisition"
vertical_datum = "not applicable"
coordinate_order = "x longitude, y latitude"
temporal_semantics = "not applicable"
station_metadata = "not applicable"
```

Create the story source manifest with the repository's existing 19-column header
and one `approved` row. Before acquisition, use `not-downloaded` for both
`sha256` and `local_path`; record version `4.1.0`, public-domain terms, expected
WGS84, line geometry, and scale-generalization limitations.

- [x] **Step 5: Make CI validate both provenance ledgers**

Add this line immediately after the existing provenance command:

```yaml
uv run python -m pipeline.provenance artifacts/provenance/story-source-manifest.csv
```

- [x] **Step 6: Run the tests before network acquisition**

Run:

```bash
uv run pytest tests/story/test_map_context.py tests/test_acquisition.py -q
uv run python -m pipeline.provenance artifacts/provenance/story-source-manifest.csv
```

Expected: tests pass and the story manifest validates one record.

- [x] **Step 7: Acquire and inspect the exact coastline asset**

Run only after confirming the repository is on the implementation commit and the
source contract above is unchanged:

```bash
STORY_MAP_OUTPUT="$(uv run python scripts/acquire_tohoku.py --config config/story-map-context.toml --root . --run-tag story-map-context --lane story)"
printf '%s\n' "$STORY_MAP_OUTPUT"
STORY_MAP_RUN_PATH="${STORY_MAP_OUTPUT##* to }"
test -d "$STORY_MAP_RUN_PATH"
uv run python -c "from pathlib import Path; import geopandas as gpd; p=Path('data/raw/natural-earth/ne_110m_coastline_v4.1.0.zip'); g=gpd.read_file('zip://' + str(p)); print({'rows': len(g), 'crs': g.crs.to_string() if g.crs else None, 'types': sorted(g.geom_type.unique())})"
```

Expected: one downloaded or checksum-verified cached asset; nonzero rows; CRS
`EPSG:4326`; only `LineString` and `MultiLineString` geometry.

Use the observed acquisition `outputs.json` values to replace both
`not-downloaded` fields in the story source manifest. Record the exact checksum,
row count, CRS, geometry types, command, run ID, version, and public-domain
terms in `context/story/SOURCES.md`. Preserve any unexpected value as a blocker
instead of changing the contract to fit it.

- [x] **Step 8: Revalidate and commit the governed source**

Run:

```bash
uv run python -m pipeline.provenance artifacts/provenance/story-source-manifest.csv
git check-ignore data/raw/natural-earth/ne_110m_coastline_v4.1.0.zip
git status --short
```

Expected: one valid story source record; the ZIP and checksum sidecar remain
ignored; only contract, provenance, test, CI, context, and lane-metadata changes
are tracked.

```bash
git add config/story-map-context.toml artifacts/provenance/story-source-manifest.csv context/story/SOURCES.md scripts/acquire_tohoku.py tests/test_acquisition.py tests/story/test_map_context.py .github/workflows/ci.yml "$STORY_MAP_RUN_PATH"
git commit -m "data(story): add governed Pacific coastline context"
```

### Task 3: Expose exact-grid coverage timelines from shared missingness logic

**Files:**

- Modify: `pipeline/missingness.py:35-230`
- Modify: `tests/test_missingness.py:258-330`

**Interfaces:**

- Consumes: `ExpectedWindow`, normalized `observation.csv`, and existing UTC/grid semantics.
- Produces: `CoveragePosition`, `OffGridObservation`, `CoastalCoverageTimeline`, and `build_coastal_coverage_timelines(processed_dir, windows)`.

- [x] **Step 1: Write the failing timeline test**

Add imports for the three new records and function, then add:

```python
def test_coverage_timeline_preserves_exact_blank_absent_and_off_grid_states(
    tmp_path: Path,
) -> None:
    processed = _stage_profile_inputs(tmp_path)
    window = ExpectedWindow(
        station_id="coast",
        name="Coastal fixture",
        start_utc="2011-03-11T00:00:00Z",
        end_utc_exclusive="2011-03-11T00:03:00Z",
        cadence_seconds=60,
    )

    timeline = build_coastal_coverage_timelines(processed, (window,))[0]

    assert [(point.expected_at_utc, point.status) for point in timeline.positions] == [
        ("2011-03-11T00:00:00Z", "observed"),
        ("2011-03-11T00:01:00Z", "absent_timestamp"),
        ("2011-03-11T00:02:00Z", "source_blank"),
    ]
    assert [point.observed_at_utc for point in timeline.off_grid] == [
        "2011-03-11T00:00:59Z"
    ]
    assert timeline.off_grid[0].raw_value_available is True
```

- [x] **Step 2: Run the test and observe the missing interface**

Run: `uv run pytest tests/test_missingness.py::test_coverage_timeline_preserves_exact_blank_absent_and_off_grid_states -q`

Expected: FAIL on the missing imports.

- [x] **Step 3: Add immutable coverage records**

Add `Literal` to the typing imports and define:

```python
CoverageStatus = Literal["observed", "source_blank", "absent_timestamp"]


@dataclass(frozen=True, slots=True)
class CoveragePosition:
    station_id: str
    expected_at_utc: str
    status: CoverageStatus


@dataclass(frozen=True, slots=True)
class OffGridObservation:
    station_id: str
    observed_at_utc: str
    raw_value_available: bool


@dataclass(frozen=True, slots=True)
class CoastalCoverageTimeline:
    station_id: str
    name: str
    start_utc: str
    end_utc_exclusive: str
    cadence_seconds: int
    positions: tuple[CoveragePosition, ...]
    off_grid: tuple[OffGridObservation, ...]
```

- [x] **Step 4: Implement the exact-grid timeline without snapping**

Add a public function that reads `observation.csv` through `_read_csv`, groups
rows by station, and for every window:

```python
def build_coastal_coverage_timelines(
    processed_dir: Path, windows: tuple[ExpectedWindow, ...]
) -> tuple[CoastalCoverageTimeline, ...]:
    rows = _read_csv(
        processed_dir / "observation.csv",
        {"station_id", "observed_at_utc", "raw_value"},
    )
    by_station: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_station[row["station_id"]].append(row)

    timelines: list[CoastalCoverageTimeline] = []
    for window in windows:
        start = _parse_utc(window.start_utc)
        end = _parse_utc(window.end_utc_exclusive)
        cadence = window.cadence_seconds
        exact: dict[int, dict[str, str]] = {}
        off_grid: list[OffGridObservation] = []
        for row in by_station.get(window.station_id, []):
            observed_at = _parse_utc(row["observed_at_utc"])
            if not start <= observed_at < end:
                continue
            offset_seconds = (observed_at - start).total_seconds()
            if offset_seconds.is_integer() and int(offset_seconds) % cadence == 0:
                offset = int(offset_seconds) // cadence
                if offset in exact:
                    raise MissingnessError(
                        f"duplicate exact-grid timestamp for {window.station_id}"
                    )
                exact[offset] = row
            else:
                off_grid.append(
                    OffGridObservation(
                        station_id=window.station_id,
                        observed_at_utc=row["observed_at_utc"],
                        raw_value_available=bool(row["raw_value"].strip()),
                    )
                )

        expected_count = int((end - start).total_seconds()) // cadence
        positions: list[CoveragePosition] = []
        for offset in range(expected_count):
            row = exact.get(offset)
            status: CoverageStatus
            if row is None:
                status = "absent_timestamp"
            elif row["raw_value"].strip():
                status = "observed"
            else:
                status = "source_blank"
            timestamp = start + timedelta(seconds=offset * cadence)
            positions.append(
                CoveragePosition(
                    station_id=window.station_id,
                    expected_at_utc=timestamp.isoformat().replace("+00:00", "Z"),
                    status=status,
                )
            )
        timelines.append(
            CoastalCoverageTimeline(
                station_id=window.station_id,
                name=window.name,
                start_utc=window.start_utc,
                end_utc_exclusive=window.end_utc_exclusive,
                cadence_seconds=cadence,
                positions=tuple(positions),
                off_grid=tuple(sorted(off_grid, key=lambda item: item.observed_at_utc)),
            )
        )
    return tuple(timelines)
```

Import `timedelta` from `datetime`. Do not assign an off-grid row to an expected
position.

- [x] **Step 5: Reconcile the timeline with the existing profile**

Extend the test to count one `observed`, one `source_blank`, one
`absent_timestamp`, and one off-grid observation. Run:

```bash
uv run pytest tests/test_missingness.py -q
uv run ruff check pipeline/missingness.py tests/test_missingness.py
uv run pyright
```

Expected: all missingness tests pass and the existing missingness report outputs
remain byte-identical because the writer was not changed.

- [x] **Step 6: Commit the shared visual primitive**

```bash
git add pipeline/missingness.py tests/test_missingness.py
git commit -m "feat(eda): expose coastal coverage timelines"
```

### Task 4: Implement the typed atlas input and Pacific geometry core

**Files:**

- Create: `analysis/story/atlas.py`
- Create: `config/story-atlas.toml`
- Create: `tests/story/test_atlas.py`
- Modify: `analysis/story/__init__.py`

**Interfaces:**

- Consumes: explicit `event.csv`, `station.csv`, `observation.csv`, `ttt_contour.csv`, `accounting.json`, `config/tohoku-missingness.toml`, and missingness summary.
- Produces: `AtlasInputs`, `AtlasConfig`, `load_atlas_inputs`,
  `load_atlas_config`, `validate_stage_a_scope`, `shift_longitude`,
  `split_at_display_seam`, and `geodesic_range_ring`.

- [x] **Step 1: Write failing loader and geometry tests**

In `tests/story/test_atlas.py`, create a local `_stage_atlas_inputs(tmp_path)`
helper that writes one reviewed event, one DART station, one coastal station,
four observations, two valid TTT line parts, and accounting JSON using the exact
normalized column names from `tests/test_missingness.py`. Add tests asserting:

```python
def test_atlas_loader_preserves_source_semantics(tmp_path: Path) -> None:
    processed, missingness_summary = _stage_atlas_inputs(tmp_path)

    atlas = load_atlas_inputs(processed, missingness_summary)

    assert atlas.event.event_id == "official20110311054624120_30"
    assert [station.station_type for station in atlas.stations] == ["coastal", "dart"]
    assert atlas.contours[0].crs == "EPSG:4326"
    assert atlas.observations[0].raw_value == 0.0
    assert atlas.observations[0].residual_value is None


def test_pacific_shift_splits_a_line_at_the_twenty_degree_seam() -> None:
    parts = split_at_display_seam(((-10.0, 0.0), (30.0, 0.0)))
    assert parts == (
        ((-10.0, 0.0), (20.0, 0.0)),
        ((-340.0, 0.0), (-330.0, 0.0)),
    )


def test_geodesic_range_ring_uses_kilometres_without_a_speed_model() -> None:
    ring = geodesic_range_ring(latitude=38.297, longitude=142.373, radius_km=2500)
    assert len(ring) == 361
    _, _, distance_m = Geod(ellps="WGS84").inv(
        142.373, 38.297, ring[0][0], ring[0][1]
    )
    assert distance_m == pytest.approx(2_500_000, abs=1.0)
```

Use a second seam test containing at least two coordinates on each side so the
production function rejects one-coordinate output segments rather than creating
invalid `LineString` objects.

- [x] **Step 2: Run the tests and observe the missing module**

Run: `uv run pytest tests/story/test_atlas.py -q`

Expected: FAIL because `analysis.story.atlas` does not exist.

- [x] **Step 3: Define the exact immutable records**

Create these public records in `analysis/story/atlas.py`:

```python
@dataclass(frozen=True, slots=True)
class EventRecord:
    event_id: str
    origin_time_utc: datetime
    latitude: float
    longitude: float


@dataclass(frozen=True, slots=True)
class StationRecord:
    station_id: str
    source_id: str
    station_type: Literal["coastal", "dart"]
    name: str
    latitude: float
    longitude: float
    units: str
    vertical_reference: str
    horizontal_datum: str
    time_basis: str


@dataclass(frozen=True, slots=True)
class ObservationRecord:
    station_id: str
    source_time: str
    observed_at_utc: datetime
    raw_value: float | None
    residual_value: float | None
    units: str
    vertical_reference: str


@dataclass(frozen=True, slots=True)
class ContourRecord:
    contour_id: str
    hours: float
    coordinates: tuple[tuple[float, float], ...]
    crs: str
    coordinate_order: str
    longitude_boundary_precision: bool
    crosses_antimeridian: bool


@dataclass(frozen=True, slots=True)
class AtlasInputs:
    event: EventRecord
    stations: tuple[StationRecord, ...]
    observations: tuple[ObservationRecord, ...]
    contours: tuple[ContourRecord, ...]
    accounting: dict[str, object]
    missingness_summary: dict[str, object]
    input_paths: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class AtlasConfig:
    event_id: str
    evidence_state: str
    display_crs: str
    central_meridian: float
    start_hours: float
    end_hours: float
    highlighted_contour_hours: tuple[int, ...]
    range_radii_km: tuple[int, ...]
    dart_station_ids: tuple[str, ...]
    coastal_station_ids: tuple[str, ...]
    figure_dpi: int
```

Reject non-rectangular CSV, nonfinite coordinates/values, event cardinality other
than one, unknown station types, duplicate station IDs, duplicate
station/timestamps, non-EPSG:4326 contours, fewer than two contour coordinates,
and longitude beyond `180 + 1e-6`. Permit a value slightly over +180 only when
`longitude_boundary_precision` is true.

- [x] **Step 4: Add the reviewed Stage A configuration**

Create `config/story-atlas.toml`:

```toml
schema_version = "1"
event_id = "official20110311054624120_30"
evidence_state = "preliminary_storyboard_evidence"
display_crs = "+proj=eqearth +lon_0=-160 +datum=WGS84 +units=m +no_defs +type=crs"
central_meridian = -160.0
start_hours = -6.0
end_hours = 30.0
highlighted_contour_hours = [1, 3, 6, 9, 12, 15, 18, 21, 24]
range_radii_km = [2500, 5000, 7500, 10000, 12500, 15000]
dart_station_ids = ["21413", "21418", "32401", "46411"]
coastal_station_ids = ["1617760", "1770000", "9419750", "9461380", "saip", "valp"]
figure_dpi = 160
```

`load_atlas_config` must require exactly this evidence state, increasing positive
ring radii, increasing positive contour hours, `start_hours < end_hours`, and the
approved Equal Earth string. `validate_stage_a_scope` must require exact equality
between the configured and loaded DART/coastal station sets, exactly one
missingness window for each configured coastal gauge, no unknown station
reference in observations, and the configured event ID. Unit tests use a local
fixture config with one DART and one coastal ID; the real config is what enforces
the approved four-plus-six scope.

- [x] **Step 5: Implement seam handling and geodesic rings**

Use:

```python
PACIFIC_MIN_LONGITUDE = -340.0
PACIFIC_MAX_LONGITUDE = 20.0


def shift_longitude(longitude: float) -> float:
    shifted = ((longitude - PACIFIC_MIN_LONGITUDE) % 360.0) + PACIFIC_MIN_LONGITUDE
    if shifted == PACIFIC_MAX_LONGITUDE:
        return PACIFIC_MIN_LONGITUDE
    return shifted


def split_at_display_seam(
    coordinates: tuple[tuple[float, float], ...],
) -> tuple[tuple[tuple[float, float], ...], ...]:
    shifted = tuple((shift_longitude(lon), lat) for lon, lat in coordinates)
    parts: list[list[tuple[float, float]]] = [[]]
    for coordinate in shifted:
        if parts[-1] and abs(coordinate[0] - parts[-1][-1][0]) > 180.0:
            parts.append([])
        parts[-1].append(coordinate)
    return tuple(tuple(part) for part in parts if part)


def geodesic_range_ring(
    *, latitude: float, longitude: float, radius_km: int
) -> tuple[tuple[float, float], ...]:
    geod = Geod(ellps="WGS84")
    coordinates = []
    for bearing in range(361):
        ring_lon, ring_lat, _ = geod.fwd(longitude, latitude, bearing, radius_km * 1000)
        coordinates.append((ring_lon, ring_lat))
    return tuple(coordinates)
```

When a segment crosses the 20°E/-340° display seam, interpolate its seam
intersection, close the current part at 20°E or -340°, and open the next part at
the equivalent opposite boundary. Every returned part therefore remains a valid
line with at least two coordinates; record any rejected degenerate source input
instead of discarding a generated one-coordinate fragment. Preserve
`source_time`, contour coordinate order, and the publisher antimeridian flag in
the typed records even though Stage A aligns only on verified UTC.

- [x] **Step 6: Run focused and type checks**

Run:

```bash
uv run pytest tests/story/test_atlas.py -q
uv run ruff check analysis/story/atlas.py tests/story/test_atlas.py
uv run pyright
```

Expected: focused tests pass and strict type checking is clean.

- [x] **Step 7: Commit the atlas core**

```bash
git add analysis/story/atlas.py analysis/story/__init__.py config/story-atlas.toml tests/story/test_atlas.py
git commit -m "feat(story): add typed atlas geometry core"
```

### Task 5: Render the Pacific evidence map deterministically

**Files:**

- Create: `analysis/story/plots.py`
- Modify: `tests/story/test_atlas.py`
- Modify: `analysis/story/__init__.py`

**Interfaces:**

- Consumes: `AtlasInputs`, `AtlasConfig`, an explicit coastline path, and an explicit output stem.
- Produces: `PlotFiles` and `plot_pacific_evidence(...)` writing `01_pacific_evidence_map.{png,svg}`.

- [x] **Step 1: Write a failing deterministic-render test**

Write a two-feature coastline GeoJSON into the test temporary directory, call the
plot twice with distinct stems, and assert:

```python
first = plot_pacific_evidence(atlas, config, coastline_path, tmp_path / "first")
second = plot_pacific_evidence(atlas, config, coastline_path, tmp_path / "second")

assert first.png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
assert b"Pacific evidence map" in first.svg.read_bytes()
assert sha256(first.png.read_bytes()).hexdigest() == sha256(second.png.read_bytes()).hexdigest()
assert sha256(first.svg.read_bytes()).hexdigest() == sha256(second.svg.read_bytes()).hexdigest()
assert first.projection == config.display_crs
assert first.input_parts == len(atlas.contours) + 2
assert first.output_parts >= first.input_parts
```

- [x] **Step 2: Run the focused test and observe the missing plot function**

Run: `uv run pytest tests/story/test_atlas.py -k pacific_evidence -q`

Expected: FAIL on the missing import.

- [x] **Step 3: Add deterministic plot output ownership**

Define:

```python
@dataclass(frozen=True, slots=True)
class PlotFiles:
    plot_id: str
    png: Path
    svg: Path
    projection: str
    units: str
    input_parts: int
    output_parts: int


def _save_figure(figure: Figure, output_stem: Path) -> tuple[Path, Path]:
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    png = output_stem.with_suffix(".png")
    svg = output_stem.with_suffix(".svg")
    figure.savefig(
        png,
        dpi=160,
        bbox_inches="tight",
        metadata={"Software": "pacific-tsunami-warning-time"},
    )
    figure.savefig(
        svg,
        bbox_inches="tight",
        metadata={"Date": None, "Creator": "pacific-tsunami-warning-time"},
    )
    plt.close(figure)
    return png, svg
```

At module import, select the noninteractive `Agg` backend, use DejaVu Sans, set
`svg.hashsalt` to `pacific-tsunami-warning-time`, and disable path timestamp
metadata.

- [x] **Step 4: Implement one-message evidence mapping**

`plot_pacific_evidence` must:

- read the explicit coastline with GeoPandas and require EPSG:4326 line geometry;
- split coastline and TTT linework at the 20°E display seam before projecting;
- project with the exact configured Equal Earth CRS;
- draw coastline as neutral context and all source contours as subdued linework;
- directly distinguish the event star, DART triangles, and coastal circles;
- label all ten candidate stations without claiming promotion;
- include “NCEI published hourly travel-time contours; not a continuous field”;
- include “Equal Earth, central meridian 160°W” and the preliminary evidence label;
- use no basemap service, bathymetry, amplitude, wave texture, or decorative particles; and
- return input/output part accounting in `PlotFiles`.

- [x] **Step 5: Run deterministic and visual-contract checks**

Run:

```bash
uv run pytest tests/story/test_atlas.py -k pacific_evidence -q
uv run ruff check analysis/story/plots.py tests/story/test_atlas.py
uv run pyright
```

Expected: byte-identical fixture renders and clean static checks.

- [x] **Step 6: Commit the evidence map**

```bash
git add analysis/story/plots.py analysis/story/__init__.py tests/story/test_atlas.py
git commit -m "feat(story): render Pacific evidence map"
```

### Task 6: Render observation-coverage timelines

**Files:**

- Modify: `analysis/story/plots.py`
- Modify: `tests/story/test_atlas.py`

**Interfaces:**

- Consumes: `tuple[CoastalCoverageTimeline, ...]`, the shared missingness summary, and an output stem.
- Produces: `plot_observation_coverage(...)` writing `02_observation_coverage.{png,svg}`.

- [x] **Step 1: Write the failing coverage-plot test**

Build one fixture timeline with observed, blank, absent, and off-grid states and
assert deterministic PNG/SVG output plus this metadata:

```python
files = plot_observation_coverage(
    timelines,
    missingness_summary=atlas.missingness_summary,
    output_stem=tmp_path / "02_observation_coverage",
)

assert files.plot_id == "02_observation_coverage"
assert files.units == "source-supported timestamp coverage"
assert files.projection == "not applicable"
assert files.png.is_file()
assert files.svg.is_file()
```

- [x] **Step 2: Run the focused test and observe the missing function**

Run: `uv run pytest tests/story/test_atlas.py -k observation_coverage -q`

Expected: FAIL on the missing import.

- [x] **Step 3: Implement the timeline view**

Render one horizontal strip per coastal gauge over its own source-supported
window. Encode exact observations, retained source blanks, and absent timestamps
with distinct luminance and labels. Overlay off-grid observations as narrow
outlined ticks at their actual timestamps. Put strict and sample-density
coverage percentages beside each station and identify Pago Pago and Saipan from
the supplied metrics rather than a hard-coded annotation.

The legend must state that off-grid ticks were preserved rather than snapped and
that gray absence is not numeric zero. Use `_save_figure` for both outputs.

- [x] **Step 4: Verify counts and rendering**

Run:

```bash
uv run pytest tests/test_missingness.py tests/story/test_atlas.py -q
uv run ruff check analysis/story/plots.py tests/story/test_atlas.py
uv run pyright
```

Expected: shared counts remain unchanged and the new plot tests pass.

- [x] **Step 5: Commit the coverage plot**

```bash
git add analysis/story/plots.py tests/story/test_atlas.py
git commit -m "feat(story): visualize observation coverage"
```

### Task 7: Render source-honest station small multiples

**Files:**

- Modify: `analysis/story/atlas.py`
- Modify: `analysis/story/plots.py`
- Modify: `tests/story/test_atlas.py`

**Interfaces:**

- Consumes: `AtlasInputs`, origin-relative `AtlasConfig.start_hours/end_hours`, and output stem.
- Produces: `SeriesPanel`, `build_series_panels(...)`, and `plot_station_timeseries(...)` writing `03_station_timeseries.{png,svg}`.

- [ ] **Step 1: Write failing series-semantics tests**

Use one DART and one coastal fixture station:

```python
panels = build_series_panels(atlas, config)

assert panels[0].station_type == "coastal"
assert panels[0].value_field == "raw_value"
assert panels[1].station_type == "dart"
assert panels[1].value_field == "residual_value"
assert all(config.start_hours <= point.elapsed_hours <= config.end_hours for panel in panels for point in panel.points)
assert {panel.shared_y_scale for panel in panels} == {False}
```

Render the fixture twice and compare PNG/SVG hashes.

- [ ] **Step 2: Run the tests and observe the missing panel interface**

Run: `uv run pytest tests/story/test_atlas.py -k 'series or timeseries' -q`

Expected: FAIL on missing imports.

- [ ] **Step 3: Add explicit panel records**

```python
@dataclass(frozen=True, slots=True)
class SeriesPoint:
    elapsed_hours: float
    value: float


@dataclass(frozen=True, slots=True)
class SeriesPanel:
    station_id: str
    station_name: str
    station_type: Literal["coastal", "dart"]
    value_field: Literal["raw_value", "residual_value"]
    units: str
    vertical_reference: str
    shared_y_scale: bool
    points: tuple[SeriesPoint, ...]
```

`build_series_panels` selects `raw_value` for coastal stations and
`residual_value` for DART stations, filters only the configured origin-relative
window, preserves every retained source timestamp, sorts by time, and performs
no centering, smoothing, interpolation, or resampling.

- [ ] **Step 4: Render separately scaled point traces**

Create a two-column small-multiple grid ordered by station type then station ID.
Use points rather than connected lines so gaps are not visually bridged. Label
each panel with station ID, source field, units, vertical reference, and local
y-scale status. Add a common x-axis in hours from earthquake origin and a note
that panel amplitudes are not comparable.

- [ ] **Step 5: Verify source semantics and deterministic output**

Run:

```bash
uv run pytest tests/story/test_atlas.py -k 'series or timeseries' -q
uv run ruff check analysis/story/atlas.py analysis/story/plots.py tests/story/test_atlas.py
uv run pyright
```

Expected: all series tests pass with zero source-value transformations.

- [ ] **Step 6: Commit the station view**

```bash
git add analysis/story/atlas.py analysis/story/plots.py tests/story/test_atlas.py
git commit -m "feat(story): add station signal small multiples"
```

### Task 8: Render the distance-versus-contour shape diagnostic

**Files:**

- Modify: `analysis/story/plots.py`
- Modify: `tests/story/test_atlas.py`

**Interfaces:**

- Consumes: event location, configured geodesic radii in kilometres, configured NCEI contour hours, common coastline, and common projection/extent.
- Produces: `plot_distance_contour_diagnostic(...)` writing `04_distance_contour_diagnostic.{png,svg}` without a propagation-speed model.

- [ ] **Step 1: Write the failing semantic guard test**

```python
files = plot_distance_contour_diagnostic(
    atlas,
    config,
    coastline_path,
    tmp_path / "04_distance_contour_diagnostic",
)

assert files.plot_id == "04_distance_contour_diagnostic"
assert files.units == "left: geodesic kilometres; right: published contour hours"
assert files.projection == config.display_crs
assert files.png.is_file()
assert files.svg.is_file()
```

Also inspect the SVG text and assert it contains `No speed conversion` and
`not a modeled arrival at a station`.

- [ ] **Step 2: Run the focused test and observe the missing function**

Run: `uv run pytest tests/story/test_atlas.py -k distance_contour -q`

Expected: FAIL on the missing import.

- [ ] **Step 3: Implement the side-by-side comparison**

Use identical projected coastline, extent, event, and station overlays in both
panels. The left panel draws configured WGS84 geodesic range rings labeled in
kilometres. The right draws only the configured published NCEI contour hours.
The caption must state that the units differ, no speed conversion was chosen,
and nearest-contour values are not being assigned to stations.

The function must not accept a speed parameter, arrival table, residual table,
or continuous raster.

- [ ] **Step 4: Verify semantic and deterministic behavior**

Run:

```bash
uv run pytest tests/story/test_atlas.py -k distance_contour -q
uv run ruff check analysis/story/plots.py tests/story/test_atlas.py
uv run pyright
```

Expected: semantic text and byte-stability checks pass.

- [ ] **Step 5: Commit the shape diagnostic**

```bash
git add analysis/story/plots.py tests/story/test_atlas.py
git commit -m "feat(story): compare distance rings with TTT contours"
```

### Task 9: Add the reproducible atlas runner and evidence bundle

**Files:**

- Create: `analysis/story/artifacts.py`
- Create: `scripts/story/build_story_atlas.py`
- Create: `tests/story/test_story_atlas_cli.py`
- Modify: `analysis/story/__init__.py`
- Modify: `artifacts/README.md`

**Interfaces:**

- Consumes: all Task 3–8 interfaces plus explicit CLI paths and run identity.
- Produces: four PNG/SVG pairs, `atlas-manifest.json`, `decision-ledger.csv`, six-file portable run bundle, MLflow run, and generated `context/story/EDA_REPORT.md`.

- [ ] **Step 1: Write the failing end-to-end fixture test**

Stage the compact accepted fixture, coastline GeoJSON, missingness config and
summary, then call `scripts.story.build_story_atlas.main` with every path
explicit. Assert:

```python
assert result == 0
assert {path.name for path in artifact_dir.iterdir()} == {
    "01_pacific_evidence_map.png",
    "01_pacific_evidence_map.svg",
    "02_observation_coverage.png",
    "02_observation_coverage.svg",
    "03_station_timeseries.png",
    "03_station_timeseries.svg",
    "04_distance_contour_diagnostic.png",
    "04_distance_contour_diagnostic.svg",
    "atlas-manifest.json",
    "decision-ledger.csv",
}
assert {path.name for path in run_dir.iterdir()} == {
    "config.json",
    "inputs.json",
    "meta.json",
    "metrics.json",
    "notes.md",
    "outputs.json",
}
meta = json.loads((run_dir / "meta.json").read_text())
assert meta["lane"] == "story"
assert meta["evidence_state"] == "preliminary_storyboard_evidence"
assert "No story claim has been promoted" in report_path.read_text()
assert "paper" not in json.dumps(json.loads((artifact_dir / "atlas-manifest.json").read_text()))
```

Assert the MLflow run has tags `lane=story`,
`evidence_state=preliminary_storyboard_evidence`, `portable_run_id`, and the
input fingerprint.

- [ ] **Step 2: Run the integration test and observe the missing runner**

Run: `uv run pytest tests/story/test_story_atlas_cli.py -q`

Expected: FAIL because the artifacts module and CLI do not exist.

- [ ] **Step 3: Define artifact records and path fences**

In `analysis/story/artifacts.py`, define:

```python
Disposition = Literal["retain", "revise", "branch", "promote", "reject"]


@dataclass(frozen=True, slots=True)
class DecisionRecord:
    plot_id: str
    observation: str
    question: str
    follow_up: str
    result: str
    disposition: Disposition
    storyboard_implication: str
    manual_qa: str


def validate_story_output_path(path: Path) -> None:
    normalized = f"/{path.as_posix().strip('/')}/"
    if "/analysis/paper/" in normalized or "/artifacts/eda/paper/" in normalized:
        raise AtlasError(f"paper path is forbidden in story evidence: {normalized}")
    if "/app/public/data/" in normalized:
        raise AtlasError(f"exploratory output cannot be an app asset: {normalized}")
```

Every manifest and output path passes this function. Reject an existing run or
artifact directory rather than overwriting it.

- [ ] **Step 4: Support preview decisions and validated review decisions**

When `--decision-input` is omitted, write one factual preview row per plot with
disposition `retain`, meaning retain in the diagnostic atlas rather than promote
to the storyboard. Populate `observation` and `result` from calculated counts and
declared semantics, and set `storyboard_implication` to
`Await manual atlas review; no storyboard promotion.`

Add `load_decision_input(path: Path) -> tuple[DecisionRecord, ...]`. It validates:

- `schema_version = "1"` and
  `evidence_state = "preliminary_storyboard_evidence"`;
- exactly the four plot IDs, once each and in atlas order;
- nonblank reviewer, review date, observation, question, follow-up, result,
  storyboard implication, and manual-QA evidence;
- a disposition in `retain`, `revise`, `branch`, or `reject`; and
- no Stage A `promote` disposition.

When a decision input is supplied, use its reviewed prose verbatim in the
decision ledger and report, hash the TOML as an input, and retain the calculated
plot metrics separately. Never mutate the review file.

For each PNG and SVG, `atlas-manifest.json` records the artifact ID, title,
question, lane, generating command, Git SHA, candidate-build ID, source/input
checksums, CRS/projection or time basis, units, longitude handling, input/output
and rejection counts, path, media type, pixel dimensions or SVG view box,
SHA-256, evidence state, finding, limitation, disposition, storyboard
implication, and manual-QA text. Add integration assertions for every required
key and reconcile manifest hashes with the files on disk.

The report must include these sections in order:

```markdown
# Visual-Story EDA Report

## Run and evidence state
## Inputs and source boundary
## Fixed diagnostic atlas
## Adaptive decision ledger
## Interpretation
## Limitations
## Takeaways
## Next steps
## Input and output fingerprints
```

It must explicitly state that the NCTR field is unavailable, the fourth plot
compares shapes in different units, station panels use local scales, and no
arrival pick, residual comparison, station promotion, or story claim occurred.

- [ ] **Step 5: Implement the thin CLI**

The parser requires all paths and run identity explicitly, except for the
optional reviewed decision input:

```text
--processed-dir
--missingness-config
--missingness-summary
--coastline
--config
--decision-input (optional)
--artifact-dir
--run-dir
--report
--run-id
--git-sha
--working-tree clean|dirty|unknown
--mlflow-dir
--mlflow-experiment
```

The CLI sequence is fixed:

1. validate that output directories do not exist;
2. load config, optional reviewed decisions, and all scientific inputs;
3. validate the exact configured event and four-DART/six-coastal scope, then
   build shared coverage timelines;
4. render four plots;
5. hash every input and generated plot;
6. write manifest and decision ledger;
7. render the Markdown report;
8. write the portable bundle;
9. record the project-local MLflow run; and
10. write final metadata and print only output paths/run IDs.

Use the existing missingness CLI's SHA-256, path-display, JSON formatting,
fingerprint, and MLflow conventions. Do not copy raw source data into either run
bundle. Log configuration, input/version references, Git SHA, metrics, every
generated artifact, report, and retain/revise/branch/reject decision in MLflow;
keep the portable six-file bundle as the independent reconstruction record.

- [ ] **Step 6: Verify integration, decision validation, overwrite refusal, and lane fences**

Test both preview mode and a complete four-plot decision TOML fixture. Add
failure cases for a missing/duplicate plot decision, `promote`, blank review
text, an existing artifact directory, existing run directory, paper artifact
path, missing coastline, and mismatched event ID. Run:

```bash
uv run pytest tests/story/test_story_atlas_cli.py -q
uv run ruff check analysis/story scripts/story tests/story
uv run pyright
```

Expected: all integration/error tests pass, the decision-input hash is recorded,
and no partial output survives a failed run.

- [ ] **Step 7: Commit the runner**

```bash
git add analysis/story/artifacts.py analysis/story/__init__.py scripts/story/build_story_atlas.py tests/story/test_story_atlas_cli.py artifacts/README.md
git commit -m "feat(story): add reproducible atlas runner"
```

### Task 10: Add the thin Marimo atlas viewer

**Files:**

- Create: `notebooks/story/tohoku_storyboard_eda.py`
- Modify: `tests/story/test_dependencies.py`

**Interfaces:**

- Consumes: zero or more existing `artifacts/eda/story/*/atlas-manifest.json`
  files.
- Produces: a read-only reactive selector and viewer; no metrics, transforms,
  scientific records, plots, or repository writes.

- [ ] **Step 1: Write the failing notebook boundary test**

Add a source-level guard to `tests/story/test_dependencies.py`:

```python
def test_story_notebook_is_a_thin_read_only_view() -> None:
    source = Path("notebooks/story/tohoku_storyboard_eda.py").read_text()
    for forbidden in (
        "analysis.story.plots",
        "observation.csv",
        "station.csv",
        "mlflow",
        ".write_text(",
        "print(",
    ):
        assert forbidden not in source
```

- [ ] **Step 2: Run the test and observe the missing notebook**

Run: `uv run pytest tests/story/test_dependencies.py -q`

Expected: FAIL because the notebook does not exist.

- [ ] **Step 3: Create the thin reactive notebook**

Use the same Marimo DAG pattern as `notebooks/tohoku_missingness.py`. Discover
only atlas manifests below `artifacts/eda/story`, offer their run IDs in a
selector, and show a clear empty state when none exists. Cells may:

- load and validate selected manifest JSON;
- show evidence-state and source-boundary callouts;
- display the four already-generated PNG files;
- read and display the selected decision-ledger rows; and
- link readers to `context/story/EDA_REPORT.md`.

Cells must not import plotting functions, load normalized CSV files, calculate
metrics, modify files, call MLflow, or use `print()`.

- [ ] **Step 4: Verify empty-state execution and commit**

Run:

```bash
uv run pytest tests/story/test_dependencies.py -q
uv run marimo check notebooks/story/tohoku_storyboard_eda.py
uv run marimo export html notebooks/story/tohoku_storyboard_eda.py -o /tmp/tohoku-storyboard-eda-empty.html --force
uv run ruff check notebooks/story/tohoku_storyboard_eda.py tests/story/test_dependencies.py
uv run pyright
git diff --check
```

Expected: tests and checks pass, the headless export renders the empty-state
callout, and no repository file is created by notebook execution.

```bash
git add notebooks/story/tohoku_storyboard_eda.py tests/story/test_dependencies.py
git commit -m "feat(story): add thin atlas notebook"
```

### Task 11: Run the real atlas and record adaptive findings

**Files:**

- Create: `config/story-atlas-decisions.toml`
- Modify: `context/story/PROJECT.md`
- Modify: `context/story/TASKS.md`
- Modify: `context/story/EDA_REPORT.md`
- Modify: `context/story/STORYBOARD.md`
- Modify: `context/STRUCTURE.md`
- Modify: `context/HANDOVER.md`
- Modify: `graphify-out/graph.json`
- Modify: `graphify-out/graph.html` if Graphify changes it
- Modify: `graphify-out/GRAPH_REPORT.md`
- Generate: `artifacts/eda/story/$STORY_RUN_ID/`
- Generate: `artifacts/logs/runs/$STORY_RUN_ID/`

**Interfaces:**

- Consumes: the committed implementation, explicit accepted candidate build,
  governed coastline, and a human-readable review decision for each plot.
- Produces: manually inspected preliminary evidence, a committed adaptive
  decision input, a reproducible canonical run, and a Checker-ready handoff.

- [ ] **Step 1: Confirm the implementation boundary is clean and create a temporary preview**

Run these commands in one shell so the variables remain exact:

```bash
test -z "$(git status --porcelain)"
STORY_PREVIEW_SHA="$(git rev-parse --short HEAD)"
STORY_PREVIEW_RUN_ID="$(date -u +%Y-%m-%d__%H%M)__story-atlas-preview__${STORY_PREVIEW_SHA}"
STORY_PREVIEW_ROOT="$(mktemp -d /tmp/tsunami-story-preview.XXXXXX)"
uv run python scripts/story/build_story_atlas.py --processed-dir data/processed/tohoku/2026-09-09-valparaiso-reviewed-7576ffb-a --missingness-config config/tohoku-missingness.toml --missingness-summary artifacts/eda/missingness/missingness-summary.json --coastline data/raw/natural-earth/ne_110m_coastline_v4.1.0.zip --config config/story-atlas.toml --artifact-dir "${STORY_PREVIEW_ROOT}/artifacts" --run-dir "${STORY_PREVIEW_ROOT}/run" --report "${STORY_PREVIEW_ROOT}/EDA_REPORT.md" --run-id "$STORY_PREVIEW_RUN_ID" --git-sha "$STORY_PREVIEW_SHA" --working-tree clean --mlflow-dir .mlflow/mlruns --mlflow-experiment story-tohoku-eda
```

Expected: the tracked tree was clean at invocation and all preview scientific
outputs exist only below the unique temporary directory.

- [ ] **Step 2: Perform visual and source-value QA on the preview**

Open the four preview PNGs with the local image viewer and record concrete
observations for:

- full-size and thumbnail/squint legibility;
- grayscale and deuteranopia/protanopia simulations;
- correct station/event placement for the event, Hilo, and Valparaíso;
- exact source contour labels for 1, 6, and 24 hours;
- coverage totals for Hilo, Pago Pago, and Saipan;
- no bridged gap in Saipan and no connected-gap implication in station panels;
- identical projection and extent in the two diagnostic panels;
- explicit different-unit warning on the ring/contour comparison; and
- no visual claim of amplitude comparability, continuous wavefront, observed
  arrival, station promotion, or actionable warning time.

Cross-check each displayed count and label against the normalized CSVs,
missingness summary, and atlas manifest. If any check disagrees, stop and return
the defect to the task that owns the transform; do not rationalize it in prose.

- [ ] **Step 3: Create and validate the adaptive review input**

Apply the design's branch table exactly:

- legible map and usable evidence chain: retain the fixed core;
- basin clutter: branch to regional small multiples in a new reviewed task;
- CRS, seam, or geometry ambiguity: reject the spatial result and return the
  defect to the shared contract;
- dominant observation gaps: branch to an observability-first candidate story;
- visibly non-radial contour structure: retain the distance candidate for T-003B;
- weak shape contrast: revise the candidate toward coverage or multi-clock
  explanation without selecting stations from the desired result.

Create `config/story-atlas-decisions.toml` with top-level `schema_version`,
`evidence_state`, `reviewer`, and the exact UTC date returned by `date -u +%F`.
Add one table for each exact plot ID. Every table contains `observation`,
`question`, `follow_up`, `result`, `disposition`, and
`storyboard_implication`, plus `manual_qa` containing the plot-specific checks
actually performed. Use only what the preview and source cross-checks actually
showed. Do not use `promote` in Stage A.

Run:

```bash
uv run python -c "from pathlib import Path; from analysis.story.artifacts import load_decision_input; rows=load_decision_input(Path('config/story-atlas-decisions.toml')); assert len(rows) == 4; assert all(row.disposition != 'promote' for row in rows)"
git diff --check
git add config/story-atlas-decisions.toml
git commit -m "docs(story): record atlas review decisions"
```

- [ ] **Step 4: Run the canonical atlas from the committed review**

Confirm the tree is clean, derive a new immutable run identity from the review
commit, and keep all scientific inputs exact:

```bash
test -z "$(git status --porcelain)"
STORY_GIT_SHA="$(git rev-parse --short HEAD)"
STORY_RUN_ID="$(date -u +%Y-%m-%d__%H%M)__story-atlas__${STORY_GIT_SHA}"
uv run python scripts/story/build_story_atlas.py --processed-dir data/processed/tohoku/2026-09-09-valparaiso-reviewed-7576ffb-a --missingness-config config/tohoku-missingness.toml --missingness-summary artifacts/eda/missingness/missingness-summary.json --coastline data/raw/natural-earth/ne_110m_coastline_v4.1.0.zip --config config/story-atlas.toml --decision-input config/story-atlas-decisions.toml --artifact-dir "artifacts/eda/story/${STORY_RUN_ID}" --run-dir "artifacts/logs/runs/${STORY_RUN_ID}" --report context/story/EDA_REPORT.md --run-id "$STORY_RUN_ID" --git-sha "$STORY_GIT_SHA" --working-tree clean --mlflow-dir .mlflow/mlruns --mlflow-experiment story-tohoku-eda
uv run marimo export html notebooks/story/tohoku_storyboard_eda.py -o /tmp/tohoku-storyboard-eda.html --force
```

Expected: the canonical report and ledger reproduce the committed review; the
notebook selects and displays the new run without changing repository files.

- [ ] **Step 5: Rebuild independently and compare stable evidence**

Create another unique temporary directory and run the same CLI with the same
scientific/configuration inputs and committed review, a distinct verification
run ID, and `--working-tree dirty` because canonical generated outputs now exist.
Compare all eight figure SHA-256 values, all four decision rows, calculated
metrics, input fingerprint, and configuration hash. Exclude only run ID,
timestamp, working-tree status, MLflow identity, and absolute output paths.
Scientific and visual outputs must match byte-for-byte.

- [ ] **Step 6: Update durable status without overclaiming**

Set T-003A to `in-review`, record the exact portable and MLflow run IDs, figure
hashes, observations, and verification commands in `context/story/TASKS.md` and
`context/HANDOVER.md`, and keep T-003B pending. Update `context/STRUCTURE.md` to
mark the implemented paths active. Keep `context/story/STORYBOARD.md` at “no
promoted scene” while recording the candidate branch selected for later review.
Do not hand-edit the script-generated `context/story/EDA_REPORT.md`.

- [ ] **Step 7: Run the full gate and refresh the project graph**

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
uv run python -m pipeline.provenance artifacts/provenance/source-manifest.csv
uv run python -m pipeline.provenance artifacts/provenance/story-source-manifest.csv
uv run marimo check notebooks/story/tohoku_storyboard_eda.py
npm run check
graphify update .
graphify query "How do the Stage A story atlas inputs produce preliminary figures, evidence, and the T-003B gate?"
git diff --check
```

Expected: every command passes; Graphify returns the story modules, generated
evidence paths, context report, and later gate without paper-lane imports.

- [ ] **Step 8: Commit the real preliminary atlas**

```bash
git add "artifacts/eda/story/${STORY_RUN_ID}" "artifacts/logs/runs/${STORY_RUN_ID}" context/story/PROJECT.md context/story/TASKS.md context/story/EDA_REPORT.md context/story/STORYBOARD.md context/STRUCTURE.md context/HANDOVER.md graphify-out/graph.json graphify-out/GRAPH_REPORT.md
git add graphify-out/graph.html
git commit -m "docs(story): record preliminary atlas findings"
```

The Maker hands this commit to a scientific/cartographic Checker. T-003A becomes
`done` only after the Checker reruns the evidence and accepts or requests fixes.

## Stage A Completion Gate

Stage A is complete only when:

- all four diagnostics rebuild deterministically from explicit accepted inputs;
- every figure has PNG/SVG, projection or time basis, units, hashes, and manual QA;
- the report contains observed results, interpretation, limitations, takeaways,
  and the next adaptive branch;
- the notebook is a read-only thin view;
- the story manifest and shared source manifest both validate;
- the paper and app export fences pass;
- no arrival-based or promotion claim appears; and
- the independent Checker records an accepted disposition.

T-003B remains a separate plan after T-002E publishes a reviewed shared release.
