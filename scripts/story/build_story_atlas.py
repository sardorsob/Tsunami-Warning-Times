"""Build the preliminary visual-story diagnostic atlas and evidence bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import sys
from collections.abc import Sequence
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

import mlflow

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from analysis.story.artifacts import (  # noqa: E402
    DecisionRecord,
    display_path,
    load_decision_input,
    preview_decisions,
    render_story_report,
    sha256_file,
    validate_story_output_path,
    write_atlas_manifest,
    write_decision_ledger,
    write_json,
)
from analysis.story.atlas import (  # noqa: E402
    AtlasError,
    AtlasInputs,
    build_series_panels,
    load_atlas_config,
    load_atlas_inputs,
    validate_stage_a_scope,
)
from analysis.story.plots import (  # noqa: E402
    PlotFiles,
    plot_distance_contour_diagnostic,
    plot_observation_coverage,
    plot_pacific_evidence,
    plot_station_timeseries,
)
from pipeline.missingness import (  # noqa: E402
    MissingnessError,
    build_coastal_coverage_timelines,
    load_expected_windows,
)


def _command(args: argparse.Namespace) -> str:
    values: list[tuple[str, object]] = [
        ("--processed-dir", args.processed_dir),
        ("--missingness-config", args.missingness_config),
        ("--missingness-summary", args.missingness_summary),
        ("--coastline", args.coastline),
        ("--config", args.config),
    ]
    if args.decision_input is not None:
        values.append(("--decision-input", args.decision_input))
    values.extend(
        [
            ("--artifact-dir", args.artifact_dir),
            ("--run-dir", args.run_dir),
            ("--report", args.report),
            ("--run-id", args.run_id),
            ("--git-sha", args.git_sha),
            ("--working-tree", args.working_tree),
            ("--mlflow-dir", args.mlflow_dir),
            ("--mlflow-experiment", args.mlflow_experiment),
        ]
    )
    parts = ["uv run python scripts/story/build_story_atlas.py"]
    for flag, value in values:
        rendered = display_path(value) if isinstance(value, Path) else str(value)
        parts.extend((flag, shlex.quote(rendered)))
    return " ".join(parts)


def _input_fingerprint(input_records: list[dict[str, str]]) -> str:
    payload = json.dumps(input_records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _rejection_count(atlas: AtlasInputs) -> int:
    row_counts = atlas.accounting.get("row_counts")
    if not isinstance(row_counts, dict):
        return 0
    value = cast(dict[str, object], row_counts).get("rejected_record", 0)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise AtlasError("accounting rejected_record count must be a non-negative integer")
    return value


def _output_records(
    plots: tuple[PlotFiles, ...],
    *,
    staging_artifact_dir: Path,
    published_artifact_dir: Path,
) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for plot in plots:
        for suffix, source in (("png", plot.png), ("svg", plot.svg)):
            published = published_artifact_dir / f"{plot.plot_id}.{suffix}"
            records.append({"path": display_path(published), "sha256": sha256_file(source)})
    for name in ("atlas-manifest.json", "decision-ledger.csv"):
        source = staging_artifact_dir / name
        published = published_artifact_dir / name
        records.append({"path": display_path(published), "sha256": sha256_file(source)})
    return records


def _record_mlflow(
    *,
    tracking_dir: Path,
    experiment_name: str,
    run_id: str,
    git_sha: str,
    input_fingerprint: str,
    candidate_build_id: str,
    artifact_dir: Path,
    report_path: Path,
    run_dir: Path,
    config_paths: tuple[Path, ...],
    metrics: dict[str, int | float],
    decisions: tuple[DecisionRecord, ...],
) -> str:
    tracking_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")
    os.environ.setdefault("MLFLOW_DISABLE_AGENT_HINT", "true")
    mlflow.set_tracking_uri(tracking_dir.resolve().as_uri())
    mlflow.set_experiment(experiment_name)  # pyright: ignore[reportUnknownMemberType]
    with mlflow.start_run(
        run_name=run_id,
        tags={
            "candidate_build_id": candidate_build_id,
            "evidence_state": "preliminary_storyboard_evidence",
            "git_sha": git_sha,
            "input_fingerprint_sha256": input_fingerprint,
            "lane": "story",
            "portable_run_id": run_id,
        },
    ) as active_run:
        mlflow.log_params(
            {
                "candidate_build_id": candidate_build_id,
                "input_fingerprint_sha256": input_fingerprint,
                "plot_count": 4,
                **{f"decision_{decision.plot_id}": decision.disposition for decision in decisions},
            }
        )
        mlflow.log_metrics({key: float(value) for key, value in metrics.items()})
        for path in config_paths:
            mlflow.log_artifact(str(path), artifact_path="configuration")
        for path in sorted(artifact_dir.iterdir()):
            mlflow.log_artifact(str(path), artifact_path="atlas")
        mlflow.log_artifact(str(report_path), artifact_path="report")
        for name in ("config.json", "inputs.json", "metrics.json", "notes.md", "outputs.json"):
            mlflow.log_artifact(str(run_dir / name), artifact_path="portable-run")
        return active_run.info.run_id


def _preflight(args: argparse.Namespace) -> None:
    for output in (args.artifact_dir, args.run_dir, args.report):
        validate_story_output_path(output)
    if args.artifact_dir == args.run_dir:
        raise AtlasError("artifact and run directories must be distinct")
    if args.artifact_dir.exists():
        raise AtlasError(f"artifact directory already exists: {args.artifact_dir}")
    if args.run_dir.exists():
        raise AtlasError(f"run directory already exists: {args.run_dir}")
    if not args.processed_dir.is_dir():
        raise AtlasError(f"processed directory does not exist: {args.processed_dir}")
    for path in (
        args.missingness_config,
        args.missingness_summary,
        args.coastline,
        args.config,
    ):
        if not path.is_file():
            raise AtlasError(f"required input file does not exist: {path}")
    if args.decision_input is not None and not args.decision_input.is_file():
        raise AtlasError(f"decision input does not exist: {args.decision_input}")
    for plot_id in (
        "01_pacific_evidence_map",
        "02_observation_coverage",
        "03_station_timeseries",
        "04_distance_contour_diagnostic",
    ):
        for suffix in ("png", "svg"):
            validate_story_output_path(args.artifact_dir / f"{plot_id}.{suffix}")
    validate_story_output_path(args.artifact_dir / "atlas-manifest.json")
    validate_story_output_path(args.artifact_dir / "decision-ledger.csv")


def _run(args: argparse.Namespace) -> tuple[str, dict[str, str]]:
    _preflight(args)
    config = load_atlas_config(args.config)
    reviewed_decisions = (
        load_decision_input(args.decision_input) if args.decision_input is not None else None
    )
    atlas = load_atlas_inputs(args.processed_dir, args.missingness_summary)
    windows = load_expected_windows(args.missingness_config)
    validate_stage_a_scope(atlas, config, windows)
    timelines = build_coastal_coverage_timelines(args.processed_dir, windows)
    panels = build_series_panels(atlas, config)
    command = _command(args)

    input_paths = [
        args.config,
        args.missingness_config,
        *atlas.input_paths,
        args.coastline,
    ]
    if args.decision_input is not None:
        input_paths.append(args.decision_input)
    unique_input_paths = tuple(dict.fromkeys(input_paths))
    input_records = [
        {"path": display_path(path), "sha256": sha256_file(path)} for path in unique_input_paths
    ]
    input_fingerprint = _input_fingerprint(input_records)
    metrics: dict[str, int | float] = {
        "contour_count": len(atlas.contours),
        "coverage_grid_positions": sum(len(timeline.positions) for timeline in timelines),
        "coverage_off_grid": sum(len(timeline.off_grid) for timeline in timelines),
        "highlighted_contour_hour_count": len(config.highlighted_contour_hours),
        "observation_count": len(atlas.observations),
        "range_radius_count": len(config.range_radii_km),
        "rejection_count": _rejection_count(atlas),
        "series_point_count": sum(len(panel.points) for panel in panels),
        "station_count": len(atlas.stations),
    }
    decisions = reviewed_decisions or preview_decisions(metrics)

    args.artifact_dir.parent.mkdir(parents=True, exist_ok=True)
    args.run_dir.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    with (
        TemporaryDirectory(
            prefix=f".{args.artifact_dir.name}-", dir=args.artifact_dir.parent
        ) as artifact_stage_text,
        TemporaryDirectory(
            prefix=f".{args.run_dir.name}-", dir=args.run_dir.parent
        ) as run_stage_text,
        TemporaryDirectory(
            prefix=f".{args.report.stem}-", dir=args.report.parent
        ) as report_stage_text,
    ):
        artifact_stage = Path(artifact_stage_text)
        run_stage = Path(run_stage_text)
        report_stage = Path(report_stage_text) / args.report.name
        plots = (
            plot_pacific_evidence(
                atlas,
                config,
                args.coastline,
                artifact_stage / "01_pacific_evidence_map",
            ),
            plot_observation_coverage(
                timelines,
                missingness_summary=atlas.missingness_summary,
                output_stem=artifact_stage / "02_observation_coverage",
            ),
            plot_station_timeseries(
                panels,
                config,
                artifact_stage / "03_station_timeseries",
            ),
            plot_distance_contour_diagnostic(
                atlas,
                config,
                args.coastline,
                artifact_stage / "04_distance_contour_diagnostic",
            ),
        )
        metrics.update(
            {
                "atlas_media_file_count": 8,
                "map_input_parts": plots[0].input_parts,
                "map_output_parts": plots[0].output_parts,
                "distance_input_parts": plots[3].input_parts,
                "distance_output_parts": plots[3].output_parts,
            }
        )
        ledger_path = artifact_stage / "decision-ledger.csv"
        manifest_path = artifact_stage / "atlas-manifest.json"
        write_decision_ledger(ledger_path, decisions)
        write_atlas_manifest(
            manifest_path,
            plots=plots,
            decisions=decisions,
            run_id=args.run_id,
            command=command,
            git_sha=args.git_sha,
            candidate_build_id=args.processed_dir.name,
            input_records=input_records,
            evidence_state=config.evidence_state,
            rejection_count=_rejection_count(atlas),
            published_artifact_dir=args.artifact_dir,
        )
        output_records = _output_records(
            plots,
            staging_artifact_dir=artifact_stage,
            published_artifact_dir=args.artifact_dir,
        )
        report_stage.write_text(
            render_story_report(
                run_id=args.run_id,
                git_sha=args.git_sha,
                command=command,
                candidate_build_id=args.processed_dir.name,
                decisions=decisions,
                metrics=metrics,
                input_records=input_records,
                output_records=output_records,
            ),
            encoding="utf-8",
        )

        write_json(
            run_stage / "config.json",
            {
                "atlas": asdict(config),
                "decisions": "reviewed" if reviewed_decisions is not None else "preview",
                "expected_windows": [asdict(window) for window in windows],
                "policies": {
                    "arrival_comparison": "blocked",
                    "continuous_nctr_field": "unavailable_no_proxy",
                    "imputation": "disabled",
                    "lane": "story",
                    "station_promotion": "disabled",
                },
            },
        )
        write_json(run_stage / "inputs.json", input_records)
        write_json(run_stage / "metrics.json", metrics)
        (run_stage / "notes.md").write_text(
            """# Visual-story atlas run notes

This portable bundle reconstructs preliminary story-only diagnostic evidence.
It uses published contours, source-supported coverage, source-preserving station
points, and geodesic range rings. It performs no interpolation, speed conversion,
arrival picking, station promotion, application export, or story-claim promotion.
""",
            encoding="utf-8",
        )
        portable_outputs = [
            *output_records,
            {"path": display_path(args.report), "sha256": sha256_file(report_stage)},
        ]
        write_json(run_stage / "outputs.json", portable_outputs)
        config_paths = [args.config, args.missingness_config]
        if args.decision_input is not None:
            config_paths.append(args.decision_input)
        mlflow_run_id = _record_mlflow(
            tracking_dir=args.mlflow_dir,
            experiment_name=args.mlflow_experiment,
            run_id=args.run_id,
            git_sha=args.git_sha,
            input_fingerprint=input_fingerprint,
            candidate_build_id=args.processed_dir.name,
            artifact_dir=artifact_stage,
            report_path=report_stage,
            run_dir=run_stage,
            config_paths=tuple(config_paths),
            metrics=metrics,
            decisions=decisions,
        )
        write_json(
            run_stage / "meta.json",
            {
                "commands": [command],
                "evidence_state": config.evidence_state,
                "git_sha": args.git_sha,
                "input_fingerprint_sha256": input_fingerprint,
                "lane": "story",
                "mlflow_experiment": args.mlflow_experiment,
                "mlflow_run_id": mlflow_run_id,
                "mlflow_tracking_dir": display_path(args.mlflow_dir),
                "mode": "offline-checksummed-eda",
                "run_id": args.run_id,
                "timestamp_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "working_tree": args.working_tree,
            },
        )

        artifact_moved = False
        run_moved = False
        try:
            artifact_stage.replace(args.artifact_dir)
            artifact_moved = True
            run_stage.replace(args.run_dir)
            run_moved = True
            report_stage.replace(args.report)
        except OSError:
            if run_moved:
                shutil.rmtree(args.run_dir, ignore_errors=True)
            if artifact_moved:
                shutil.rmtree(args.artifact_dir, ignore_errors=True)
            raise

    return mlflow_run_id, {
        "artifact_dir": display_path(args.artifact_dir),
        "report": display_path(args.report),
        "run_dir": display_path(args.run_dir),
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Run the fixed Stage A atlas and write reconstructable evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processed-dir", type=Path, required=True)
    parser.add_argument("--missingness-config", type=Path, required=True)
    parser.add_argument("--missingness-summary", type=Path, required=True)
    parser.add_argument("--coastline", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--decision-input", type=Path)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--git-sha", required=True)
    parser.add_argument("--working-tree", choices=("clean", "dirty", "unknown"), required=True)
    parser.add_argument("--mlflow-dir", type=Path, required=True)
    parser.add_argument("--mlflow-experiment", required=True)
    args = parser.parse_args(argv)
    try:
        mlflow_run_id, paths = _run(args)
    except (AtlasError, MissingnessError, OSError) as error:
        parser.error(str(error))
    print(
        json.dumps(
            {"mlflow_run_id": mlflow_run_id, "paths": paths, "run_id": args.run_id},
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
