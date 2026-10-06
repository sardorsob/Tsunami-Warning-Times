"""Real-input runner integration; requires the already accepted local data cache."""

import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from pipeline.eda_report import write_run

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data/processed/tohoku/2026-09-09-valparaiso-reviewed-7576ffb-a"
ANCHOR = ROOT / "artifacts/logs/runs/2026-09-09__1749__missingness__7b6d386/inputs.json"


@pytest.mark.skipif(not PROCESSED.exists(), reason="accepted local scientific cache unavailable")
def test_real_audit_is_deterministic_checksums_inputs_and_refuses_overwrite(tmp_path: Path) -> None:
    outputs = [tmp_path / name for name in ("one", "two")]
    for output in outputs:
        write_run(
            ROOT,
            PROCESSED,
            ANCHOR,
            ROOT / "config/tohoku-arrival-audit.toml",
            output,
            git_sha="test-sha",
            run_id="test-run",
        )
    files = sorted(p.relative_to(outputs[0]) for p in outputs[0].rglob("*") if p.is_file())
    assert files
    assert all((outputs[0] / p).read_bytes() == (outputs[1] / p).read_bytes() for p in files)
    summary = json.loads((outputs[0] / "summary.json").read_text())
    assert summary["counts"]["observation"] == 143655
    assert len(summary["summaries"]) == 10
    assert len(summary["picks"]) == 160
    assert len(summary["inputs"]) >= 25
    assert len(summary["adaptive_ledger"]) == 8
    assert len(summary["qc_records"]) == 140
    assert any(r["kind"] == "gap_sentinel" for r in summary["raw_traces"])
    assert all(p["residual_disagreement_above_0_00002_m"] == 0 for p in summary["profiles"])
    assert all(s["modeled_arrival_utc"] == "unavailable" for s in summary["summaries"])
    with pytest.raises(FileExistsError):
        write_run(
            ROOT,
            PROCESSED,
            ANCHOR,
            ROOT / "config/tohoku-arrival-audit.toml",
            outputs[0],
            git_sha="test-sha",
            run_id="test-run",
        )
    assert (outputs[0] / "summary.json").read_text() == (outputs[1] / "summary.json").read_text()


def test_bad_anchor_does_not_publish_partial_run(tmp_path: Path) -> None:
    anchor = tmp_path / "bad.json"
    anchor.write_text('[{"path":"config/tohoku-arrival-audit.toml","sha256":"bad"}]')
    with pytest.raises(ValueError, match="checksum"):
        write_run(
            ROOT,
            PROCESSED,
            anchor,
            ROOT / "config/tohoku-arrival-audit.toml",
            tmp_path / "output",
            git_sha="test",
            run_id="test",
        )
    assert not (tmp_path / "output").exists()


def test_populated_audit_notebook_exports_visible_evidence(tmp_path: Path) -> None:
    notebook = tmp_path / "viewer.py"
    shutil.copyfile(ROOT / "notebooks/tohoku_arrival_audit.py", notebook)
    run = tmp_path / "artifacts/eda/shared/test"
    run.mkdir(parents=True)
    (tmp_path / "context").mkdir()
    (tmp_path / "context/EDA_RUN.json").write_text(
        json.dumps({"bundle": "artifacts/eda/shared/test"})
    )
    stale = tmp_path / "artifacts/eda/shared/zz-stale"
    stale.mkdir()
    (stale / "summary.json").write_text("{}")
    (run / "summary.json").write_text(json.dumps({"summaries": [{"station_id": "test"}]}))
    (run / "report.md").write_text("# Fixture evidence report")
    png = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j7XkAAAAASUVORK5CYII="
    )
    for name in ["setting-status.png", "dart-candidates.png", "early-crossing-check.png"]:
        (run / name).write_bytes(png)
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
    output = json.dumps([cell["outputs"] for cell in session["cells"]])
    assert "Fixture evidence report" in output
    assert "Arrival comparison is unapproved" in output
    assert output.count("<img") == 3
