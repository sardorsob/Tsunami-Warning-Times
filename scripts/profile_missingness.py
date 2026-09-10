"""Profile Tōhoku missingness and write inspectable EDA evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections.abc import Sequence
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

import mlflow

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.missingness import (  # noqa: E402
    MissingnessError,
    load_expected_windows,
    profile_missingness,
    write_missingness_artifacts,
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _append_fingerprints(
    report_path: Path,
    *,
    input_records: list[dict[str, str]],
    artifact_paths: dict[str, Path],
) -> None:
    """Append non-circular file fingerprints to the canonical report."""
    lines = [
        "",
        "## Input and output fingerprints",
        "",
        "The portable run bundle records these same fingerprints as JSON. The",
        "source manifest remains authoritative for the 18 contracted source assets.",
        "",
        "### Normalized inputs",
        "",
        "| File | SHA-256 |",
        "| --- | --- |",
    ]
    lines.extend(
        f"| `{Path(record['path']).name}` | `{record['sha256']}` |"
        for record in input_records
    )
    lines.extend(
        [
            "",
            "### Generated machine-readable outputs",
            "",
            "| File | SHA-256 |",
            "| --- | --- |",
        ]
    )
    lines.extend(
        f"| `{path.name}` | `{_sha256(path)}` |"
        for name, path in sorted(artifact_paths.items())
        if name != "report"
    )
    report_path.write_text(
        report_path.read_text(encoding="utf-8") + "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def _command(args: argparse.Namespace) -> str:
    values = (
        ("--processed-dir", args.processed_dir),
        ("--config", args.config),
        ("--artifact-dir", args.artifact_dir),
        ("--run-dir", args.run_dir),
        ("--report", args.report),
        ("--run-id", args.run_id),
        ("--git-sha", args.git_sha),
        ("--working-tree", args.working_tree),
        ("--mlflow-dir", args.mlflow_dir),
        ("--mlflow-experiment", args.mlflow_experiment),
    )
    parts = ["uv run python scripts/profile_missingness.py"]
    parts.extend(
        f"{flag} {_display_path(value) if isinstance(value, Path) else value}"
        for flag, value in values
    )
    return " ".join(parts)


def _record_mlflow(
    *,
    profile_metrics: dict[str, int | float],
    artifact_paths: dict[str, Path],
    tracking_dir: Path,
    experiment_name: str,
    portable_run_id: str,
    portable_run_dir: Path,
    git_sha: str,
    processed_dir: Path,
    input_fingerprint_sha256: str,
) -> str:
    """Record the EDA slice in the project-local MLflow file store."""
    tracking_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")
    os.environ.setdefault("MLFLOW_DISABLE_AGENT_HINT", "true")
    mlflow.set_tracking_uri(tracking_dir.resolve().as_uri())
    mlflow.set_experiment(experiment_name)  # pyright: ignore[reportUnknownMemberType]
    with mlflow.start_run(
        run_name=portable_run_id,
        tags={
            "data_stage": "accepted-normalized",
            "disposition": "preliminary-missingness-slice",
            "git_sha": git_sha,
            "portable_run_id": portable_run_id,
            "portable_run_bundle": _display_path(portable_run_dir),
            "station_selection": "frozen",
        },
    ) as active_run:
        mlflow.log_param("input_fingerprint_sha256", input_fingerprint_sha256)
        mlflow.log_param("imputation", "disabled")
        mlflow.log_param("profile", "missingness")
        mlflow.log_param("processed_dir", _display_path(processed_dir))
        mlflow.log_metrics({key: float(value) for key, value in profile_metrics.items()})
        for path in artifact_paths.values():
            mlflow.log_artifact(str(path), artifact_path="missingness")
        return active_run.info.run_id


def main(argv: Sequence[str] | None = None) -> int:
    """Run the missingness profile and write the portable evidence bundle."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processed-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--git-sha", required=True)
    parser.add_argument("--mlflow-dir", type=Path, required=True)
    parser.add_argument("--mlflow-experiment", required=True)
    parser.add_argument("--working-tree", choices=("clean", "dirty", "unknown"), default="unknown")
    args = parser.parse_args(argv)
    if args.run_dir.exists():
        parser.error(f"run directory already exists: {args.run_dir}")

    try:
        windows = load_expected_windows(args.config)
        profile = profile_missingness(args.processed_dir, windows)
        command = _command(args)
        artifact_paths = write_missingness_artifacts(
            profile,
            artifact_dir=args.artifact_dir,
            report_path=args.report,
            run_id=args.run_id,
            git_sha=args.git_sha,
            command=command,
        )
    except MissingnessError as error:
        parser.error(str(error))

    args.run_dir.mkdir(parents=True)
    input_paths = [
        args.config,
        *(
            args.processed_dir / name
            for name in (
                "accounting.json",
                "observation.csv",
                "rejected_record.csv",
                "station.csv",
                "ttt_contour.csv",
            )
        ),
    ]
    _write_json(
        args.run_dir / "config.json",
        {
            "expected_windows": [asdict(window) for window in windows],
            "missingness_policy": {
                "absent_timestamp_is_not_a_null_cell": True,
                "coastal_fitted_and_residual_are_not_applicable": True,
                "dart_mixed_cadence_is_not_a_uniform_grid": True,
                "imputation": "disabled",
                "off_grid_source_times": "preserved",
            },
        },
    )
    input_records = [
        {"path": _display_path(path), "sha256": _sha256(path)} for path in input_paths
    ]
    _write_json(args.run_dir / "inputs.json", input_records)
    input_fingerprint = _sha256(args.run_dir / "inputs.json")
    _append_fingerprints(
        args.report,
        input_records=input_records,
        artifact_paths=artifact_paths,
    )
    metrics: dict[str, int | float] = {
        "approved_source_assets": profile.approved_source_assets,
        "blocked_source_assets": profile.blocked_source_assets,
        "coastal_sample_density_unavailable_percent": (
            profile.coastal_sample_density_unavailable_percent
        ),
        "coastal_strict_unavailable_percent": profile.coastal_strict_unavailable_percent,
        "dart_sentinel_percent": profile.dart_sentinel_percent,
        "observation_rows": profile.observation_rows,
        "raw_null_percent": profile.raw_null_percent,
        "raw_null_rows": profile.raw_null_rows,
        "structural_not_applicable_percent": profile.structural_not_applicable_percent,
        "structural_not_applicable_rows": profile.structural_not_applicable_rows,
    }
    _write_json(args.run_dir / "metrics.json", metrics)
    (args.run_dir / "notes.md").write_text(
        """# Missingness profile run notes

This is the first bounded T-002D EDA slice. It distinguishes source blanks,
absent expected timestamps, structural not-applicable fields, deliberate
quarantine, unknown metadata, and whole-asset unavailability. It performs no
imputation, timestamp snapping, arrival picking, or station promotion.

Pooled MCAR is not supported by the observed station/time concentration. MAR is
only a possible conditional analysis assumption; MNAR cannot be excluded without
publisher outage, telemetry, maintenance, or QC evidence.
""",
        encoding="utf-8",
    )
    _write_json(
        args.run_dir / "outputs.json",
        {
            name: {"path": _display_path(path), "sha256": _sha256(path)}
            for name, path in sorted(artifact_paths.items())
        },
    )
    mlflow_run_id = _record_mlflow(
        profile_metrics=metrics,
        artifact_paths=artifact_paths,
        tracking_dir=args.mlflow_dir,
        experiment_name=args.mlflow_experiment,
        portable_run_id=args.run_id,
        portable_run_dir=args.run_dir,
        git_sha=args.git_sha,
        processed_dir=args.processed_dir,
        input_fingerprint_sha256=input_fingerprint,
    )
    _write_json(
        args.run_dir / "meta.json",
        {
            "commands": [command],
            "evidence_disposition": "preliminary-missingness-slice",
            "git_sha": args.git_sha,
            "mlflow_experiment": args.mlflow_experiment,
            "mlflow_run_id": mlflow_run_id,
            "mlflow_tracking_dir": _display_path(args.mlflow_dir),
            "mode": "offline-checksummed-eda",
            "run_id": args.run_id,
            "timestamp_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "working_tree": args.working_tree,
        },
    )
    print(
        json.dumps(
            {
                "artifact_paths": {
                    name: _display_path(path) for name, path in artifact_paths.items()
                },
                "mlflow_run_id": mlflow_run_id,
                "run_dir": _display_path(args.run_dir),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
