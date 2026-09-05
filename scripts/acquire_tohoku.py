"""Acquire the approved Tohoku source contracts and record one portable run result."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.acquisition import (  # noqa: E402
    AcquisitionResult,
    ContractError,
    Fetcher,
    ResponseMetadata,
    SourceContract,
    acquire_all,
    download_url,
    load_contracts,
)

SENSITIVE_RESPONSE_HEADERS = frozenset(
    {"authorization", "cookie", "proxy-authorization", "set-cookie", "x-api-key"}
)


def offline_fetcher(url: str, destination: Path, timeout_seconds: float) -> ResponseMetadata:
    """Prevent a CLI offline run from accessing the network."""
    del url, destination, timeout_seconds
    raise URLError("offline mode")


def sanitize_run_tag(run_tag: str) -> str:
    """Return a filesystem-safe lowercase run-tag component."""
    return re.sub(r"[^a-z0-9]+", "-", run_tag.casefold()).strip("-")


def utc_now() -> datetime:
    """Return the current UTC timestamp; separated for deterministic tests."""
    return datetime.now(UTC)


def git_short_sha(root: Path) -> str:
    """Return the checked-out Git short SHA, or an explicit unavailable value."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def working_tree_status(root: Path) -> str:
    """Return code/config tree state while ignoring prior generated run bundles."""
    try:
        output = subprocess.check_output(
            [
                "git",
                "status",
                "--porcelain",
                "--untracked-files=all",
                "--",
                ".",
                ":(exclude)artifacts/logs/runs/**",
            ],
            cwd=root,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return "dirty" if output else "clean"


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _contract_record(contract: SourceContract) -> dict[str, str]:
    return {
        "availability": contract.availability,
        "coordinate_order": contract.coordinate_order,
        "crs": contract.crs,
        "expected_content_signature": contract.expected_content_signature,
        "expected_prefix": contract.expected_prefix,
        "format": contract.format,
        "horizontal_datum": contract.horizontal_datum,
        "local_path": contract.local_path.as_posix(),
        "publisher": contract.publisher,
        "reason": contract.reason,
        "source_class": contract.source_class,
        "source_id": contract.source_id,
        "station_metadata": contract.station_metadata,
        "temporal_semantics": contract.temporal_semantics,
        "units": contract.units,
        "url": contract.url,
        "vertical_datum": contract.vertical_datum,
    }


def _result_record(result: AcquisitionResult) -> dict[str, object]:
    return {
        "bytes": result.bytes,
        "content_type": result.content_type,
        "headers": {
            key: "[redacted]" if key.casefold() in SENSITIVE_RESPONSE_HEADERS else value
            for key, value in sorted(result.headers.items())
        },
        "local_path": result.local_path.as_posix(),
        "reason": result.reason,
        "sha256": result.sha256,
        "source_id": result.source_id,
        "status": result.status,
    }


def write_run_evidence(
    *,
    root: Path,
    run_tag: str,
    config_path: Path,
    contracts: Sequence[SourceContract],
    results: Sequence[AcquisitionResult],
    command: str,
    mode: str,
    now_utc: Callable[[], datetime] = utc_now,
    git_sha: Callable[[], str] | None = None,
    working_tree: Callable[[], str] | None = None,
) -> Path:
    """Write one immutable portable bundle without copying raw scientific data."""
    safe_tag = sanitize_run_tag(run_tag)
    if not safe_tag:
        raise ValueError("--run-tag must include at least one letter or number")
    timestamp = now_utc().astimezone(UTC).replace(second=0, microsecond=0)
    revision = git_sha() if git_sha is not None else git_short_sha(root)
    tree_status = working_tree() if working_tree is not None else working_tree_status(root)
    evidence_disposition = {
        "clean": "ready-for-review",
        "dirty": "implementation-under-review",
    }.get(tree_status, "working-tree-unknown")
    run_id = f"{timestamp:%Y-%m-%d__%H%M}__{safe_tag}__{revision}"
    run_path = root / "artifacts/logs/runs" / run_id
    run_path.mkdir(parents=True, exist_ok=False)
    config_bytes = config_path.read_bytes()
    ordered_contracts = sorted(contracts, key=lambda contract: contract.source_id)
    ordered_results = sorted(results, key=lambda result: result.source_id)
    status_counts = Counter(result.status for result in ordered_results)
    bytes_by_status = {
        status: sum(result.bytes for result in ordered_results if result.status == status)
        for status in sorted(status_counts)
    }
    _write_json(
        run_path / "meta.json",
        {
            "command": command,
            "evidence_disposition": evidence_disposition,
            "git_sha": revision,
            "mode": mode,
            "run_id": run_id,
            "timestamp_utc": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "working_tree": tree_status,
        },
    )
    _write_json(
        run_path / "config.json",
        {
            "path": config_path.as_posix(),
            "sha256": hashlib.sha256(config_bytes).hexdigest(),
            "toml": config_bytes.decode("utf-8"),
        },
    )
    _write_json(
        run_path / "inputs.json",
        [_contract_record(contract) for contract in ordered_contracts],
    )
    _write_json(
        run_path / "outputs.json",
        [_result_record(result) for result in ordered_results],
    )
    _write_json(
        run_path / "metrics.json",
        {
            "bytes_by_status": bytes_by_status,
            "status_counts": dict(sorted(status_counts.items())),
            "total_bytes": sum(result.bytes for result in ordered_results),
            "total_contracts": len(ordered_contracts),
        },
    )
    (run_path / "notes.md").write_text(
        "# Acquisition run notes\n\n"
        "## Decision\n\n"
        "Only contracts marked `approved` were eligible for retrieval; blocked contracts "
        "were recorded without network access.\n\n"
        "## Limitations\n\n"
        "Source-specific limits, missingness, datum, CRS, and temporal-semantics "
        "constraints remain in `inputs.json`; cached assets have no new response headers.\n",
        encoding="utf-8",
    )
    return run_path


def main(argv: list[str] | None = None) -> int:
    """Run the source-independent acquisition command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/tohoku-data-proof.toml"))
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--run-tag", default="acquisition")
    parser.add_argument("--offline", action="store_true", help="do not access the network")
    args = parser.parse_args(argv)
    if not sanitize_run_tag(args.run_tag):
        parser.error("--run-tag must include at least one letter or number")

    try:
        contracts = load_contracts(args.config)
    except ContractError as error:
        parser.error(str(error))

    fetcher: Fetcher = offline_fetcher if args.offline else download_url
    results = acquire_all(contracts, args.root, fetcher=fetcher)
    command = " ".join(["uv run python scripts/acquire_tohoku.py", *sys.argv[1:]])
    try:
        evidence_path = write_run_evidence(
            root=args.root,
            run_tag=args.run_tag,
            config_path=args.config,
            contracts=contracts,
            results=results,
            command=command,
            mode="offline" if args.offline else "live",
        )
    except (OSError, ValueError, UnicodeDecodeError) as error:
        parser.error(f"could not write run evidence: {error}")
    usable = sum(result.status in {"downloaded", "cached"} for result in results)
    print(f"Wrote {len(results)} acquisition outcome(s) to {evidence_path}")
    if usable == 0:
        print("No usable approved assets were available.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
