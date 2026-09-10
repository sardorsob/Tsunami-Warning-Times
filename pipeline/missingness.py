"""Profile missingness without confusing nulls, absent timestamps, and inapplicable fields."""

from __future__ import annotations

import csv
import json
import tomllib
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import cast


class MissingnessError(ValueError):
    """Raised when missingness cannot be measured without guessing."""


def _parse_utc(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise MissingnessError(f"invalid UTC timestamp {value!r}") from error
    if not value.endswith("Z") or parsed.utcoffset() != UTC.utcoffset(parsed):
        raise MissingnessError(f"timestamp is not explicit UTC: {value!r}")
    return parsed


def _percent(count: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(100 * count / denominator, 4)


@dataclass(frozen=True, slots=True)
class ExpectedWindow:
    """One source-supported regular grid used only for completeness accounting."""

    station_id: str
    name: str
    start_utc: str
    end_utc_exclusive: str
    cadence_seconds: int

    def __post_init__(self) -> None:
        start = _parse_utc(self.start_utc)
        end = _parse_utc(self.end_utc_exclusive)
        if self.cadence_seconds <= 0:
            raise MissingnessError("cadence_seconds must be positive")
        duration_seconds = int((end - start).total_seconds())
        if duration_seconds <= 0:
            raise MissingnessError("expected window end must be after its start")
        if duration_seconds % self.cadence_seconds:
            raise MissingnessError(
                "expected window must contain a whole number of cadence intervals"
            )


@dataclass(frozen=True, slots=True)
class CoastalWindowProfile:
    """Completeness measures for one regular coastal-gauge window."""

    station_id: str
    name: str
    start_utc: str
    end_utc_exclusive: str
    cadence_seconds: int
    expected_positions: int
    accepted_rows: int
    exact_grid_rows: int
    off_grid_rows: int
    source_blank_rows: int
    absent_expected_positions: int
    strict_unavailable_positions: int
    sample_density_unavailable_positions: int
    strict_coverage_percent: float
    sample_density_coverage_percent: float
    longest_observed_gap_seconds: int
    first_observed_utc: str
    last_observed_utc: str


@dataclass(frozen=True, slots=True)
class DartCadenceProfile:
    """Observed DART cadence evidence without imposing a false regular grid."""

    station_id: str
    accepted_rows: int
    raw_null_rows: int
    interval_seconds: tuple[int, ...]
    intervals_over_900_seconds: int
    maximum_interval_seconds: int


@dataclass(frozen=True, slots=True)
class MissingnessProfile:
    """Dataset-level and source-segmented missingness evidence."""

    observation_rows: int
    raw_null_rows: int
    raw_null_percent: float
    structural_not_applicable_rows: int
    structural_not_applicable_percent: float
    unexpected_dart_modeled_field_null_rows: int
    coastal_observation_rows: int
    coastal_raw_null_rows: int
    coastal_raw_null_percent: float
    coastal_expected_positions: int
    coastal_strict_unavailable_positions: int
    coastal_strict_unavailable_percent: float
    coastal_sample_density_unavailable_positions: int
    coastal_sample_density_unavailable_percent: float
    approved_source_assets: int
    blocked_source_assets: int
    total_source_assets: int
    blocked_source_asset_percent: float
    rejected_observation_rows: int
    rejection_reason_counts: dict[str, int]
    dart_input_rows: int
    dart_sentinel_rows: int
    dart_sentinel_percent: float
    ttt_available_hour_labels: tuple[int, ...]
    ttt_missing_hour_labels: tuple[int, ...]
    unknown_horizontal_datum_stations: int
    unknown_vertical_reference_stations: int
    total_stations: int
    coastal_windows: tuple[CoastalWindowProfile, ...]
    dart_cadence: tuple[DartCadenceProfile, ...]


def load_expected_windows(path: Path) -> tuple[ExpectedWindow, ...]:
    """Load source-supported regular-grid contracts from TOML."""
    try:
        document = cast(dict[str, object], tomllib.loads(path.read_text(encoding="utf-8")))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise MissingnessError(f"could not read missingness config {path}: {error}") from error
    windows_value = document.get("windows")
    if not isinstance(windows_value, dict) or not windows_value:
        raise MissingnessError("missingness config requires non-empty [windows] tables")
    windows: list[ExpectedWindow] = []
    for key, values_value in sorted(cast(dict[str, object], windows_value).items()):
        if not isinstance(values_value, dict):
            raise MissingnessError(f"window {key!r} must be a TOML table")
        values = cast(dict[str, object], values_value)
        text_fields = ("station_id", "name", "start_utc", "end_utc_exclusive")
        if not all(isinstance(values.get(field), str) for field in text_fields):
            raise MissingnessError(f"window {key!r} has missing text fields")
        cadence = values.get("cadence_seconds")
        if not isinstance(cadence, int):
            raise MissingnessError(f"window {key!r} cadence_seconds must be an integer")
        windows.append(
            ExpectedWindow(
                station_id=cast(str, values["station_id"]),
                name=cast(str, values["name"]),
                start_utc=cast(str, values["start_utc"]),
                end_utc_exclusive=cast(str, values["end_utc_exclusive"]),
                cadence_seconds=cadence,
            )
        )
    station_ids = {window.station_id for window in windows}
    if len(station_ids) != len(windows):
        raise MissingnessError("missingness config contains duplicate station IDs")
    return tuple(windows)


def _read_csv(path: Path, required_columns: set[str]) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            fieldnames = set(reader.fieldnames or ())
            missing_columns = required_columns - fieldnames
            if missing_columns:
                raise MissingnessError(
                    f"{path} is missing columns: {', '.join(sorted(missing_columns))}"
                )
            rows: list[dict[str, str]] = []
            for row_number, raw_row in enumerate(reader, start=2):
                if any(key is None or value is None for key, value in raw_row.items()):
                    raise MissingnessError(f"{path}:{row_number} is not a rectangular CSV row")
                rows.append(cast(dict[str, str], raw_row))
            return rows
    except OSError as error:
        raise MissingnessError(f"could not read {path}: {error}") from error


def _load_accounting(path: Path) -> dict[str, object]:
    try:
        value: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise MissingnessError(f"could not read accounting file {path}: {error}") from error
    if not isinstance(value, dict):
        raise MissingnessError("accounting file must contain a JSON object")
    return cast(dict[str, object], value)


def _profile_coastal_window(
    rows: list[dict[str, str]], window: ExpectedWindow
) -> CoastalWindowProfile:
    start = _parse_utc(window.start_utc)
    end = _parse_utc(window.end_utc_exclusive)
    expected_positions = int((end - start).total_seconds()) // window.cadence_seconds
    selected: list[tuple[datetime, dict[str, str]]] = []
    for row in rows:
        observed_at = _parse_utc(row["observed_at_utc"])
        if start <= observed_at < end:
            selected.append((observed_at, row))
    selected.sort(key=lambda item: item[0])

    exact_offsets: set[int] = set()
    exact_blank_rows = 0
    for observed_at, row in selected:
        offset_microseconds = int((observed_at - start).total_seconds() * 1_000_000)
        cadence_microseconds = window.cadence_seconds * 1_000_000
        if offset_microseconds % cadence_microseconds == 0:
            exact_offsets.add(offset_microseconds // cadence_microseconds)
            exact_blank_rows += not row["raw_value"].strip()
    exact_grid_rows = len(exact_offsets)
    absent_expected_positions = expected_positions - exact_grid_rows
    source_blank_rows = sum(not row["raw_value"].strip() for _, row in selected)
    strict_unavailable = absent_expected_positions + exact_blank_rows
    sample_usable_rows = sum(bool(row["raw_value"].strip()) for _, row in selected)
    sample_density_unavailable = max(0, expected_positions - sample_usable_rows)
    intervals = [
        int((current[0] - previous[0]).total_seconds())
        for previous, current in zip(selected, selected[1:], strict=False)
    ]

    return CoastalWindowProfile(
        station_id=window.station_id,
        name=window.name,
        start_utc=window.start_utc,
        end_utc_exclusive=window.end_utc_exclusive,
        cadence_seconds=window.cadence_seconds,
        expected_positions=expected_positions,
        accepted_rows=len(selected),
        exact_grid_rows=exact_grid_rows,
        off_grid_rows=len(selected) - exact_grid_rows,
        source_blank_rows=source_blank_rows,
        absent_expected_positions=absent_expected_positions,
        strict_unavailable_positions=strict_unavailable,
        sample_density_unavailable_positions=sample_density_unavailable,
        strict_coverage_percent=_percent(
            expected_positions - strict_unavailable, expected_positions
        ),
        sample_density_coverage_percent=_percent(
            expected_positions - sample_density_unavailable, expected_positions
        ),
        longest_observed_gap_seconds=max(intervals, default=0),
        first_observed_utc=(
            selected[0][0].isoformat().replace("+00:00", "Z") if selected else "unknown"
        ),
        last_observed_utc=(
            selected[-1][0].isoformat().replace("+00:00", "Z") if selected else "unknown"
        ),
    )


def _profile_dart(
    observations_by_station: dict[str, list[dict[str, str]]], dart_station_ids: set[str]
) -> tuple[DartCadenceProfile, ...]:
    profiles: list[DartCadenceProfile] = []
    for station_id in sorted(dart_station_ids):
        rows = observations_by_station.get(station_id, [])
        timestamps = sorted(_parse_utc(row["observed_at_utc"]) for row in rows)
        intervals = [
            int((current - previous).total_seconds())
            for previous, current in zip(timestamps, timestamps[1:], strict=False)
        ]
        profiles.append(
            DartCadenceProfile(
                station_id=station_id,
                accepted_rows=len(rows),
                raw_null_rows=sum(not row["raw_value"].strip() for row in rows),
                interval_seconds=tuple(sorted(set(intervals))),
                intervals_over_900_seconds=sum(interval > 900 for interval in intervals),
                maximum_interval_seconds=max(intervals, default=0),
            )
        )
    return tuple(profiles)


def profile_missingness(
    processed_dir: Path, expected_windows: tuple[ExpectedWindow, ...]
) -> MissingnessProfile:
    """Measure distinct missingness mechanisms in normalized Tōhoku outputs."""
    station_rows = _read_csv(
        processed_dir / "station.csv",
        {"station_id", "source_id", "station_type", "horizontal_datum", "vertical_reference"},
    )
    observation_rows = _read_csv(
        processed_dir / "observation.csv",
        {
            "observation_id",
            "source_id",
            "station_id",
            "observed_at_utc",
            "raw_value",
            "fitted_value",
            "residual_value",
        },
    )
    rejected_rows = _read_csv(
        processed_dir / "rejected_record.csv",
        {"source_id", "record_type", "reason_code"},
    )
    contour_rows = _read_csv(processed_dir / "ttt_contour.csv", {"hours"})
    accounting = _load_accounting(processed_dir / "accounting.json")

    stations_by_id = {row["station_id"]: row for row in station_rows}
    if len(stations_by_id) != len(station_rows):
        raise MissingnessError("station.csv contains duplicate station IDs")
    observations_by_station: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen_station_times: set[tuple[str, str]] = set()
    for row in observation_rows:
        station_id = row["station_id"]
        if station_id not in stations_by_id:
            raise MissingnessError(f"observation references unknown station {station_id!r}")
        station_time = (station_id, row["observed_at_utc"])
        if station_time in seen_station_times:
            raise MissingnessError(f"duplicate station/timestamp pair {station_time!r}")
        seen_station_times.add(station_time)
        _parse_utc(row["observed_at_utc"])
        observations_by_station[station_id].append(row)

    coastal_station_ids = {
        station_id for station_id, row in stations_by_id.items() if row["station_type"] == "coastal"
    }
    dart_station_ids = {
        station_id for station_id, row in stations_by_id.items() if row["station_type"] == "dart"
    }
    configured_window_ids = {window.station_id for window in expected_windows}
    if configured_window_ids != coastal_station_ids:
        raise MissingnessError(
            "expected-window station IDs must exactly match normalized coastal station IDs"
        )

    coastal_rows = [row for row in observation_rows if row["station_id"] in coastal_station_ids]
    structural_rows = sum(
        not row["fitted_value"].strip() and not row["residual_value"].strip()
        for row in coastal_rows
    )
    if structural_rows != len(coastal_rows):
        raise MissingnessError("coastal fitted/residual fields are not consistently inapplicable")
    unexpected_dart_nulls = sum(
        not row["fitted_value"].strip() or not row["residual_value"].strip()
        for row in observation_rows
        if row["station_id"] in dart_station_ids
    )

    coastal_profiles = tuple(
        _profile_coastal_window(observations_by_station[window.station_id], window)
        for window in sorted(expected_windows, key=lambda item: item.station_id)
    )
    coastal_expected = sum(profile.expected_positions for profile in coastal_profiles)
    coastal_strict_unavailable = sum(
        profile.strict_unavailable_positions for profile in coastal_profiles
    )
    coastal_density_unavailable = sum(
        profile.sample_density_unavailable_positions for profile in coastal_profiles
    )

    rejection_counts = Counter(row["reason_code"] for row in rejected_rows)
    dart_sources = {stations_by_id[station_id]["source_id"] for station_id in dart_station_ids}
    dart_sentinel_rows = sum(
        row["reason_code"] == "unexpected_sentinel" and row["source_id"] in dart_sources
        for row in rejected_rows
    )
    source_outcomes_value = accounting.get("source_outcomes")
    if not isinstance(source_outcomes_value, list):
        raise MissingnessError("accounting source_outcomes must be a list")
    dart_input_rows = 0
    for outcome_value in cast(list[object], source_outcomes_value):
        if not isinstance(outcome_value, dict):
            raise MissingnessError("accounting source outcome must be an object")
        outcome = cast(dict[str, object], outcome_value)
        if outcome.get("source_id") in dart_sources:
            input_count = outcome.get("input_count")
            if not isinstance(input_count, int):
                raise MissingnessError("DART source outcome is missing integer input_count")
            dart_input_rows += input_count

    coverage_value = accounting.get("source_coverage")
    if not isinstance(coverage_value, dict):
        raise MissingnessError("accounting source_coverage must be an object")
    coverage = cast(dict[str, object], coverage_value)
    approved = coverage.get("approved")
    blocked = coverage.get("blocked")
    total = coverage.get("total")
    if not all(isinstance(value, int) for value in (approved, blocked, total)):
        raise MissingnessError("source coverage counts must be integers")
    approved_count = cast(int, approved)
    blocked_count = cast(int, blocked)
    total_count = cast(int, total)
    if approved_count + blocked_count != total_count:
        raise MissingnessError("source coverage counts do not reconcile")

    available_hours = tuple(sorted({int(float(row["hours"])) for row in contour_rows}))
    if any(float(row["hours"]) != int(float(row["hours"])) for row in contour_rows):
        raise MissingnessError("TTT hour labels must be whole hours for sequence-gap profiling")
    missing_hours = tuple(
        hour
        for hour in range(1, max(available_hours, default=0) + 1)
        if hour not in available_hours
    )
    raw_null_rows = sum(not row["raw_value"].strip() for row in observation_rows)
    coastal_raw_null_rows = sum(not row["raw_value"].strip() for row in coastal_rows)

    return MissingnessProfile(
        observation_rows=len(observation_rows),
        raw_null_rows=raw_null_rows,
        raw_null_percent=_percent(raw_null_rows, len(observation_rows)),
        structural_not_applicable_rows=structural_rows,
        structural_not_applicable_percent=_percent(structural_rows, len(observation_rows)),
        unexpected_dart_modeled_field_null_rows=unexpected_dart_nulls,
        coastal_observation_rows=len(coastal_rows),
        coastal_raw_null_rows=coastal_raw_null_rows,
        coastal_raw_null_percent=_percent(coastal_raw_null_rows, len(coastal_rows)),
        coastal_expected_positions=coastal_expected,
        coastal_strict_unavailable_positions=coastal_strict_unavailable,
        coastal_strict_unavailable_percent=_percent(coastal_strict_unavailable, coastal_expected),
        coastal_sample_density_unavailable_positions=coastal_density_unavailable,
        coastal_sample_density_unavailable_percent=_percent(
            coastal_density_unavailable, coastal_expected
        ),
        approved_source_assets=approved_count,
        blocked_source_assets=blocked_count,
        total_source_assets=total_count,
        blocked_source_asset_percent=_percent(blocked_count, total_count),
        rejected_observation_rows=sum(row["record_type"] == "observation" for row in rejected_rows),
        rejection_reason_counts=dict(sorted(rejection_counts.items())),
        dart_input_rows=dart_input_rows,
        dart_sentinel_rows=dart_sentinel_rows,
        dart_sentinel_percent=_percent(dart_sentinel_rows, dart_input_rows),
        ttt_available_hour_labels=available_hours,
        ttt_missing_hour_labels=missing_hours,
        unknown_horizontal_datum_stations=sum(
            row["horizontal_datum"].strip().casefold() == "unknown" for row in station_rows
        ),
        unknown_vertical_reference_stations=sum(
            row["vertical_reference"].strip().casefold() == "unknown" for row in station_rows
        ),
        total_stations=len(station_rows),
        coastal_windows=coastal_profiles,
        dart_cadence=_profile_dart(observations_by_station, dart_station_ids),
    )


def _write_csv_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise MissingnessError(f"refusing to write empty table {path}")
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=tuple(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _mechanism_rows(profile: MissingnessProfile) -> list[dict[str, object]]:
    return [
        {
            "mechanism": "source_blank_value",
            "count": profile.raw_null_rows,
            "denominator": profile.observation_rows,
            "percent": profile.raw_null_percent,
            "interpretation": "upstream value missing at a retained timestamp; exact cause unknown",
        },
        {
            "mechanism": "structural_not_applicable",
            "count": profile.structural_not_applicable_rows,
            "denominator": profile.observation_rows,
            "percent": profile.structural_not_applicable_percent,
            "interpretation": "coastal sources do not publish DART fitted/residual fields",
        },
        {
            "mechanism": "coastal_strict_grid_unavailable",
            "count": profile.coastal_strict_unavailable_positions,
            "denominator": profile.coastal_expected_positions,
            "percent": profile.coastal_strict_unavailable_percent,
            "interpretation": "expected timestamp absent or exact-grid value blank",
        },
        {
            "mechanism": "dart_sentinel_quarantine",
            "count": profile.dart_sentinel_rows,
            "denominator": profile.dart_input_rows,
            "percent": profile.dart_sentinel_percent,
            "interpretation": "ambiguous 9999 measurement row deliberately excluded",
        },
        {
            "mechanism": "source_asset_unavailable",
            "count": profile.blocked_source_assets,
            "denominator": profile.total_source_assets,
            "percent": profile.blocked_source_asset_percent,
            "interpretation": "whole contracted asset unavailable; not row-level missingness",
        },
    ]


def render_missingness_report(
    profile: MissingnessProfile, *, run_id: str, git_sha: str, command: str
) -> str:
    """Render the canonical Markdown explanation from calculated evidence."""
    coastal_lines = [
        "| Station | Accepted | Expected | Source blanks | Absent timestamps | Off-grid | "
        "Strict unavailable | Strict coverage | Longest observed gap |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for station in profile.coastal_windows:
        coastal_lines.append(
            f"| {station.name} | {station.accepted_rows:,} | {station.expected_positions:,} | "
            f"{station.source_blank_rows:,} | {station.absent_expected_positions:,} | "
            f"{station.off_grid_rows:,} | {station.strict_unavailable_positions:,} | "
            f"{station.strict_coverage_percent:.4f}% | "
            f"{station.longest_observed_gap_seconds:,} s |"
        )
    mechanism_lines = [
        "| Mechanism | Count | Denominator | Rate | Interpretation |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in _mechanism_rows(profile):
        mechanism_lines.append(
            f"| `{row['mechanism']}` | {int(cast(int, row['count'])):,} | "
            f"{int(cast(int, row['denominator'])):,} | "
            f"{float(cast(float, row['percent'])):.4f}% | {row['interpretation']} |"
        )
    dart_lines = [
        "| DART station | Accepted | Observed intervals (s) | >900 s | Maximum interval |",
        "| --- | ---: | --- | ---: | ---: |",
    ]
    for station in profile.dart_cadence:
        intervals = ", ".join(str(value) for value in station.interval_seconds)
        dart_lines.append(
            f"| {station.station_id} | {station.accepted_rows:,} | {intervals} | "
            f"{station.intervals_over_900_seconds:,} | {station.maximum_interval_seconds:,} s |"
        )
    missing_hours = ", ".join(str(value) for value in profile.ttt_missing_hour_labels) or "none"
    return f"""# Tōhoku Missingness EDA

## Run and scope

- Run ID: `{run_id}`
- Git SHA: `{git_sha}`
- Command: `{command}`
- Scope: the first, missingness-focused slice of T-002D; no arrival pick, model
  residual, or station promotion decision is made here.

The accepted table contains **{profile.observation_rows:,} station samples**.
There are **{profile.raw_null_rows:,} missing raw values
({profile.raw_null_percent:.4f}%)**, but that pooled cell rate hides missing
timestamps and strong station concentration. The six coastal windows have
**{profile.coastal_strict_unavailable_positions:,} unavailable exact-minute
positions out of {profile.coastal_expected_positions:,}
({profile.coastal_strict_unavailable_percent:.4f}%)**. A sample-density view,
which allows valid off-grid observations to count without snapping them to a
minute, gives {profile.coastal_sample_density_unavailable_percent:.4f}%
unavailable.

## Checks performed

- separated blank raw measurements from absent expected timestamps;
- separated source missingness from structurally inapplicable columns;
- retained zero as a numeric observation;
- measured exact-grid and sample-density coastal coverage separately;
- summarized DART cadence without imposing a false uniform grid;
- counted explicit source-record quarantine and whole-asset unavailability;
- exposed unknown datum metadata separately from missing observations; and
- inspected the TTT hour-label sequence without assuming absent labels were
  intended publisher outputs.

## Coastal completeness

{chr(10).join(coastal_lines)}

Saipan's off-grid rows are valid source observations, not errors. They remain at
their original timestamps. Pago Pago and Saipan are the material continuity
risks; the other four coastal series have high requested-window coverage.

## Missingness mechanisms

{chr(10).join(mechanism_lines)}

The **{profile.structural_not_applicable_rows:,}** coastal rows with empty
`fitted_value` and `residual_value` are not missing observations: those
DART-specific quantities do not exist in the coastal sources. They must not be
imputed. All DART rows retained for analysis have populated raw, fitted, and
residual fields; unexpected retained DART modeled-field null rows:
**{profile.unexpected_dart_modeled_field_null_rows:,}**.

## DART cadence

{chr(10).join(dart_lines)}

DART reporting changes among source-supported cadences, so cadence transitions
are sampling-by-design until evidence shows otherwise. Intervals over 900
seconds remain follow-up gaps rather than being silently treated as ordinary
cadence.

## Statistical interpretation

**Pooled MCAR is not supported.** Missingness is strongly concentrated by
station and contiguous time window. Some analyses may assume MAR after
conditioning on station, time, source, and reporting mode, but the current data
do not prove that assumption. MNAR cannot be ruled out because an outage could
be related to unobserved sea conditions. Distinguishing MAR from MNAR requires
publisher telemetry, maintenance, or quality-control logs that are not present
in this bundle.

This is not primarily century-scale technology missingness. The 2011 sources
already recorded minute- and second-scale values. The observed patterns are
more consistent with localized source, telemetry, QC, or archival interruption,
but the exact causes remain unknown unless publisher evidence resolves them.

## Other incompleteness

- Source assets: {profile.approved_source_assets} approved and
  {profile.blocked_source_assets} blocked out of {profile.total_source_assets};
  the blocked NCTR continuous field is asset-level unavailability, not a row
  null rate.
- Station metadata: {profile.unknown_horizontal_datum_stations} of
  {profile.total_stations} horizontal datums and
  {profile.unknown_vertical_reference_stations} of {profile.total_stations}
  vertical references remain explicitly `unknown`.
- TTT contours: source hour labels {missing_hours} are absent inside the
  1-through-{max(profile.ttt_available_hour_labels, default=0)} sequence. That
  is an upstream sequence gap with unknown intent, not proven local data loss.

## Adaptive EDA decision ledger

- **Pooled null rate hides absent rows:** reconstruct source-supported coastal
  grids. This check now belongs in the fixed core profile.
- **Pago Pago and Saipan dominate unavailability:** map their gap blocks and
  test arrival-pick sensitivity without interpolation before promotion.
- **Saipan contains valid `:59` timestamps:** keep strict-grid and
  sample-density coverage separate; preserve source time rather than snapping.
- **DART cadence is mixed by source design:** inspect intervals above documented
  cadence before labeling gaps; long intervals remain open checks.
- **Outage metadata is absent:** seek publisher telemetry/QC evidence if causal
  classification affects conclusions; MAR/MNAR remain unresolved.

## Limitations, takeaways, and next steps

Tests and deterministic calculations establish where missingness appears and
whether it came from local filtering. They do not establish the upstream causal
mechanism. The pipeline introduced no imputation and keeps rejected rows and the
blocked asset visible.

Next, T-002D should visualize gap blocks, inspect DART intervals over 900
seconds, define pre-arrival completeness gates, and run arrival-pick sensitivity
with an explicit no-interpolation baseline. Station inclusion remains frozen
until those checks are reviewed.
"""


def write_missingness_artifacts(
    profile: MissingnessProfile,
    *,
    artifact_dir: Path,
    report_path: Path,
    run_id: str,
    git_sha: str,
    command: str,
) -> dict[str, Path]:
    """Write deterministic JSON/CSV evidence and its canonical Markdown report."""
    artifact_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path = artifact_dir / "missingness-summary.json"
    coastal_path = artifact_dir / "coastal-missingness.csv"
    mechanisms_path = artifact_dir / "missingness-mechanisms.csv"
    summary_path.write_text(
        json.dumps(asdict(profile), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_csv_rows(coastal_path, [asdict(row) for row in profile.coastal_windows])
    _write_csv_rows(mechanisms_path, _mechanism_rows(profile))
    report_path.write_text(
        render_missingness_report(profile, run_id=run_id, git_sha=git_sha, command=command),
        encoding="utf-8",
    )
    return {
        "summary": summary_path,
        "coastal_csv": coastal_path,
        "mechanisms_csv": mechanisms_path,
        "report": report_path,
    }
