# Tōhoku Data Coverage and Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the requested Tōhoku source contracts, acquire every approved
asset reproducibly, and produce deterministic analysis-ready tables plus a
data-quality report without beginning EDA.

**Architecture:** A TOML source contract drives a standard-library acquisition
module that treats each source independently and writes immutable raw files plus a
portable run bundle. A separate normalization module parses accepted USGS FDSN CSV,
NCEI TTT GeoJSON, NCEI DART text, and NOAA CO-OPS JSON into deterministic CSV and
JSON artifacts; inaccessible or scientifically ambiguous assets remain explicit in
coverage and rejection records.

**Tech Stack:** Python 3.12 standard library, `uv`, pytest, Ruff, Pyright, TOML,
CSV, JSON, SHA-256, NOAA/USGS HTTPS APIs

**Spec:** `docs/superpowers/specs/2026-09-04-tohoku-data-pipeline-eda-design.md`

## Global Constraints

- Execute on `main` with project-owner authorization recorded on 2026-09-05.
- Commit each accepted task or meaningful TDD subtask with one Conventional
  Commit and no co-author trailer.
- Do not infer a CRS, datum, unit, coordinate order, or time basis.
- Keep blocked sources visible; never replace the requested NCTR, Saipan, or
  Chilean assets with an unapproved proxy.
- Raw and bulky processed data remain ignored; tracked reports and run summaries
  contain checksums, counts, evidence, limitations, and next steps.
- T-002D EDA does not begin in this plan.

---

### Task 1: Source-contract ledger and blocked-state validation

**Files:**
- Create: `config/tohoku-data-proof.toml`
- Modify: `pipeline/provenance.py`
- Modify: `tests/test_provenance.py`
- Modify: `artifacts/provenance/source-manifest.csv`
- Modify: `artifacts/provenance/source-manifest.md`
- Modify: `context/ACQUISITION_REPORT.md`
- Modify: `context/TASKS.md`

**Interfaces:**
- Consumes: authoritative source metadata and the existing manifest columns.
- Produces: `blocked` as a valid manifest status and one exact contract per source
  asset in `config/tohoku-data-proof.toml`.

- [ ] **Step 1: Write the failing blocked-status test**

```python
def test_manifest_accepts_a_blocked_asset(tmp_path: Path) -> None:
    manifest = write_manifest(tmp_path, status="blocked")
    assert validate_manifest(manifest).records == 1
```

- [ ] **Step 2: Verify the new status fails for the intended reason**

Run: `uv run pytest tests/test_provenance.py::test_manifest_accepts_a_blocked_asset -q`

Expected: failure reporting `unsupported status 'blocked'`.

- [ ] **Step 3: Add the minimal manifest behavior**

Add `blocked` to `ALLOWED_STATUSES`, document that it means the requested asset
has a recorded access or contract blocker and cannot feed acquisition, then run the
focused and full provenance tests.

- [ ] **Step 4: Record exact contracts**

The TOML must declare, per asset: `source_id`, `source_class`, `availability`,
`url`, `local_path`, `format`, `publisher`, expected content signature, units,
CRS/datum/time semantics, and station metadata where applicable. Record these
pre-residual DART selections:

- near field: 21418 and 21413, the two stations NCEI explicitly groups as near;
- far field: 46411 and 32401, selected to span the northeast and southeast
  Pacific before any modeled residual is inspected.

Record the six coastal candidates exactly: Tanapag Harbor/Saipan 1633227, Adak
9461380, Hilo 1617760, Crescent City 9419750, Pago Pago 1770000, and Valparaíso
IOC code `valp`.

- [ ] **Step 5: Publish and verify the coverage decision**

Populate `context/ACQUISITION_REPORT.md` with authoritative links, observed smoke
checks, approved-versus-blocked counts, contract details, limitations, and next
steps. Run:

```bash
uv run python -m pipeline.provenance artifacts/provenance/source-manifest.csv
uv run pytest tests/test_provenance.py -q
uv run ruff check pipeline/provenance.py tests/test_provenance.py
uv run pyright
git diff --check
```

- [ ] **Step 6: Obtain a fresh scientific checker disposition and commit**

The checker verifies station IDs/coordinates, source-owned units/time semantics,
the no-residual station rule, and every blocked reason. Address material findings,
mark T-002A done, and commit as `docs(data): resolve Tohoku source contracts`.

---

### Task 2: Atomic, source-independent acquisition core

**Files:**
- Create: `pipeline/acquisition.py`
- Create: `scripts/acquire_tohoku.py`
- Create: `tests/test_acquisition.py`
- Create: `tests/fixtures/acquisition/sample.json`

**Interfaces:**
- Consumes: `config/tohoku-data-proof.toml` source tables with
  `availability = "approved"`.
- Produces:
  `load_contracts(path: Path) -> tuple[SourceContract, ...]`,
  `download_url(url: str, destination: Path, timeout_seconds: float) -> ResponseMetadata`,
  `acquire_source(contract: SourceContract, root: Path, fetcher: Fetcher = download_url) -> AcquisitionResult`,
  and `acquire_all(contracts: Sequence[SourceContract], root: Path, fetcher: Fetcher = download_url) -> tuple[AcquisitionResult, ...]`.

`SourceContract` contains the Task 1 TOML fields verbatim (`crs`,
`temporal_semantics`, and `station_metadata` retain those exact names), including
an explicit `reason` and a whitespace-tolerant `expected_prefix` used for a
minimal response-identity check. `ResponseMetadata` contains
`content_type: str` and `headers: dict[str, str]`. `AcquisitionResult` contains
`source_id`, `status`, `local_path`, `bytes`, `sha256`, and `reason`; `Fetcher` is
`Callable[[str, Path, float], ResponseMetadata]` so tests can write controlled
bytes without mocking the acquisition logic.

- [ ] **Step 1: Test successful atomic acquisition before implementation**

```python
def test_acquire_source_writes_verified_bytes_atomically(tmp_path: Path) -> None:
    contract = SourceContract(
        source_id="sample",
        source_class="event",
        availability="approved",
        url="https://example.test/sample.json",
        local_path=PurePosixPath("data/raw/sample.json"),
        format="json",
        publisher="fixture",
        expected_prefix="{",
        units="not applicable",
        crs="not applicable",
        horizontal_datum="not applicable",
        vertical_datum="not applicable",
        coordinate_order="not applicable",
        temporal_semantics="not applicable",
        station_metadata="not applicable",
        reason="not applicable",
    )
    result = acquire_source(
        contract,
        tmp_path,
        fetcher=fixture_fetcher(b'{"ok":true}'),
    )
    assert result.status == "downloaded"
    assert result.bytes == 11
    assert result.sha256 == hashlib.sha256(b'{"ok":true}').hexdigest()
    assert (tmp_path / contract.local_path).read_bytes() == b'{"ok":true}'
```

Verify RED, implement only the typed dataclasses, streamed temporary-file write,
non-empty/signature check
(`payload.lstrip().startswith(contract.expected_prefix.encode("utf-8"))`),
SHA-256, and atomic `Path.replace`, then verify GREEN.

- [ ] **Step 2: Test idempotent cache reuse**

The test acquires once, calls again with an opener that raises if invoked, and
asserts `status == "cached"` with the same checksum. Implement checksum validation
of the existing file without reopening the network.

- [ ] **Step 3: Test immutable conflict handling**

Pre-create the target with unexpected bytes and assert the result is
`quarantined`, the original target bytes are unchanged, and the reason code is
`existing_checksum_conflict`.

- [ ] **Step 4: Test partial-source failure**

Run two contracts through `acquire_all`, make one opener raise `URLError`, and
assert one download plus one quarantine are returned in source-ID order. Implement
bounded retries only for transient URL/timeout failures and never abort sibling
sources.

- [ ] **Step 5: Test blocked contracts never access the network**

Assert a blocked contract yields `status == "blocked"`, retains its recorded
reason, and does not call the opener.

- [ ] **Step 6: Add the thin CLI and verify the subtask**

The CLI accepts `--config`, `--root`, `--run-tag`, and `--offline`; it calls the
module and exits nonzero only for invalid configuration or zero usable approved
assets. Run focused tests, Ruff, Pyright, and `--help`, then commit as
`feat(data): add atomic source acquisition`.

---

### Task 3: Live source bundle, checksums, and acquisition report

**Files:**
- Modify: `artifacts/provenance/source-manifest.csv`
- Modify: `context/ACQUISITION_REPORT.md`
- Modify: `context/TASKS.md`
- Create per run: `artifacts/logs/runs/<run-id>/meta.json`
- Create per run: `artifacts/logs/runs/<run-id>/config.json`
- Create per run: `artifacts/logs/runs/<run-id>/inputs.json`
- Create per run: `artifacts/logs/runs/<run-id>/outputs.json`
- Create per run: `artifacts/logs/runs/<run-id>/metrics.json`
- Create per run: `artifacts/logs/runs/<run-id>/notes.md`

**Interfaces:**
- Consumes: Task 2 CLI and accepted Task 1 contracts.
- Produces: immutable ignored raw files, tracked compact run evidence, and source
  manifest checksum/local-path updates for successful assets.

- [ ] **Step 1: Run the approved live bundle once**

Run: `uv run python scripts/acquire_tohoku.py --config config/tohoku-data-proof.toml --root . --run-tag initial`

Expected approved attempts: USGS event FDSN CSV, NCEI TTT metadata JSON and
GeoJSON, NCTR coefficient HTML, DART 21418/21413/46411/32401 text, and NOAA
CO-OPS Adak/Hilo/Crescent City/Pago Pago JSON. Expected blocked records are the
continuous NCTR field, Saipan series, and Valparaíso series.

- [ ] **Step 2: Re-run and prove idempotence**

Run the same command with `--run-tag initial-rerun`; compare each approved asset's
SHA-256 and byte count. Every second-run success must be `cached`, and no raw file
may change.

- [ ] **Step 3: Manually inspect representative identities**

Check the USGS event ID and coordinates, three TTT contour features and `HOURS`,
all four DART station files, and all available coastal metadata blocks against
source pages. Record observed values rather than a generic pass statement.

- [ ] **Step 4: Reconcile and commit T-002B**

Regenerate the acquisition report and run bundle, validate the manifest, obtain a
data-quality checker disposition, mark T-002B done, and commit as
`data: acquire and fingerprint Tohoku sources`. Raw files remain untracked.

---

### Task 4: Event, contour, and water-level normalization

**Files:**
- Create: `pipeline/normalize.py`
- Create: `scripts/build_tohoku_data.py`
- Create: `tests/test_normalize.py`
- Create: `tests/fixtures/normalize/usgs_event.csv`
- Create: `tests/fixtures/normalize/ttt_contours.geojson`
- Create: `tests/fixtures/normalize/dart_station.txt`
- Create: `tests/fixtures/normalize/coops_station.json`

**Interfaces:**
- Consumes: Task 3 raw inventory and checksummed raw files only.
- Produces:
  `normalize_event(path: Path, expected_id: str) -> EventRecord`,
  `normalize_ttt(path: Path) -> tuple[list[TTTContourRecord], list[RejectedRecord]]`,
  `normalize_dart(path: Path, station: StationRecord) -> tuple[list[ObservationRecord], list[RejectedRecord]]`,
  `normalize_coastal(path: Path, station: StationRecord) -> tuple[list[ObservationRecord], list[RejectedRecord]]`,
  and `build_tables(config_path: Path, inventory_path: Path, root: Path) -> BuildResult`.

The record dataclasses mirror the canonical grains in the approved spec.
`ObservationRecord` keeps `source_time`, `observed_at_utc`, `raw_value`,
`fitted_value`, `residual_value`, `units`, and `vertical_reference` separate.
`BuildResult` contains deterministic output paths, row counts, checksums, and
rejection counts.

- [ ] **Step 1: Test USGS event normalization**

Assert the exact one-row FDSN CSV schema, event ID, latitude-then-longitude/depth
field order, reviewed status, magnitude type, and ISO UTC timestamp. Reject a
missing required column, multiple rows, or wrong event ID.

- [ ] **Step 2: Test TTT contour normalization**

Assert one output row per `MultiLineString` part, numeric nonnegative `hours`,
EPSG:4326 longitude/latitude ranges, stable part IDs, and zero preserved as data.
Reject missing `HOURS`, empty parts, and coordinates outside the documented CRS;
flag rather than silently wrap antimeridian crossings.

- [ ] **Step 3: Test DART normalization**

Parse the documented eleven whitespace-separated columns. Assert calendar fields
produce UTC, Julian day agrees within source precision, raw/fitted/residual values
remain meters water column, and duplicate timestamps or malformed rows become
stable rejected records.

- [ ] **Step 4: Test NOAA CO-OPS normalization**

Assert station metadata matches the configured station ID and coordinates,
timestamps are interpreted as GMT/UTC from the request contract, values remain
meters relative to requested station datum, missing values are null rather than
zero, and API error payloads quarantine the asset.

- [ ] **Step 5: Add the thin deterministic build CLI**

Write sorted CSV tables for `event`, `ttt_contour`, `station`, `observation`, and
`rejected_record`, plus JSON schemas and an accounting summary. The CLI accepts
`--inventory`, `--config`, `--root`, and `--run-tag`; it never downloads.

- [ ] **Step 6: Verify the normalization core and commit**

Run every focused RED/GREEN cycle, then:

```bash
uv run pytest tests/test_normalize.py -q
uv run ruff check pipeline/normalize.py scripts/build_tohoku_data.py tests/test_normalize.py
uv run pyright
```

Commit as `feat(data): normalize Tohoku source records`.

---

### Task 5: Live data-quality build and requested-phase closure

**Files:**
- Modify: `context/DATA_QUALITY_REPORT.md`
- Modify: `context/DATA_CARD.md`
- Modify: `context/HANDOVER.md`
- Modify: `context/TASKS.md`
- Modify: `context/DECISIONS.md` only if a source disposition changes

**Interfaces:**
- Consumes: Task 4 deterministic builder and Task 3 checksummed inventory.
- Produces: two identical processed builds, quality/accounting evidence, and an
  explicit T-002C disposition while leaving T-002D pending.

- [ ] **Step 1: Build twice and compare**

Run the builder with separate run tags, then compare row counts and SHA-256 values
for every deterministic table/schema. A mismatch blocks completion.

- [ ] **Step 2: Profile the accepted grain**

For each table record row/column counts, keys, duplicate rates, null rates, time
ranges, coordinate ranges, contour-hour distribution, station coverage, cadence
segments, gaps, and rejected reason counts. Keep unavailable sources in coverage
denominators.

- [ ] **Step 3: Perform manual scientific QA**

Trace three contours, all four DART records, and each of the six coastal candidates
to raw or blocker evidence. Compare at least three normalized timestamps/values
with raw lines and record exact values in the report.

- [ ] **Step 4: Obtain checker disposition and close T-002C**

An independent reviewer audits identity, counts, units/time/datum handling,
determinism, and rejection visibility. Resolve material findings, mark T-002C done
or revise with the recorded reason, and keep T-002D pending.

- [ ] **Step 5: Run the full repository gate and commit**

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
uv run python -m pipeline.provenance artifacts/provenance/source-manifest.csv
npm run check
graphify update .
git diff --check
```

Record the fresh outputs in `context/HANDOVER.md` and commit as
`data: validate Tohoku analysis tables`.
