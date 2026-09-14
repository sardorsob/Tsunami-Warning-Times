import csv
import json
from hashlib import sha256
from pathlib import Path

import pytest
from pyproj import Geod

from analysis.story.atlas import (
    AtlasError,
    build_series_panels,
    geodesic_range_ring,
    load_atlas_config,
    load_atlas_inputs,
    shift_longitude,
    split_at_display_seam,
    validate_stage_a_scope,
)
from analysis.story.plots import (
    plot_distance_contour_diagnostic,
    plot_observation_coverage,
    plot_pacific_evidence,
    plot_station_timeseries,
)
from pipeline.missingness import (
    CoastalCoverageTimeline,
    CoveragePosition,
    ExpectedWindow,
    OffGridObservation,
)

EVENT_COLUMNS = (
    "event_id",
    "origin_time_utc",
    "latitude",
    "longitude",
    "depth_km",
    "magnitude",
    "magnitude_type",
    "status",
)
STATION_COLUMNS = (
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
)
OBSERVATION_COLUMNS = (
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
)
TTT_COLUMNS = (
    "contour_id",
    "source_object_id",
    "hours",
    "coordinates",
    "crs",
    "coordinate_order",
    "longitude_boundary_precision",
    "crosses_antimeridian",
)


def _write_csv(path: Path, columns: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _stage_atlas_inputs(
    root: Path, *, contour_longitude: str = "179.0", boundary_precision: str = "false"
) -> tuple[Path, Path]:
    processed = root / "processed"
    processed.mkdir()
    _write_csv(
        processed / "event.csv",
        EVENT_COLUMNS,
        [
            {
                "event_id": "official20110311054624120_30",
                "origin_time_utc": "2011-03-11T05:46:24.120Z",
                "latitude": "38.297",
                "longitude": "142.373",
                "depth_km": "29.0",
                "magnitude": "9.1",
                "magnitude_type": "mww",
                "status": "reviewed",
            }
        ],
    )
    _write_csv(
        processed / "station.csv",
        STATION_COLUMNS,
        [
            {
                "station_id": "dart",
                "source_id": "dart-source",
                "station_type": "dart",
                "name": "DART fixture",
                "latitude": "30.0",
                "longitude": "150.0",
                "availability": "approved",
                "units": "m water column",
                "vertical_reference": "unknown",
                "selection_role": "fixture",
                "reason": "not applicable",
                "horizontal_datum": "unknown",
                "coordinate_order": "latitude, longitude",
                "time_basis": "UTC",
            },
            {
                "station_id": "coast",
                "source_id": "coastal-source",
                "station_type": "coastal",
                "name": "Coastal fixture",
                "latitude": "20.0",
                "longitude": "-155.0",
                "availability": "approved",
                "units": "m",
                "vertical_reference": "STND",
                "selection_role": "fixture",
                "reason": "not applicable",
                "horizontal_datum": "unknown",
                "coordinate_order": "latitude, longitude",
                "time_basis": "GMT",
            },
        ],
    )
    _write_csv(
        processed / "observation.csv",
        OBSERVATION_COLUMNS,
        [
            {
                "observation_id": "coast-zero",
                "source_id": "coastal-source",
                "station_id": "coast",
                "source_time": "2011-03-11 05:46",
                "observed_at_utc": "2011-03-11T05:46:00Z",
                "raw_value": "0",
                "fitted_value": "",
                "residual_value": "",
                "source_extra": "",
                "units": "m",
                "vertical_reference": "STND",
            },
            {
                "observation_id": "coast-blank",
                "source_id": "coastal-source",
                "station_id": "coast",
                "source_time": "2011-03-11 05:47",
                "observed_at_utc": "2011-03-11T05:47:00Z",
                "raw_value": "",
                "fitted_value": "",
                "residual_value": "",
                "source_extra": "",
                "units": "m",
                "vertical_reference": "STND",
            },
            {
                "observation_id": "dart-one",
                "source_id": "dart-source",
                "station_id": "dart",
                "source_time": "2011 03 11 05 46 24",
                "observed_at_utc": "2011-03-11T05:46:24Z",
                "raw_value": "10.0",
                "fitted_value": "9.0",
                "residual_value": "1.0",
                "source_extra": "",
                "units": "m water column",
                "vertical_reference": "unknown",
            },
            {
                "observation_id": "dart-two",
                "source_id": "dart-source",
                "station_id": "dart",
                "source_time": "2011 03 11 05 47 24",
                "observed_at_utc": "2011-03-11T05:47:24Z",
                "raw_value": "11.0",
                "fitted_value": "9.5",
                "residual_value": "1.5",
                "source_extra": "",
                "units": "m water column",
                "vertical_reference": "unknown",
            },
        ],
    )
    _write_csv(
        processed / "ttt_contour.csv",
        TTT_COLUMNS,
        [
            {
                "contour_id": "one-a",
                "source_object_id": "1",
                "hours": "1",
                "coordinates": json.dumps([[170.0, 0.0], [float(contour_longitude), 1.0]]),
                "crs": "EPSG:4326",
                "coordinate_order": "longitude, latitude",
                "longitude_boundary_precision": boundary_precision,
                "crosses_antimeridian": "false",
            },
            {
                "contour_id": "six-a",
                "source_object_id": "6",
                "hours": "6",
                "coordinates": json.dumps([[-170.0, 0.0], [-160.0, 1.0]]),
                "crs": "EPSG:4326",
                "coordinate_order": "longitude, latitude",
                "longitude_boundary_precision": "false",
                "crosses_antimeridian": "false",
            },
        ],
    )
    (processed / "accounting.json").write_text(
        json.dumps({"row_counts": {"event": 1, "station": 2, "observation": 4}}),
        encoding="utf-8",
    )
    missingness_summary = root / "missingness-summary.json"
    missingness_summary.write_text(
        json.dumps({"coastal_windows": [{"station_id": "coast"}]}),
        encoding="utf-8",
    )
    return processed, missingness_summary


def _write_fixture_config(path: Path) -> None:
    path.write_text(
        """schema_version = "1"
event_id = "official20110311054624120_30"
evidence_state = "preliminary_storyboard_evidence"
display_crs = "+proj=eqearth +lon_0=-160 +datum=WGS84 +units=m +no_defs +type=crs"
central_meridian = -160.0
start_hours = -6.0
end_hours = 30.0
highlighted_contour_hours = [1, 6]
range_radii_km = [2500]
dart_station_ids = ["dart"]
coastal_station_ids = ["coast"]
figure_dpi = 160
""",
        encoding="utf-8",
    )


def _write_coastline(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "name": "fixture-coastline",
                "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
                "features": [
                    {
                        "type": "Feature",
                        "properties": {"feature_id": "west"},
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [[-10.0, -20.0], [10.0, 20.0]],
                        },
                    },
                    {
                        "type": "Feature",
                        "properties": {"feature_id": "east"},
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [[30.0, -20.0], [40.0, 20.0]],
                        },
                    },
                ],
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def test_atlas_loader_preserves_source_semantics(tmp_path: Path) -> None:
    processed, missingness_summary = _stage_atlas_inputs(tmp_path)

    atlas = load_atlas_inputs(processed, missingness_summary)

    assert atlas.event.event_id == "official20110311054624120_30"
    assert [station.station_type for station in atlas.stations] == ["coastal", "dart"]
    assert atlas.observations[0].source_time == "2011-03-11 05:46"
    assert atlas.observations[0].raw_value == 0.0
    assert atlas.observations[0].residual_value is None
    assert atlas.contours[0].crs == "EPSG:4326"
    assert atlas.contours[0].coordinate_order == "longitude, latitude"
    assert atlas.contours[0].crosses_antimeridian is False


def test_atlas_loader_rejects_unflagged_longitude_outside_precision_tolerance(
    tmp_path: Path,
) -> None:
    processed, missingness_summary = _stage_atlas_inputs(
        tmp_path, contour_longitude="180.000002", boundary_precision="false"
    )

    with pytest.raises(AtlasError, match="longitude"):
        load_atlas_inputs(processed, missingness_summary)


def test_pacific_shift_splits_a_line_at_the_twenty_degree_seam() -> None:
    assert shift_longitude(30.0) == -330.0
    assert split_at_display_seam(((-10.0, 0.0), (30.0, 0.0))) == (
        ((-10.0, 0.0), (20.0, 0.0)),
        ((-340.0, 0.0), (-330.0, 0.0)),
    )
    assert split_at_display_seam(((30.0, 0.0), (-10.0, 10.0))) == (
        ((-330.0, 0.0), (-340.0, 2.5)),
        ((20.0, 2.5), (-10.0, 10.0)),
    )


def test_geodesic_range_ring_uses_kilometres_without_a_speed_model() -> None:
    ring = geodesic_range_ring(latitude=38.297, longitude=142.373, radius_km=2500)

    assert len(ring) == 361
    _, _, distance_m = Geod(ellps="WGS84").inv(142.373, 38.297, ring[0][0], ring[0][1])
    assert distance_m == pytest.approx(2_500_000, abs=1.0)


def test_stage_a_scope_matches_configured_event_stations_and_windows(tmp_path: Path) -> None:
    processed, missingness_summary = _stage_atlas_inputs(tmp_path)
    config_path = tmp_path / "story-atlas.toml"
    _write_fixture_config(config_path)

    atlas = load_atlas_inputs(processed, missingness_summary)
    config = load_atlas_config(config_path)
    validate_stage_a_scope(
        atlas,
        config,
        (
            ExpectedWindow(
                station_id="coast",
                name="Coastal fixture",
                start_utc="2011-03-11T00:00:00Z",
                end_utc_exclusive="2011-03-11T01:00:00Z",
                cadence_seconds=60,
            ),
        ),
    )

    assert config.dart_station_ids == ("dart",)
    assert config.coastal_station_ids == ("coast",)


def test_project_story_config_fixes_the_approved_four_plus_six_scope() -> None:
    config = load_atlas_config(Path("config/story-atlas.toml"))

    assert config.dart_station_ids == ("21413", "21418", "32401", "46411")
    assert config.coastal_station_ids == (
        "1617760",
        "1770000",
        "9419750",
        "9461380",
        "saip",
        "valp",
    )


def test_pacific_evidence_map_is_deterministic_and_records_geometry_counts(
    tmp_path: Path,
) -> None:
    processed, missingness_summary = _stage_atlas_inputs(tmp_path)
    config_path = tmp_path / "story-atlas.toml"
    coastline_path = tmp_path / "coastline.geojson"
    _write_fixture_config(config_path)
    _write_coastline(coastline_path)
    atlas = load_atlas_inputs(processed, missingness_summary)
    config = load_atlas_config(config_path)

    first = plot_pacific_evidence(atlas, config, coastline_path, tmp_path / "first")
    second = plot_pacific_evidence(atlas, config, coastline_path, tmp_path / "second")

    assert first.png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert b"Pacific evidence map" in first.svg.read_bytes()
    assert sha256(first.png.read_bytes()).hexdigest() == sha256(second.png.read_bytes()).hexdigest()
    assert sha256(first.svg.read_bytes()).hexdigest() == sha256(second.svg.read_bytes()).hexdigest()
    assert first.projection == config.display_crs
    assert first.input_parts == len(atlas.contours) + 2
    assert first.output_parts >= first.input_parts


def test_distance_contour_diagnostic_keeps_incompatible_units_separate(
    tmp_path: Path,
) -> None:
    processed, missingness_summary = _stage_atlas_inputs(tmp_path)
    config_path = tmp_path / "story-atlas.toml"
    coastline_path = tmp_path / "coastline.geojson"
    _write_fixture_config(config_path)
    _write_coastline(coastline_path)
    atlas = load_atlas_inputs(processed, missingness_summary)
    config = load_atlas_config(config_path)

    first = plot_distance_contour_diagnostic(
        atlas,
        config,
        coastline_path,
        tmp_path / "first-distance",
    )
    second = plot_distance_contour_diagnostic(
        atlas,
        config,
        coastline_path,
        tmp_path / "second-distance",
    )

    assert first.plot_id == "04_distance_contour_diagnostic"
    assert first.units == "left: geodesic kilometres; right: published contour hours"
    assert first.projection == config.display_crs
    assert first.png.is_file()
    assert first.svg.is_file()
    assert b"No speed conversion" in first.svg.read_bytes()
    assert b"not a modeled arrival at a station" in first.svg.read_bytes()
    assert sha256(first.png.read_bytes()).hexdigest() == sha256(second.png.read_bytes()).hexdigest()
    assert sha256(first.svg.read_bytes()).hexdigest() == sha256(second.svg.read_bytes()).hexdigest()


def test_series_panels_preserve_station_specific_source_semantics(tmp_path: Path) -> None:
    processed, missingness_summary = _stage_atlas_inputs(tmp_path)
    config_path = tmp_path / "story-atlas.toml"
    _write_fixture_config(config_path)
    atlas = load_atlas_inputs(processed, missingness_summary)
    config = load_atlas_config(config_path)

    panels = build_series_panels(atlas, config)

    assert panels[0].station_type == "coastal"
    assert panels[0].value_field == "raw_value"
    assert panels[0].points[0].value == 0.0
    assert panels[1].station_type == "dart"
    assert panels[1].value_field == "residual_value"
    assert [point.value for point in panels[1].points] == [1.0, 1.5]
    assert all(
        config.start_hours <= point.elapsed_hours <= config.end_hours
        for panel in panels
        for point in panel.points
    )
    assert {panel.shared_y_scale for panel in panels} == {False}


def test_station_timeseries_is_deterministic_and_warns_against_amplitude_comparison(
    tmp_path: Path,
) -> None:
    processed, missingness_summary = _stage_atlas_inputs(tmp_path)
    config_path = tmp_path / "story-atlas.toml"
    _write_fixture_config(config_path)
    atlas = load_atlas_inputs(processed, missingness_summary)
    config = load_atlas_config(config_path)
    panels = build_series_panels(atlas, config)

    first = plot_station_timeseries(panels, config, tmp_path / "first-series")
    second = plot_station_timeseries(panels, config, tmp_path / "second-series")

    assert first.plot_id == "03_station_timeseries"
    assert first.units == "station-local source units"
    assert first.projection == "not applicable"
    assert b"Panel amplitudes are not comparable" in first.svg.read_bytes()
    assert sha256(first.png.read_bytes()).hexdigest() == sha256(second.png.read_bytes()).hexdigest()
    assert sha256(first.svg.read_bytes()).hexdigest() == sha256(second.svg.read_bytes()).hexdigest()


def test_observation_coverage_plot_preserves_all_missingness_states(
    tmp_path: Path,
) -> None:
    timeline = CoastalCoverageTimeline(
        station_id="coast",
        name="Coastal fixture",
        start_utc="2011-03-11T00:00:00Z",
        end_utc_exclusive="2011-03-11T00:03:00Z",
        cadence_seconds=60,
        positions=(
            CoveragePosition("coast", "2011-03-11T00:00:00Z", "observed"),
            CoveragePosition("coast", "2011-03-11T00:01:00Z", "source_blank"),
            CoveragePosition("coast", "2011-03-11T00:02:00Z", "absent_timestamp"),
        ),
        off_grid=(OffGridObservation("coast", "2011-03-11T00:00:59Z", True),),
    )
    summary: dict[str, object] = {
        "coastal_windows": [
            {
                "station_id": "coast",
                "name": "Coastal fixture",
                "strict_coverage_percent": 33.3333,
                "sample_density_coverage_percent": 66.6667,
            }
        ]
    }

    first = plot_observation_coverage(
        (timeline,),
        missingness_summary=summary,
        output_stem=tmp_path / "first-coverage",
    )
    second = plot_observation_coverage(
        (timeline,),
        missingness_summary=summary,
        output_stem=tmp_path / "second-coverage",
    )

    assert first.plot_id == "02_observation_coverage"
    assert first.units == "source-supported timestamp coverage"
    assert first.projection == "not applicable"
    assert first.png.is_file()
    assert first.svg.is_file()
    assert b"Off-grid ticks are preserved rather than snapped" in first.svg.read_bytes()
    assert b"Gray absence is not numeric zero" in first.svg.read_bytes()
    assert sha256(first.png.read_bytes()).hexdigest() == sha256(second.png.read_bytes()).hexdigest()
    assert sha256(first.svg.read_bytes()).hexdigest() == sha256(second.svg.read_bytes()).hexdigest()
