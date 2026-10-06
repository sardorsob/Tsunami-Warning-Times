"""Behavior checks for the retrospective timing audit (synthetic, not field evidence)."""

from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import cast

import pytest

from pipeline.eda import (
    Sample,
    detect_crossing,
    group_observations,
    summarize_sensitivity,
    verify_fingerprints,
)
from pipeline.eda_audit import station_profile

ORIGIN = datetime(2011, 3, 11, 6, tzinfo=UTC)


def test_profile_preserves_qc_extreme_and_exposes_residual_disagreement() -> None:
    rows = [
        sample(0, 0),
        Sample(ORIGIN + timedelta(seconds=60), "x", 100, 0.1, 99, True),
        sample(600, 0),
    ]
    profile, gaps = station_profile(rows, "a", 120)
    assert profile["raw_max"] == 100
    assert profile["qc_flagged"] == 1
    assert profile["raw_minus_fit_minus_residual_max_abs"] == pytest.approx(0.9)
    assert gaps[0]["seconds"] == 540


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
    assert result["status"] == "incomplete_search"
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


def test_empty_or_truncated_control_is_not_evidence_of_quiet() -> None:
    for rows in [baseline(), baseline() + [sample(0, 0)]]:
        assert pick(rows)["status"] == "incomplete_search"
    quiet = pick(baseline() + [sample(t, 0) for t in range(0, 3600, 60)])
    assert quiet["status"] == "no_detection"


def test_earlier_gap_is_not_forgotten_when_candidate_has_local_bracket() -> None:
    result = pick(baseline() + [sample(0, 0), sample(600, 0), sample(660, 0.05), sample(720, 0.05)])
    assert result["lower_utc"] != "unknown"
    assert result["pre_candidate_max_gap_seconds"] == 600
    quiet = pick(baseline() + [sample(t, 0) for t in range(0, 3600, 60)])
    assert summarize_sensitivity([result], [quiet], 300)["screen_pass"] is False


def test_checksum_mismatch_fails_before_analysis(tmp_path: Path) -> None:
    path = tmp_path / "table.csv"
    path.write_text("changed", encoding="utf-8")
    with pytest.raises(ValueError, match="checksum"):
        verify_fingerprints(tmp_path, [{"path": "table.csv", "sha256": "0" * 64}])
    with pytest.raises(ValueError, match="outside"):
        verify_fingerprints(tmp_path, [{"path": "../outside.csv", "sha256": "0" * 64}])


def test_observation_join_refuses_orphans_duplicates_and_semantic_mismatch() -> None:
    station = dict(station_id="a", source_id="s", units="m", vertical_reference="unknown")
    row = dict(
        observation_id="a-1",
        station_id="a",
        source_id="s",
        source_time="preserved",
        observed_at_utc="2011-03-11T00:00:00Z",
        raw_value="0",
        fitted_value="",
        residual_value="",
        source_extra="",
        units="m",
        vertical_reference="unknown",
    )
    grouped = group_observations([row], {"a": station})
    assert grouped["a"][0].raw == 0
    for changed, message in [
        ({"station_id": "b"}, "orphan"),
        ({"units": "cm"}, "semantics"),
        ({"raw_value": "nan"}, "finite"),
    ]:
        with pytest.raises(ValueError, match=message):
            group_observations([row | changed], {"a": station})
    with pytest.raises(ValueError, match="duplicate"):
        group_observations([row, row], {"a": station})


def test_qc_flag_is_retained_and_blocks_diagnostic_use() -> None:
    station = dict(station_id="a", source_id="s", units="m", vertical_reference="unknown")
    row = dict(
        observation_id="a-1",
        station_id="a",
        source_id="s",
        source_time="preserved",
        observed_at_utc="2011-03-11T00:00:00Z",
        raw_value="0",
        fitted_value="",
        residual_value="",
        source_extra='{"out_of_range":"T"}',
        units="m",
        vertical_reference="unknown",
    )
    result = group_observations([row], {"a": station})["a"][0]
    assert result.raw == 0
    assert result.qc_bad
