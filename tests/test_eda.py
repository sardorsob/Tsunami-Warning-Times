"""Behavior checks for the retrospective timing audit (synthetic, not field evidence)."""

from datetime import UTC, datetime, timedelta
from typing import cast

import pytest

from pipeline.eda import Sample, detect_crossing, summarize_sensitivity

ORIGIN = datetime(2011, 3, 11, 6, tzinfo=UTC)


def sample(seconds: int, value: float | None, *, bad: bool = False) -> Sample:
    return Sample(ORIGIN + timedelta(seconds=seconds), str(seconds), value, value, 0.0, bad)


def baseline() -> list[Sample]:
    return [sample(t, 0.0) for t in range(-7200, 0, 60)]


def pick(rows: list[Sample]) -> dict[str, object]:
    return detect_crossing(
        rows,
        origin=ORIGIN,
        baseline_hours=2,
        threshold_floor=0.03,
        noise_multiplier=5.0,
        persistence_seconds=60,
        max_gap_seconds=120,
        support_cadence=60,
        minimum_samples=6,
        minimum_coverage=0.9,
        search_hours=1,
        field="raw",
    )


def test_crossing_preserves_source_time_bracket_and_confirmation() -> None:
    result = pick(baseline() + [sample(0, 0.0), sample(60, 0.04), sample(120, 0.05)])
    assert result["status"] == "candidate"
    assert result["candidate_utc"] == "2011-03-11T06:01:00Z"
    assert result["lower_utc"] == "2011-03-11T06:00:00Z"
    assert result["confirmation_utc"] == "2011-03-11T06:02:00Z"
    assert result["source_time"] == "60"


@pytest.mark.parametrize("breaker", [sample(120, None), sample(120, 0.05, bad=True)])
def test_missing_or_flagged_sample_resets_persistence(breaker: Sample) -> None:
    result = pick(baseline() + [sample(60, 0.05), breaker, sample(180, 0.05)])
    assert result["status"] == "no_detection"
    assert result["candidate_utc"] == "unknown"


def test_long_gap_does_not_bridge_candidate_or_invent_lower_bound() -> None:
    result = pick(baseline() + [sample(0, 0), sample(300, 0.05), sample(360, 0.05)])
    assert result["status"] == "candidate"
    assert result["lower_utc"] == "unknown"
    assert result["pre_candidate_gap_seconds"] == 300


def test_baseline_boundaries_count_against_support() -> None:
    result = pick([sample(t, 0) for t in range(-600, 0, 60)] + [sample(0, 0.1)])
    assert result["status"] == "ineligible_baseline"
    assert cast(float, result["baseline_coverage"]) < 0.2


def test_negative_excursion_detected_without_zero_becoming_missing() -> None:
    result = pick(baseline() + [sample(0, 0), sample(60, -0.05), sample(120, -0.04)])
    assert result["status"] == "candidate"
    assert result["baseline_samples"] == 120


def test_duplicate_or_nonfinite_samples_are_rejected() -> None:
    with pytest.raises(ValueError, match="strictly increasing"):
        pick(baseline() + [sample(0, 0), sample(0, 0.1)])
    with pytest.raises(ValueError, match="finite"):
        pick(baseline() + [sample(0, float("nan"))])


def test_no_success_only_stability_summary() -> None:
    crossing = pick(baseline() + [sample(0, 0), sample(60, 0.05), sample(120, 0.04)])
    quiet = pick(baseline() + [sample(0, 0), sample(60, 0)])
    result = summarize_sensitivity([crossing, quiet], [quiet, quiet], 300)
    assert result["all_settings_detect"] is False
    assert result["screen_pass"] is False
    assert result["detected_settings"] == 1


def test_positive_or_unevaluable_control_blocks_screen() -> None:
    crossing = pick(baseline() + [sample(0, 0), sample(60, 0.05), sample(120, 0.04)])
    for control in [crossing, pick([sample(0, 0)])]:
        assert summarize_sensitivity([crossing], [control], 300)["screen_pass"] is False
