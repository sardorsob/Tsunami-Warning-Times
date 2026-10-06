"""Write the coordinator-approved descriptive-only release after independent review."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline.eda_release import release_decision  # noqa: E402
from pipeline.eda_report import write_json  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    root = Path(__file__).resolve().parents[1]
    value = release_decision(root, args.bundle.resolve(), args.review.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_json(args.output, value)
    print(f"Wrote {args.output}; arrival_comparison_allowed=false")


if __name__ == "__main__":
    main()
