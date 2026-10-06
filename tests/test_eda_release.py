"""The review interface must not turn descriptive acceptance into arrival permission."""

import hashlib
import json
from pathlib import Path

import pytest

from pipeline.eda_release import release_decision


def test_restricted_release_is_checksummed_and_never_grants_arrival_permission(
    tmp_path: Path,
) -> None:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "meta.json").write_text('{"run_id":"synthetic-test"}')
    (bundle / "inputs.json").write_text("[]")
    (bundle / "outputs.json").write_text(
        json.dumps(
            [
                {
                    "path": "meta.json",
                    "sha256": hashlib.sha256((bundle / "meta.json").read_bytes()).hexdigest(),
                }
            ]
        )
    )
    receipt = tmp_path / "review.md"
    receipt.write_text("Synthetic test receipt")
    decision = release_decision(tmp_path, bundle, receipt)
    assert decision["arrival_comparison_allowed"] is False
    assert decision["physical_arrival_records_released"] == 0
    assert decision["disposition"] == "revise_arrival_comparison"
    assert decision["review_receipt"]["sha256"] == hashlib.sha256(receipt.read_bytes()).hexdigest()
    (bundle / "meta.json").write_text("changed")
    with pytest.raises(ValueError, match="checksum"):
        release_decision(tmp_path, bundle, receipt)
