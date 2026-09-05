"""Acquire the approved Tohoku source contracts and record one portable run result."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.acquisition import (  # noqa: E402
    AcquisitionResult,
    ContractError,
    Fetcher,
    ResponseMetadata,
    acquire_all,
    download_url,
    load_contracts,
)


def offline_fetcher(url: str, destination: Path, timeout_seconds: float) -> ResponseMetadata:
    """Prevent a CLI offline run from accessing the network."""
    del url, destination, timeout_seconds
    raise URLError("offline mode")


def write_run_evidence(root: Path, run_tag: str, results: tuple[AcquisitionResult, ...]) -> Path:
    """Write portable acquisition outcomes without copying raw scientific data."""
    run_path = root / "artifacts/logs/runs" / run_tag
    run_path.mkdir(parents=True, exist_ok=True)
    evidence_path = run_path / "acquisition.json"
    evidence_path.write_text(
        json.dumps(
            {
                "results": [
                    {
                        "bytes": result.bytes,
                        "local_path": result.local_path.as_posix(),
                        "reason": result.reason,
                        "sha256": result.sha256,
                        "source_id": result.source_id,
                        "status": result.status,
                    }
                    for result in results
                ]
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return evidence_path


def main(argv: list[str] | None = None) -> int:
    """Run the source-independent acquisition command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/tohoku-data-proof.toml"))
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--run-tag", default="acquisition")
    parser.add_argument("--offline", action="store_true", help="do not access the network")
    args = parser.parse_args(argv)
    if Path(args.run_tag).name != args.run_tag or args.run_tag in {"", ".", ".."}:
        parser.error("--run-tag must be a simple directory name")

    try:
        contracts = load_contracts(args.config)
    except ContractError as error:
        parser.error(str(error))

    fetcher: Fetcher = offline_fetcher if args.offline else download_url
    results = acquire_all(contracts, args.root, fetcher=fetcher)
    evidence_path = write_run_evidence(args.root, args.run_tag, results)
    usable = sum(result.status in {"downloaded", "cached"} for result in results)
    print(f"Wrote {len(results)} acquisition outcome(s) to {evidence_path}")
    if usable == 0:
        print("No usable approved assets were available.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
