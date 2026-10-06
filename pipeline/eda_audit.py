"""Checksummed, descriptive shared EDA; no arrival or story-selection promotion."""

from __future__ import annotations

import csv
import hashlib
import json
import tomllib
from collections import Counter
from datetime import timedelta
from itertools import product
from pathlib import Path
from statistics import median
from typing import Any, Literal

from pyproj import Geod
from shapely.geometry import LineString

from pipeline.eda import Sample, detect_crossing, group_observations, summarize_sensitivity, utc
from pipeline.missingness import _parse_utc  # pyright: ignore[reportPrivateUsage]


def fingerprint(path: Path, root: Path) -> dict[str, str]:
    """Record bytes and a portable repository-relative path."""
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def read_table(path: Path) -> list[dict[str, str]]:
    """Require rectangular CSV records, including for provenance inputs."""
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError(f"invalid CSV header: {path.name}")
        if any(None in row or None in row.values() for row in rows):
            raise ValueError(f"nonrectangular CSV: {path.name}")
        return rows


def station_profile(
    samples: list[Sample], station_id: str, gap_limit: int
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Describe retained values and gaps without dropping outliers or imputing."""
    result: dict[str, Any] = {
        "station_id": station_id,
        "rows": len(samples),
        "qc_flagged": sum(s.qc_bad for s in samples),
    }
    for field in ("raw", "residual", "fitted"):
        values = [v for s in samples if (v := getattr(s, field)) is not None]
        result.update(
            {
                f"{field}_missing": len(samples) - len(values),
                f"{field}_min": min(values) if values else "unknown",
                f"{field}_median": median(values) if values else "unknown",
                f"{field}_max": max(values) if values else "unknown",
                f"{field}_zero": values.count(0.0),
            }
        )
    differences = [
        abs(s.raw - s.fitted - s.residual)
        for s in samples
        if s.raw is not None and s.fitted is not None and s.residual is not None
    ]
    result["raw_minus_fit_minus_residual_max_abs"] = max(differences, default="unknown")
    result["residual_disagreement_above_0_00002_m"] = sum(v > 0.00002 for v in differences)
    intervals = [
        (a, b, (b.at - a.at).total_seconds()) for a, b in zip(samples, samples[1:], strict=False)
    ]
    result["cadence_counts_seconds"] = dict(sorted(Counter(g for _, _, g in intervals).items()))
    result["first_utc"] = utc(samples[0].at) if samples else "unknown"
    result["last_utc"] = utc(samples[-1].at) if samples else "unknown"
    gaps = [
        {
            "station_id": station_id,
            "start_utc": utc(a.at),
            "end_utc": utc(b.at),
            "seconds": g,
            "left_source_time": a.source_time,
            "right_source_time": b.source_time,
        }
        for a, b, g in intervals
        if g > gap_limit
    ]
    result["long_intervals"] = len(gaps)
    result["max_interval_seconds"] = max((g for _, _, g in intervals), default="unknown")
    return result, gaps


def audit(root: Path, processed: Path, anchor: Path, config: Path) -> dict[str, Any]:
    """Audit the accepted bytes against tracked anchors before running frozen settings."""
    from pipeline.eda import verify_fingerprints

    anchors: list[dict[str, str]] = json.loads(anchor.read_text())
    verify_fingerprints(root, anchors)
    accounting_path = processed / "accounting.json"
    if fingerprint(accounting_path, root) not in anchors:
        raise ValueError("processed accounting is not covered by trusted anchor")
    accounting = json.loads(accounting_path.read_text())
    inputs = [fingerprint(anchor, root), fingerprint(config, root), *anchors]
    records = [
        {
            "path": (processed / f"{name}.{'json' if name == 'schemas' else 'csv'}")
            .relative_to(root)
            .as_posix(),
            "sha256": checksum,
        }
        for name, checksum in accounting["output_checksums"].items()
    ]
    verify_fingerprints(root, records)
    inputs.extend(records)
    inventory_path = root / accounting["input_inventory"]
    inventory = json.loads(inventory_path.read_text())
    outcomes = {row["source_id"]: row for row in inventory}
    raw_records: list[dict[str, str]] = []
    for outcome in accounting["source_outcomes"]:
        if outcome["availability"] != "approved":
            continue
        source = outcomes[outcome["source_id"]]
        if source["sha256"] != outcome["sha256"]:
            raise ValueError("raw inventory differs from accepted accounting")
        raw_records.append({"path": source["local_path"], "sha256": outcome["sha256"]})
    verify_fingerprints(root, raw_records)
    inputs.extend([fingerprint(inventory_path, root), *raw_records])
    tables = {name: read_table(processed / f"{name}.csv") for name in accounting["row_counts"]}
    if {key: len(rows) for key, rows in tables.items()} != accounting["row_counts"]:
        raise ValueError("row accounting differs")
    settings = tomllib.loads(config.read_text())
    event = tables["event"][0]
    if (
        len(tables["event"]) != 1
        or event["event_id"] != settings["event_id"]
        or event["origin_time_utc"] != settings["origin_utc"]
    ):
        raise ValueError("event identity/origin differs from frozen protocol")
    stations = {row["station_id"]: row for row in tables["station"]}
    if len(stations) != len(tables["station"]) or sorted(stations) != sorted(
        settings["station_ids"]
    ):
        raise ValueError("station grain or frozen cohort differs")
    grouped = group_observations(tables["observation"], stations)
    origin = _parse_utc(settings["origin_utc"])
    profiles: list[dict[str, Any]] = []
    gaps: list[dict[str, Any]] = []
    picks: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    windows: list[dict[str, Any]] = []
    geod = Geod(ellps="WGS84")
    for station_id, station in sorted(stations.items()):
        samples = grouped[station_id]
        dart = station["station_type"] == "dart"
        field: Literal["raw", "residual"] = "residual" if dart else "raw"
        gap_limit = settings["dart_max_gap_seconds" if dart else "coastal_max_gap_seconds"]
        profile, station_gaps = station_profile(samples, station_id, gap_limit)
        _, _, distance = geod.inv(
            float(event["longitude"]),
            float(event["latitude"]),
            float(station["longitude"]),
            float(station["latitude"]),
        )
        profile.update(
            name=station["name"],
            station_type=station["station_type"],
            source_distance_km=distance / 1000,
            datum=station["vertical_reference"],
            units=station["units"],
            horizontal_datum=station["horizontal_datum"],
        )
        profiles.append(profile)
        gaps.extend(station_gaps)
        event_picks: list[dict[str, Any]] = []
        controls: list[dict[str, Any]] = []
        for baseline, floor, persistence in product(
            settings["baseline_hours"],
            settings["threshold_floors_m"],
            settings["persistence_seconds"],
        ):
            for window in ("event", "control"):
                start = (
                    origin
                    if window == "event"
                    else origin - timedelta(hours=settings["control_hours"])
                )
                result = detect_crossing(
                    samples,
                    origin=start,
                    baseline_hours=baseline,
                    threshold_floor=floor,
                    noise_multiplier=settings["noise_multiplier"],
                    persistence_seconds=persistence,
                    max_gap_seconds=gap_limit,
                    support_cadence=900 if dart else 60,
                    minimum_samples=settings["minimum_baseline_samples"],
                    minimum_coverage=settings["minimum_baseline_coverage"],
                    search_hours=settings["search_hours"]
                    if window == "event"
                    else settings["control_hours"],
                    field=field,
                )
                result.update(
                    station_id=station_id,
                    window=window,
                    baseline_hours=baseline,
                    threshold_floor_m=floor,
                    persistence_seconds=persistence,
                    field=field,
                    interpretation="diagnostic_residual" if dart else "unsupported_raw_control",
                )
                picks.append(result)
                (event_picks if window == "event" else controls).append(result)
        summary = summarize_sensitivity(
            event_picks, controls, settings["maximum_stability_spread_seconds"]
        )
        summary.update(
            station_id=station_id,
            field=field,
            measurement_supported=dart,
            physical_arrival_status="unvalidated" if dart else "unsupported_raw_water_level",
        )
        summaries.append(summary)
        # Adaptive evidence: retain every distinct candidate's surrounding source samples.
        candidate_times = sorted(
            {
                _parse_utc(str(p["candidate_utc"]))
                for p in [*event_picks, *controls]
                if p["status"] == "candidate"
            }
        )
        for candidate in candidate_times:
            for s in samples:
                if abs((s.at - candidate).total_seconds()) <= 900:
                    windows.append(
                        {
                            "station_id": station_id,
                            "candidate_utc": utc(candidate),
                            "observed_at_utc": utc(s.at),
                            "source_time": s.source_time,
                            "raw": s.raw,
                            "residual": s.residual,
                            "fitted": s.fitted,
                            "qc_bad": s.qc_bad,
                        }
                    )
    contour_stats: Counter[str] = Counter()
    for row in tables["ttt_contour"]:
        coordinates = json.loads(row["coordinates"])
        if row["crs"] != "EPSG:4326" or not LineString(coordinates).is_valid:
            raise ValueError("invalid contour CRS or geometry")
        contour_stats["parts"] += 1
        contour_stats["vertices"] += len(coordinates)
        contour_stats["longitude_roundoff_vertices"] += sum(abs(x) > 180 for x, _ in coordinates)
        contour_stats["unsplit_longitude_jumps"] += sum(
            abs(b[0] - a[0]) > 180 for a, b in zip(coordinates, coordinates[1:], strict=False)
        )
    return dict(
        settings=settings,
        inputs=sorted({r["path"]: r for r in inputs}.values(), key=lambda r: r["path"]),
        counts=accounting["row_counts"],
        source_coverage=accounting["source_coverage"],
        rejection_reasons=accounting["rejection_reason_counts"],
        profiles=profiles,
        gaps=gaps,
        picks=picks,
        summaries=summaries,
        candidate_windows=windows,
        geometry=dict(contour_stats),
    )
