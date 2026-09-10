import csv
import json
from pathlib import Path

import pytest
from mlflow import MlflowClient

import pipeline.missingness as missingness_module
from pipeline.missingness import (
    ExpectedWindow,
    MissingnessError,
    profile_missingness,
    write_missingness_artifacts,
)
from scripts.profile_missingness import main as profile_main

OBSERVATION_COLUMNS = (
    "observation_id",
    "source_id",
    "station_id",
    "source_time",
    "observed_at_utc",
    "raw_value",
    "fitted_value",
    "residual_value",
    "source_extra",
    "units",
    "vertical_reference",
)
STATION_COLUMNS = (
    "station_id",
    "source_id",
    "station_type",
    "name",
    "latitude",
    "longitude",
    "availability",
    "units",
    "vertical_reference",
    "selection_role",
    "reason",
    "horizontal_datum",
    "coordinate_order",
    "time_basis",
)
REJECTION_COLUMNS = ("rejection_id", "source_id", "record_type", "reason_code", "detail")
TTT_COLUMNS = (
    "contour_id",
    "source_object_id",
    "hours",
    "coordinates",
    "crs",
    "coordinate_order",
    "longitude_boundary_precision",
    "crosses_antimeridian",
)


def _write_csv(path: Path, columns: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _stage_profile_inputs(root: Path) -> Path:
    processed = root / "processed"
    processed.mkdir()
    _write_csv(
        processed / "station.csv",
        STATION_COLUMNS,
        [
            {
                "station_id": "dart",
                "source_id": "dart-source",
                "station_type": "dart",
                "name": "DART fixture",
                "latitude": "0",
                "longitude": "0",
                "availability": "approved",
                "units": "m water column",
                "vertical_reference": "unknown",
                "selection_role": "fixture",
                "reason": "not applicable",
                "horizontal_datum": "unknown",
                "coordinate_order": "latitude, longitude",
                "time_basis": "UTC",
            },
            {
                "station_id": "coast",
                "source_id": "coastal-source",
                "station_type": "coastal",
                "name": "Coastal fixture",
                "latitude": "1",
                "longitude": "1",
                "availability": "approved",
                "units": "m",
                "vertical_reference": "MLLW",
                "selection_role": "fixture",
                "reason": "not applicable",
                "horizontal_datum": "unknown",
                "coordinate_order": "latitude, longitude",
                "time_basis": "UTC",
            },
        ],
    )
    _write_csv(
        processed / "observation.csv",
        OBSERVATION_COLUMNS,
        [
            {
                "observation_id": "dart-1",
                "source_id": "dart-source",
                "station_id": "dart",
                "source_time": "fixture",
                "observed_at_utc": "2011-03-11T00:00:00Z",
                "raw_value": "10",
                "fitted_value": "9",
                "residual_value": "1",
                "source_extra": "",
                "units": "m water column",
                "vertical_reference": "unknown",
            },
            {
                "observation_id": "coast-1",
                "source_id": "coastal-source",
                "station_id": "coast",
                "source_time": "fixture",
                "observed_at_utc": "2011-03-11T00:00:00Z",
                "raw_value": "0",
                "fitted_value": "",
                "residual_value": "",
                "source_extra": "",
                "units": "m",
                "vertical_reference": "MLLW",
            },
            {
                "observation_id": "coast-2",
                "source_id": "coastal-source",
                "station_id": "coast",
                "source_time": "fixture",
                "observed_at_utc": "2011-03-11T00:00:59Z",
                "raw_value": "2",
                "fitted_value": "",
                "residual_value": "",
                "source_extra": "",
                "units": "m",
                "vertical_reference": "MLLW",
            },
            {
                "observation_id": "coast-3",
                "source_id": "coastal-source",
                "station_id": "coast",
                "source_time": "fixture",
                "observed_at_utc": "2011-03-11T00:02:00Z",
                "raw_value": "",
                "fitted_value": "",
                "residual_value": "",
                "source_extra": "",
                "units": "m",
                "vertical_reference": "MLLW",
            },
        ],
    )
    _write_csv(
        processed / "rejected_record.csv",
        REJECTION_COLUMNS,
        [
            {
                "rejection_id": "dart-bad",
                "source_id": "dart-source",
                "record_type": "observation",
                "reason_code": "unexpected_sentinel",
                "detail": "fixture",
            },
            {
                "rejection_id": "coast-bad",
                "source_id": "coastal-source",
                "record_type": "observation",
                "reason_code": "duplicate_timestamp",
                "detail": "fixture",
            },
            {
                "rejection_id": "field-blocked",
                "source_id": "blocked-field",
                "record_type": "source_asset",
                "reason_code": "blocked_source",
                "detail": "fixture",
            },
        ],
    )
    _write_csv(
        processed / "ttt_contour.csv",
        TTT_COLUMNS,
        [
            {
                "contour_id": "one",
                "source_object_id": "1",
                "hours": "1",
                "coordinates": "[]",
                "crs": "EPSG:4326",
                "coordinate_order": "longitude, latitude",
                "longitude_boundary_precision": "false",
                "crosses_antimeridian": "false",
            },
            {
                "contour_id": "three",
                "source_object_id": "3",
                "hours": "3",
                "coordinates": "[]",
                "crs": "EPSG:4326",
                "coordinate_order": "longitude, latitude",
                "longitude_boundary_precision": "false",
                "crosses_antimeridian": "false",
            },
        ],
    )
    (processed / "accounting.json").write_text(
        json.dumps(
            {
                "source_coverage": {"approved": 2, "blocked": 1, "total": 3},
                "source_outcomes": [
                    {
                        "source_id": "dart-source",
                        "input_count": 2,
                        "accepted_count": 1,
                        "rejected_count": 1,
                    },
                    {
                        "source_id": "coastal-source",
                        "input_count": 4,
                        "accepted_count": 3,
                        "rejected_count": 1,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return processed


def _write_profile_config(path: Path) -> None:
    path.write_text(
        """profile_version = "fixture"

[windows.coast]
station_id = "coast"
name = "Coastal fixture"
start_utc = "2011-03-11T00:00:00Z"
end_utc_exclusive = "2011-03-11T00:03:00Z"
cadence_seconds = 60
""",
        encoding="utf-8",
    )


def test_profile_separates_structural_nulls_from_measurement_and_grid_gaps(
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

    profile = profile_missingness(processed, (window,))

    assert profile.observation_rows == 4
    assert (profile.raw_null_rows, profile.raw_null_percent) == (1, 25.0)
    assert (profile.structural_not_applicable_rows, profile.structural_not_applicable_percent) == (
        3,
        75.0,
    )
    assert profile.rejection_reason_counts == {
        "blocked_source": 1,
        "duplicate_timestamp": 1,
        "unexpected_sentinel": 1,
    }
    assert (profile.approved_source_assets, profile.blocked_source_assets) == (2, 1)
    assert profile.dart_input_rows == 2
    assert profile.dart_sentinel_rows == 1
    assert profile.ttt_missing_hour_labels == (2,)
    assert profile.unknown_horizontal_datum_stations == 2
    assert profile.unknown_vertical_reference_stations == 1
    assert profile.unexpected_dart_modeled_field_null_rows == 0

    coast = profile.coastal_windows[0]
    assert coast.accepted_rows == 3
    assert coast.expected_positions == 3
    assert coast.exact_grid_rows == 2
    assert coast.off_grid_rows == 1
    assert coast.source_blank_rows == 1
    assert coast.absent_expected_positions == 1
    assert coast.strict_unavailable_positions == 2
    assert coast.sample_density_unavailable_positions == 1
    assert coast.strict_coverage_percent == 33.3333


def test_expected_window_rejects_a_duration_that_is_not_divisible_by_cadence() -> None:
    with pytest.raises(MissingnessError, match="whole number of cadence intervals"):
        ExpectedWindow(
            station_id="coast",
            name="Coastal fixture",
            start_utc="2011-03-11T00:00:00Z",
            end_utc_exclusive="2011-03-11T00:02:30Z",
            cadence_seconds=60,
        )


def test_load_expected_windows_reads_the_auditable_grid_contract(tmp_path: Path) -> None:
    config_path = tmp_path / "missingness.toml"
    _write_profile_config(config_path)

    assert hasattr(missingness_module, "load_expected_windows")
    windows = missingness_module.load_expected_windows(config_path)

    assert windows == (
        ExpectedWindow(
            station_id="coast",
            name="Coastal fixture",
            start_utc="2011-03-11T00:00:00Z",
            end_utc_exclusive="2011-03-11T00:03:00Z",
            cadence_seconds=60,
        ),
    )


def test_writer_preserves_machine_readable_counts_and_human_interpretation(
    tmp_path: Path,
) -> None:
    processed = _stage_profile_inputs(tmp_path)
    profile = profile_missingness(
        processed,
        (
            ExpectedWindow(
                station_id="coast",
                name="Coastal fixture",
                start_utc="2011-03-11T00:00:00Z",
                end_utc_exclusive="2011-03-11T00:03:00Z",
                cadence_seconds=60,
            ),
        ),
    )
    artifact_dir = tmp_path / "artifacts"
    report_path = tmp_path / "EDA_REPORT.md"

    paths = write_missingness_artifacts(
        profile,
        artifact_dir=artifact_dir,
        report_path=report_path,
        run_id="fixture-run",
        git_sha="abc1234",
        command="python scripts/profile_missingness.py",
    )

    summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
    assert summary["raw_null_rows"] == 1
    assert summary["coastal_windows"][0]["strict_unavailable_positions"] == 2
    assert "Pooled MCAR is not supported" in report_path.read_text(encoding="utf-8")
    with paths["coastal_csv"].open(newline="", encoding="utf-8") as source:
        assert list(csv.DictReader(source))[0]["station_id"] == "coast"


def test_cli_writes_portable_run_evidence_without_hiding_the_blocked_asset(
    tmp_path: Path,
) -> None:
    processed = _stage_profile_inputs(tmp_path)
    config_path = tmp_path / "missingness.toml"
    _write_profile_config(config_path)
    artifact_dir = tmp_path / "curated"
    run_dir = tmp_path / "run"
    report_path = tmp_path / "EDA_REPORT.md"
    tracking_dir = tmp_path / "mlflow"

    result = profile_main(
        [
            "--processed-dir",
            str(processed),
            "--config",
            str(config_path),
            "--artifact-dir",
            str(artifact_dir),
            "--run-dir",
            str(run_dir),
            "--report",
            str(report_path),
            "--run-id",
            "fixture-run",
            "--git-sha",
            "abc1234",
            "--mlflow-dir",
            str(tracking_dir),
            "--mlflow-experiment",
            "fixture-missingness",
        ]
    )

    assert result == 0
    assert {path.name for path in run_dir.iterdir()} == {
        "config.json",
        "inputs.json",
        "meta.json",
        "metrics.json",
        "notes.md",
        "outputs.json",
    }
    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["blocked_source_assets"] == 1
    assert metrics["coastal_strict_unavailable_percent"] == 66.6667
    client = MlflowClient(tracking_uri=tracking_dir.resolve().as_uri())
    experiment = client.get_experiment_by_name("fixture-missingness")
    assert experiment is not None
    runs = client.search_runs([experiment.experiment_id])
    assert len(runs) == 1
    assert runs[0].data.metrics["raw_null_percent"] == 25.0
    assert len(runs[0].data.params["input_fingerprint_sha256"]) == 64
    assert runs[0].data.tags["portable_run_id"] == "fixture-run"
    assert runs[0].data.tags["station_selection"] == "frozen"
    report = report_path.read_text(encoding="utf-8")
    assert "## Input and output fingerprints" in report
    assert "`accounting.json`" in report
    assert "`missingness-summary.json`" in report
    assert len(json.loads((run_dir / "inputs.json").read_text())[0]["sha256"]) == 64
