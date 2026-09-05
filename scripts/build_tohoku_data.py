"""Build deterministic normalized Tōhoku tables from a verified raw inventory."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.normalize import NormalizationError, build_tables  # noqa: E402


def main(argv: Sequence[str] | None = None) -> int:
    """Run the offline normalization builder."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("config/tohoku-data-proof.toml"))
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--run-tag", default="build")
    args = parser.parse_args(argv)
    try:
        result = build_tables(
            args.config,
            args.inventory,
            args.root,
            run_tag=args.run_tag,
        )
    except (FileExistsError, NormalizationError) as error:
        parser.error(str(error))
    print(
        json.dumps(
            {
                "checksums": result.checksums,
                "output_paths": {
                    name: path.as_posix() for name, path in result.output_paths.items()
                },
                "rejection_counts": result.rejection_counts,
                "row_counts": result.row_counts,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
