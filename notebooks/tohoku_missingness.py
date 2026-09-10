import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def imports():
    import json
    from pathlib import Path
    from typing import cast

    import marimo as mo

    return Path, cast, json, mo


@app.cell
def title(mo):
    title_view = mo.md(
        """
        # Tōhoku missingness EDA

        This notebook is a reactive view over the script-generated missingness
        artifact. It performs no acquisition, transformation, imputation,
        timestamp snapping, or unique metric calculation.
        """
    )
    mo.show_code(title_view, position="above")
    return


@app.cell
def artifact_selector(mo):
    summary_path_input = mo.ui.text(
        value="artifacts/eda/missingness/missingness-summary.json",
        label="Missingness summary",
        full_width=True,
    )
    mo.show_code(summary_path_input, position="above")
    return (summary_path_input,)


@app.cell
def load_summary(Path, cast, json, mo, summary_path_input):
    resolved_summary_path = Path(summary_path_input.value)
    mo.stop(
        not resolved_summary_path.is_file(),
        mo.callout(
            f"Missing artifact: `{resolved_summary_path}`. Run "
            "`scripts/profile_missingness.py` first.",
            kind="warn",
        ),
    )
    summary_value = json.loads(resolved_summary_path.read_text(encoding="utf-8"))
    summary_data = cast(dict[str, object], summary_value)
    load_view = mo.callout(
        f"Loaded `{resolved_summary_path}`. The Markdown EDA report remains the "
        "canonical interpretation surface.",
        kind="info",
    )
    mo.show_code(load_view, position="above")
    return (summary_data,)


@app.cell
def headline_metrics(cast, mo, summary_data):
    headline_view = mo.hstack(
        [
            mo.stat(
                value=f"{cast(int, summary_data['observation_rows']):,}",
                label="Accepted observations",
            ),
            mo.stat(
                value=f"{cast(float, summary_data['raw_null_percent']):.4f}%",
                label="Raw-value nulls",
            ),
            mo.stat(
                value=(f"{cast(float, summary_data['coastal_strict_unavailable_percent']):.4f}%"),
                label="Strict coastal unavailability",
            ),
            mo.stat(
                value=f"{cast(int, summary_data['blocked_source_assets'])}/"
                f"{cast(int, summary_data['total_source_assets'])}",
                label="Blocked assets",
            ),
        ],
        widths="equal",
        gap=1,
    )
    mo.show_code(headline_view, position="above")
    return


@app.cell
def coastal_table(cast, mo, summary_data):
    coastal_rows = cast(list[dict[str, object]], summary_data["coastal_windows"])
    coastal_view = mo.vstack(
        [
            mo.md(
                """
                ## Coastal coverage

                Strict coverage requires an observation exactly on the
                source-supported minute grid. Sample-density coverage also
                counts valid off-grid source observations without moving them.
                """
            ),
            mo.ui.table(coastal_rows, pagination=False, show_column_summaries=False),
        ]
    )
    mo.show_code(coastal_view, position="above")
    return


@app.cell
def interpretation(mo):
    interpretation_view = mo.callout(
        mo.md(
            """
            **Interpretation:** pooled MCAR is not supported because missingness
            is concentrated by station and contiguous time. MAR is only a
            possible conditional assumption; MNAR cannot be excluded without
            publisher telemetry, maintenance, or QC evidence. Structural
            coastal fitted/residual blanks are not observations to impute.
            """
        ),
        kind="warn",
    )
    mo.show_code(interpretation_view, position="above")
    return


if __name__ == "__main__":
    app.run()
