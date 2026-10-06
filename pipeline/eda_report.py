"""Deterministic run bundles and explanatory diagnostics for the shared timing audit."""
# ruff: noqa: E501 -- Markdown prose/table rows are deliberately kept intact.
# pyright: reportUnknownMemberType=false
# Matplotlib's public plotting methods expose untyped **kwargs in pinned stubs.

from __future__ import annotations

import csv
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from pipeline.eda_audit import audit
from pipeline.missingness import (
    load_expected_windows,
    profile_missingness,
    write_missingness_artifacts,
)


def write_json(path: Path, value: object) -> None:
    """Stable, finite JSON; scientific unavailable values are explicit strings."""
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Preserve all columns, including failure-only fields."""
    columns = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, restval="unknown", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    k: "unknown"
                    if v is None
                    else json.dumps(v, sort_keys=True)
                    if isinstance(v, dict)
                    else v
                    for k, v in row.items()
                }
            )


def figures(result: dict[str, Any], output: Path) -> None:
    """All-setting status and DART timing range; neither encodes a physical arrival."""
    with plt.rc_context(
        {
            "font.size": 14,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "svg.hashsalt": "tohoku-audit-v1",
        }
    ):
        fig, ax = plt.subplots(figsize=(12, 8))
        profiles = result["profiles"]
        labels = [
            p["name"] + (" [raw control]" if p["station_type"] != "dart" else "") for p in profiles
        ]
        statuses = [
            ("candidate", "Crossing", "#176578", ""),
            ("no_detection", "No crossing", "#666666", "//"),
            ("incomplete_search", "Incomplete search", "#9F4A12", ".."),
            ("ineligible_baseline", "Baseline fails", "#513A76", "xx"),
        ]
        left = [0] * len(labels)
        for status, label, color, hatch in statuses:
            counts = [
                sum(
                    p["station_id"] == row["station_id"]
                    and p["window"] == "event"
                    and p["status"] == status
                    for p in result["picks"]
                )
                for row in profiles
            ]
            ax.barh(
                labels,
                counts,
                left=left,
                label=label,
                color=color,
                hatch=hatch,
                edgecolor="white",
                linewidth=0.8,
            )  # pyright: ignore[reportUnknownMemberType]
            for i, count in enumerate(counts):
                if count:
                    ax.text(
                        left[i] + count / 2,
                        i,
                        str(count),
                        ha="center",
                        va="center",
                        color="white",
                        fontweight="bold",
                    )
            left = [a + b for a, b in zip(left, counts, strict=True)]
        ax.invert_yaxis()
        ax.set_xlim(0, 8)
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
        ax.set_title("A threshold crossing is not a validated arrival", loc="left", pad=48)
        fig.text(
            0.31,
            0.88,
            "Eight frozen settings per station · event window: origin to +30 h",
            fontsize=12,
        )
        ax.legend(
            loc="upper left", bbox_to_anchor=(-0.02, -0.035), ncol=2, frameon=False, fontsize=12
        )
        fig.text(
            0.03,
            0.035,
            "Sources: NOAA/NCEI DART; NOAA CO-OPS, NTWC/UHSLC and IOC coastal archives.\n"
            "Coastal inputs are raw tidal water levels; all crossings remain diagnostic.",
            fontsize=11,
        )
        fig.subplots_adjust(left=0.31, right=0.96, top=0.84, bottom=0.2)
        fig.savefig(output / "setting-status.png", dpi=120)
        fig.savefig(output / "setting-status.svg", metadata={"Date": None})
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(12, 6))
        dart = [p for p in profiles if p["station_type"] == "dart"]
        labels2: list[str] = []
        for i, profile in enumerate(dart):
            station_id = profile["station_id"]
            picks = [
                p
                for p in result["picks"]
                if p["station_id"] == station_id
                and p["window"] == "event"
                and p["status"] == "candidate"
            ]
            hours = [p["candidate_elapsed_seconds"] / 3600 for p in picks]
            summary = next(s for s in result["summaries"] if s["station_id"] == station_id)
            labels2.append(
                f"{profile['name']}\n~{profile['source_distance_km']:,.0f} km from origin"
            )
            if hours:
                lo, hi = min(hours), max(hours)
                ax.plot([lo, hi], [i, i], color="#176578", linewidth=4, marker="|")
                ax.scatter(hours, [i] * len(hours), color="#176578", s=30)  # pyright: ignore[reportUnknownMemberType]
                ax.annotate(
                    f" {len(picks)}/8 detect; {summary['control_crossings']}/8 control crossings",
                    (hi, i),
                    xytext=(8, 10),
                    textcoords="offset points",
                    fontsize=12,
                )
            else:
                ax.text(0.2, i, "0/8 detect", va="center")
        ax.set_yticks(range(len(dart)), labels2)
        ax.invert_yaxis()
        ax.set_xlim(0, 30)
        ax.set_ylim(len(dart) - 0.5, -0.6)
        ax.set_xlabel("Hours after earthquake origin (UTC)")
        ax.set_title(
            "DART settings give candidate times, not model discrepancies", loc="left", pad=25
        )
        fig.text(
            0.03,
            0.025,
            "Source: NOAA/NCEI DART residuals · lines span detected settings, not confidence intervals.\n"
            "Distance: WGS84 approximation; station datum unknown. No station modeled-arrival field exists.",
            fontsize=11,
        )
        fig.subplots_adjust(left=0.24, right=0.97, top=0.83, bottom=0.23)
        fig.savefig(output / "dart-candidates.png", dpi=120)
        fig.savefig(output / "dart-candidates.svg", metadata={"Date": None})
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(12, 6))
        waveform = result["early_waveform"]
        ax.plot(
            [r["minutes"] for r in waveform],
            [r["residual"] for r in waveform],
            color="#176578",
            linewidth=1.5,
        )
        near = [
            p["candidate_elapsed_seconds"] / 60
            for p in result["picks"]
            if p["station_id"] == "21418" and p["window"] == "event" and p["status"] == "candidate"
        ]
        ax.axvline(min(near), color="#9F4A12", linestyle=":")
        ax.axvline(25, color="#513A76", linestyle="--")
        ax.text(4, 1.7, f"Threshold candidate\n~{min(near):.2f} min", fontsize=13, color="#9F4A12")
        ax.text(
            26,
            1.7,
            "NOAA first-recording reference\napproximately 25 min",
            fontsize=13,
            color="#513A76",
        )
        ax.set(
            xlim=(-5, 60),
            xlabel="Minutes after earthquake origin (UTC)",
            ylabel="Publisher residual (m water column)",
        )
        ax.set_title(
            "A stable early crossing conflicts with NOAA’s tsunami timing", loc="left", pad=22
        )
        fig.text(
            0.03,
            0.025,
            "DART 21418 · NOAA/NCEI residuals; NOAA/PMEL/NCTR event-page reference.\n"
            "The reference is approximate, not a validated exact pick. Early signal mechanism is unclassified.",
            fontsize=11,
        )
        fig.subplots_adjust(left=0.1, right=0.97, top=0.83, bottom=0.23)
        fig.savefig(output / "early-crossing-check.png", dpi=120)
        fig.savefig(output / "early-crossing-check.svg", metadata={"Date": None})
        plt.close(fig)


def render_report(result: dict[str, Any], run_id: str, git_sha: str) -> str:
    """Result-dependent findings and follow-ups, retaining every station and failed setting."""
    lines = [
        "# Tōhoku shared EDA — timing support audit",
        "",
        f"Run `{run_id}` · implementation `{git_sha}` · frozen protocol `{result['settings']['protocol_version']}`.",
        "",
        "## Scope and disposition",
        "",
        "This completes the shared descriptive/sensitivity audit, not physical-arrival validation. "
        "The data proof needs **revision for arrival comparisons**. Descriptive coverage and preliminary "
        "story diagnostics are usable; community timing selection and modeled-minus-observed claims remain blocked.",
        "",
        f"Verified {result['counts']['observation']:,} accepted observations, "
        f"{result['counts']['station']} stations, {result['geometry']['parts']:,} contour parts and "
        f"{result['geometry']['vertices']:,} vertices against accepted hashes. "
        "All 17 acquired raw assets reconcile. The 18th asset, the continuous NCTR field, remains blocked.",
        "",
        "## All-station sensitivity results",
        "",
        "Eight frozen event settings and eight disjoint pre-origin controls per station. "
        "Coastal raw-water-level runs are unsupported controls, never arrival estimates. "
        "The spread is across successful settings only; failed settings remain visible and prevent promotion.",
        "",
        "| Station | Field | Detect / 8 | Control crossings / 8 | Unevaluable controls / 8 | Spread (s) | Screen |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in result["summaries"]:
        lines.append(
            f"| {row['station_id']} | {row['field']} | {row['detected_settings']} | "
            f"{row['control_crossings']} | {row['control_ineligible']} | {row['spread_seconds']} | "
            f"{'pass, unvalidated' if row['screen_pass'] else 'fail'} |"
        )
    lines += [
        "",
        "Even a passing screen would require independent onset validation. "
        "No physical-arrival or modeled-arrival timestamp is released. No maximum-wave, public-alert, "
        "evacuation or actionable-warning time is calculated.",
        "",
        "## Adaptive evidence ledger",
        "",
        "Observation → question → follow-up → decision; frozen detector settings were not retuned.",
        "",
    ]
    for profile, summary in zip(result["profiles"], result["summaries"], strict=True):
        lines.append(
            f"- **{profile['name']}**: {profile['long_intervals']} intervals exceed the declared "
            f"cadence limit; {profile['qc_flagged']} retained source-QC flags. "
            f"Follow-up: inspect the exact endpoints in `gaps.csv` and all candidate ±15-minute "
            f"source windows in `candidate-windows.csv`; {summary['control_crossings']}/8 "
            f"controls cross and {summary['control_ineligible']}/8 are unevaluable. "
            f"Decision: {summary['physical_arrival_status']}; "
            "do not use the threshold timestamp as a physical arrival."
        )
    lines += ["", "### Completed evidence-triggered follow-ups", ""]
    for finding in result["adaptive_ledger"]:
        lines.append(
            f"- **Observation:** {finding['observation']} **Question:** {finding['question']} "
            f"**Check:** {finding['follow_up']} **Evidence:** {finding['evidence']} "
            f"**Decision:** {finding['decision']}"
        )
    lines += [
        "",
        "The first exploratory run reported 231 residual-consistency exceedances at the "
        "0.00002 m boundary. Exact-decimal rechecking showed floating-point cancellation, not "
        "source disagreement. The corrected comparison and a regression test preserve the "
        "original tolerance; no detector setting or source value changed.",
    ]
    lines += [
        "",
        "## Distribution, fit, geometry, and join checks",
        "",
        "`profiles.csv` retains raw/fitted/residual extrema, medians, zeros, blanks and cadence histograms. "
        "Extremes are described, not silently trimmed; source-QC exclusions affect the detector only. "
        "Raw minus fitted is compared with the publisher residual using a 0.00002 m rounding tolerance.",
        "",
    ]
    for p in result["profiles"]:
        if p["station_type"] == "dart":
            lines.append(
                f"- {p['name']}: maximum |raw − fitted − residual| "
                f"{p['raw_minus_fit_minus_residual_max_abs']:.8g} m; "
                f"{p['residual_disagreement_above_0_00002_m']} rows exceed tolerance."
            )
    lines += [
        "",
        f"Contour audit: {result['geometry'].get('longitude_roundoff_vertices', 0)} boundary-roundoff "
        f"vertices; {result['geometry'].get('unsplit_longitude_jumps', 0)} unsplit >180° jumps. "
        "No geometry repaired, CRS overwritten, or datum inferred. Observation IDs and station–UTC "
        "keys are unique; station joins and source/unit/vertical-reference semantics reconcile.",
        "",
        "WGS84 source distances are descriptive approximations because all station horizontal datums "
        "are unknown. The DART timing-versus-distance figure shows candidate ranges, not travel speeds "
        "or modeled residuals. Hourly contours cannot supply a defensible station-arrival value; the "
        "continuous NCTR field remains unavailable, so its internal structure cannot be inspected.",
        "",
        "## Missingness remains part of this audit",
        "",
        "The existing missingness profiler is rerun on these exact inputs. See this run's "
        "`missingness-report.md` and `missingness/` tables for denominators, per-station continuity "
        "and the original adaptive ledger. Structural coastal fitted/residual blanks are not imputed. "
        "Upstream missing values, absent timestamps, quarantined sentinels and inaccessible assets remain "
        "distinct. MCAR/MAR/MNAR mechanisms are not identified from these records alone.",
        "",
        "## Takeaways and next steps",
        "",
        "1. Keep the preliminary atlas for source geography and coverage, with its existing chart-review caveats.",
        "2. Resolve an observed-onset method for the coastal tidal series and independently validate DART picks; "
        "do not choose stations by attractive agreement.",
        "3. Obtain an arrival-capable modeled product or approve a separately validated extraction method. "
        "Do not substitute nearest contours for the blocked field.",
        "4. Only after a new scientific review grants arrival-comparison permission should Stage B "
        "select communities and draft a timing-discrepancy story. Paper modeling stays separate.",
        "",
        "## Reproduction and evidence",
        "",
        "Run `scripts/run_tohoku_eda.py --help`. `meta.json` records the command, Git SHA, no-randomness "
        "policy and protocol; `inputs.json` anchors source/processed bytes; `outputs.json` hashes all "
        "stable outputs. `sensitivity.csv` includes every outcome and sampling bracket. Figures are "
        "diagnostics with CSV alternatives; the Marimo notebook only displays these outputs.",
        "",
    ]
    return "\n".join(lines)


def write_run(
    root: Path,
    processed: Path,
    anchor: Path,
    config: Path,
    output: Path,
    *,
    git_sha: str,
    run_id: str,
) -> dict[str, Any]:
    """Publish a complete new bundle only; refuse overwrite and clean failed staging."""
    if output.exists():
        raise FileExistsError(output)
    result = audit(root, processed, anchor, config)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".arrival-audit-", dir=output.parent) as temporary:
        stage = Path(temporary) / "bundle"
        stage.mkdir()
        for key, name in [
            ("profiles", "profiles"),
            ("picks", "sensitivity"),
            ("gaps", "gaps"),
            ("candidate_windows", "candidate-windows"),
            ("summaries", "station-decisions"),
            ("adaptive_ledger", "adaptive-ledger"),
            ("raw_traces", "raw-traces"),
            ("qc_records", "qc-records"),
            ("early_waveform", "early-waveform"),
        ]:
            write_csv(stage / f"{name}.csv", result[key])
        write_json(stage / "summary.json", result)
        write_json(stage / "inputs.json", result["inputs"])
        write_json(stage / "config.json", result["settings"])
        command = (
            f"uv run python scripts/run_tohoku_eda.py --output <new-directory> "
            f"--run-id {run_id} --git-sha {git_sha}"
        )
        write_json(
            stage / "meta.json",
            dict(
                run_id=run_id,
                git_sha=git_sha,
                command=command,
                randomness="none",
                disposition="revise_arrival_comparison",
            ),
        )
        profile = profile_missingness(
            processed,
            expected_windows=load_expected_windows(root / "config/tohoku-missingness.toml"),
        )
        write_missingness_artifacts(
            profile,
            artifact_dir=stage / "missingness",
            report_path=stage / "missingness-report.md",
            run_id=run_id,
            git_sha=git_sha,
            command=command,
        )
        (stage / "report.md").write_text(render_report(result, run_id, git_sha), encoding="utf-8")
        figures(result, stage)
        write_json(
            stage / "outputs.json",
            [
                {
                    "path": p.relative_to(stage).as_posix(),
                    "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                }
                for p in sorted(stage.rglob("*"))
                if p.is_file()
            ],
        )
        if output.exists():
            raise FileExistsError(output)
        stage.rename(output)
    return result
