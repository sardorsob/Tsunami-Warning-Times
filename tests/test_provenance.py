import csv
from pathlib import Path

import pytest

from pipeline.provenance import REQUIRED_COLUMNS, ManifestError, validate_manifest


def write_manifest(path: Path, **overrides: str) -> None:
    """Write one valid source row, replacing named values for negative tests."""
    row = {
        "source_id": "contest-rules",
        "title": "Contest rules",
        "publisher": "PacificVis",
        "url": "https://example.org/rules",
        "accessed_on": "2026-09-04",
        "status": "approved",
        "version_or_date": "2027 contest",
        "license_or_terms": "not applicable",
        "spatial_reference": "not applicable",
        "horizontal_datum": "not applicable",
        "vertical_datum": "not applicable",
        "coordinate_order": "not applicable",
        "temporal_reference": "not applicable",
        "units": "not applicable",
        "processing_level": "official rule page",
        "missingness": "not applicable",
        "sha256": "not-downloaded",
        "local_path": "not-downloaded",
        "notes": "Official contest page.",
    }
    row.update(overrides)
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerow(row)


def test_valid_manifest_returns_record_count(tmp_path: Path) -> None:
    manifest = tmp_path / "sources.csv"
    write_manifest(manifest)

    assert validate_manifest(manifest).records == 1


def test_manifest_rejects_an_unresolved_spatial_field(tmp_path: Path) -> None:
    manifest = tmp_path / "sources.csv"
    write_manifest(manifest, coordinate_order="")

    with pytest.raises(ManifestError, match="blank coordinate_order"):
        validate_manifest(manifest)


def test_manifest_requires_extended_iso_access_date(tmp_path: Path) -> None:
    manifest = tmp_path / "sources.csv"
    write_manifest(manifest, accessed_on="20260904")

    with pytest.raises(ManifestError, match="accessed_on must be YYYY-MM-DD"):
        validate_manifest(manifest)


def test_manifest_rejects_duplicate_source_ids(tmp_path: Path) -> None:
    manifest = tmp_path / "sources.csv"
    write_manifest(manifest)
    with manifest.open("a", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=REQUIRED_COLUMNS)
        writer.writerow(
            {
                "source_id": "contest-rules",
                "title": "Duplicate",
                "publisher": "PacificVis",
                "url": "https://example.org/duplicate",
                "accessed_on": "2026-09-04",
                "status": "candidate",
                "version_or_date": "2027 contest",
                "license_or_terms": "not applicable",
                "spatial_reference": "not applicable",
                "horizontal_datum": "not applicable",
                "vertical_datum": "not applicable",
                "coordinate_order": "not applicable",
                "temporal_reference": "not applicable",
                "units": "not applicable",
                "processing_level": "official rule page",
                "missingness": "not applicable",
                "sha256": "not-downloaded",
                "local_path": "not-downloaded",
                "notes": "Duplicate test row.",
            }
        )

    with pytest.raises(ManifestError, match="duplicate source_id"):
        validate_manifest(manifest)


@pytest.mark.parametrize(
    ("sha256", "local_path"),
    [
        ("a" * 64, "not-downloaded"),
        ("not-downloaded", "data/raw/source.nc"),
    ],
)
def test_manifest_rejects_inconsistent_download_state(
    tmp_path: Path, sha256: str, local_path: str
) -> None:
    manifest = tmp_path / "sources.csv"
    write_manifest(manifest, sha256=sha256, local_path=local_path)

    with pytest.raises(ManifestError, match="download state"):
        validate_manifest(manifest)


def test_manifest_rejects_local_path_traversal(tmp_path: Path) -> None:
    manifest = tmp_path / "sources.csv"
    write_manifest(manifest, sha256="a" * 64, local_path="../../outside.nc")

    with pytest.raises(ManifestError, match="repository-relative POSIX path"):
        validate_manifest(manifest)


def test_manifest_accepts_a_downloaded_asset(tmp_path: Path) -> None:
    manifest = tmp_path / "sources.csv"
    write_manifest(manifest, sha256="a" * 64, local_path="data/raw/source.nc")

    assert validate_manifest(manifest).records == 1
