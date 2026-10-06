"""Run the frozen shared timing audit; no downloads, imputation, or arrival promotion."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

import mlflow

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline.eda_report import write_json, write_run  # noqa: E402


def main() -> None:
    """Publish a fresh bundle, optionally mirror its report and track its evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--git-sha", required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--replace-report", action="store_true")
    parser.add_argument("--mlflow", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.report and args.report.exists() and not args.replace_report:
        parser.error("report exists; explicit --replace-report required")
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    if not sha.startswith(args.git_sha):
        parser.error("--git-sha must match the executing checkout")
    result = write_run(
        root,
        root / "data/processed/tohoku/2026-09-09-valparaiso-reviewed-7576ffb-a",
        root / "artifacts/logs/runs/2026-09-09__1749__missingness__7b6d386/inputs.json",
        root / "config/tohoku-arrival-audit.toml",
        args.output,
        git_sha=args.git_sha,
        run_id=args.run_id,
    )
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_bytes((args.output / "report.md").read_bytes())
        write_json(
            args.report.parent / "EDA_RUN.json",
            {
                "bundle": args.output.resolve().relative_to(root).as_posix(),
                "run_id": args.run_id,
                "git_sha": args.git_sha,
                "report_sha256": hashlib.sha256(
                    (args.output / "report.md").read_bytes()
                ).hexdigest(),
                "arrival_comparison_allowed": False,
            },
        )
    if args.mlflow:
        os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")
        os.environ.setdefault("MLFLOW_DISABLE_AGENT_HINT", "true")
        mlflow.set_tracking_uri((root / ".mlflow/mlruns").as_uri())
        mlflow.set_experiment("tohoku-eda")  # pyright: ignore[reportUnknownMemberType]
        with mlflow.start_run(
            run_name=args.run_id,
            tags={
                "git_sha": sha,
                "lane": "shared-eda",
                "disposition": "revise_arrival_comparison",
                "portable_run_bundle": str(args.output),
                "selection": "all-ten-stations",
            },
        ) as run:
            mlflow.log_params(
                {
                    "protocol": result["settings"]["protocol_version"],
                    "settings_per_station": 8,
                    "randomness": "none",
                    "input_fingerprint": hashlib.sha256(
                        (args.output / "inputs.json").read_bytes()
                    ).hexdigest(),
                }
            )
            mlflow.log_metrics(
                {
                    "observations": result["counts"]["observation"],
                    "diagnostic_screen_pass": sum(s["screen_pass"] for s in result["summaries"]),
                    "physical_arrivals_released": 0,
                }
            )
            mlflow.log_artifacts(str(args.output), artifact_path="shared-eda")
            write_json(
                args.output / "tracking.json",
                {
                    "mlflow_run_id": run.info.run_id,
                    "stable_manifest": "outputs.json",
                    "note": "tracking receipt excluded from deterministic outputs",
                },
            )
    print(f"Wrote {args.output}; arrival comparison remains unapproved.")


if __name__ == "__main__":
    main()
