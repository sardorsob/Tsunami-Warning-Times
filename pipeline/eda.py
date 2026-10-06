"""Retrospective timing diagnostics; threshold candidates are not physical arrivals."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from math import isfinite
from pathlib import Path
from statistics import median
from typing import Literal, cast

from pipeline.missingness import _parse_utc  # pyright: ignore[reportPrivateUsage]
from pipeline.normalize import IOC_QC_FLAGS


def verify_fingerprints(root: Path, records: list[dict[str, str]]) -> None:
    """Refuse changed inputs and paths escaping the explicitly supplied repository."""
    seen: set[Path] = set()
    for record in records:
        path = (root / record["path"]).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("fingerprint path outside repository")
        if path in seen:
            raise ValueError("duplicate fingerprint path")
        seen.add(path)
        if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
            raise ValueError(f"checksum mismatch: {record['path']}")


def group_observations(
    rows: list[dict[str, str]], stations: dict[str, dict[str, str]]
) -> dict[str, list[Sample]]:
    """Validate grain and measurement semantics before sorting preserved observations."""
    grouped: dict[str, list[Sample]] = {key: [] for key in stations}
    identities: set[str] = set()
    keys: set[tuple[str, datetime]] = set()
    for row in rows:
        station = stations.get(row["station_id"])
        if station is None:
            raise ValueError("orphan observation")
        if any(row[k] != station[k] for k in ("source_id", "units", "vertical_reference")):
            raise ValueError("observation semantics differ from station")
        at = _parse_utc(row["observed_at_utc"])
        key = (row["station_id"], at)
        if row["observation_id"] in identities or key in keys:
            raise ValueError("duplicate observation")
        identities.add(row["observation_id"])
        keys.add(key)
        values: list[float | None] = []
        for field in ("raw_value", "residual_value", "fitted_value"):
            value = float(row[field]) if row[field] else None
            if value is not None and not isfinite(value):
                raise ValueError("observation must be finite")
            values.append(value)
        extra = row["source_extra"]
        flags = cast(dict[str, object], json.loads(extra)) if extra.startswith("{") else {}
        bad = any(str(flags.get(k, "F")).upper() in ("T", "TRUE", "1") for k in IOC_QC_FLAGS)
        grouped[key[0]].append(Sample(at, row["source_time"], *values, qc_bad=bad))
    for samples in grouped.values():
        samples.sort(key=lambda sample: sample.at)
    return grouped


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
        pre_candidate_max_gap_seconds="unknown",
        earlier_support_complete=False,
        search_coverage=0.0,
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
    search_valid = [
        s.at
        for s in samples
        if origin <= s.at < end and getattr(s, field) is not None and not s.qc_bad
    ]
    search_bounds = [origin, *search_valid, end]
    search_gaps = [
        (b - a).total_seconds() for a, b in zip(search_bounds, search_bounds[1:], strict=False)
    ]
    support = sum(min(g, support_cadence) for g in search_gaps) / (search_hours * 3600)
    result.update(search_coverage=support, search_max_gap_seconds=max(search_gaps))
    if not search_valid or support < minimum_coverage or max(search_gaps) > max_gap_seconds:
        result["status"] = "incomplete_search"
    last_valid = baseline[-1].at
    largest_gap = 0.0
    earlier_invalid = False
    for row in samples:
        if not origin <= row.at < end:
            continue
        gap = (row.at - previous.at).total_seconds()
        value = row.raw if field == "raw" else row.residual
        valid = value is not None and not row.qc_bad
        if valid:
            largest_gap = max(largest_gap, (row.at - last_valid).total_seconds())
            last_valid = row.at
        else:
            earlier_invalid = True
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
                    pre_candidate_max_gap_seconds=largest_gap,
                    earlier_support_complete=largest_gap <= max_gap_seconds and not earlier_invalid,
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
        control_ineligible=sum(c["status"] not in ("candidate", "no_detection") for c in controls),
        spread_seconds=spread if spread is not None else "unknown",
        screen_pass=all_detect
        and controls_quiet
        and spread is not None
        and spread <= max_spread
        and all(p["lower_utc"] != "unknown" and p["earlier_support_complete"] for p in picks),
        physical_arrival_status="unvalidated",
        modeled_arrival_utc="unavailable",
    )
