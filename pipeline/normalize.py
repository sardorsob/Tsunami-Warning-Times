"""Normalize checksummed Tōhoku source assets into explicit canonical records."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import shutil
import tempfile
import tomllib
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import cast

from pipeline.acquisition import ContractError, SourceContract, load_contracts

FDSN_EVENT_COLUMNS: tuple[str, ...] = (
    "time",
    "latitude",
    "longitude",
    "depth",
    "mag",
    "magType",
    "nst",
    "gap",
    "dmin",
    "rms",
    "net",
    "id",
    "updated",
    "place",
    "type",
    "horizontalError",
    "depthError",
    "magError",
    "magNst",
    "status",
    "locationSource",
    "magSource",
)
EPSG4326_LONGITUDE_TOLERANCE = 1e-8
DART_JULIAN_DAY_TOLERANCE = 1e-6
DART_UNDOCUMENTED_SENTINEL = 9999.0
IOC_QC_FLAGS: tuple[str, ...] = (
    "missing",
    "out_of_range",
    "spikes_via_median",
    "exceeded_neighbours",
    "flat_line",
    "distinctness",
    "completeness",
    "shift",
)


class NormalizationError(ValueError):
    """Raised when an asset cannot safely enter normalized outputs."""


@dataclass(frozen=True, slots=True)
class EventRecord:
    """One reviewed earthquake origin from the USGS FDSN service."""

    event_id: str
    origin_time_utc: str
    latitude: float
    longitude: float
    depth_km: float
    magnitude: float
    magnitude_type: str
    status: str


@dataclass(frozen=True, slots=True)
class TTTContourRecord:
    """One unmodified source line part from a travel-time contour."""

    contour_id: str
    source_object_id: int
    hours: float
    coordinates: tuple[tuple[float, float], ...]
    crs: str
    coordinate_order: str
    longitude_boundary_precision: bool
    crosses_antimeridian: bool


@dataclass(frozen=True, slots=True)
class RejectedRecord:
    """One source record excluded with a stable identity and reason code."""

    rejection_id: str
    source_id: str
    record_type: str
    reason_code: str
    detail: str


@dataclass(frozen=True, slots=True)
class StationRecord:
    """One configured DART deployment or coastal-gauge candidate."""

    station_id: str
    source_id: str
    station_type: str
    name: str
    latitude: float
    longitude: float
    availability: str
    units: str
    vertical_reference: str
    selection_role: str
    reason: str
    horizontal_datum: str
    coordinate_order: str
    time_basis: str


@dataclass(frozen=True, slots=True)
class ObservationRecord:
    """One source sample with raw time and interpreted UTC kept separate."""

    observation_id: str
    source_id: str
    station_id: str
    source_time: str
    observed_at_utc: str
    raw_value: float | None
    fitted_value: float | None
    residual_value: float | None
    source_extra: str | None
    units: str
    vertical_reference: str


@dataclass(frozen=True, slots=True)
class BuildResult:
    """Paths, row counts, checksums, and rejection counts from one build."""

    output_paths: dict[str, PurePosixPath]
    row_counts: dict[str, int]
    checksums: dict[str, str]
    rejection_counts: dict[str, int]


@dataclass(frozen=True, slots=True)
class _InventoryRecord:
    source_id: str
    status: str
    local_path: str
    bytes: int
    sha256: str
    reason: str


def _parse_utc(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise NormalizationError(f"invalid UTC timestamp {value!r}") from error
    if not value.endswith("Z") or parsed.utcoffset() is None:
        raise NormalizationError(f"invalid UTC timestamp {value!r}")
    return parsed


def normalize_event(path: Path, expected_id: str) -> EventRecord:
    """Validate and normalize exactly one reviewed USGS FDSN event row."""
    try:
        with path.open(newline="", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            if tuple(reader.fieldnames or ()) != FDSN_EVENT_COLUMNS:
                raise NormalizationError("event asset does not have the exact FDSN CSV schema")
            rows = list(reader)
    except OSError as error:
        raise NormalizationError(f"could not read event asset {path}: {error}") from error
    if len(rows) != 1:
        raise NormalizationError("event asset must contain exactly one event row")

    row = rows[0]
    if row["id"] != expected_id:
        raise NormalizationError(f"unexpected event ID {row['id']!r}")
    if row["status"] != "reviewed":
        raise NormalizationError("USGS event status is not reviewed")
    if row["magType"] != "mww":
        raise NormalizationError("USGS event magnitude type is not mww")
    _parse_utc(row["time"])
    try:
        latitude = float(row["latitude"])
        longitude = float(row["longitude"])
        depth_km = float(row["depth"])
        magnitude = float(row["mag"])
    except ValueError as error:
        raise NormalizationError(
            "event coordinates, depth, and magnitude must be numeric"
        ) from error
    if not all(math.isfinite(value) for value in (latitude, longitude, depth_km, magnitude)):
        raise NormalizationError("event coordinates, depth, and magnitude must be finite")
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise NormalizationError("event coordinates are outside EPSG:4326 bounds")

    return EventRecord(
        event_id=row["id"],
        origin_time_utc=row["time"],
        latitude=latitude,
        longitude=longitude,
        depth_km=depth_km,
        magnitude=magnitude,
        magnitude_type=row["magType"],
        status=row["status"],
    )


def _ttt_rejection(reference: str, reason: str, detail: str) -> RejectedRecord:
    return RejectedRecord(
        rejection_id=reference,
        source_id="ncei-ttt-tohoku-layer17-geojson",
        record_type="ttt_contour",
        reason_code=reason,
        detail=detail,
    )


def _feature_reference(feature: dict[str, object], index: int) -> tuple[int | None, str]:
    properties_value = feature.get("properties")
    if not isinstance(properties_value, dict):
        return None, f"ttt-feature-index-{index:06d}"
    properties = cast(dict[str, object], properties_value)
    object_id = properties.get("OBJECTID")
    if not isinstance(object_id, int) or isinstance(object_id, bool):
        return None, f"ttt-feature-index-{index:06d}"
    return object_id, f"ttt-feature-{object_id}"


def _coordinate_part(value: object) -> tuple[tuple[float, float], ...] | None:
    if not isinstance(value, list) or not value:
        return None
    coordinates: list[tuple[float, float]] = []
    for position_value in cast(list[object], value):
        if not isinstance(position_value, list):
            return None
        position = cast(list[object], position_value)
        if len(position) != 2:
            return None
        longitude, latitude = position
        if (
            not isinstance(longitude, (int, float))
            or isinstance(longitude, bool)
            or not isinstance(latitude, (int, float))
            or isinstance(latitude, bool)
        ):
            return None
        numeric = (float(longitude), float(latitude))
        if not all(math.isfinite(item) for item in numeric):
            return None
        coordinates.append(numeric)
    return tuple(coordinates) if len(coordinates) >= 2 else None


def normalize_ttt(path: Path) -> tuple[list[TTTContourRecord], list[RejectedRecord]]:
    """Explode valid EPSG:4326 TTT line parts without changing source coordinates."""
    try:
        document_value: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise NormalizationError(f"could not read TTT GeoJSON {path}: {error}") from error
    if not isinstance(document_value, dict):
        raise NormalizationError("TTT asset must be a GeoJSON FeatureCollection")
    document = cast(dict[str, object], document_value)
    if document.get("type") != "FeatureCollection":
        raise NormalizationError("TTT asset must be a GeoJSON FeatureCollection")
    raw_features = document.get("features")
    if not isinstance(raw_features, list):
        raise NormalizationError("TTT FeatureCollection must contain a features list")
    if not raw_features:
        raise NormalizationError("TTT FeatureCollection contains no features")

    records: list[TTTContourRecord] = []
    rejected: list[RejectedRecord] = []
    observed_object_ids: set[int] = set()
    for index, raw_feature in enumerate(cast(list[object], raw_features), start=1):
        if not isinstance(raw_feature, dict):
            rejected.append(
                _ttt_rejection(
                    f"ttt-feature-index-{index:06d}",
                    "malformed_feature",
                    "feature is not an object",
                )
            )
            continue
        feature = cast(dict[str, object], raw_feature)
        if feature.get("type") != "Feature":
            rejected.append(
                _ttt_rejection(
                    f"ttt-feature-index-{index:06d}",
                    "malformed_feature",
                    "feature type is not 'Feature'",
                )
            )
            continue
        object_id, feature_ref = _feature_reference(feature, index)
        if object_id is not None and object_id in observed_object_ids:
            rejected.append(
                _ttt_rejection(
                    f"ttt-duplicate-object-{object_id}-index-{index:06d}",
                    "duplicate_object_id",
                    f"OBJECTID {object_id} was already observed",
                )
            )
            continue
        if object_id is not None:
            observed_object_ids.add(object_id)
        properties_value = feature.get("properties")
        properties = (
            cast(dict[str, object], properties_value)
            if isinstance(properties_value, dict)
            else None
        )
        hours_value = properties.get("HOURS") if properties is not None else None
        if not isinstance(hours_value, (int, float)) or isinstance(hours_value, bool):
            rejected.append(_ttt_rejection(feature_ref, "missing_hours", "HOURS is not numeric"))
            continue
        hours = float(hours_value)
        if not math.isfinite(hours) or hours < 0:
            rejected.append(_ttt_rejection(feature_ref, "negative_hours", "HOURS is negative"))
            continue
        if object_id is None:
            rejected.append(
                _ttt_rejection(feature_ref, "missing_object_id", "OBJECTID is not an integer")
            )
            continue
        geometry_value = feature.get("geometry")
        if not isinstance(geometry_value, dict):
            rejected.append(_ttt_rejection(feature_ref, "empty_geometry", "geometry is absent"))
            continue
        geometry = cast(dict[str, object], geometry_value)
        geometry_type = geometry.get("type")
        raw_coordinates = geometry.get("coordinates")
        if geometry_type == "LineString":
            parts: list[object] = [raw_coordinates]
        elif geometry_type == "MultiLineString":
            if not isinstance(raw_coordinates, list) or not raw_coordinates:
                rejected.append(
                    _ttt_rejection(
                        feature_ref,
                        "empty_geometry",
                        "MultiLineString coordinates are absent or empty",
                    )
                )
                continue
            parts = cast(list[object], raw_coordinates)
        else:
            rejected.append(
                _ttt_rejection(feature_ref, "unsupported_geometry", f"type is {geometry_type!r}")
            )
            continue
        for part_index, raw_part in enumerate(parts, start=1):
            part_ref = f"ttt-{object_id}-part-{part_index:04d}"
            coordinates = _coordinate_part(raw_part)
            if coordinates is None:
                rejected.append(
                    _ttt_rejection(
                        part_ref, "empty_geometry_part", "line part is empty or malformed"
                    )
                )
                continue
            out_of_range = any(
                latitude < -90
                or latitude > 90
                or longitude < -180
                or longitude > 180 + EPSG4326_LONGITUDE_TOLERANCE
                for longitude, latitude in coordinates
            )
            if out_of_range:
                rejected.append(
                    _ttt_rejection(
                        part_ref,
                        "coordinate_out_of_range",
                        "coordinate exceeds documented EPSG:4326 bounds",
                    )
                )
                continue
            records.append(
                TTTContourRecord(
                    contour_id=part_ref,
                    source_object_id=object_id,
                    hours=hours,
                    coordinates=coordinates,
                    crs="EPSG:4326",
                    coordinate_order="longitude, latitude",
                    longitude_boundary_precision=any(
                        longitude > 180 for longitude, _ in coordinates
                    ),
                    crosses_antimeridian=any(
                        abs(right[0] - left[0]) > 180
                        for left, right in zip(coordinates, coordinates[1:], strict=False)
                    ),
                )
            )
    return records, rejected


def _station_rejection(
    station: StationRecord,
    reference: str,
    reason: str,
    detail: str,
    *,
    record_type: str = "observation",
) -> RejectedRecord:
    return RejectedRecord(
        rejection_id=reference,
        source_id=station.source_id,
        record_type=record_type,
        reason_code=reason,
        detail=detail,
    )


def _finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError("value is not finite")
    return parsed


def normalize_dart(
    path: Path, station: StationRecord
) -> tuple[list[ObservationRecord], list[RejectedRecord]]:
    """Normalize one NCEI DART file while retaining malformed rows as rejections."""
    if (
        station.station_type != "dart"
        or station.availability != "approved"
        or station.time_basis != "UTC"
        or station.units != "m water column"
        or station.vertical_reference != "unknown"
    ):
        raise NormalizationError(
            "normalize_dart requires an approved UTC DART station in m water column with "
            "unknown vertical reference"
        )
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise NormalizationError(f"could not read DART asset {path}: {error}") from error
    if not any(line.strip() for line in lines):
        raise NormalizationError("approved asset contains no DART rows")

    observations: list[ObservationRecord] = []
    rejected: list[RejectedRecord] = []
    observed_times: set[str] = set()
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        reference = f"dart-{station.station_id}-line-{line_number:06d}"
        values = line.split()
        if len(values) != 11:
            rejected.append(
                _station_rejection(
                    station, reference, "invalid_column_count", f"observed {len(values)} tokens"
                )
            )
            continue
        try:
            source_julian = _finite_float(values[0])
            year, month, day, hour, minute, second = (int(value) for value in values[1:7])
            observed = datetime(year, month, day, hour, minute, second, tzinfo=UTC)
            raw_value, fitted_value, residual_value = (
                _finite_float(value) for value in values[7:10]
            )
        except (ValueError, OverflowError) as error:
            rejected.append(
                _station_rejection(station, reference, "malformed_row", str(error))
            )
            continue
        if DART_UNDOCUMENTED_SENTINEL in (raw_value, fitted_value, residual_value):
            rejected.append(
                _station_rejection(
                    station,
                    reference,
                    "unexpected_sentinel",
                    "9999.0 appears in a named measurement field; publisher semantics are "
                    "undocumented, so the record is quarantined",
                )
            )
            continue
        expected_julian = observed.timetuple().tm_yday + (
            hour * 3600 + minute * 60 + second
        ) / 86400
        if abs(source_julian - expected_julian) > DART_JULIAN_DAY_TOLERANCE:
            rejected.append(
                _station_rejection(
                    station,
                    reference,
                    "julian_day_mismatch",
                    f"source {source_julian:.6f}; calendar {expected_julian:.6f}",
                )
            )
            continue
        observed_at_utc = observed.strftime("%Y-%m-%dT%H:%M:%SZ")
        if observed_at_utc in observed_times:
            rejected.append(
                _station_rejection(
                    station, reference, "duplicate_timestamp", observed_at_utc
                )
            )
            continue
        observed_times.add(observed_at_utc)
        observations.append(
            ObservationRecord(
                observation_id=f"{station.station_id}-{observed_at_utc}",
                source_id=station.source_id,
                station_id=station.station_id,
                source_time=values[0],
                observed_at_utc=observed_at_utc,
                raw_value=raw_value,
                fitted_value=fitted_value,
                residual_value=residual_value,
                source_extra=values[10],
                units=station.units,
                vertical_reference=station.vertical_reference,
            )
        )
    return observations, rejected


def normalize_coastal(
    path: Path, station: StationRecord
) -> tuple[list[ObservationRecord], list[RejectedRecord]]:
    """Normalize one GMT/metric/STND NOAA CO-OPS response without filling gaps."""
    if (
        station.station_type != "coastal"
        or station.availability != "approved"
        or station.units != "m"
        or station.vertical_reference != "STND"
        or station.time_basis != "GMT"
    ):
        raise NormalizationError(
            "normalize_coastal requires an approved coastal station with GMT and m/STND contract"
        )
    asset_reference = f"coastal-{station.station_id}-asset"

    def reject_asset(
        reason: str, detail: str
    ) -> tuple[list[ObservationRecord], list[RejectedRecord]]:
        return [], [
            _station_rejection(
                station,
                asset_reference,
                reason,
                detail,
                record_type="source_asset",
            )
        ]

    try:
        document_value: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise NormalizationError(f"could not read coastal asset {path}: {error}") from error
    if not isinstance(document_value, dict):
        return reject_asset("malformed_asset", "response is not a JSON object")
    document = cast(dict[str, object], document_value)
    if "error" in document:
        return reject_asset("api_error_asset", json.dumps(document["error"]))
    metadata_value = document.get("metadata")
    if not isinstance(metadata_value, dict):
        return reject_asset("station_metadata_mismatch", "metadata is absent")
    metadata = cast(dict[str, object], metadata_value)
    try:
        metadata_id = str(metadata["id"])
        metadata_latitude = _finite_float(str(metadata["lat"]))
        metadata_longitude = _finite_float(str(metadata["lon"]))
    except (KeyError, ValueError) as error:
        return reject_asset("station_metadata_mismatch", str(error))
    if (
        metadata_id != station.station_id
        or abs(metadata_latitude - station.latitude) > 1e-6
        or abs(metadata_longitude - station.longitude) > 1e-6
    ):
        return reject_asset(
            "station_metadata_mismatch",
            "response station ID or coordinates differ from configuration",
        )
    raw_data_value = document.get("data")
    if not isinstance(raw_data_value, list):
        return reject_asset("malformed_asset", "data is not a list")
    if not raw_data_value:
        raise NormalizationError("approved asset contains no CO-OPS rows")
    raw_data = cast(list[object], raw_data_value)

    observations: list[ObservationRecord] = []
    rejected: list[RejectedRecord] = []
    observed_times: set[str] = set()
    for row_number, raw_row_value in enumerate(raw_data, start=1):
        reference = f"coastal-{station.station_id}-row-{row_number:06d}"
        if not isinstance(raw_row_value, dict):
            rejected.append(
                _station_rejection(station, reference, "malformed_row", "row is not an object")
            )
            continue
        raw_row = cast(dict[str, object], raw_row_value)
        source_time = raw_row.get("t")
        if not isinstance(source_time, str):
            rejected.append(
                _station_rejection(station, reference, "malformed_timestamp", "t is not text")
            )
            continue
        try:
            observed = datetime.strptime(source_time, "%Y-%m-%d %H:%M").replace(tzinfo=UTC)
        except ValueError as error:
            rejected.append(
                _station_rejection(station, reference, "malformed_timestamp", str(error))
            )
            continue
        observed_at_utc = observed.strftime("%Y-%m-%dT%H:%M:%SZ")
        if observed_at_utc in observed_times:
            rejected.append(
                _station_rejection(
                    station, reference, "duplicate_timestamp", observed_at_utc
                )
            )
            continue
        value = raw_row.get("v")
        try:
            raw_value = None if value in {None, ""} else _finite_float(str(value))
        except (TypeError, ValueError) as error:
            rejected.append(
                _station_rejection(station, reference, "malformed_value", str(error))
            )
            continue
        observed_times.add(observed_at_utc)
        observations.append(
            ObservationRecord(
                observation_id=f"{station.station_id}-{observed_at_utc}",
                source_id=station.source_id,
                station_id=station.station_id,
                source_time=source_time,
                observed_at_utc=observed_at_utc,
                raw_value=raw_value,
                fitted_value=None,
                residual_value=None,
                source_extra=None,
                units=station.units,
                vertical_reference=station.vertical_reference,
            )
        )
    return observations, rejected


def normalize_ioc_valparaiso(
    path: Path, station: StationRecord
) -> tuple[list[ObservationRecord], list[RejectedRecord]]:
    """Normalize the explicit IOC Valparaíso radar response and retain its QC flags."""
    if (
        station.station_type != "coastal"
        or station.availability != "approved"
        or station.station_id != "valp"
        or station.units != "m"
        or station.vertical_reference != "unknown"
        or station.time_basis != "UTC"
    ):
        raise NormalizationError(
            "normalize_ioc_valparaiso requires the approved valp coastal station with "
            "UTC, metres, and unknown vertical reference"
        )
    asset_reference = "coastal-valp-asset"

    def reject_asset(
        reason: str, detail: str
    ) -> tuple[list[ObservationRecord], list[RejectedRecord]]:
        return [], [
            _station_rejection(
                station,
                asset_reference,
                reason,
                detail,
                record_type="source_asset",
            )
        ]

    try:
        document_value: object = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise NormalizationError(f"could not read IOC coastal asset {path}: {error}") from error
    except json.JSONDecodeError as error:
        return reject_asset("malformed_asset", str(error))
    if not isinstance(document_value, dict):
        return reject_asset("malformed_asset", "response is not a JSON object")
    document = cast(dict[str, object], document_value)
    data_value = document.get("data")
    pagination_value = document.get("pagination")
    if not isinstance(data_value, list):
        return reject_asset("malformed_asset", "data is not a list")
    if not data_value:
        raise NormalizationError("approved asset contains no IOC coastal rows")
    if not isinstance(pagination_value, dict):
        return reject_asset("pagination_mismatch", "pagination is absent")
    pagination = cast(dict[str, object], pagination_value)
    expected_pagination: dict[str, object] = {
        "total_days": 3,
        "current_page": 1,
        "total_pages": 1,
        "next_page": None,
        "prev_page": None,
    }
    if any(pagination.get(key) != value for key, value in expected_pagination.items()):
        return reject_asset(
            "pagination_mismatch",
            "response does not cover the contracted three-day single-page request",
        )
    data = cast(list[object], data_value)
    if any(
        not isinstance(row, dict) or cast(dict[str, object], row).get("sensor") != "rad"
        for row in data
    ):
        return reject_asset("sensor_mismatch", "response contains a non-rad sensor row")

    observations: list[ObservationRecord] = []
    candidates: list[tuple[int, str, ObservationRecord]] = []
    indexed_rejections: list[tuple[int, RejectedRecord]] = []
    for row_number, row_value in enumerate(data, start=1):
        row = cast(dict[str, object], row_value)
        reference = f"coastal-valp-row-{row_number:06d}"
        source_time = row.get("stime")
        if not isinstance(source_time, str):
            indexed_rejections.append(
                (
                    row_number,
                    _station_rejection(
                        station, reference, "malformed_timestamp", "stime is not text"
                    ),
                )
            )
            continue
        try:
            observed = datetime.strptime(source_time, "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=UTC
            )
        except ValueError as error:
            indexed_rejections.append(
                (
                    row_number,
                    _station_rejection(
                        station, reference, "malformed_timestamp", str(error)
                    ),
                )
            )
            continue
        qc = {name: row.get(name) for name in IOC_QC_FLAGS}
        if any(value not in {"F", "T"} for value in qc.values()):
            indexed_rejections.append(
                (
                    row_number,
                    _station_rejection(
                        station,
                        reference,
                        "malformed_row",
                        "QC flags must all be F or T",
                    ),
                )
            )
            continue
        value = row.get("slevel")
        try:
            raw_value = None if value == "NA" else _finite_float(str(value))
        except (TypeError, ValueError) as error:
            indexed_rejections.append(
                (
                    row_number,
                    _station_rejection(station, reference, "malformed_value", str(error)),
                )
            )
            continue
        observed_at_utc = observed.strftime("%Y-%m-%dT%H:%M:%SZ")
        extra = {"sensor": "rad", **qc}
        candidates.append(
            (
                row_number,
                reference,
                ObservationRecord(
                    observation_id=f"{station.station_id}-{observed_at_utc}",
                    source_id=station.source_id,
                    station_id=station.station_id,
                    source_time=source_time,
                    observed_at_utc=observed_at_utc,
                    raw_value=raw_value,
                    fitted_value=None,
                    residual_value=None,
                    source_extra=json.dumps(extra, sort_keys=True, separators=(",", ":")),
                    units=station.units,
                    vertical_reference=station.vertical_reference,
                ),
            )
        )

    timestamp_counts = Counter(record.observed_at_utc for _, _, record in candidates)
    for row_number, reference, record in candidates:
        duplicate_count = timestamp_counts[record.observed_at_utc]
        if duplicate_count > 1:
            indexed_rejections.append(
                (
                    row_number,
                    _station_rejection(
                        station,
                        reference,
                        "duplicate_timestamp",
                        f"{record.observed_at_utc}; all {duplicate_count} rows quarantined",
                    ),
                )
            )
        else:
            observations.append(record)
    rejected = [record for _, record in sorted(indexed_rejections, key=lambda item: item[0])]
    return observations, rejected


def normalize_ntwc_saipan(
    path: Path, station: StationRecord
) -> tuple[list[ObservationRecord], list[RejectedRecord]]:
    """Normalize one checksummed NTWC event-archive coastal text file."""
    if (
        station.station_type != "coastal"
        or station.availability != "approved"
        or station.units != "m"
        or station.vertical_reference != "MLLW"
        or station.time_basis != "UTC"
    ):
        raise NormalizationError(
            "normalize_ntwc_saipan requires an approved coastal station with UTC and m/MLLW"
        )
    asset_reference = f"coastal-{station.station_id}-asset"

    def reject_asset(detail: str) -> tuple[list[ObservationRecord], list[RejectedRecord]]:
        return [], [
            _station_rejection(
                station,
                asset_reference,
                "source_header_mismatch",
                detail,
                record_type="source_asset",
            )
        ]

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise NormalizationError(f"could not read NTWC coastal asset {path}: {error}") from error
    if len(lines) < 5:
        return reject_asset("expected four header lines and at least one sample")

    identity = lines[0].split()
    measurement = lines[1].split()
    if (
        len(identity) != 7
        or identity[:4] != ["Saipan,_USA", "none", "UHSLC", "Continuous"]
        or identity[6] != "20110311"
        or len(measurement) != 8
        or measurement != ["NGWLMS", "m", "UTC", "1", "min", "MLLW", "NTWC", "Unfiltered"]
        or lines[2] != "1_minute_data_via_GOES"
        or lines[3]
        != "Data Format: SampleTime(epochal 1/1/1970)  WaterLevel  SampleTime(yyymmddhhmmss)"
    ):
        return reject_asset(
            "identity, measurement, or format header differs from the accepted contract"
        )
    try:
        latitude = _finite_float(identity[4])
        longitude = _finite_float(identity[5])
    except ValueError as error:
        return reject_asset(str(error))
    if abs(latitude - station.latitude) > 1e-6 or abs(longitude - station.longitude) > 1e-6:
        return reject_asset("source coordinates differ from configuration")

    observations: list[ObservationRecord] = []
    candidates: list[tuple[int, str, ObservationRecord]] = []
    indexed_rejections: list[tuple[int, RejectedRecord]] = []
    for row_number, line in enumerate(lines[4:], start=1):
        reference = f"coastal-{station.station_id}-row-{row_number:06d}"
        values = line.split()
        if len(values) != 3:
            indexed_rejections.append(
                (
                    row_number,
                    _station_rejection(
                        station, reference, "malformed_row", "expected three fields"
                    ),
                )
            )
            continue
        epoch_text, raw_value_text, source_time = values
        try:
            epoch = int(epoch_text)
            observed = datetime.strptime(source_time, "%Y%m%d%H%M%S").replace(tzinfo=UTC)
            raw_value = _finite_float(raw_value_text)
        except ValueError as error:
            indexed_rejections.append(
                (
                    row_number,
                    _station_rejection(station, reference, "malformed_row", str(error)),
                )
            )
            continue
        try:
            epoch_time = datetime.fromtimestamp(epoch, tz=UTC)
        except (OSError, OverflowError, ValueError) as error:
            indexed_rejections.append(
                (
                    row_number,
                    _station_rejection(
                        station, reference, "malformed_timestamp", str(error)
                    ),
                )
            )
            continue
        if epoch_time != observed:
            indexed_rejections.append(
                (
                    row_number,
                    _station_rejection(
                        station,
                        reference,
                        "timestamp_mismatch",
                        f"epoch {epoch_text} differs from calendar time {source_time}",
                    ),
                )
            )
            continue
        observed_at_utc = observed.strftime("%Y-%m-%dT%H:%M:%SZ")
        candidates.append(
            (
                row_number,
                reference,
                ObservationRecord(
                    observation_id=f"{station.station_id}-{observed_at_utc}",
                    source_id=station.source_id,
                    station_id=station.station_id,
                    source_time=source_time,
                    observed_at_utc=observed_at_utc,
                    raw_value=raw_value,
                    fitted_value=None,
                    residual_value=None,
                    source_extra=f"epoch={epoch_text}",
                    units=station.units,
                    vertical_reference=station.vertical_reference,
                ),
            )
        )

    timestamp_counts = Counter(record.observed_at_utc for _, _, record in candidates)
    for row_number, reference, record in candidates:
        duplicate_count = timestamp_counts[record.observed_at_utc]
        if duplicate_count > 1:
            indexed_rejections.append(
                (
                    row_number,
                    _station_rejection(
                        station,
                        reference,
                        "duplicate_timestamp",
                        f"{record.observed_at_utc}; all {duplicate_count} rows quarantined",
                    ),
                )
            )
        else:
            observations.append(record)
    rejected = [record for _, record in sorted(indexed_rejections, key=lambda item: item[0])]
    return observations, rejected


def _sha256(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            size += len(chunk)
            digest.update(chunk)
    return size, digest.hexdigest()


def _load_inventory(path: Path) -> dict[str, _InventoryRecord]:
    try:
        document_value: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise NormalizationError(f"could not read raw inventory {path}: {error}") from error
    if not isinstance(document_value, list):
        raise NormalizationError("raw inventory must be a JSON list")
    document = cast(list[object], document_value)
    records: dict[str, _InventoryRecord] = {}
    for index, raw_record_value in enumerate(document, start=1):
        if not isinstance(raw_record_value, dict):
            raise NormalizationError(f"raw inventory row {index} is not an object")
        raw_record = cast(dict[str, object], raw_record_value)
        try:
            source_id = raw_record["source_id"]
            status = raw_record["status"]
            local_path = raw_record["local_path"]
            byte_count = raw_record["bytes"]
            sha256 = raw_record["sha256"]
            reason = raw_record["reason"]
        except KeyError as error:
            raise NormalizationError(
                f"raw inventory row {index} is missing {error.args[0]!r}"
            ) from error
        if (
            not all(
                isinstance(value, str)
                for value in (source_id, status, local_path, sha256, reason)
            )
            or not isinstance(byte_count, int)
            or isinstance(byte_count, bool)
            or byte_count < 0
        ):
            raise NormalizationError(f"raw inventory row {index} has invalid field types")
        if source_id in records:
            raise NormalizationError(f"raw inventory has duplicate source_id {source_id!r}")
        records[cast(str, source_id)] = _InventoryRecord(
            source_id=cast(str, source_id),
            status=cast(str, status),
            local_path=cast(str, local_path),
            bytes=byte_count,
            sha256=cast(str, sha256),
            reason=cast(str, reason),
        )
    return records


def _verify_inventory(
    contracts: tuple[SourceContract, ...], inventory: dict[str, _InventoryRecord], root: Path
) -> dict[str, Path]:
    contract_ids = {contract.source_id for contract in contracts}
    if set(inventory) != contract_ids:
        raise NormalizationError("raw inventory source IDs differ from the source contract")
    verified: dict[str, Path] = {}
    for contract in contracts:
        item = inventory[contract.source_id]
        if contract.availability == "blocked":
            if (
                item.status != "blocked"
                or item.local_path != "not-downloaded"
                or item.sha256 != "not-downloaded"
                or item.bytes != 0
            ):
                raise NormalizationError(
                    f"blocked source {contract.source_id!r} has inconsistent inventory state"
                )
            continue
        if item.status not in {"cached", "downloaded"}:
            raise NormalizationError(
                f"approved source {contract.source_id!r} is not present in raw inventory"
            )
        if item.local_path != contract.local_path.as_posix():
            raise NormalizationError(f"raw path mismatch for {contract.source_id!r}")
        raw_path = root / contract.local_path
        try:
            resolved_path = raw_path.resolve(strict=True)
        except OSError as error:
            raise NormalizationError(
                f"raw asset is unavailable for {contract.source_id!r}"
            ) from error
        if not resolved_path.is_relative_to(root) or not resolved_path.is_file():
            raise NormalizationError(
                f"raw asset path escapes the build root for {contract.source_id!r}"
            )
        sidecar_path = raw_path.with_name(f"{raw_path.name}.sha256")
        try:
            resolved_sidecar = sidecar_path.resolve(strict=True)
        except OSError as error:
            raise NormalizationError(
                f"checksum sidecar is unavailable for {contract.source_id!r}"
            ) from error
        if not resolved_sidecar.is_relative_to(root) or not resolved_sidecar.is_file():
            raise NormalizationError(
                f"checksum sidecar escapes the build root for {contract.source_id!r}"
            )
        try:
            size, digest = _sha256(resolved_path)
            sidecar = resolved_sidecar.read_text(encoding="utf-8").strip()
        except OSError as error:
            raise NormalizationError(
                f"could not verify raw checksum for {contract.source_id!r}: {error}"
            ) from error
        if size != item.bytes or digest != item.sha256 or sidecar != digest:
            raise NormalizationError(f"raw checksum mismatch for {contract.source_id!r}")
        verified[contract.source_id] = resolved_path
    return verified


def _load_stations(
    document: dict[str, object], contracts: tuple[SourceContract, ...]
) -> tuple[StationRecord, ...]:
    raw_stations_value = document.get("stations")
    if not isinstance(raw_stations_value, dict):
        raise NormalizationError("source contract is missing parseable [stations] metadata")
    raw_stations = cast(dict[str, object], raw_stations_value)
    contracts_by_id = {contract.source_id: contract for contract in contracts}
    expected_sources = {
        contract.source_id
        for contract in contracts
        if contract.source_class
        in {"DART observation time series", "coastal water-level observation"}
    }
    stations: list[StationRecord] = []
    station_ids: set[str] = set()
    source_ids: set[str] = set()
    required_text = (
        "source_id",
        "station_id",
        "station_type",
        "name",
        "units",
        "vertical_reference",
        "selection_role",
        "time_basis",
    )
    for name, raw_values_value in raw_stations.items():
        if not isinstance(raw_values_value, dict):
            raise NormalizationError(f"station {name!r} is not a TOML table")
        raw_values = cast(dict[str, object], raw_values_value)
        if any(not isinstance(raw_values.get(field), str) for field in required_text):
            raise NormalizationError(f"station {name!r} has missing text metadata")
        source_id = cast(str, raw_values["source_id"])
        station_id = cast(str, raw_values["station_id"])
        station_type = cast(str, raw_values["station_type"])
        if source_id in source_ids or station_id in station_ids:
            raise NormalizationError("station IDs and station source IDs must be unique")
        contract = contracts_by_id.get(source_id)
        expected_type = (
            "dart"
            if contract and contract.source_class == "DART observation time series"
            else "coastal"
        )
        if contract is None or source_id not in expected_sources or station_type != expected_type:
            raise NormalizationError(f"station {name!r} does not match its source contract")
        latitude = raw_values.get("latitude")
        longitude = raw_values.get("longitude")
        if (
            not isinstance(latitude, (int, float))
            or isinstance(latitude, bool)
            or not isinstance(longitude, (int, float))
            or isinstance(longitude, bool)
            or not math.isfinite(float(latitude))
            or not math.isfinite(float(longitude))
            or not -90 <= float(latitude) <= 90
            or not -180 <= float(longitude) <= 180
        ):
            raise NormalizationError(f"station {name!r} has invalid coordinates")
        source_ids.add(source_id)
        station_ids.add(station_id)
        stations.append(
            StationRecord(
                station_id=station_id,
                source_id=source_id,
                station_type=station_type,
                name=cast(str, raw_values["name"]),
                latitude=float(latitude),
                longitude=float(longitude),
                availability=contract.availability,
                units=cast(str, raw_values["units"]),
                vertical_reference=cast(str, raw_values["vertical_reference"]),
                selection_role=cast(str, raw_values["selection_role"]),
                reason=contract.reason,
                horizontal_datum=contract.horizontal_datum,
                coordinate_order=contract.coordinate_order,
                time_basis=cast(str, raw_values["time_basis"]),
            )
        )
    if source_ids != expected_sources:
        raise NormalizationError("station metadata does not cover every DART and coastal candidate")
    return tuple(sorted(stations, key=lambda station: station.station_id))


def _load_config_document(path: Path) -> dict[str, object]:
    try:
        return cast(dict[str, object], tomllib.loads(path.read_text(encoding="utf-8")))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise NormalizationError(f"could not read build configuration: {error}") from error


def _validate_ttt_metadata(path: Path) -> None:
    try:
        document_value: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise NormalizationError(f"TTT metadata is not readable JSON: {error}") from error
    if not isinstance(document_value, dict):
        raise NormalizationError("TTT metadata must be a JSON object")
    document = cast(dict[str, object], document_value)
    extent_value = document.get("extent")
    extent = cast(dict[str, object], extent_value) if isinstance(extent_value, dict) else {}
    reference_value = extent.get("spatialReference")
    reference = (
        cast(dict[str, object], reference_value) if isinstance(reference_value, dict) else {}
    )
    if (
        document.get("name") != "2011/3/11 Tohoku, Japan"
        or document.get("geometryType") != "esriGeometryPolyline"
        or reference.get("wkid") != 4326
    ):
        raise NormalizationError(
            "TTT metadata does not match the Tohoku polyline layer in WKID 4326"
        )


TTT_FEATURE_REJECTION_CODES = frozenset(
    {
        "malformed_feature",
        "duplicate_object_id",
        "missing_hours",
        "negative_hours",
        "missing_object_id",
        "empty_geometry",
        "unsupported_geometry",
    }
)
TTT_PART_REJECTION_CODES = frozenset({"empty_geometry_part", "coordinate_out_of_range"})


def _ttt_source_accounting(
    path: Path, contours: list[TTTContourRecord], rejected: list[RejectedRecord]
) -> dict[str, object]:
    try:
        document_value: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise NormalizationError(f"could not reconcile TTT input: {error}") from error
    if not isinstance(document_value, dict):
        raise NormalizationError("could not reconcile TTT input object")
    document = cast(dict[str, object], document_value)
    features_value = document.get("features")
    if not isinstance(features_value, list):
        raise NormalizationError("could not reconcile TTT feature input")
    raw_features = cast(list[object], features_value)
    feature_input = len(raw_features)
    part_input = 0
    for raw_feature in raw_features:
        if not isinstance(raw_feature, dict):
            continue
        geometry_value = cast(dict[str, object], raw_feature).get("geometry")
        if not isinstance(geometry_value, dict):
            continue
        geometry = cast(dict[str, object], geometry_value)
        coordinates_value = geometry.get("coordinates")
        if geometry.get("type") == "LineString":
            part_input += 1
        elif geometry.get("type") == "MultiLineString" and isinstance(
            coordinates_value, list
        ):
            part_input += len(cast(list[object], coordinates_value))

    unknown_rejections = {
        record.reason_code
        for record in rejected
        if record.reason_code
        not in TTT_FEATURE_REJECTION_CODES | TTT_PART_REJECTION_CODES
    }
    if unknown_rejections:
        raise NormalizationError(
            f"TTT accounting has unknown rejection codes: {sorted(unknown_rejections)}"
        )
    feature_rejected = sum(
        record.reason_code in TTT_FEATURE_REJECTION_CODES for record in rejected
    )
    part_rejected = sum(record.reason_code in TTT_PART_REJECTION_CODES for record in rejected)
    feature_accepted = feature_input - feature_rejected
    part_accepted = len(contours)
    unparsed_parts = part_input - part_accepted - part_rejected
    if feature_accepted < 0 or feature_input != feature_accepted + feature_rejected:
        raise NormalizationError("TTT feature accounting does not reconcile")
    if unparsed_parts < 0:
        raise NormalizationError("TTT part accounting does not reconcile")
    return {
        "input_count": feature_input,
        "accepted_count": feature_accepted,
        "rejected_count": feature_rejected,
        "output_count": part_accepted,
        "feature_accounting": {
            "input": feature_input,
            "accepted": feature_accepted,
            "rejected": feature_rejected,
        },
        "part_accounting": {
            "input": part_input,
            "accepted": part_accepted,
            "rejected": part_rejected,
            "not_parsed_due_to_feature_rejection": unparsed_parts,
            "output": part_accepted,
        },
    }


def _dart_input_count(path: Path) -> int:
    try:
        return sum(bool(line.strip()) for line in path.read_text(encoding="utf-8").splitlines())
    except OSError as error:
        raise NormalizationError(f"could not reconcile DART input: {error}") from error


def _coastal_input_count(path: Path, rejected: list[RejectedRecord]) -> int:
    if any(record.record_type == "source_asset" for record in rejected):
        return 1
    try:
        document_value: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise NormalizationError(f"could not reconcile CO-OPS input: {error}") from error
    if not isinstance(document_value, dict):
        raise NormalizationError("could not reconcile CO-OPS input object")
    data_value = cast(dict[str, object], document_value).get("data")
    if not isinstance(data_value, list):
        raise NormalizationError("could not reconcile CO-OPS data rows")
    return len(cast(list[object], data_value))


def _ntwc_coastal_input_count(path: Path, rejected: list[RejectedRecord]) -> int:
    if any(record.record_type == "source_asset" for record in rejected):
        return 1
    try:
        return max(0, len(path.read_text(encoding="utf-8").splitlines()) - 4)
    except OSError as error:
        raise NormalizationError(f"could not reconcile NTWC coastal input: {error}") from error


def _observation_source_accounting(
    input_count: int,
    accepted: list[ObservationRecord],
    rejected: list[RejectedRecord],
) -> dict[str, object]:
    if input_count != len(accepted) + len(rejected):
        raise NormalizationError("observation source accounting does not reconcile")
    return {
        "input_count": input_count,
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "output_count": len(accepted),
    }


def _csv_value(value: object) -> object:
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, tuple):
        return json.dumps(value, separators=(",", ":"))
    return value


def _write_csv(path: Path, columns: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: _csv_value(row[column]) for column in columns})


SCHEMAS: dict[str, object] = {
    "event": {
        "grain": "one reviewed earthquake origin",
        "primary_key": ["event_id"],
        "crs": "EPSG:4326 longitude/latitude stored in separate columns",
        "fields": {
            "event_id": {"type": "string", "nullable": False},
            "origin_time_utc": {"type": "UTC timestamp", "nullable": False},
            "latitude": {"type": "number", "units": "degrees north", "nullable": False},
            "longitude": {"type": "number", "units": "degrees east", "nullable": False},
            "depth_km": {"type": "number", "units": "km", "nullable": False},
            "magnitude": {"type": "number", "nullable": False},
            "magnitude_type": {"type": "string", "nullable": False},
            "status": {"type": "string", "nullable": False},
        },
    },
    "ttt_contour": {
        "grain": "one source contour line part",
        "primary_key": ["contour_id"],
        "crs": "EPSG:4326",
        "coordinate_order": "longitude, latitude",
        "geometry_encoding": "JSON coordinate array in CSV",
        "fields": {
            "contour_id": {"type": "string", "nullable": False},
            "source_object_id": {"type": "integer", "nullable": False},
            "hours": {"type": "number", "units": "hours", "nullable": False},
            "coordinates": {"type": "array", "nullable": False},
            "crs": {"type": "string", "nullable": False},
            "coordinate_order": {"type": "string", "nullable": False},
            "longitude_boundary_precision": {"type": "boolean", "nullable": False},
            "crosses_antimeridian": {"type": "boolean", "nullable": False},
        },
    },
    "station": {
        "grain": "one requested DART deployment or coastal candidate",
        "primary_key": ["station_id"],
        "crs": "source-stated latitude/longitude; horizontal datum may be unknown",
        "fields": {
            "station_id": {"type": "string", "nullable": False},
            "source_id": {"type": "string", "nullable": False},
            "station_type": {"type": "string", "nullable": False},
            "name": {"type": "string", "nullable": False},
            "latitude": {"type": "number", "units": "degrees north", "nullable": False},
            "longitude": {"type": "number", "units": "degrees east", "nullable": False},
            "availability": {"type": "string", "nullable": False},
            "units": {"type": "string", "nullable": False},
            "vertical_reference": {"type": "string", "nullable": False},
            "selection_role": {"type": "string", "nullable": False},
            "reason": {"type": "string", "nullable": False},
            "horizontal_datum": {"type": "string", "nullable": False},
            "coordinate_order": {"type": "string", "nullable": False},
            "time_basis": {"type": "string", "nullable": False},
        },
    },
    "observation": {
        "grain": "one station sample",
        "primary_key": ["observation_id"],
        "missingness": "empty CSV value means source missing; zero remains numeric zero",
        "time": (
            "source_time retained; observed_at_utc derived only from verified UTC/GMT contracts"
        ),
        "fields": {
            "observation_id": {"type": "string", "nullable": False},
            "source_id": {"type": "string", "nullable": False},
            "station_id": {"type": "string", "nullable": False},
            "source_time": {"type": "string", "nullable": False},
            "observed_at_utc": {"type": "UTC timestamp", "nullable": False},
            "raw_value": {"type": "number", "nullable": True},
            "fitted_value": {"type": "number", "nullable": True},
            "residual_value": {"type": "number", "nullable": True},
            "source_extra": {"type": "string", "nullable": True},
            "units": {"type": "string", "nullable": False},
            "vertical_reference": {"type": "string", "nullable": False},
        },
    },
    "rejected_record": {
        "grain": "one blocked asset or rejected source record",
        "primary_key": ["rejection_id"],
        "fields": {
            "rejection_id": {"type": "string", "nullable": False},
            "source_id": {"type": "string", "nullable": False},
            "record_type": {"type": "string", "nullable": False},
            "reason_code": {"type": "string", "nullable": False},
            "detail": {"type": "string", "nullable": False},
        },
    },
}


def _sanitize_run_tag(run_tag: str) -> str:
    sanitized = re.sub(r"[^a-z0-9]+", "-", run_tag.casefold()).strip("-")
    if not sanitized:
        raise NormalizationError("run tag must contain at least one letter or digit")
    return sanitized


def build_tables(
    config_path: Path, inventory_path: Path, root: Path, *, run_tag: str = "build"
) -> BuildResult:
    """Build deterministic normalized tables from verified local raw assets only."""
    root_resolved = root.resolve()
    try:
        contracts = load_contracts(config_path)
    except ContractError as error:
        raise NormalizationError(f"invalid source contract: {error}") from error
    config_document = _load_config_document(config_path)
    inventory = _load_inventory(inventory_path)
    verified = _verify_inventory(contracts, inventory, root_resolved)
    stations = _load_stations(config_document, contracts)
    event_id = config_document.get("event_id")
    if not isinstance(event_id, str):
        raise NormalizationError("source contract is missing event_id")

    contracts_by_class: dict[str, list[SourceContract]] = {}
    for contract in contracts:
        contracts_by_class.setdefault(contract.source_class, []).append(contract)
    event_contracts = contracts_by_class.get("event metadata", [])
    contour_contracts = contracts_by_class.get("modeled travel-time contours", [])
    metadata_contracts = contracts_by_class.get("modeled travel-time contour metadata", [])
    if (
        len(event_contracts) != 1
        or len(contour_contracts) != 1
        or len(metadata_contracts) != 1
    ):
        raise NormalizationError(
            "build requires exactly one event, TTT metadata, and TTT contour asset"
        )
    contour_contract = contour_contracts[0]
    metadata_contract = metadata_contracts[0]
    if (
        contour_contract.crs != "output SR 4326 requested from service"
        or contour_contract.coordinate_order != "longitude, latitude"
        or metadata_contract.crs != "WKID 4326"
    ):
        raise NormalizationError("TTT metadata contract does not justify EPSG:4326 labels")
    _validate_ttt_metadata(verified[metadata_contract.source_id])

    event = normalize_event(verified[event_contracts[0].source_id], event_id)
    contours, rejected = normalize_ttt(verified[contour_contract.source_id])
    source_accounting: dict[str, dict[str, object]] = {
        event_contracts[0].source_id: {
            "input_count": 1,
            "accepted_count": 1,
            "rejected_count": 0,
            "output_count": 1,
        },
        contour_contract.source_id: _ttt_source_accounting(
            verified[contour_contract.source_id], contours, rejected
        ),
    }
    observations: list[ObservationRecord] = []
    for station in stations:
        contract = next(item for item in contracts if item.source_id == station.source_id)
        if station.availability == "blocked":
            rejected.append(
                RejectedRecord(
                    rejection_id=f"blocked-source-{station.source_id}",
                    source_id=station.source_id,
                    record_type="source_asset",
                    reason_code="blocked_source",
                    detail=station.reason,
                )
            )
        elif station.station_type == "dart":
            accepted, station_rejected = normalize_dart(verified[contract.source_id], station)
            source_accounting[contract.source_id] = _observation_source_accounting(
                _dart_input_count(verified[contract.source_id]), accepted, station_rejected
            )
            observations.extend(accepted)
            rejected.extend(station_rejected)
        else:
            if contract.format == "NTWC event archive ASCII":
                accepted, station_rejected = normalize_ntwc_saipan(
                    verified[contract.source_id], station
                )
                input_count = _ntwc_coastal_input_count(
                    verified[contract.source_id], station_rejected
                )
            else:
                accepted, station_rejected = normalize_coastal(
                    verified[contract.source_id], station
                )
                input_count = _coastal_input_count(
                    verified[contract.source_id], station_rejected
                )
            source_accounting[contract.source_id] = _observation_source_accounting(
                input_count,
                accepted,
                station_rejected,
            )
            observations.extend(accepted)
            rejected.extend(station_rejected)
    station_sources = {station.source_id for station in stations}
    for contract in contracts:
        if contract.availability == "blocked" and contract.source_id not in station_sources:
            rejected.append(
                RejectedRecord(
                    rejection_id=f"blocked-source-{contract.source_id}",
                    source_id=contract.source_id,
                    record_type="source_asset",
                    reason_code="blocked_source",
                    detail=contract.reason,
                )
            )

    contours.sort(key=lambda record: record.contour_id)
    observations.sort(key=lambda record: (record.station_id, record.observed_at_utc))
    rejected.sort(key=lambda record: (record.source_id, record.rejection_id))
    row_counts = {
        "event": 1,
        "observation": len(observations),
        "rejected_record": len(rejected),
        "station": len(stations),
        "ttt_contour": len(contours),
    }
    reason_counts = Counter(record.reason_code for record in rejected)
    rejection_counts = {
        "api_or_record_rejection": len(rejected) - reason_counts["blocked_source"],
        "blocked_source": reason_counts["blocked_source"],
    }
    tables: dict[str, tuple[tuple[str, ...], list[dict[str, object]]]] = {
        "event": (
            (
                "event_id",
                "origin_time_utc",
                "latitude",
                "longitude",
                "depth_km",
                "magnitude",
                "magnitude_type",
                "status",
            ),
            [
                {
                    "event_id": event.event_id,
                    "origin_time_utc": event.origin_time_utc,
                    "latitude": event.latitude,
                    "longitude": event.longitude,
                    "depth_km": event.depth_km,
                    "magnitude": event.magnitude,
                    "magnitude_type": event.magnitude_type,
                    "status": event.status,
                }
            ],
        ),
        "ttt_contour": (
            (
                "contour_id",
                "source_object_id",
                "hours",
                "coordinates",
                "crs",
                "coordinate_order",
                "longitude_boundary_precision",
                "crosses_antimeridian",
            ),
            [
                {
                    "contour_id": record.contour_id,
                    "source_object_id": record.source_object_id,
                    "hours": record.hours,
                    "coordinates": record.coordinates,
                    "crs": record.crs,
                    "coordinate_order": record.coordinate_order,
                    "longitude_boundary_precision": record.longitude_boundary_precision,
                    "crosses_antimeridian": record.crosses_antimeridian,
                }
                for record in contours
            ],
        ),
        "station": (
            (
                "station_id",
                "source_id",
                "station_type",
                "name",
                "latitude",
                "longitude",
                "availability",
                "units",
                "vertical_reference",
                "selection_role",
                "reason",
                "horizontal_datum",
                "coordinate_order",
                "time_basis",
            ),
            [
                {
                    "station_id": station.station_id,
                    "source_id": station.source_id,
                    "station_type": station.station_type,
                    "name": station.name,
                    "latitude": station.latitude,
                    "longitude": station.longitude,
                    "availability": station.availability,
                    "units": station.units,
                    "vertical_reference": station.vertical_reference,
                    "selection_role": station.selection_role,
                    "reason": station.reason,
                    "horizontal_datum": station.horizontal_datum,
                    "coordinate_order": station.coordinate_order,
                    "time_basis": station.time_basis,
                }
                for station in stations
            ],
        ),
        "observation": (
            (
                "observation_id",
                "source_id",
                "station_id",
                "source_time",
                "observed_at_utc",
                "raw_value",
                "fitted_value",
                "residual_value",
                "source_extra",
                "units",
                "vertical_reference",
            ),
            [
                {
                    "observation_id": record.observation_id,
                    "source_id": record.source_id,
                    "station_id": record.station_id,
                    "source_time": record.source_time,
                    "observed_at_utc": record.observed_at_utc,
                    "raw_value": record.raw_value,
                    "fitted_value": record.fitted_value,
                    "residual_value": record.residual_value,
                    "source_extra": record.source_extra,
                    "units": record.units,
                    "vertical_reference": record.vertical_reference,
                }
                for record in observations
            ],
        ),
        "rejected_record": (
            ("rejection_id", "source_id", "record_type", "reason_code", "detail"),
            [
                {
                    "rejection_id": record.rejection_id,
                    "source_id": record.source_id,
                    "record_type": record.record_type,
                    "reason_code": record.reason_code,
                    "detail": record.detail,
                }
                for record in rejected
            ],
        ),
    }

    tag = _sanitize_run_tag(run_tag)
    output_candidate = root_resolved / "data/processed/tohoku"
    try:
        output_root = output_candidate.resolve(strict=False)
    except OSError as error:
        raise NormalizationError(f"could not resolve output root: {error}") from error
    if not output_root.is_relative_to(root_resolved):
        raise NormalizationError("output root escapes the resolved build root")
    output_candidate.mkdir(parents=True, exist_ok=True)
    output_root = output_candidate.resolve(strict=True)
    if not output_root.is_relative_to(root_resolved):
        raise NormalizationError("output root escapes the resolved build root")
    final_path = output_root / tag
    lock_path = output_root / f".{tag}.lock"
    try:
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as error:
        raise FileExistsError(f"build is already publishing run tag {tag!r}") from error
    os.close(lock_fd)
    temporary_path: Path | None = None
    try:
        if final_path.exists():
            raise FileExistsError(f"build output already exists: {final_path}")
        temporary_path = Path(tempfile.mkdtemp(prefix=f".{tag}.", dir=output_root))
        output_files: dict[str, Path] = {}
        for table_name, (columns, rows) in tables.items():
            table_path = temporary_path / f"{table_name}.csv"
            _write_csv(table_path, columns, rows)
            output_files[table_name] = table_path
        schemas_path = temporary_path / "schemas.json"
        schemas_path.write_text(
            json.dumps(SCHEMAS, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        output_files["schemas"] = schemas_path
        output_checksums = {
            name: _sha256(path)[1] for name, path in sorted(output_files.items())
        }
        source_outcomes: list[dict[str, object]] = []
        for contract in contracts:
            role = (
                "blocked"
                if contract.availability == "blocked"
                else "coverage_only_not_continuous_field"
                if contract.source_class == "model source coefficients"
                else "coverage_only_archival_companion"
                if contract.source_class == "coastal water-level archival companion"
                else "validation_input"
                if contract.source_class == "modeled travel-time contour metadata"
                else "normalized"
            )
            counts = source_accounting.get(contract.source_id)
            if counts is None:
                counts = (
                    {
                        "input_count": 0,
                        "accepted_count": 0,
                        "rejected_count": 0,
                        "output_count": 0,
                    }
                    if contract.availability == "blocked"
                    else {
                        "input_count": 1,
                        "accepted_count": 1,
                        "rejected_count": 0,
                        "output_count": 0,
                    }
                )
            station_output_count = int(contract.source_id in station_sources)
            blocked_count = int(contract.availability == "blocked")
            parser_rejection_count = sum(
                record.source_id == contract.source_id for record in rejected
            )
            source_outcomes.append(
                {
                    **counts,
                    "blocked_count": blocked_count,
                    "station_output_count": station_output_count,
                    "rejection_output_count": parser_rejection_count,
                    "input_grain": (
                        "feature"
                        if contract.source_class == "modeled travel-time contours"
                        else "sample"
                        if contract.source_class
                        in {"DART observation time series", "coastal water-level observation"}
                        else "asset"
                    ),
                    "output_grain": (
                        "contour_part"
                        if contract.source_class == "modeled travel-time contours"
                        else "observation"
                        if contract.source_class
                        in {"DART observation time series", "coastal water-level observation"}
                        else "event"
                        if contract.source_class == "event metadata"
                        else "none"
                    ),
                    "availability": contract.availability,
                    "bytes": inventory[contract.source_id].bytes,
                    "normalization_role": role,
                    "sha256": inventory[contract.source_id].sha256,
                    "source_id": contract.source_id,
                    "status": inventory[contract.source_id].status,
                }
            )
        accounting = {
            "input_inventory": inventory_path.as_posix(),
            "nctr_model_field": "blocked_no_proxy",
            "nctr_source_coefficients": "coverage_only_not_continuous_field",
            "output_checksums": output_checksums,
            "rejection_counts": rejection_counts,
            "rejection_reason_counts": dict(sorted(reason_counts.items())),
            "row_counts": row_counts,
            "source_coverage": {
                "approved": sum(contract.availability == "approved" for contract in contracts),
                "blocked": sum(contract.availability == "blocked" for contract in contracts),
                "total": len(contracts),
            },
            "source_outcomes": source_outcomes,
        }
        accounting_path = temporary_path / "accounting.json"
        accounting_path.write_text(
            json.dumps(accounting, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        output_files["accounting"] = accounting_path
        all_checksums = {name: _sha256(path)[1] for name, path in sorted(output_files.items())}
        if final_path.exists():
            raise FileExistsError(f"build output already exists: {final_path}")
        os.rename(temporary_path, final_path)
        temporary_path = None
        return BuildResult(
            output_paths={
                name: PurePosixPath((final_path / path.name).relative_to(root_resolved).as_posix())
                for name, path in sorted(output_files.items())
            },
            row_counts=row_counts,
            checksums=all_checksums,
            rejection_counts=rejection_counts,
        )
    finally:
        if temporary_path is not None:
            shutil.rmtree(temporary_path, ignore_errors=True)
        lock_path.unlink(missing_ok=True)
