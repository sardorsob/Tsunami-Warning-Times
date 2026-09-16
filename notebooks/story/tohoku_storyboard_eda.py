import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def imports():
    import csv
    import json
    from pathlib import Path
    from typing import cast

    import marimo as mo

    return Path, cast, csv, json, mo


@app.cell
def title(mo):
    title_view = mo.md(
        """
        # Tōhoku visual-story diagnostic atlas

        This is a read-only reactive view over script-generated Stage A
        artifacts. It does not load normalized tables, calculate metrics,
        transform scientific records, render plots, or modify repository files.

        [Read the canonical story EDA report](../../context/story/EDA_REPORT.md)
        """
    )
    return (title_view,)


@app.cell
def discover_manifests(Path, mo):
    manifest_paths = tuple(
        sorted(Path("artifacts/eda/story").glob("*/atlas-manifest.json"))
    )
    manifest_options = {
        manifest_path.parent.name: manifest_path.as_posix()
        for manifest_path in manifest_paths
    }
    selected_run_label = next(iter(manifest_options), None)
    run_selector = mo.ui.dropdown(
        options=manifest_options,
        value=selected_run_label,
        label="Generated atlas run",
        full_width=True,
    )
    selector_view = mo.vstack(
        [
            mo.md("## Select generated evidence"),
            run_selector,
        ]
    )
    return manifest_paths, run_selector, selector_view


@app.cell
def require_manifest(Path, cast, manifest_paths, mo, run_selector):
    mo.stop(
        not manifest_paths,
        mo.callout(
            "No story atlas manifest exists under `artifacts/eda/story`. "
            "Run the reviewed atlas command before using this viewer.",
            kind="warn",
        ),
    )
    selected_manifest_path = Path(cast(str, run_selector.value))
    return (selected_manifest_path,)


@app.cell
def load_manifest(cast, json, mo, selected_manifest_path):
    manifest_value = json.loads(selected_manifest_path.read_text(encoding="utf-8"))
    mo.stop(
        not isinstance(manifest_value, dict),
        mo.callout("The selected manifest is not a JSON object.", kind="danger"),
    )
    manifest_data = cast(dict[str, object], manifest_value)
    required_manifest_fields = {"schema_version", "run_id", "lane", "evidence_state", "artifacts"}
    mo.stop(
        not required_manifest_fields.issubset(manifest_data),
        mo.callout("The selected manifest is missing required lineage fields.", kind="danger"),
    )
    mo.stop(
        manifest_data["lane"] != "story"
        or manifest_data["evidence_state"] != "preliminary_storyboard_evidence",
        mo.callout(
            "The selected manifest is not preliminary story-lane evidence.",
            kind="danger",
        ),
    )
    artifact_values = manifest_data["artifacts"]
    mo.stop(
        not isinstance(artifact_values, list),
        mo.callout("The selected manifest has no artifact list.", kind="danger"),
    )
    artifact_records = cast(list[dict[str, object]], artifact_values)
    return artifact_records, manifest_data


@app.cell
def evidence_boundary(manifest_data, mo, selected_manifest_path):
    boundary_view = mo.vstack(
        [
            mo.callout(
                f"Loaded `{selected_manifest_path}` with evidence state "
                f"`{manifest_data['evidence_state']}`.",
                kind="info",
            ),
            mo.callout(
                "The continuous NCTR field remains unavailable. Published "
                "hourly contours are not a continuous field, station panels "
                "use local scales, and Stage A makes no arrival or promotion claim.",
                kind="warn",
            ),
        ]
    )
    return (boundary_view,)


@app.cell
def generated_figures(Path, cast, artifact_records, mo):
    expected_plot_ids = (
        "01_pacific_evidence_map_png",
        "02_observation_coverage_png",
        "03_station_timeseries_png",
        "04_distance_contour_diagnostic_png",
    )
    png_records = {
        cast(str, record["artifact_id"]): record
        for record in artifact_records
        if record.get("media_type") == "image/png"
    }
    missing_plot_ids = tuple(
        plot_id for plot_id in expected_plot_ids if plot_id not in png_records
    )
    mo.stop(
        bool(missing_plot_ids),
        mo.callout(
            f"The selected manifest is missing PNG entries: {missing_plot_ids}",
            kind="danger",
        ),
    )
    figure_views = []
    for plot_id in expected_plot_ids:
        record = png_records[plot_id]
        image_path = Path(cast(str, record["path"]))
        figure_views.append(
            mo.vstack(
                [
                    mo.md(
                        f"## {cast(str, record['title'])}\n\n"
                        f"**Disposition:** `{cast(str, record['disposition'])}`  \n"
                        f"**Finding:** {cast(str, record['finding'])}  \n"
                        f"**Limitation:** {cast(str, record['limitation'])}"
                    ),
                    mo.image(
                        src=image_path.as_posix(),
                        alt=cast(str, record["title"]),
                        width="100%",
                    ),
                ]
            )
        )
    figures_view = mo.vstack(figure_views, gap=2)
    return (figures_view,)


@app.cell
def decision_ledger(cast, csv, mo, selected_manifest_path):
    decision_path = selected_manifest_path.parent / "decision-ledger.csv"
    mo.stop(
        not decision_path.is_file(),
        mo.callout(f"Missing decision ledger: `{decision_path}`.", kind="danger"),
    )
    with decision_path.open(newline="", encoding="utf-8") as decision_source:
        decision_rows = [
            cast(dict[str, object], row) for row in csv.DictReader(decision_source)
        ]
    decision_view = mo.vstack(
        [
            mo.md("## Adaptive decision ledger"),
            mo.ui.table(
                decision_rows,
                pagination=False,
                show_column_summaries=False,
            ),
            mo.md(
                "The ledger is generated evidence. Record review changes in the "
                "validated decision input and rebuild the atlas."
            ),
        ]
    )
    return (decision_view,)


if __name__ == "__main__":
    app.run()
