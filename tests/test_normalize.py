import csv
import hashlib
import json
import shutil
import tomllib
from dataclasses import replace
from pathlib import Path

import pytest

import pipeline.normalize as normalize_module
from pipeline.normalize import (
    NormalizationError,
    StationRecord,
    build_tables,
    normalize_coastal,
    normalize_dart,
    normalize_event,
    normalize_ttt,
)
from scripts.build_tohoku_data import main as build_main

FIXTURES = Path(__file__).parent / "fixtures/normalize"
EVENT_ID = "official20110311054624120_30"


def dart_station() -> StationRecord:
    return StationRecord(
        station_id="21418",
        source_id="ncei-dart-21418-20110301to20110320",
        station_type="dart",
        name="DART 21418",
        latitude=38.718,
        longitude=148.698,
        availability="approved",
        units="m water column",
        vertical_reference="unknown",
        selection_role="near field",
        reason="not applicable",
        horizontal_datum="unknown",
        coordinate_order="latitude, longitude",
        time_basis="UTC",
    )


def coastal_station() -> StationRecord:
    return StationRecord(
        station_id="9461380",
        source_id="coops-adak-9461380-20110311to20110313",
        station_type="coastal",
        name="Adak",
        latitude=51.8606,
        longitude=-176.6376,
        availability="approved",
        units="m",
        vertical_reference="STND",
        selection_role="coastal candidate",
        reason="not applicable",
        horizontal_datum="unknown",
        coordinate_order="latitude, longitude",
        time_basis="GMT",
    )


def ntwc_saipan_station() -> StationRecord:
    return StationRecord(
        station_id="saip",
        source_id="ntwc-uhslc-saipan-20110311",
        station_type="coastal",
        name="Saipan",
        latitude=15.2266,
        longitude=145.742,
        availability="approved",
        units="m",
        vertical_reference="MLLW",
        selection_role="coastal candidate",
        reason="not applicable",
        horizontal_datum="unknown",
        coordinate_order="latitude, longitude",
        time_basis="UTC",
    )


def ioc_valparaiso_station() -> StationRecord:
    return StationRecord(
        station_id="valp",
        source_id="ioc-valparaiso-rad-20110311to20110314",
        station_type="coastal",
        name="Valparaíso",
        latitude=-33.02767128,
        longitude=-71.62787275,
        availability="approved",
        units="m",
        vertical_reference="unknown",
        selection_role="coastal candidate",
        reason="not applicable",
        horizontal_datum="unknown",
        coordinate_order="latitude, longitude",
        time_basis="UTC",
    )


def test_normalize_event_accepts_the_exact_reviewed_fdsn_record() -> None:
    event = normalize_event(FIXTURES / "usgs_event.csv", EVENT_ID)

    assert event.event_id == EVENT_ID
    assert event.origin_time_utc == "2011-03-11T05:46:24.120Z"
    assert (event.latitude, event.longitude, event.depth_km) == (38.297, 142.373, 29.0)
    assert (event.magnitude, event.magnitude_type) == (9.1, "mww")
    assert event.status == "reviewed"


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("missing-column", "exact FDSN CSV schema"),
        ("duplicate-row", "exactly one event row"),
        ("wrong-id", "unexpected event ID"),
    ],
)
def test_normalize_event_rejects_identity_or_schema_drift(
    tmp_path: Path, mutation: str, message: str
) -> None:
    source = FIXTURES / "usgs_event.csv"
    with source.open(newline="", encoding="utf-8") as source_file:
        rows = list(csv.reader(source_file))
    if mutation == "missing-column":
        rows = [row[:-1] for row in rows]
    elif mutation == "duplicate-row":
        rows.append(rows[1])
    else:
        rows[1][11] = "wrong-event"
    mutated = tmp_path / "event.csv"
    with mutated.open("w", newline="", encoding="utf-8") as target:
        csv.writer(target).writerows(rows)

    with pytest.raises(NormalizationError, match=message):
        normalize_event(mutated, EVENT_ID)


def test_normalize_event_rejects_nonfinite_measurements(tmp_path: Path) -> None:
    rows = list(csv.reader((FIXTURES / "usgs_event.csv").open(encoding="utf-8")))
    rows[1][3] = "nan"
    path = tmp_path / "nonfinite-event.csv"
    with path.open("w", newline="", encoding="utf-8") as target:
        csv.writer(target).writerows(rows)

    with pytest.raises(NormalizationError, match="finite"):
        normalize_event(path, EVENT_ID)


def test_normalize_ttt_explodes_parts_and_preserves_boundary_precision() -> None:
    contours, rejected = normalize_ttt(FIXTURES / "ttt_contours.geojson")

    assert [record.contour_id for record in contours] == [
        "ttt-4-part-0001",
        "ttt-4-part-0002",
        "ttt-8-part-0001",
    ]
    assert [record.hours for record in contours] == [0.0, 0.0, 1.0]
    assert contours[2].coordinates[-1] == (180.0000000001, 1.0)
    assert contours[2].longitude_boundary_precision is True
    assert contours[2].crosses_antimeridian is False
    assert [record.reason_code for record in rejected] == [
        "missing_hours",
        "empty_geometry_part",
        "coordinate_out_of_range",
        "negative_hours",
    ]
    assert [record.rejection_id for record in rejected] == [
        "ttt-feature-12",
        "ttt-16-part-0001",
        "ttt-16-part-0002",
        "ttt-feature-20",
    ]


def test_normalize_ttt_rejects_non_geojson_or_invalid_json(tmp_path: Path) -> None:
    for payload in ('{"type":"Point"}', "not json"):
        path = tmp_path / "contours.geojson"
        path.write_text(payload, encoding="utf-8")

        with pytest.raises(NormalizationError):
            normalize_ttt(path)


def test_normalize_ttt_rejects_duplicate_object_ids(tmp_path: Path) -> None:
    document = json.loads((FIXTURES / "ttt_contours.geojson").read_text(encoding="utf-8"))
    document["features"].append(document["features"][0])
    path = tmp_path / "duplicate.geojson"
    path.write_text(json.dumps(document), encoding="utf-8")

    contours, rejected = normalize_ttt(path)

    contour_ids = [record.contour_id for record in contours]
    assert len(contour_ids) == len(set(contour_ids))
    assert rejected[-1].reason_code == "duplicate_object_id"


def test_normalize_ttt_rejects_a_one_position_linestring(tmp_path: Path) -> None:
    document = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": 1,
                "properties": {"OBJECTID": 1, "HOURS": 1},
                "geometry": {"type": "LineString", "coordinates": [[0, 0]]},
            }
        ],
    }
    path = tmp_path / "one-position.geojson"
    path.write_text(json.dumps(document), encoding="utf-8")

    contours, rejected = normalize_ttt(path)

    assert contours == []
    assert rejected[0].reason_code == "empty_geometry_part"


def test_normalize_ttt_rejects_an_empty_linestring(tmp_path: Path) -> None:
    document: dict[str, object] = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": 1,
                "properties": {"OBJECTID": 1, "HOURS": 1},
                "geometry": {"type": "LineString", "coordinates": []},
            }
        ],
    }
    path = tmp_path / "empty-line.geojson"
    path.write_text(json.dumps(document), encoding="utf-8")

    contours, rejected = normalize_ttt(path)

    assert contours == []
    assert rejected[0].reason_code == "empty_geometry_part"


def test_normalize_ttt_rejects_a_non_feature_object_with_stable_identity(
    tmp_path: Path,
) -> None:
    document = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "not-a-feature",
                "id": 1,
                "properties": {"OBJECTID": 1, "HOURS": 1},
                "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
            }
        ],
    }
    path = tmp_path / "not-feature.geojson"
    path.write_text(json.dumps(document), encoding="utf-8")

    contours, rejected = normalize_ttt(path)

    assert contours == []
    assert rejected[0].rejection_id == "ttt-feature-index-000001"
    assert rejected[0].reason_code == "malformed_feature"


def test_normalize_ttt_rejects_an_empty_feature_collection(tmp_path: Path) -> None:
    path = tmp_path / "empty.geojson"
    path.write_text('{"type":"FeatureCollection","features":[]}', encoding="utf-8")

    with pytest.raises(NormalizationError, match="no features"):
        normalize_ttt(path)


def test_normalize_ttt_rejects_an_empty_multilinestring(tmp_path: Path) -> None:
    document: dict[str, object] = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"OBJECTID": 1, "HOURS": 1},
                "geometry": {"type": "MultiLineString", "coordinates": []},
            }
        ],
    }
    path = tmp_path / "empty-multiline.geojson"
    path.write_text(json.dumps(document), encoding="utf-8")

    contours, rejected = normalize_ttt(path)

    assert contours == []
    assert [row.reason_code for row in rejected] == ["empty_geometry"]


def test_normalize_dart_retains_eleven_source_fields_and_rejects_bad_rows() -> None:
    observations, rejected = normalize_dart(FIXTURES / "dart_station.txt", dart_station())

    assert [row.observed_at_utc for row in observations] == [
        "2011-03-01T00:00:00Z",
        "2011-03-01T00:15:00Z",
    ]
    assert observations[0].source_time == "60.000000"
    assert (
        observations[0].raw_value,
        observations[0].fitted_value,
        observations[0].residual_value,
        observations[0].source_extra,
    ) == (5662.89485, 5662.88318, 0.01167, "0.000")
    assert observations[0].units == "m water column"
    assert observations[0].vertical_reference == "unknown"
    assert [row.reason_code for row in rejected] == [
        "duplicate_timestamp",
        "invalid_column_count",
        "julian_day_mismatch",
    ]
    assert [row.rejection_id for row in rejected] == [
        "dart-21418-line-000003",
        "dart-21418-line-000004",
        "dart-21418-line-000005",
    ]


def test_normalize_dart_rejects_an_empty_approved_asset(tmp_path: Path) -> None:
    path = tmp_path / "empty-dart.txt"
    path.write_text("\n", encoding="utf-8")

    with pytest.raises(NormalizationError, match="no DART rows"):
        normalize_dart(path, dart_station())


def test_normalize_dart_quarantines_the_undocumented_9999_sentinel(
    tmp_path: Path,
) -> None:
    path = tmp_path / "sentinel-dart.txt"
    path.write_text(
        "60.000000 2011 3 1 0 0 0 9999.00000 5662.88318 9999.00000 0.000\n",
        encoding="utf-8",
    )

    observations, rejected = normalize_dart(path, dart_station())

    assert observations == []
    assert [row.reason_code for row in rejected] == ["unexpected_sentinel"]
    assert "publisher semantics are undocumented" in rejected[0].detail


def test_normalize_dart_rejects_a_non_dart_station() -> None:
    coastal = replace(dart_station(), station_type="coastal", time_basis="GMT")

    with pytest.raises(NormalizationError, match="DART station"):
        normalize_dart(FIXTURES / "dart_station.txt", coastal)


def test_observation_normalizers_require_the_verified_source_time_basis() -> None:
    with pytest.raises(NormalizationError, match="UTC"):
        normalize_dart(
            FIXTURES / "dart_station.txt", replace(dart_station(), time_basis="unknown")
        )
    with pytest.raises(NormalizationError, match="GMT"):
        normalize_coastal(
            FIXTURES / "coops_station.json",
            replace(coastal_station(), time_basis="unknown"),
        )


@pytest.mark.parametrize(
    "station",
    [
        replace(dart_station(), units="ft"),
        replace(dart_station(), vertical_reference="MSL"),
    ],
)
def test_normalize_dart_requires_canonical_units_and_vertical_reference(
    station: StationRecord,
) -> None:
    with pytest.raises(NormalizationError, match="m water column.*unknown"):
        normalize_dart(FIXTURES / "dart_station.txt", station)


def test_normalize_coastal_keeps_missing_and_zero_as_distinct_samples() -> None:
    observations, rejected = normalize_coastal(
        FIXTURES / "coops_station.json", coastal_station()
    )

    assert [row.observed_at_utc for row in observations] == [
        "2011-03-11T00:00:00Z",
        "2011-03-11T00:01:00Z",
        "2011-03-11T00:02:00Z",
    ]
    assert [row.raw_value for row in observations] == [1.113, None, 0.0]
    assert all(row.fitted_value is None and row.residual_value is None for row in observations)
    assert observations[0].source_time == "2011-03-11 00:00"
    assert (observations[0].units, observations[0].vertical_reference) == ("m", "STND")
    assert [row.reason_code for row in rejected] == [
        "duplicate_timestamp",
        "malformed_timestamp",
    ]


@pytest.mark.parametrize(
    ("payload", "reason"),
    [
        ({"error": {"message": "No data was found."}}, "api_error_asset"),
        (
            {
                "metadata": {
                    "id": "wrong",
                    "name": "Adak Island",
                    "lat": "51.8606",
                    "lon": "-176.6376",
                },
                "data": [],
            },
            "station_metadata_mismatch",
        ),
    ],
)
def test_normalize_coastal_quarantines_api_errors_or_wrong_station_metadata(
    tmp_path: Path, payload: object, reason: str
) -> None:
    import json

    path = tmp_path / "coops.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    observations, rejected = normalize_coastal(path, coastal_station())

    assert observations == []
    assert [row.reason_code for row in rejected] == [reason]
    assert rejected[0].rejection_id == "coastal-9461380-asset"
    assert rejected[0].record_type == "source_asset"


def test_normalize_coastal_rejects_a_structured_value_without_crashing(
    tmp_path: Path,
) -> None:
    payload = {
        "metadata": {
            "id": "9461380",
            "name": "Adak Island",
            "lat": "51.8606",
            "lon": "-176.6376",
        },
        "data": [{"t": "2011-03-11 00:00", "v": {"unexpected": "object"}}],
    }
    path = tmp_path / "structured-value.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    observations, rejected = normalize_coastal(path, coastal_station())

    assert observations == []
    assert rejected[0].reason_code == "malformed_value"


def test_normalize_coastal_rejects_an_empty_approved_asset(tmp_path: Path) -> None:
    payload: dict[str, object] = {
        "metadata": {
            "id": "9461380",
            "name": "Adak Island",
            "lat": "51.8606",
            "lon": "-176.6376",
        },
        "data": [],
    }
    path = tmp_path / "empty-coops.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(NormalizationError, match="no CO-OPS rows"):
        normalize_coastal(path, coastal_station())


def test_normalize_ntwc_saipan_preserves_declared_time_units_and_datum() -> None:
    assert hasattr(normalize_module, "normalize_ntwc_saipan")
    normalizer = normalize_module.normalize_ntwc_saipan

    observations, rejected = normalizer(
        FIXTURES / "ntwc_saipan.070", ntwc_saipan_station()
    )

    assert [row.observed_at_utc for row in observations] == [
        "2011-03-11T00:00:00Z",
        "2011-03-11T00:01:00Z",
        "2011-03-11T00:01:59Z",
    ]
    assert [row.raw_value for row in observations] == [2.239, 2.238, 2.234]
    assert [row.source_time for row in observations] == [
        "20110311000000",
        "20110311000100",
        "20110311000159",
    ]
    assert [row.source_extra for row in observations] == [
        "epoch=1299801600",
        "epoch=1299801660",
        "epoch=1299801719",
    ]
    assert all(row.units == "m" and row.vertical_reference == "MLLW" for row in observations)
    assert rejected == []


def test_normalize_ntwc_saipan_rejects_duplicate_or_conflicting_times(
    tmp_path: Path,
) -> None:
    assert hasattr(normalize_module, "normalize_ntwc_saipan")
    normalizer = normalize_module.normalize_ntwc_saipan
    path = tmp_path / "saipan.070"
    path.write_text(
        (FIXTURES / "ntwc_saipan.070").read_text(encoding="utf-8")
        + "1299801660 2.240000 20110311000100\n"
        + "1299801780 2.241000 20110311000400\n",
        encoding="utf-8",
    )

    observations, rejected = normalizer(path, ntwc_saipan_station())

    assert [row.observed_at_utc for row in observations] == [
        "2011-03-11T00:00:00Z",
        "2011-03-11T00:01:59Z",
    ]
    assert [row.reason_code for row in rejected] == [
        "duplicate_timestamp",
        "duplicate_timestamp",
        "timestamp_mismatch",
    ]
    assert [row.rejection_id for row in rejected[:2]] == [
        "coastal-saip-row-000002",
        "coastal-saip-row-000004",
    ]
    assert all("all 2 rows quarantined" in row.detail for row in rejected[:2])


def test_normalize_ntwc_saipan_rejects_unverified_header(tmp_path: Path) -> None:
    assert hasattr(normalize_module, "normalize_ntwc_saipan")
    normalizer = normalize_module.normalize_ntwc_saipan
    path = tmp_path / "saipan.070"
    path.write_text(
        (FIXTURES / "ntwc_saipan.070")
        .read_text(encoding="utf-8")
        .replace(" m UTC 1 min MLLW ", " cm UTC 1 min MLLW "),
        encoding="utf-8",
    )

    observations, rejected = normalizer(path, ntwc_saipan_station())

    assert observations == []
    assert [row.reason_code for row in rejected] == ["source_header_mismatch"]


def test_normalize_ntwc_saipan_quarantines_unrepresentable_epoch(tmp_path: Path) -> None:
    assert hasattr(normalize_module, "normalize_ntwc_saipan")
    normalizer = normalize_module.normalize_ntwc_saipan
    path = tmp_path / "saipan.070"
    path.write_text(
        (FIXTURES / "ntwc_saipan.070").read_text(encoding="utf-8")
        + "999999999999999999999 2.240000 20110311000200\n",
        encoding="utf-8",
    )

    observations, rejected = normalizer(path, ntwc_saipan_station())

    assert len(observations) == 3
    assert [row.reason_code for row in rejected] == ["malformed_timestamp"]


def test_normalize_ioc_valparaiso_preserves_zero_missingness_and_qc_flags() -> None:
    assert hasattr(normalize_module, "normalize_ioc_valparaiso")
    normalizer = normalize_module.normalize_ioc_valparaiso

    observations, rejected = normalizer(
        FIXTURES / "ioc_valparaiso.json", ioc_valparaiso_station()
    )

    assert [row.observed_at_utc for row in observations] == [
        "2011-03-11T00:01:00Z",
        "2011-03-11T00:02:00Z",
        "2011-03-11T00:03:00Z",
    ]
    assert [row.raw_value for row in observations] == [0.0, 2.5, None]
    assert all(row.units == "m" and row.vertical_reference == "unknown" for row in observations)
    assert json.loads(observations[1].source_extra or "{}") == {
        "completeness": "F",
        "distinctness": "F",
        "exceeded_neighbours": "T",
        "flat_line": "F",
        "missing": "F",
        "out_of_range": "F",
        "sensor": "rad",
        "shift": "F",
        "spikes_via_median": "F",
    }
    assert rejected == []


def test_normalize_ioc_valparaiso_quarantines_every_conflicting_duplicate(
    tmp_path: Path,
) -> None:
    assert hasattr(normalize_module, "normalize_ioc_valparaiso")
    normalizer = normalize_module.normalize_ioc_valparaiso
    document = json.loads((FIXTURES / "ioc_valparaiso.json").read_text(encoding="utf-8"))
    duplicate = dict(document["data"][0])
    duplicate["slevel"] = 1.25
    document["data"].append(duplicate)
    path = tmp_path / "valp.json"
    path.write_text(json.dumps(document), encoding="utf-8")

    observations, rejected = normalizer(path, ioc_valparaiso_station())

    assert len(observations) == 2
    assert [row.reason_code for row in rejected] == [
        "duplicate_timestamp",
        "duplicate_timestamp",
    ]
    assert all("all 2 rows quarantined" in row.detail for row in rejected)


def test_normalize_ioc_valparaiso_rejects_wrong_sensor_or_pagination(tmp_path: Path) -> None:
    assert hasattr(normalize_module, "normalize_ioc_valparaiso")
    normalizer = normalize_module.normalize_ioc_valparaiso
    source = (FIXTURES / "ioc_valparaiso.json").read_text(encoding="utf-8")
    variants = (
        (source.replace('"sensor": "rad"', '"sensor": "prs"', 1), "sensor_mismatch"),
        (source.replace('"total_pages": 1', '"total_pages": 2'), "pagination_mismatch"),
    )

    for payload, reason in variants:
        path = tmp_path / f"{reason}.json"
        path.write_text(payload, encoding="utf-8")
        observations, rejected = normalizer(path, ioc_valparaiso_station())
        assert observations == []
        assert [row.reason_code for row in rejected] == [reason]


def stage_fixture_bundle(root: Path) -> tuple[Path, Path]:
    config = root / "config.toml"
    source_config = Path(__file__).parents[1] / "config/tohoku-data-proof.toml"
    shutil.copyfile(source_config, config)
    document = tomllib.loads(config.read_text(encoding="utf-8"))
    stations = {
        values["source_id"]: values for values in document["stations"].values()
    }
    inventory: list[dict[str, object]] = []
    for asset in document["assets"].values():
        source_id = asset["source_id"]
        if asset["availability"] == "blocked":
            inventory.append(
                {
                    "source_id": source_id,
                    "status": "blocked",
                    "local_path": "not-downloaded",
                    "bytes": 0,
                    "sha256": "not-downloaded",
                    "reason": asset["reason"],
                }
            )
            continue
        if asset["source_class"] == "event metadata":
            payload = (FIXTURES / "usgs_event.csv").read_bytes()
        elif asset["source_class"] == "modeled travel-time contours":
            payload = (FIXTURES / "ttt_contours.geojson").read_bytes()
        elif asset["source_class"] == "DART observation time series":
            payload = (FIXTURES / "dart_station.txt").read_bytes()
        elif asset["source_class"] == "coastal water-level observation":
            if asset["format"] == "NTWC event archive ASCII":
                payload = (FIXTURES / "ntwc_saipan.070").read_bytes()
            else:
                payload_document = json.loads(
                    (FIXTURES / "coops_station.json").read_text(encoding="utf-8")
                )
                station = stations[source_id]
                payload_document["metadata"].update(
                    {
                        "id": station["station_id"],
                        "lat": str(station["latitude"]),
                        "lon": str(station["longitude"]),
                    }
                )
                payload = json.dumps(payload_document, separators=(",", ":")).encode()
        elif asset["source_class"] == "coastal water-level archival companion":
            payload = (FIXTURES / "ntwc_saipan.070").read_bytes()
        elif asset["source_class"] == "modeled travel-time contour metadata":
            payload = json.dumps(
                {
                    "name": "2011/3/11 Tohoku, Japan",
                    "geometryType": "esriGeometryPolyline",
                    "extent": {"spatialReference": {"wkid": 4326}},
                },
                separators=(",", ":"),
            ).encode()
        else:
            payload = b"<!DOCTYPE HTML><html></html>"
        raw_path = root / asset["local_path"]
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest()
        raw_path.with_name(f"{raw_path.name}.sha256").write_text(
            f"{digest}\n", encoding="utf-8"
        )
        inventory.append(
            {
                "source_id": source_id,
                "status": "cached",
                "local_path": asset["local_path"],
                "bytes": len(payload),
                "sha256": digest,
                "reason": "not applicable",
            }
        )
    inventory_path = root / "inventory.json"
    inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
    return config, inventory_path


def replace_staged_asset(
    root: Path, inventory_path: Path, source_id: str, payload: bytes
) -> None:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    item = next(row for row in inventory if row["source_id"] == source_id)
    raw_path = root / item["local_path"]
    raw_path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    raw_path.with_name(f"{raw_path.name}.sha256").write_text(
        f"{digest}\n", encoding="utf-8"
    )
    item["bytes"] = len(payload)
    item["sha256"] = digest
    inventory_path.write_text(json.dumps(inventory), encoding="utf-8")


@pytest.mark.parametrize(
    "payload",
    [
        b"not json",
        b'{"name":"wrong","geometryType":"esriGeometryPolyline","extent":{"spatialReference":{"wkid":4326}}}',
        (
            b'{"name":"2011/3/11 Tohoku, Japan","geometryType":"esriGeometryPoint",'
            b'"extent":{"spatialReference":{"wkid":4326}}}'
        ),
        (
            b'{"name":"2011/3/11 Tohoku, Japan","geometryType":"esriGeometryPolyline",'
            b'"extent":{"spatialReference":{"wkid":3857}}}'
        ),
    ],
)
def test_build_tables_rejects_unverified_ttt_metadata_before_publication(
    tmp_path: Path, payload: bytes
) -> None:
    config, inventory = stage_fixture_bundle(tmp_path)
    replace_staged_asset(
        tmp_path, inventory, "ncei-ttt-tohoku-layer17-metadata", payload
    )

    with pytest.raises(NormalizationError, match="TTT metadata"):
        build_tables(config, inventory, tmp_path, run_tag="bad-metadata")

    assert not (tmp_path / "data/processed/tohoku/bad-metadata").exists()


def test_build_tables_verifies_inputs_and_writes_complete_deterministic_outputs(
    tmp_path: Path,
) -> None:
    config, inventory = stage_fixture_bundle(tmp_path)

    first = build_tables(config, inventory, tmp_path, run_tag="fixture-a")
    second = build_tables(config, inventory, tmp_path, run_tag="fixture-b")

    assert first.row_counts == {
        "event": 1,
        "observation": 23,
        "rejected_record": 26,
        "station": 10,
        "ttt_contour": 3,
    }
    assert first.rejection_counts == {
        "api_or_record_rejection": 24,
        "blocked_source": 2,
    }
    assert set(first.output_paths) == {
        "accounting",
        "event",
        "observation",
        "rejected_record",
        "schemas",
        "station",
        "ttt_contour",
    }
    assert first.checksums == second.checksums
    assert all((tmp_path / path).is_file() for path in first.output_paths.values())

    station_path = tmp_path / first.output_paths["station"]
    with station_path.open(newline="", encoding="utf-8") as source:
        station_rows = list(csv.DictReader(source))
    assert [row["station_id"] for row in station_rows] == [
        "1617760",
        "1770000",
        "21413",
        "21418",
        "32401",
        "46411",
        "9419750",
        "9461380",
        "saip",
        "valp",
    ]
    blocked_station_states = {
        row["availability"]
        for row in station_rows
        if row["station_id"] in {"saip", "valp"}
    }
    assert blocked_station_states == {"approved", "blocked"}

    accounting = json.loads(
        (tmp_path / first.output_paths["accounting"]).read_text(encoding="utf-8")
    )
    assert accounting["source_coverage"] == {
        "approved": 15,
        "blocked": 2,
        "total": 17,
    }
    assert accounting["nctr_model_field"] == "blocked_no_proxy"
    assert accounting["nctr_source_coefficients"] == "coverage_only_not_continuous_field"
    outcomes = {row["source_id"]: row for row in accounting["source_outcomes"]}
    assert {
        key: outcomes["usgs-tohoku-origin-csv"][key]
        for key in ("input_count", "accepted_count", "rejected_count", "output_count")
    } == {"input_count": 1, "accepted_count": 1, "rejected_count": 0, "output_count": 1}
    ttt = outcomes["ncei-ttt-tohoku-layer17-geojson"]
    assert ttt["feature_accounting"] == {"input": 5, "accepted": 3, "rejected": 2}
    assert ttt["part_accounting"] == {
        "input": 7,
        "accepted": 3,
        "rejected": 2,
        "not_parsed_due_to_feature_rejection": 2,
        "output": 3,
    }
    assert {
        key: outcomes["ncei-dart-21418-20110301to20110320"][key]
        for key in ("input_count", "accepted_count", "rejected_count", "output_count")
    } == {"input_count": 5, "accepted_count": 2, "rejected_count": 3, "output_count": 2}
    assert {
        key: outcomes["coops-adak-9461380-20110311to20110313"][key]
        for key in ("input_count", "accepted_count", "rejected_count", "output_count")
    } == {"input_count": 5, "accepted_count": 3, "rejected_count": 2, "output_count": 3}
    assert {
        key: outcomes["ntwc-uhslc-saipan-20110311"][key]
        for key in ("input_count", "accepted_count", "rejected_count", "output_count")
    } == {"input_count": 3, "accepted_count": 3, "rejected_count": 0, "output_count": 3}
    assert outcomes["ncei-ttt-tohoku-layer17-metadata"]["normalization_role"] == (
        "validation_input"
    )
    assert outcomes["nctr-tohoku-source-coefficients"]["normalization_role"] == (
        "coverage_only_not_continuous_field"
    )
    assert outcomes["ntwc-uhslc-saipan-20110312"]["normalization_role"] == (
        "coverage_only_archival_companion"
    )
    assert outcomes["ntwc-uhslc-saipan-20110313"]["normalization_role"] == (
        "coverage_only_archival_companion"
    )
    assert outcomes["nctr-tohoku-model-field"]["blocked_count"] == 1

    schemas = json.loads(
        (tmp_path / first.output_paths["schemas"]).read_text(encoding="utf-8")
    )
    for table_name in ("event", "observation", "rejected_record", "station", "ttt_contour"):
        with (tmp_path / first.output_paths[table_name]).open(
            newline="", encoding="utf-8"
        ) as source:
            columns = csv.DictReader(source).fieldnames
        assert set(schemas[table_name]["fields"]) == set(columns or [])


def test_build_tables_rejects_a_checksum_mismatch_without_publishing(tmp_path: Path) -> None:
    config, inventory = stage_fixture_bundle(tmp_path)
    inventory_rows = json.loads(inventory.read_text(encoding="utf-8"))
    inventory_rows[0]["sha256"] = "0" * 64
    inventory.write_text(json.dumps(inventory_rows), encoding="utf-8")

    with pytest.raises(NormalizationError, match="checksum"):
        build_tables(config, inventory, tmp_path, run_tag="failed")

    assert not (tmp_path / "data/processed/tohoku/failed").exists()


def test_build_tables_rejects_a_checksum_sidecar_symlink_escape(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    config, inventory = stage_fixture_bundle(root)
    raw_path = root / "data/raw/usgs/official20110311054624120_30.csv"
    sidecar = raw_path.with_name(f"{raw_path.name}.sha256")
    digest = sidecar.read_text(encoding="utf-8")
    sidecar.unlink()
    outside = tmp_path / "outside.sha256"
    outside.write_text(digest, encoding="utf-8")
    sidecar.symlink_to(outside)

    with pytest.raises(NormalizationError, match="checksum sidecar.*escapes"):
        build_tables(config, inventory, root, run_tag="sidecar-escape")

    assert not (root / "data/processed/tohoku/sidecar-escape").exists()


def test_build_tables_rejects_an_output_root_symlink_escape(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    config, inventory = stage_fixture_bundle(root)
    outside = tmp_path / "outside"
    outside.mkdir()
    processed = root / "data/processed"
    processed.mkdir(parents=True)
    (processed / "tohoku").symlink_to(outside, target_is_directory=True)

    with pytest.raises(NormalizationError, match="output root.*escapes"):
        build_tables(config, inventory, root, run_tag="output-escape")

    assert list(outside.iterdir()) == []


def test_build_tables_exposes_an_invalid_contract_as_a_normalization_error(
    tmp_path: Path,
) -> None:
    config, inventory = stage_fixture_bundle(tmp_path)
    config.write_text("not valid TOML =", encoding="utf-8")

    with pytest.raises(NormalizationError, match="source contract"):
        build_tables(config, inventory, tmp_path, run_tag="failed-contract")


def test_build_cli_accepts_explicit_inputs_and_never_downloads(tmp_path: Path) -> None:
    config, inventory = stage_fixture_bundle(tmp_path)

    exit_code = build_main(
        [
            "--config",
            str(config),
            "--inventory",
            str(inventory),
            "--root",
            str(tmp_path),
            "--run-tag",
            "cli-fixture",
        ]
    )

    assert exit_code == 0
    assert (tmp_path / "data/processed/tohoku/cli-fixture/accounting.json").is_file()
