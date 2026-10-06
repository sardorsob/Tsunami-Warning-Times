"""Retrospective timing diagnostics; threshold candidates are not physical arrivals."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from math import isfinite
from statistics import median
from typing import Literal


@dataclass(frozen=True)
class Sample:
    """One preserved source observation; QC exclusion affects diagnostics only."""

    at: datetime
    source_time: str
    raw: float | None
    residual: float | None
    fitted: float | None
    qc_bad: bool = False


def utc(value: datetime) -> str:
    """Preserve source timestamp precision when serializing UTC."""
    return value.isoformat().replace("+00:00", "Z")


def detect_crossing(
    samples: list[Sample],
    *,
    origin: datetime,
    baseline_hours: int,
    threshold_floor: float,
    noise_multiplier: float,
    persistence_seconds: int,
    max_gap_seconds: int,
    support_cadence: int,
    minimum_samples: int,
    minimum_coverage: float,
    search_hours: int,
    field: Literal["raw", "residual"],
) -> dict[str, object]:
    """Find a sampled sustained excursion without filling gaps or inventing bounds."""
    if (
        baseline_hours <= 0
        or threshold_floor <= 0
        or noise_multiplier <= 0
        or persistence_seconds <= 0
        or max_gap_seconds <= 0
        or support_cadence <= 0
        or minimum_samples < 2
        or not 0 < minimum_coverage <= 1
        or search_hours <= 0
    ):
        raise ValueError("invalid detector settings")
    for index, row in enumerate(samples):
        if row.at.tzinfo is None or row.at.utcoffset() != timedelta(0):
            raise ValueError("samples must have UTC timestamps")
        if index and row.at <= samples[index - 1].at:
            raise ValueError("samples must be strictly increasing")
        value = getattr(row, field)
        if value is not None and not isfinite(value):
            raise ValueError("sample value must be finite")
    start = origin - timedelta(hours=baseline_hours)
    baseline = [
        s
        for s in samples
        if start <= s.at < origin and getattr(s, field) is not None and not s.qc_bad
    ]
    boundaries = [start, *(s.at for s in baseline), origin]
    gaps = [(b - a).total_seconds() for a, b in zip(boundaries, boundaries[1:], strict=False)]
    coverage = sum(min(g, support_cadence) for g in gaps) / (baseline_hours * 3600)
    result: dict[str, object] = dict(
        status="ineligible_baseline",
        baseline_samples=len(baseline),
        baseline_coverage=round(coverage, 6),
        baseline_max_gap_seconds=max(gaps),
        center_m="unknown",
        threshold_m="unknown",
        candidate_utc="unknown",
        lower_utc="unknown",
        confirmation_utc="unknown",
        source_time="unknown",
        pre_candidate_gap_seconds="unknown",
        candidate_elapsed_seconds="unknown",
    )
    if (
        len(baseline) < minimum_samples
        or coverage < minimum_coverage
        or max(gaps) > max_gap_seconds
    ):
        return result
    values = [float(getattr(s, field)) for s in baseline]
    center = median(values)
    noise = 1.4826 * median(abs(x - center) for x in values)
    threshold = max(threshold_floor, noise_multiplier * noise)
    result.update(status="no_detection", center_m=center, threshold_m=threshold)
    first: Sample | None = None
    previous = baseline[-1]
    lower: datetime | None = None
    run_lower: datetime | None = None
    run_gap: float = 0
    end = origin + timedelta(hours=search_hours)
    for row in samples:
        if not origin <= row.at < end:
            continue
        gap = (row.at - previous.at).total_seconds()
        value = row.raw if field == "raw" else row.residual
        valid = value is not None and not row.qc_bad
        if gap > max_gap_seconds or not valid:
            first = None
            lower = None
        if valid and value is not None and abs(value - center) > threshold:
            if first is None:
                first, run_lower, run_gap = row, lower, gap
            elif (row.at - first.at).total_seconds() >= persistence_seconds:
                result.update(
                    status="candidate",
                    candidate_utc=utc(first.at),
                    lower_utc=utc(run_lower) if run_lower else "unknown",
                    confirmation_utc=utc(row.at),
                    source_time=first.source_time,
                    pre_candidate_gap_seconds=run_gap,
                    candidate_elapsed_seconds=(first.at - origin).total_seconds(),
                )
                return result
        elif valid:
            first, lower = None, row.at
        previous = row
    return result


def summarize_sensitivity(
    picks: list[dict[str, object]],
    controls: list[dict[str, object]],
    max_spread: int,
) -> dict[str, object]:
    """Keep failed settings and control failures in the sensitivity denominator."""
    from pipeline.missingness import _parse_utc  # pyright: ignore[reportPrivateUsage]

    times = [_parse_utc(str(p["candidate_utc"])) for p in picks if p["status"] == "candidate"]
    spread = (max(times) - min(times)).total_seconds() if times else None
    all_detect = bool(picks) and len(times) == len(picks)
    controls_quiet = len(controls) == len(picks) and all(
        c["status"] == "no_detection" for c in controls
    )
    return dict(
        settings=len(picks),
        detected_settings=len(times),
        all_settings_detect=all_detect,
        control_crossings=sum(c["status"] == "candidate" for c in controls),
        control_ineligible=sum(c["status"] == "ineligible_baseline" for c in controls),
        spread_seconds=spread if spread is not None else "unknown",
        screen_pass=all_detect
        and controls_quiet
        and spread is not None
        and spread <= max_spread
        and all(p["lower_utc"] != "unknown" for p in picks),
        physical_arrival_status="unvalidated",
        modeled_arrival_utc="unavailable",
    )
