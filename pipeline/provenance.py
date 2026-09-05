"""Validate the project's source-provenance manifest."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

REQUIRED_COLUMNS: tuple[str, ...] = (
    "source_id",
    "title",
    "publisher",
    "url",
    "accessed_on",
    "status",
    "version_or_date",
    "license_or_terms",
    "spatial_reference",
    "horizontal_datum",
    "vertical_datum",
    "coordinate_order",
    "temporal_reference",
    "units",
    "processing_level",
    "missingness",
    "sha256",
    "local_path",
    "notes",
)
ALLOWED_STATUSES = frozenset({"candidate", "approved", "rejected", "superseded"})


class ManifestError(ValueError):
    """Raised when the source manifest violates its documented contract."""


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Summary of a successful manifest validation."""

    records: int


def validate_manifest(path: Path) -> ValidationResult:
    """Validate required fields and basic provenance invariants in a CSV manifest."""
    try:
        with path.open(newline="", encoding="utf-8") as source_file:
            reader = csv.DictReader(source_file)
            fieldnames = tuple(reader.fieldnames or ())
            missing_columns = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
            if missing_columns:
                raise ManifestError(f"missing columns: {', '.join(missing_columns)}")

            errors: list[str] = []
            source_ids: set[str] = set()
            records = 0
            for row_number, row in enumerate(reader, start=2):
                records += 1
                values = {column: (row.get(column) or "").strip() for column in REQUIRED_COLUMNS}
                missing_values = [column for column, value in values.items() if not value]
                if missing_values:
                    errors.append(f"row {row_number}: blank {', '.join(missing_values)}")

                source_id = values["source_id"]
                if source_id in source_ids:
                    errors.append(f"row {row_number}: duplicate source_id {source_id!r}")
                source_ids.add(source_id)

                if values["status"] not in ALLOWED_STATUSES:
                    errors.append(f"row {row_number}: unsupported status {values['status']!r}")

                parsed_url = urlparse(values["url"])
                if parsed_url.scheme != "https" or not parsed_url.netloc:
                    errors.append(f"row {row_number}: url must be an absolute HTTPS URL")

                try:
                    accessed_on = date.fromisoformat(values["accessed_on"])
                    if accessed_on.isoformat() != values["accessed_on"]:
                        raise ValueError
                except ValueError:
                    errors.append(f"row {row_number}: accessed_on must be YYYY-MM-DD")

                digest = values["sha256"]
                if digest != "not-downloaded" and (
                    len(digest) != 64
                    or any(character not in "0123456789abcdef" for character in digest)
                ):
                    errors.append(
                        f"row {row_number}: sha256 must be lowercase hex or not-downloaded"
                    )

                local_path_value = values["local_path"]
                if (digest == "not-downloaded") != (local_path_value == "not-downloaded"):
                    errors.append(
                        f"row {row_number}: download state requires sha256 and local_path "
                        "to both be not-downloaded or both identify a downloaded asset"
                    )
                elif local_path_value != "not-downloaded":
                    local_path = PurePosixPath(local_path_value)
                    has_windows_drive = bool(local_path.parts) and ":" in local_path.parts[0]
                    if (
                        local_path.is_absolute()
                        or local_path.as_posix() != local_path_value
                        or local_path_value == "."
                        or ".." in local_path.parts
                        or "\\" in local_path_value
                        or has_windows_drive
                    ):
                        errors.append(
                            f"row {row_number}: local_path must be a normalized "
                            "repository-relative POSIX path"
                        )
    except OSError as error:
        raise ManifestError(f"could not read {path}: {error}") from error

    if errors:
        raise ManifestError("\n".join(errors))
    return ValidationResult(records=records)


def main() -> int:
    """Run manifest validation from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="CSV source manifest to validate")
    args = parser.parse_args()

    try:
        result = validate_manifest(args.path)
    except ManifestError as error:
        parser.error(str(error))

    print(f"Validated {result.records} source record(s) in {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
