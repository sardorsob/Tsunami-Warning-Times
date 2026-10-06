import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def imports():
    import json
    from pathlib import Path

    import marimo as mo

    return Path, json, mo


@app.cell
def title(mo):
    mo.output.replace(
        mo.md(
            "# Tōhoku timing-support audit\n\n"
            "Read-only view of script-generated evidence. "
            "Threshold crossings are not validated arrivals."
        )
    )
    return


@app.cell
def selector(Path, json, mo):
    _pointer = Path("context/EDA_RUN.json")
    _bundle = (
        json.loads(_pointer.read_text(encoding="utf-8"))["bundle"]
        if _pointer.is_file()
        else "artifacts/eda/shared/no-canonical-run"
    )
    run_path = mo.ui.text(
        value=_bundle,
        label="Audit run directory",
        full_width=True,
    )
    mo.output.replace(run_path)
    return (run_path,)


@app.cell
def evidence(Path, json, mo, run_path):
    folder = Path(run_path.value)
    mo.stop(
        not (folder / "summary.json").is_file(),
        mo.callout("Run scripts/run_tohoku_eda.py first.", kind="warn"),
    )
    summary = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
    mo.output.replace(
        mo.vstack(
            [
                mo.callout(
                    "Arrival comparison is unapproved; all ten stations remain in the denominator.",
                    kind="warn",
                ),
                mo.ui.table(summary["summaries"], pagination=False, show_column_summaries=False),
                mo.image(
                    src=str(folder / "setting-status.png"),
                    alt="Outcomes of all eight settings per station",
                ),
                mo.image(
                    src=str(folder / "dart-candidates.png"),
                    alt="DART diagnostic candidate ranges, not physical arrivals",
                ),
                mo.image(
                    src=str(folder / "early-crossing-check.png"),
                    alt="DART 21418 crossing conflicts with NOAA's approximate tsunami timing",
                ),
                mo.md((folder / "report.md").read_text(encoding="utf-8")),
            ]
        )
    )
    return


if __name__ == "__main__":
    app.run()
