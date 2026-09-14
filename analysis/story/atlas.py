"""Typed, source-preserving inputs and geometry for the Stage A story atlas."""

from __future__ import annotations

import csv
import json
import math
import tomllib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal, cast

from pyproj import Geod

from pipeline.missingness import ExpectedWindow

PACIFIC_MIN_LONGITUDE = -340.0
PACIFIC_MAX_LONGITUDE = 20.0
LONGITUDE_TOLERANCE = 1e-6
DISPLAY_CRS = "+proj=eqearth +lon_0=-160 +datum=WGS84 +units=m +no_defs +type=crs"

StationType = Literal["coastal", "dart"]
Coordinate = tuple[float, float]


class AtlasError(ValueError):
    """Raised when an atlas input would require guessing or silent repair."""


@dataclass(frozen=True, slots=True)
class EventRecord:
    """Reviewed event identity and origin."""

    event_id: str
    origin_time_utc: datetime
    latitude: float
    longitude: float


@dataclass(frozen=True, slots=True)
class StationRecord:
    """Source-stated station location and measurement semantics."""

    station_id: str
    source_id: str
    station_type: StationType
    name: str
    latitude: float
    longitude: float
    units: str
    vertical_reference: str
    horizontal_datum: str
    time_basis: str


@dataclass(frozen=True, slots=True)
class ObservationRecord:
    """One observation with source time kept separate from verified UTC."""

    station_id: str
    source_time: str
    observed_at_utc: datetime
    raw_value: float | None
    residual_value: float | None
    units: str
    vertical_reference: str


@dataclass(frozen=True, slots=True)
class ContourRecord:
    """One published NCEI travel-time contour part."""

    contour_id: str
    hours: float
    coordinates: tuple[Coordinate, ...]
    crs: str
    coordinate_order: str
    longitude_boundary_precision: bool
    crosses_antimeridian: bool


@dataclass(frozen=True, slots=True)
class AtlasInputs:
    """Validated normalized inputs for preliminary story diagnostics."""

    event: EventRecord
    stations: tuple[StationRecord, ...]
    observations: tuple[ObservationRecord, ...]
    contours: tuple[ContourRecord, ...]
    accounting: dict[str, object]
    missingness_summary: dict[str, object]
    input_paths: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class AtlasConfig:
    """Reviewed Stage A projection, window, and candidate scope."""

    event_id: str
    evidence_state: str
    display_crs: str
    central_meridian: float
    start_hours: float
    end_hours: float
    highlighted_contour_hours: tuple[int, ...]
    range_radii_km: tuple[int, ...]
    dart_station_ids: tuple[str, ...]
    coastal_station_ids: tuple[str, ...]
    figure_dpi: int


def _read_csv(path: Path, required_columns: set[str]) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            missing = required_columns - set(reader.fieldnames or ())
            if missing:
                raise AtlasError(f"{path} is missing columns: {', '.join(sorted(missing))}")
            rows: list[dict[str, str]] = []
            for row_number, raw_row in enumerate(reader, start=2):
                if any(key is None or value is None for key, value in raw_row.items()):
                    raise AtlasError(f"{path}:{row_number} is not a rectangular CSV row")
                rows.append(cast(dict[str, str], raw_row))
            return rows
    except OSError as error:
        raise AtlasError(f"could not read {path}: {error}") from error


def _load_json_object(path: Path, label: str) -> dict[str, object]:
    try:
        value: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AtlasError(f"could not read {label} {path}: {error}") from error
    if not isinstance(value, dict):
        raise AtlasError(f"{label} must contain a JSON object")
    return cast(dict[str, object], value)


def _parse_utc(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise AtlasError(f"invalid UTC timestamp {value!r}") from error
    if not value.endswith("Z") or parsed.utcoffset() != UTC.utcoffset(parsed):
        raise AtlasError(f"timestamp is not explicit UTC: {value!r}")
    return parsed


def _finite(value: str, field: str) -> float:
    try:
        parsed = float(value)
    except ValueError as error:
        raise AtlasError(f"{field} must be numeric") from error
    if not math.isfinite(parsed):
        raise AtlasError(f"{field} must be finite")
    return parsed


def _optional_finite(value: str, field: str) -> float | None:
    return _finite(value, field) if value.strip() else None


def _boolean(value: str, field: str) -> bool:
    if value == "true":
        return True
    if value == "false":
        return False
    raise AtlasError(f"{field} must be true or false")


def _coordinate(longitude: float, latitude: float, *, boundary_precision: bool) -> Coordinate:
    if not (-90.0 <= latitude <= 90.0):
        raise AtlasError(f"latitude outside [-90, 90]: {latitude}")
    if not (-180.0 - LONGITUDE_TOLERANCE <= longitude <= 180.0 + LONGITUDE_TOLERANCE):
        raise AtlasError(f"longitude outside precision tolerance: {longitude}")
    if not (-180.0 <= longitude <= 180.0) and not boundary_precision:
        raise AtlasError(
            f"longitude outside [-180, 180] lacks boundary precision flag: {longitude}"
        )
    return longitude, latitude


def _parse_coordinates(value: str, *, boundary_precision: bool) -> tuple[Coordinate, ...]:
    try:
        raw: object = json.loads(value)
    except json.JSONDecodeError as error:
        raise AtlasError(f"invalid contour coordinates JSON: {error}") from error
    if not isinstance(raw, list):
        raise AtlasError("contour must contain at least two coordinates")
    raw_coordinates = cast(list[object], raw)
    if len(raw_coordinates) < 2:
        raise AtlasError("contour must contain at least two coordinates")
    coordinates: list[Coordinate] = []
    for item in raw_coordinates:
        if not isinstance(item, list):
            raise AtlasError("each contour coordinate must be a two-value array")
        raw_coordinate = cast(list[object], item)
        if len(raw_coordinate) != 2:
            raise AtlasError("each contour coordinate must be a two-value array")
        longitude_value, latitude_value = raw_coordinate
        if (
            not isinstance(longitude_value, (int, float))
            or isinstance(longitude_value, bool)
            or not isinstance(latitude_value, (int, float))
            or isinstance(latitude_value, bool)
        ):
            raise AtlasError("contour coordinates must be numeric")
        longitude = float(longitude_value)
        latitude = float(latitude_value)
        if not math.isfinite(longitude) or not math.isfinite(latitude):
            raise AtlasError("contour coordinates must be finite")
        coordinates.append(_coordinate(longitude, latitude, boundary_precision=boundary_precision))
    return tuple(coordinates)


def load_atlas_inputs(processed_dir: Path, missingness_summary_path: Path) -> AtlasInputs:
    """Load normalized inputs while preserving source semantics and explicit unknowns."""
    event_path = processed_dir / "event.csv"
    station_path = processed_dir / "station.csv"
    observation_path = processed_dir / "observation.csv"
    contour_path = processed_dir / "ttt_contour.csv"
    accounting_path = processed_dir / "accounting.json"

    event_rows = _read_csv(
        event_path,
        {"event_id", "origin_time_utc", "latitude", "longitude", "status"},
    )
    if len(event_rows) != 1:
        raise AtlasError("event.csv must contain exactly one event")
    event_row = event_rows[0]
    if event_row["status"] != "reviewed":
        raise AtlasError("event.csv event must have reviewed status")
    event_longitude = _finite(event_row["longitude"], "event longitude")
    event_latitude = _finite(event_row["latitude"], "event latitude")
    _coordinate(event_longitude, event_latitude, boundary_precision=False)
    event = EventRecord(
        event_id=event_row["event_id"],
        origin_time_utc=_parse_utc(event_row["origin_time_utc"]),
        latitude=event_latitude,
        longitude=event_longitude,
    )

    station_rows = _read_csv(
        station_path,
        {
            "station_id",
            "source_id",
            "station_type",
            "name",
            "latitude",
            "longitude",
            "availability",
            "units",
            "vertical_reference",
            "horizontal_datum",
            "time_basis",
        },
    )
    stations: list[StationRecord] = []
    station_ids: set[str] = set()
    for row in station_rows:
        station_id = row["station_id"]
        if not station_id or station_id in station_ids:
            raise AtlasError(f"duplicate or blank station ID {station_id!r}")
        station_ids.add(station_id)
        station_type_value = row["station_type"]
        if station_type_value not in {"coastal", "dart"}:
            raise AtlasError(f"unknown station type {station_type_value!r}")
        if row["availability"] != "approved":
            raise AtlasError(f"station {station_id!r} is not approved")
        text_values = (
            row["source_id"],
            row["name"],
            row["units"],
            row["vertical_reference"],
            row["horizontal_datum"],
            row["time_basis"],
        )
        if any(not value.strip() for value in text_values):
            raise AtlasError(f"station {station_id!r} has a blank semantic field")
        longitude = _finite(row["longitude"], f"station {station_id} longitude")
        latitude = _finite(row["latitude"], f"station {station_id} latitude")
        _coordinate(longitude, latitude, boundary_precision=False)
        stations.append(
            StationRecord(
                station_id=station_id,
                source_id=row["source_id"],
                station_type=cast(StationType, station_type_value),
                name=row["name"],
                latitude=latitude,
                longitude=longitude,
                units=row["units"],
                vertical_reference=row["vertical_reference"],
                horizontal_datum=row["horizontal_datum"],
                time_basis=row["time_basis"],
            )
        )
    stations.sort(key=lambda station: (station.station_type, station.station_id))

    observation_rows = _read_csv(
        observation_path,
        {
            "observation_id",
            "station_id",
            "source_time",
            "observed_at_utc",
            "raw_value",
            "residual_value",
            "units",
            "vertical_reference",
        },
    )
    station_types = {station.station_id: station.station_type for station in stations}
    observations: list[tuple[str, ObservationRecord]] = []
    seen_station_times: set[tuple[str, datetime]] = set()
    for row in observation_rows:
        station_id = row["station_id"]
        if station_id not in station_types:
            raise AtlasError(f"observation references unknown station {station_id!r}")
        observed_at = _parse_utc(row["observed_at_utc"])
        station_time = (station_id, observed_at)
        if station_time in seen_station_times:
            raise AtlasError(f"duplicate station/timestamp pair {station_time!r}")
        seen_station_times.add(station_time)
        if not row["source_time"].strip():
            raise AtlasError(f"observation {row['observation_id']!r} has blank source_time")
        if not row["units"].strip() or not row["vertical_reference"].strip():
            raise AtlasError(f"observation {row['observation_id']!r} has blank semantics")
        observations.append(
            (
                row["observation_id"],
                ObservationRecord(
                    station_id=station_id,
                    source_time=row["source_time"],
                    observed_at_utc=observed_at,
                    raw_value=_optional_finite(row["raw_value"], "raw_value"),
                    residual_value=_optional_finite(row["residual_value"], "residual_value"),
                    units=row["units"],
                    vertical_reference=row["vertical_reference"],
                ),
            )
        )
    observations.sort(
        key=lambda item: (
            station_types[item[1].station_id],
            item[1].station_id,
            item[1].observed_at_utc,
            item[0],
        )
    )

    contour_rows = _read_csv(
        contour_path,
        {
            "contour_id",
            "hours",
            "coordinates",
            "crs",
            "coordinate_order",
            "longitude_boundary_precision",
            "crosses_antimeridian",
        },
    )
    contours: list[ContourRecord] = []
    contour_ids: set[str] = set()
    for row in contour_rows:
        contour_id = row["contour_id"]
        if not contour_id or contour_id in contour_ids:
            raise AtlasError(f"duplicate or blank contour ID {contour_id!r}")
        contour_ids.add(contour_id)
        if row["crs"] != "EPSG:4326":
            raise AtlasError(f"contour {contour_id!r} must use EPSG:4326")
        if row["coordinate_order"] != "longitude, latitude":
            raise AtlasError(f"contour {contour_id!r} has unexpected coordinate order")
        boundary_precision = _boolean(
            row["longitude_boundary_precision"], "longitude_boundary_precision"
        )
        crosses_antimeridian = _boolean(row["crosses_antimeridian"], "crosses_antimeridian")
        coordinates = _parse_coordinates(row["coordinates"], boundary_precision=boundary_precision)
        computed_crossing = any(
            abs(current[0] - previous[0]) > 180.0
            for previous, current in zip(coordinates, coordinates[1:], strict=False)
        )
        if computed_crossing != crosses_antimeridian:
            raise AtlasError(f"contour {contour_id!r} antimeridian flag disagrees with geometry")
        hours = _finite(row["hours"], f"contour {contour_id} hours")
        if hours <= 0:
            raise AtlasError(f"contour {contour_id!r} hours must be positive")
        contours.append(
            ContourRecord(
                contour_id=contour_id,
                hours=hours,
                coordinates=coordinates,
                crs=row["crs"],
                coordinate_order=row["coordinate_order"],
                longitude_boundary_precision=boundary_precision,
                crosses_antimeridian=crosses_antimeridian,
            )
        )
    contours.sort(key=lambda contour: (contour.hours, contour.contour_id))

    return AtlasInputs(
        event=event,
        stations=tuple(stations),
        observations=tuple(record for _, record in observations),
        contours=tuple(contours),
        accounting=_load_json_object(accounting_path, "accounting"),
        missingness_summary=_load_json_object(missingness_summary_path, "missingness summary"),
        input_paths=(
            event_path,
            station_path,
            observation_path,
            contour_path,
            accounting_path,
            missingness_summary_path,
        ),
    )


def _text(document: dict[str, object], field: str) -> str:
    value = document.get(field)
    if not isinstance(value, str) or not value.strip():
        raise AtlasError(f"atlas config {field} must be nonblank text")
    return value


def _number(document: dict[str, object], field: str) -> float:
    value = document.get(field)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise AtlasError(f"atlas config {field} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise AtlasError(f"atlas config {field} must be finite")
    return result


def _integer_tuple(document: dict[str, object], field: str) -> tuple[int, ...]:
    value = document.get(field)
    if not isinstance(value, list) or not value:
        raise AtlasError(f"atlas config {field} must be a non-empty integer list")
    raw_values = cast(list[object], value)
    if any(not isinstance(item, int) or isinstance(item, bool) for item in raw_values):
        raise AtlasError(f"atlas config {field} must be a non-empty integer list")
    return tuple(cast(int, item) for item in raw_values)


def _station_ids(document: dict[str, object], field: str) -> tuple[str, ...]:
    value = document.get(field)
    if not isinstance(value, list) or not value:
        raise AtlasError(f"atlas config {field} must be a non-empty text list")
    raw_values = cast(list[object], value)
    if any(not isinstance(item, str) or not item.strip() for item in raw_values):
        raise AtlasError(f"atlas config {field} must be a non-empty text list")
    station_ids = tuple(cast(str, item) for item in raw_values)
    if len(set(station_ids)) != len(station_ids):
        raise AtlasError(f"atlas config {field} contains duplicate station IDs")
    return station_ids


def load_atlas_config(path: Path) -> AtlasConfig:
    """Load and validate the fixed Stage A atlas contract."""
    try:
        document = cast(dict[str, object], tomllib.loads(path.read_text(encoding="utf-8")))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise AtlasError(f"could not read atlas config {path}: {error}") from error
    if document.get("schema_version") != "1":
        raise AtlasError("atlas config schema_version must be '1'")
    evidence_state = _text(document, "evidence_state")
    if evidence_state != "preliminary_storyboard_evidence":
        raise AtlasError("atlas config must use preliminary_storyboard_evidence")
    display_crs = _text(document, "display_crs")
    if display_crs != DISPLAY_CRS:
        raise AtlasError("atlas config must use the reviewed Pacific Equal Earth CRS")
    central_meridian = _number(document, "central_meridian")
    if central_meridian != -160.0:
        raise AtlasError("atlas config central_meridian must be -160")
    start_hours = _number(document, "start_hours")
    end_hours = _number(document, "end_hours")
    if start_hours >= end_hours:
        raise AtlasError("atlas config start_hours must be less than end_hours")
    contour_hours = _integer_tuple(document, "highlighted_contour_hours")
    range_radii = _integer_tuple(document, "range_radii_km")
    if any(value <= 0 for value in contour_hours) or tuple(sorted(set(contour_hours))) != (
        contour_hours
    ):
        raise AtlasError("highlighted_contour_hours must be unique, increasing, and positive")
    if any(value <= 0 for value in range_radii) or tuple(sorted(set(range_radii))) != range_radii:
        raise AtlasError("range_radii_km must be unique, increasing, and positive")
    figure_dpi_value = document.get("figure_dpi")
    if (
        not isinstance(figure_dpi_value, int)
        or isinstance(figure_dpi_value, bool)
        or figure_dpi_value <= 0
    ):
        raise AtlasError("atlas config figure_dpi must be a positive integer")
    return AtlasConfig(
        event_id=_text(document, "event_id"),
        evidence_state=evidence_state,
        display_crs=display_crs,
        central_meridian=central_meridian,
        start_hours=start_hours,
        end_hours=end_hours,
        highlighted_contour_hours=contour_hours,
        range_radii_km=range_radii,
        dart_station_ids=_station_ids(document, "dart_station_ids"),
        coastal_station_ids=_station_ids(document, "coastal_station_ids"),
        figure_dpi=figure_dpi_value,
    )


def validate_stage_a_scope(
    atlas: AtlasInputs, config: AtlasConfig, windows: tuple[ExpectedWindow, ...]
) -> None:
    """Require the reviewed event, station groups, contour hours, and coastal windows."""
    if atlas.event.event_id != config.event_id:
        raise AtlasError("atlas event ID does not match the reviewed config")
    actual_dart = {
        station.station_id for station in atlas.stations if station.station_type == "dart"
    }
    actual_coastal = {
        station.station_id for station in atlas.stations if station.station_type == "coastal"
    }
    if actual_dart != set(config.dart_station_ids):
        raise AtlasError("loaded DART station IDs do not match the reviewed config")
    if actual_coastal != set(config.coastal_station_ids):
        raise AtlasError("loaded coastal station IDs do not match the reviewed config")
    window_ids = [window.station_id for window in windows]
    if len(window_ids) != len(set(window_ids)) or set(window_ids) != actual_coastal:
        raise AtlasError("missingness windows must match each coastal station exactly once")
    available_hours = {
        int(contour.hours) for contour in atlas.contours if contour.hours.is_integer()
    }
    if not set(config.highlighted_contour_hours).issubset(available_hours):
        raise AtlasError("reviewed highlighted contour hours are missing from the input")


def shift_longitude(longitude: float) -> float:
    """Shift a longitude into the Pacific display domain [-340, 20)."""
    shifted = ((longitude - PACIFIC_MIN_LONGITUDE) % 360.0) + PACIFIC_MIN_LONGITUDE
    if shifted == PACIFIC_MAX_LONGITUDE:
        return PACIFIC_MIN_LONGITUDE
    return shifted


def split_at_display_seam(
    coordinates: tuple[Coordinate, ...],
) -> tuple[tuple[Coordinate, ...], ...]:
    """Split linework at 20°E while retaining an endpoint on each seam side."""
    if len(coordinates) < 2:
        raise AtlasError("linework must contain at least two coordinates")
    shifted = tuple((shift_longitude(longitude), latitude) for longitude, latitude in coordinates)
    parts: list[list[Coordinate]] = [[shifted[0]]]
    previous = shifted[0]
    for current in shifted[1:]:
        delta = current[0] - previous[0]
        if delta < -180.0:
            unwrapped_current = current[0] + 360.0
            fraction = (PACIFIC_MAX_LONGITUDE - previous[0]) / (unwrapped_current - previous[0])
            seam_latitude = previous[1] + fraction * (current[1] - previous[1])
            parts[-1].append((PACIFIC_MAX_LONGITUDE, seam_latitude))
            parts.append([(PACIFIC_MIN_LONGITUDE, seam_latitude), current])
        elif delta > 180.0:
            unwrapped_current = current[0] - 360.0
            fraction = (PACIFIC_MIN_LONGITUDE - previous[0]) / (unwrapped_current - previous[0])
            seam_latitude = previous[1] + fraction * (current[1] - previous[1])
            parts[-1].append((PACIFIC_MIN_LONGITUDE, seam_latitude))
            parts.append([(PACIFIC_MAX_LONGITUDE, seam_latitude), current])
        else:
            parts[-1].append(current)
        previous = current
    return tuple(tuple(part) for part in parts)


def geodesic_range_ring(
    *, latitude: float, longitude: float, radius_km: int
) -> tuple[Coordinate, ...]:
    """Return a WGS84 geodesic distance ring in kilometres, with no speed model."""
    _coordinate(longitude, latitude, boundary_precision=False)
    if radius_km <= 0:
        raise AtlasError("radius_km must be positive")
    geod = Geod(ellps="WGS84")
    coordinates: list[Coordinate] = []
    for bearing in range(361):
        ring_longitude, ring_latitude, _ = geod.fwd(longitude, latitude, bearing, radius_km * 1000)
        coordinates.append((ring_longitude, ring_latitude))
    return tuple(coordinates)
