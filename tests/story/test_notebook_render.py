"""Verify visible notebook output, not just successful execution."""

import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path


def test_populated_atlas_notebook_displays_figures_and_decisions(tmp_path: Path) -> None:
    notebook = tmp_path / "viewer.py"
    shutil.copyfile("notebooks/story/tohoku_storyboard_eda.py", notebook)
    run = tmp_path / "artifacts/eda/story/test"
    run.mkdir(parents=True)
    png = run / "fixture.png"
    png.write_bytes(
        base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j7XkAAAAASUVORK5CYII="
        )
    )
    artifacts = [
        dict(
            artifact_id=f"{name}_png",
            path=str(png),
            media_type="image/png",
            title=name,
            disposition="retain",
            finding="fixture finding",
            limitation="fixture limitation",
        )
        for name in (
            "01_pacific_evidence_map",
            "02_observation_coverage",
            "03_station_timeseries",
            "04_distance_contour_diagnostic",
        )
    ]
    (run / "atlas-manifest.json").write_text(
        json.dumps(
            dict(
                schema_version=1,
                run_id="test",
                lane="story",
                evidence_state="preliminary_storyboard_evidence",
                artifacts=artifacts,
            )
        ),
        encoding="utf-8",
    )
    (run / "decision-ledger.csv").write_text(
        "plot_id,disposition\nfixture,retain\n", encoding="utf-8"
    )
    subprocess.run(
        [
            sys.executable,
            "-m",
            "marimo",
            "export",
            "html",
            str(notebook),
            "-o",
            str(tmp_path / "viewer.html"),
            "--no-include-code",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        timeout=60,
    )
    session = json.loads((tmp_path / "__marimo__/session/viewer.py.json").read_text())
    rendered = json.dumps([cell["outputs"] for cell in session["cells"]])
    assert "Tōhoku" in rendered or "T\\u014dhoku" in rendered
    assert "Adaptive decision ledger" in rendered
    assert "01_pacific_evidence_map" in rendered
    assert "<img" in rendered
