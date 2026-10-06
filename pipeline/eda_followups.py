"""Evidence-triggered checks added after the first frozen timing audit, without retuning."""
# ruff: noqa: E501 -- Keep generated Markdown ledger prose intact.

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pipeline.eda import Sample, utc
from pipeline.missingness import _parse_utc  # pyright: ignore[reportPrivateUsage]


def follow_up(
    result: dict[str, Any],
    grouped: dict[str, list[Sample]],
    stations: dict[str, dict[str, str]],
    outcomes: dict[str, Any],
    root: Path,
) -> None:
    """Trace suspicious candidates, gaps and QC extrema to preserved publisher bytes."""
    origin = _parse_utc(result["settings"]["origin_utc"])
    ledger: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    for station_id, station in stations.items():
        if station["station_type"] != "dart":
            continue
        source = outcomes[station["source_id"]]
        raw_rows: list[tuple[datetime, int, str, str]] = []
        for number, line in enumerate(
            (root / source["local_path"]).read_text(encoding="utf-8").splitlines(), 1
        ):
            cells = line.split()
            if len(cells) != 11:
                raise ValueError("unexpected accepted DART raw shape")
            raw_rows.append(
                (datetime(*(int(v) for v in cells[1:7]), tzinfo=UTC), number, cells[0], line)
            )
        picks = [
            p
            for p in result["picks"]
            if p["station_id"] == station_id
            and p["window"] == "event"
            and p["status"] == "candidate"
        ]
        targets = {str(p["source_time"]) for p in picks}
        for _, number, source_time, line in raw_rows:
            if source_time in targets:
                traces.append(
                    dict(
                        station_id=station_id,
                        kind="candidate",
                        path=source["local_path"],
                        line_number=number,
                        raw_line=line,
                    )
                )
        matching_gaps = [g for g in result["gaps"] if g["station_id"] == station_id]
        sentinel_total = 0
        for gap in matching_gaps:
            inside = [
                r
                for r in raw_rows
                if _parse_utc(gap["start_utc"]) < r[0] < _parse_utc(gap["end_utc"])
            ]
            sentinels = [
                r
                for r in inside
                if "9999.00000" in r[3] or any(float(v) == 9999 for v in r[3].split()[7:10])
            ]
            gap["raw_interior_rows"] = len(inside)
            gap["quarantined_sentinel_rows"] = len(sentinels)
            sentinel_total += len(sentinels)
            for _, number, _, line in sentinels:
                traces.append(
                    dict(
                        station_id=station_id,
                        kind="gap_sentinel",
                        path=source["local_path"],
                        line_number=number,
                        raw_line=line,
                    )
                )
        ledger.append(
            dict(
                observation=f"{station['name']}: {len(matching_gaps)} excessive intervals",
                question="Are these local quarantine effects or absent source timestamps?",
                follow_up="Compare gap interiors with original raw calendar fields and 9999 rows.",
                evidence=f"{sentinel_total} sentinel rows inside these intervals; raw-traces.csv records lines.",
                decision="Keep gaps unresolved for onset support; documented quarantine is not a technical download failure.",
            )
        )
    html_source = outcomes["nctr-tohoku-source-coefficients"]
    html = (root / html_source["local_path"]).read_text(encoding="utf-8")
    if "approximately 25 minutes" not in html:
        raise ValueError("NOAA corroboration changed; re-review approximate arrival reference")
    near = [
        p
        for p in result["picks"]
        if p["station_id"] == "21418" and p["window"] == "event" and p["status"] == "candidate"
    ]
    minutes = [p["candidate_elapsed_seconds"] / 60 for p in near]
    ledger.append(
        dict(
            observation=f"DART 21418 candidates: {min(minutes):.3f}–{max(minutes):.3f} min after origin.",
            question="Does a stable threshold crossing identify the tsunami onset?",
            follow_up="Inspect first-hour residual waveform and independently check the cached NOAA NCTR event page.",
            evidence="NOAA describes first recording at approximately 25 minutes, not an exact picking timestamp. "
            f"Cached source {html_source['local_path']}, SHA-256 {html_source['sha256']}; "
            "https://nctr.pmel.noaa.gov/honshu20110311/ (web rechecked 2026-10-05).",
            decision="Reject the early threshold crossing as a validated tsunami arrival; "
            "the source contradicts that interpretation. Early signal mechanism remains unclassified. "
            "Do not replace it with an invented exact 25-minute timestamp or tune settings to the reference.",
        )
    )
    for summary in result["summaries"]:
        summary["external_validation"] = (
            "conflicts_approximate_publisher_reference"
            if summary["station_id"] == "21418"
            else "not_validated"
        )
    for station_id in ("9461380", "saip", "valp"):
        summary = next(s for s in result["summaries"] if s["station_id"] == station_id)
        profile = next(s for s in result["profiles"] if s["station_id"] == station_id)
        ledger.append(
            dict(
                observation=f"{profile['name']}: {summary['control_crossings']} control crossings; "
                f"{summary['control_ineligible']} unevaluable controls; {profile['qc_flagged']} QC flags.",
                question="Can this series support the proposed simple onset rule?",
                follow_up="Retain all settings, baseline gap bounds and source-QC records; inspect candidate windows.",
                evidence="sensitivity.csv, candidate-windows.csv and qc-records.csv retain the exact timestamps and values.",
                decision="No coastal physical-arrival release: raw tidal levels plus continuity/QC risks "
                "require a separately reviewed observed-onset method.",
            )
        )
    result["adaptive_ledger"] = ledger
    result["raw_traces"] = traces
    result["early_waveform"] = [
        dict(
            minutes=(s.at - origin).total_seconds() / 60,
            residual=s.residual,
            observed_at_utc=utc(s.at),
        )
        for s in grouped["21418"]
        if -5 <= (s.at - origin).total_seconds() / 60 <= 60
    ]
    result["qc_records"] = [
        dict(
            station_id=sid,
            observed_at_utc=utc(s.at),
            source_time=s.source_time,
            raw=s.raw,
            residual=s.residual,
        )
        for sid, samples in grouped.items()
        for s in samples
        if s.qc_bad
    ]
