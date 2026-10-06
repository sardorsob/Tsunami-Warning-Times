"""Explicit restricted review interface; descriptive acceptance is not arrival promotion."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pipeline.eda import verify_fingerprints
from pipeline.eda_audit import fingerprint


def release_decision(root: Path, bundle: Path, review: Path) -> dict[str, Any]:
    """Bind a coordinator-supplied independent receipt to verified descriptive evidence."""
    inputs = json.loads((bundle / "inputs.json").read_text(encoding="utf-8"))
    outputs = json.loads((bundle / "outputs.json").read_text(encoding="utf-8"))
    verify_fingerprints(root, inputs)
    verify_fingerprints(bundle, outputs)
    return dict(
        schema_version=1,
        release_id="tohoku-descriptive-v1",
        event_status="data_proof_candidate",
        disposition="revise_arrival_comparison",
        allowed_uses=["descriptive_data_quality", "preliminary_story_diagnostics"],
        prohibited_uses=[
            "physical_arrival_comparison",
            "modeled_minus_observed_residual",
            "community_timing_selection",
            "actionable_warning_time",
            "operational_warning",
            "public_story_scene_promotion",
        ],
        arrival_comparison_allowed=False,
        physical_arrival_records_released=0,
        source_assets_acquired=17,
        source_assets_contracted=18,
        continuous_nctr_field="blocked_no_proxy",
        review_receipt=fingerprint(review, root),
        bundle=bundle.relative_to(root).as_posix(),
        input_manifest=fingerprint(bundle / "inputs.json", root),
        output_manifest=fingerprint(bundle / "outputs.json", root),
        next_gate="Validate observed onsets and modeled arrival evidence; obtain a new review",
    )
