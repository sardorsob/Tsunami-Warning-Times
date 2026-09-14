# pyright: reportUnknownMemberType=false
"""Deterministic static plots for preliminary visual-story evidence.

Pyright's third-party GeoPandas and Matplotlib signatures retain unknown
keyword types; source-owned values and geometry objects remain explicitly typed.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import cast

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "svg.fonttype": "none",
        "svg.hashsalt": "pacific-tsunami-warning-time",
    }
)

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from pyproj import CRS  # noqa: E402
from shapely.geometry import LineString, MultiLineString, Point  # noqa: E402
from shapely.geometry.base import BaseGeometry  # noqa: E402

from analysis.story.atlas import (  # noqa: E402
    AtlasConfig,
    AtlasError,
    AtlasInputs,
    Coordinate,
    SeriesPanel,
    geodesic_range_ring,
    shift_longitude,
    split_at_display_seam,
)
from pipeline.missingness import CoastalCoverageTimeline, CoverageStatus  # noqa: E402


@dataclass(frozen=True, slots=True)
class PlotFiles:
    """Paths and spatial accounting for one deterministic plot."""

    plot_id: str
    png: Path
    svg: Path
    projection: str
    units: str
    input_parts: int
    output_parts: int


@dataclass(frozen=True, slots=True)
class _CoverageMetric:
    station_id: str
    name: str
    strict_percent: float
    sample_density_percent: float


def _save_figure(figure: Figure, output_stem: Path, *, dpi: int) -> tuple[Path, Path]:
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    png = output_stem.with_suffix(".png")
    svg = output_stem.with_suffix(".svg")
    figure.savefig(
        png,
        dpi=dpi,
        bbox_inches="tight",
        metadata={"Software": "pacific-tsunami-warning-time"},
    )
    figure.savefig(
        svg,
        bbox_inches="tight",
        metadata={"Date": None, "Creator": "pacific-tsunami-warning-time"},
    )
    plt.close(figure)
    return png, svg


def _parse_plot_utc(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise AtlasError(f"invalid coverage timestamp {value!r}") from error
    if not value.endswith("Z") or parsed.utcoffset() != UTC.utcoffset(parsed):
        raise AtlasError(f"coverage timestamp is not explicit UTC: {value!r}")
    return parsed


def _coverage_percent(value: object, *, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise AtlasError(f"missingness summary {field} must be numeric")
    result = float(value)
    if not math.isfinite(result) or not 0.0 <= result <= 100.0:
        raise AtlasError(f"missingness summary {field} must be between 0 and 100")
    return result


def _coverage_metrics(
    missingness_summary: dict[str, object],
    timelines: tuple[CoastalCoverageTimeline, ...],
) -> dict[str, _CoverageMetric]:
    raw_windows = missingness_summary.get("coastal_windows")
    if not isinstance(raw_windows, list) or not raw_windows:
        raise AtlasError("missingness summary requires coastal_windows")
    metrics: dict[str, _CoverageMetric] = {}
    for raw_window in cast(list[object], raw_windows):
        if not isinstance(raw_window, dict):
            raise AtlasError("missingness summary coastal window must be an object")
        window = cast(dict[str, object], raw_window)
        station_id = window.get("station_id")
        name = window.get("name")
        if not isinstance(station_id, str) or not isinstance(name, str):
            raise AtlasError("missingness summary coastal window lacks station identity")
        if station_id in metrics:
            raise AtlasError(f"duplicate missingness metric for {station_id!r}")
        metrics[station_id] = _CoverageMetric(
            station_id=station_id,
            name=name,
            strict_percent=_coverage_percent(
                window.get("strict_coverage_percent"),
                field=f"{station_id} strict_coverage_percent",
            ),
            sample_density_percent=_coverage_percent(
                window.get("sample_density_coverage_percent"),
                field=f"{station_id} sample_density_coverage_percent",
            ),
        )
    timeline_ids = {timeline.station_id for timeline in timelines}
    if set(metrics) != timeline_ids:
        raise AtlasError("coverage timelines and missingness metrics must have identical stations")
    return metrics


def _status_spans(
    timeline: CoastalCoverageTimeline,
) -> dict[CoverageStatus, list[tuple[float, float]]]:
    if not timeline.positions:
        raise AtlasError(f"coverage timeline {timeline.station_id!r} has no positions")
    expected_start = _parse_plot_utc(timeline.start_utc)
    expected_end = _parse_plot_utc(timeline.end_utc_exclusive)
    cadence = timedelta(seconds=timeline.cadence_seconds)
    spans: dict[CoverageStatus, list[tuple[float, float]]] = {
        "observed": [],
        "source_blank": [],
        "absent_timestamp": [],
    }
    run_status = timeline.positions[0].status
    run_start = _parse_plot_utc(timeline.positions[0].expected_at_utc)
    previous = run_start
    for position in timeline.positions:
        if position.station_id != timeline.station_id:
            raise AtlasError(f"coverage position has wrong station for {timeline.station_id!r}")
        current = _parse_plot_utc(position.expected_at_utc)
        if current < expected_start or current >= expected_end:
            raise AtlasError(f"coverage position lies outside {timeline.station_id!r} window")
        if current != previous and current != previous + cadence:
            raise AtlasError(f"coverage timeline {timeline.station_id!r} is not an exact grid")
        if position.status != run_status:
            start_number = cast(float, mdates.date2num(run_start))
            end_number = cast(float, mdates.date2num(previous + cadence))
            spans[run_status].append((start_number, end_number - start_number))
            run_status = position.status
            run_start = current
        previous = current
    start_number = cast(float, mdates.date2num(run_start))
    end_number = cast(float, mdates.date2num(previous + cadence))
    spans[run_status].append((start_number, end_number - start_number))
    return spans


def plot_observation_coverage(
    timelines: tuple[CoastalCoverageTimeline, ...],
    *,
    missingness_summary: dict[str, object],
    output_stem: Path,
) -> PlotFiles:
    """Render source-supported coastal coverage without interpolation or snapping."""
    if not timelines:
        raise AtlasError("at least one coastal coverage timeline is required")
    station_ids = [timeline.station_id for timeline in timelines]
    if len(set(station_ids)) != len(station_ids):
        raise AtlasError("coverage timelines contain duplicate station IDs")
    metrics = _coverage_metrics(missingness_summary, timelines)

    figure = plt.figure(figsize=(13.0, 1.35 * len(timelines) + 2.4))
    figure.patch.set_facecolor("#fbfaf7")
    axes_list: list[Axes] = []
    status_colors: dict[CoverageStatus, str] = {
        "observed": "#277da1",
        "source_blank": "#f4a261",
        "absent_timestamp": "#c7c9c8",
    }
    for panel_index, timeline in enumerate(timelines, start=1):
        axes = figure.add_subplot(len(timelines), 1, panel_index)
        axes_list.append(axes)
        spans = _status_spans(timeline)
        for status, color in status_colors.items():
            if spans[status]:
                axes.broken_barh(
                    spans[status],
                    (0.0, 1.0),
                    facecolors=color,
                    edgecolors="none",
                    zorder=1,
                )
        start = _parse_plot_utc(timeline.start_utc)
        end = _parse_plot_utc(timeline.end_utc_exclusive)
        for observation in timeline.off_grid:
            if observation.station_id != timeline.station_id:
                raise AtlasError(
                    f"off-grid observation has wrong station for {timeline.station_id}"
                )
            observed_at = _parse_plot_utc(observation.observed_at_utc)
            if observed_at < start or observed_at >= end:
                raise AtlasError(
                    f"off-grid observation lies outside {timeline.station_id!r} window"
                )
            axes.vlines(
                cast(float, mdates.date2num(observed_at)),
                0.02,
                0.98,
                colors="#202124" if observation.raw_value_available else "#9c2f45",
                linewidth=0.55,
                zorder=3,
            )
        metric = metrics[timeline.station_id]
        axes.set_xlim(
            cast(float, mdates.date2num(start)),
            cast(float, mdates.date2num(end)),
        )
        axes.set_ylim(0.0, 1.0)
        axes.set_yticks([])
        axes.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=2, maxticks=4))
        axes.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%H:%M", tz=UTC))
        axes.tick_params(axis="x", labelsize=7, colors="#526068", length=2)
        for spine in axes.spines.values():
            spine.set_visible(False)
        axes.set_title(
            f"{timeline.name} · {timeline.station_id}",
            loc="left",
            fontsize=9,
            fontweight="bold",
            pad=3,
        )
        axes.text(
            1.0,
            1.08,
            f"strict {metric.strict_percent:.2f}% · sample density "
            f"{metric.sample_density_percent:.2f}%",
            transform=axes.transAxes,
            ha="right",
            va="bottom",
            fontsize=7.5,
            color="#394850",
        )

    weakest = sorted(metrics.values(), key=lambda item: (item.strict_percent, item.station_id))[:2]
    weakest_names = ", ".join(metric.name for metric in weakest)
    figure.suptitle(
        "Observation coverage by source-supported window",
        x=0.08,
        y=0.985,
        ha="left",
        fontsize=16,
        fontweight="bold",
        color="#17242b",
    )
    figure.legend(
        handles=[
            Patch(facecolor=status_colors["observed"], label="Exact observed value"),
            Patch(facecolor=status_colors["source_blank"], label="Retained source blank"),
            Patch(facecolor=status_colors["absent_timestamp"], label="Absent timestamp"),
            Line2D([], [], color="#202124", linewidth=1.0, label="Off-grid observation"),
        ],
        loc="lower center",
        ncol=4,
        frameon=False,
        fontsize=8,
        bbox_to_anchor=(0.5, 0.065),
    )
    figure.text(
        0.08,
        0.012,
        "Off-grid ticks are preserved rather than snapped · Gray absence is not numeric zero · "
        f"lowest strict coverage from supplied metrics: {weakest_names} · "
        "preliminary_storyboard_evidence",
        ha="left",
        va="bottom",
        fontsize=7.5,
        color="#394850",
    )
    figure.subplots_adjust(left=0.08, right=0.98, top=0.90, bottom=0.18, hspace=0.95)

    png, svg = _save_figure(figure, output_stem, dpi=160)
    represented_positions = sum(
        len(timeline.positions) + len(timeline.off_grid) for timeline in timelines
    )
    return PlotFiles(
        plot_id="02_observation_coverage",
        png=png,
        svg=svg,
        projection="not applicable",
        units="source-supported timestamp coverage",
        input_parts=represented_positions,
        output_parts=represented_positions,
    )


def plot_station_timeseries(
    panels: tuple[SeriesPanel, ...],
    config: AtlasConfig,
    output_stem: Path,
) -> PlotFiles:
    """Render station-local point traces without bridging gaps or comparing amplitudes."""
    if not panels:
        raise AtlasError("at least one station series panel is required")
    station_ids = [panel.station_id for panel in panels]
    if len(set(station_ids)) != len(station_ids):
        raise AtlasError("series panels contain duplicate station IDs")
    expected_order = sorted(panels, key=lambda item: (item.station_type, item.station_id))
    if list(panels) != expected_order:
        raise AtlasError("series panels must be ordered by station type then station ID")
    if any(panel.shared_y_scale for panel in panels):
        raise AtlasError("Stage A station panels must use local y-scales")

    columns = 2
    rows = math.ceil(len(panels) / columns)
    figure = plt.figure(figsize=(13.0, rows * 2.2 + 1.8))
    figure.patch.set_facecolor("#fbfaf7")
    for panel_index, panel in enumerate(panels, start=1):
        axes = figure.add_subplot(rows, columns, panel_index)
        color = "#2a9d8f" if panel.station_type == "coastal" else "#d99028"
        x_values = [point.elapsed_hours for point in panel.points]
        y_values = [point.value for point in panel.points]
        axes.scatter(
            x_values,
            y_values,
            s=5.0,
            color=color,
            edgecolors="none",
            alpha=0.72,
            rasterized=False,
            zorder=2,
        )
        axes.axvline(0.0, color="#66747b", linewidth=0.7, linestyle="--", zorder=1)
        axes.set_xlim(config.start_hours, config.end_hours)
        axes.grid(axis="y", color="#d7dcda", linewidth=0.5, alpha=0.75)
        axes.tick_params(axis="both", labelsize=7, colors="#526068", length=2)
        axes.spines["top"].set_visible(False)
        axes.spines["right"].set_visible(False)
        axes.spines["left"].set_color("#9ba5a1")
        axes.spines["bottom"].set_color("#9ba5a1")
        axes.set_title(
            f"{panel.station_name} · {panel.station_id}",
            loc="left",
            fontsize=9,
            fontweight="bold",
            pad=12,
        )
        axes.text(
            0.0,
            1.01,
            f"{panel.value_field} · {panel.units} · vertical reference "
            f"{panel.vertical_reference} · local y-scale",
            transform=axes.transAxes,
            ha="left",
            va="bottom",
            fontsize=6.8,
            color="#44535a",
        )
        if not panel.points:
            axes.text(
                0.5,
                0.5,
                "No numeric values in reviewed window",
                transform=axes.transAxes,
                ha="center",
                va="center",
                fontsize=8,
                color="#66747b",
            )

    for unused_index in range(len(panels) + 1, rows * columns + 1):
        unused = figure.add_subplot(rows, columns, unused_index)
        unused.set_axis_off()

    figure.suptitle(
        "Station signals around earthquake origin",
        x=0.07,
        y=0.992,
        ha="left",
        fontsize=16,
        fontweight="bold",
        color="#17242b",
    )
    figure.supxlabel("Hours from earthquake origin (verified UTC)", fontsize=9, y=0.045)
    figure.text(
        0.07,
        0.008,
        "Points are retained values; gaps are not bridged · Panel amplitudes are not comparable · "
        "coastal raw levels and DART residuals remain separate · "
        "preliminary_storyboard_evidence",
        ha="left",
        va="bottom",
        fontsize=7.5,
        color="#394850",
    )
    figure.subplots_adjust(left=0.07, right=0.98, top=0.92, bottom=0.10, hspace=0.60, wspace=0.22)

    png, svg = _save_figure(figure, output_stem, dpi=config.figure_dpi)
    point_count = sum(len(panel.points) for panel in panels)
    return PlotFiles(
        plot_id="03_station_timeseries",
        png=png,
        svg=svg,
        projection="not applicable",
        units="station-local source units",
        input_parts=point_count,
        output_parts=point_count,
    )


def _draw_event_and_stations(
    axes: Axes,
    atlas: AtlasInputs,
    config: AtlasConfig,
) -> None:
    event_series = _project_points(
        [Point(shift_longitude(atlas.event.longitude), atlas.event.latitude)],
        config.display_crs,
    )
    event = cast(Point, event_series.iloc[0])
    axes.scatter(
        [event.x],
        [event.y],
        marker="*",
        s=95,
        facecolor="#d1495b",
        edgecolor="#2b2526",
        linewidth=0.6,
        zorder=5,
    )
    station_series = _project_points(
        [Point(shift_longitude(station.longitude), station.latitude) for station in atlas.stations],
        config.display_crs,
    )
    station_geometries = cast(Iterable[BaseGeometry], station_series)
    for station, geometry in zip(atlas.stations, station_geometries, strict=True):
        point = cast(Point, geometry)
        is_dart = station.station_type == "dart"
        axes.scatter(
            [point.x],
            [point.y],
            marker="^" if is_dart else "o",
            s=22,
            facecolor="#f2b134" if is_dart else "#2a9d8f",
            edgecolor="#202623",
            linewidth=0.45,
            zorder=4,
        )
        axes.annotate(
            station.station_id,
            (point.x, point.y),
            xytext=(2.5, 2.5),
            textcoords="offset points",
            fontsize=5.5,
            color="#202623",
            zorder=5,
        )


def _line_extent(lines: gpd.GeoSeries) -> tuple[float, float, float, float]:
    geometries = tuple(cast(Iterable[BaseGeometry], lines))
    if not geometries:
        raise AtlasError("cannot derive an extent from empty linework")
    return (
        min(geometry.bounds[0] for geometry in geometries),
        min(geometry.bounds[1] for geometry in geometries),
        max(geometry.bounds[2] for geometry in geometries),
        max(geometry.bounds[3] for geometry in geometries),
    )


def plot_distance_contour_diagnostic(
    atlas: AtlasInputs,
    config: AtlasConfig,
    coastline_path: Path,
    output_stem: Path,
) -> PlotFiles:
    """Compare geodesic ring shape with published contour shape without conversion."""
    coastline_inputs = _load_coastline_parts(coastline_path)
    coastline_parts = tuple(
        part for source_part in coastline_inputs for part in split_at_display_seam(source_part)
    )
    projected_coastline = _project_lines(coastline_parts, config.display_crs)

    ring_sources = tuple(
        geodesic_range_ring(
            latitude=atlas.event.latitude,
            longitude=atlas.event.longitude,
            radius_km=radius_km,
        )
        for radius_km in config.range_radii_km
    )
    ring_parts_by_radius = tuple(
        (radius_km, split_at_display_seam(source))
        for radius_km, source in zip(config.range_radii_km, ring_sources, strict=True)
    )

    configured_hours = set(config.highlighted_contour_hours)
    selected_contours = tuple(
        contour
        for contour in atlas.contours
        if contour.hours.is_integer() and int(contour.hours) in configured_hours
    )
    available_hours = {int(contour.hours) for contour in selected_contours}
    if available_hours != configured_hours:
        raise AtlasError("distance diagnostic lacks one or more configured contour hours")
    selected_contour_parts = tuple(
        part for contour in selected_contours for part in split_at_display_seam(contour.coordinates)
    )

    figure = plt.figure(figsize=(14.0, 6.7))
    figure.patch.set_facecolor("#f7f4ed")
    left_axes = figure.add_subplot(1, 2, 1)
    right_axes = figure.add_subplot(1, 2, 2)
    for axes in (left_axes, right_axes):
        axes.set_facecolor("#eaf1f4")
        _draw_lines(
            axes,
            projected_coastline,
            color="#4b514d",
            linewidth=0.65,
            alpha=0.90,
        )
        _draw_event_and_stations(axes, atlas, config)

    radius_handles: list[Line2D] = []
    for radius_km, parts in ring_parts_by_radius:
        _draw_lines(
            left_axes,
            _project_lines(parts, config.display_crs),
            color="#8f4f8b",
            linewidth=0.9,
            alpha=0.70,
        )
        radius_handles.append(
            Line2D(
                [],
                [],
                color="#8f4f8b",
                linewidth=1.0,
                label=f"{radius_km:,} km",
            )
        )
    _draw_lines(
        right_axes,
        _project_lines(selected_contour_parts, config.display_crs),
        color="#397da8",
        linewidth=0.65,
        alpha=0.45,
    )

    min_x, min_y, max_x, max_y = _line_extent(projected_coastline)
    x_margin = (max_x - min_x) * 0.01
    y_margin = (max_y - min_y) * 0.035
    for axes in (left_axes, right_axes):
        axes.set_xlim(min_x - x_margin, max_x + x_margin)
        axes.set_ylim(min_y - y_margin, max_y + y_margin)
        axes.set_aspect("equal", adjustable="box")
        axes.set_axis_off()
    left_axes.set_title(
        "WGS84 geodesic range rings",
        loc="left",
        fontsize=12,
        fontweight="bold",
    )
    right_axes.set_title(
        "NCEI published travel-time contours",
        loc="left",
        fontsize=12,
        fontweight="bold",
    )
    left_axes.legend(
        handles=radius_handles,
        loc="lower left",
        ncol=2,
        fontsize=6.5,
        framealpha=0.94,
    )
    right_axes.legend(
        handles=[
            Line2D(
                [],
                [],
                color="#397da8",
                linewidth=1.1,
                label="Published hours: "
                + ", ".join(str(hour) for hour in config.highlighted_contour_hours),
            )
        ],
        loc="lower left",
        fontsize=6.5,
        framealpha=0.94,
    )
    figure.suptitle(
        "Distance and published contour shape are different evidence",
        x=0.045,
        y=0.985,
        ha="left",
        fontsize=16,
        fontweight="bold",
        color="#17242b",
    )
    figure.text(
        0.045,
        0.012,
        "Units differ · No speed conversion · nearest-contour values are not assigned to "
        "stations and are not a modeled arrival at a station · Equal Earth, central meridian "
        "160°W · preliminary_storyboard_evidence",
        ha="left",
        va="bottom",
        fontsize=7.5,
        color="#394850",
    )
    figure.subplots_adjust(left=0.04, right=0.99, top=0.91, bottom=0.09, wspace=0.04)

    png, svg = _save_figure(figure, output_stem, dpi=config.figure_dpi)
    input_parts = len(coastline_inputs) * 2 + len(ring_sources) + len(selected_contours)
    output_parts = (
        len(coastline_parts) * 2
        + sum(len(parts) for _, parts in ring_parts_by_radius)
        + len(selected_contour_parts)
    )
    return PlotFiles(
        plot_id="04_distance_contour_diagnostic",
        png=png,
        svg=svg,
        projection=config.display_crs,
        units="left: geodesic kilometres; right: published contour hours",
        input_parts=input_parts,
        output_parts=output_parts,
    )


def _two_dimensional_coordinates(line: LineString, *, label: str) -> tuple[Coordinate, ...]:
    coordinates: list[Coordinate] = []
    for coordinate in line.coords:
        if len(coordinate) != 2:
            raise AtlasError(f"{label} must contain two-dimensional coordinates")
        coordinates.append((float(coordinate[0]), float(coordinate[1])))
    if len(coordinates) < 2:
        raise AtlasError(f"{label} must contain at least two coordinates")
    return tuple(coordinates)


def _load_coastline_parts(path: Path) -> tuple[tuple[Coordinate, ...], ...]:
    try:
        coastline = gpd.read_file(path)
    except Exception as error:
        raise AtlasError(f"could not read coastline {path}: {error}") from error
    if coastline.crs is None or CRS.from_user_input(coastline.crs).to_epsg() != 4326:
        raise AtlasError("coastline must declare EPSG:4326")
    parts: list[tuple[Coordinate, ...]] = []
    geometries = cast(Iterable[BaseGeometry | None], coastline.geometry)
    for feature_index, geometry in enumerate(geometries):
        if geometry is None or geometry.is_empty:
            raise AtlasError(f"coastline feature {feature_index} is empty")
        if isinstance(geometry, LineString):
            lines = (geometry,)
        elif isinstance(geometry, MultiLineString):
            lines = tuple(geometry.geoms)
        else:
            raise AtlasError(
                f"coastline feature {feature_index} must be LineString or MultiLineString"
            )
        for part_index, line in enumerate(lines):
            parts.append(
                _two_dimensional_coordinates(
                    line,
                    label=f"coastline feature {feature_index} part {part_index}",
                )
            )
    if not parts:
        raise AtlasError("coastline contains no line geometry")
    return tuple(parts)


def _project_lines(parts: tuple[tuple[Coordinate, ...], ...], display_crs: str) -> gpd.GeoSeries:
    geographic = gpd.GeoSeries(
        [LineString(part) for part in parts],
        crs="EPSG:4326",
    )
    return geographic.to_crs(display_crs)


def _draw_lines(
    axes: Axes,
    lines: gpd.GeoSeries,
    *,
    color: str,
    linewidth: float,
    alpha: float,
) -> None:
    for geometry in cast(Iterable[BaseGeometry], lines):
        line = cast(LineString, geometry)
        x_values, y_values = line.xy
        axes.plot(
            x_values,
            y_values,
            color=color,
            linewidth=linewidth,
            alpha=alpha,
            solid_capstyle="round",
            zorder=1,
        )


def _project_points(points: list[Point], display_crs: str) -> gpd.GeoSeries:
    return gpd.GeoSeries(points, crs="EPSG:4326").to_crs(display_crs)


def plot_pacific_evidence(
    atlas: AtlasInputs,
    config: AtlasConfig,
    coastline_path: Path,
    output_stem: Path,
) -> PlotFiles:
    """Render the preliminary basin context without implying a continuous field."""
    coastline_inputs = _load_coastline_parts(coastline_path)
    coastline_parts = tuple(
        part for source_part in coastline_inputs for part in split_at_display_seam(source_part)
    )
    contour_parts = tuple(
        part for contour in atlas.contours for part in split_at_display_seam(contour.coordinates)
    )

    projected_coastline = _project_lines(coastline_parts, config.display_crs)
    projected_contours = _project_lines(contour_parts, config.display_crs)

    figure, axes = plt.subplots(figsize=(13.0, 7.6), constrained_layout=False)
    figure.patch.set_facecolor("#f7f4ed")
    axes.set_facecolor("#eaf1f4")
    _draw_lines(
        axes,
        projected_contours,
        color="#46789f",
        linewidth=0.5,
        alpha=0.30,
    )
    _draw_lines(
        axes,
        projected_coastline,
        color="#4b514d",
        linewidth=0.8,
        alpha=0.92,
    )

    event_points = _project_points(
        [Point(shift_longitude(atlas.event.longitude), atlas.event.latitude)],
        config.display_crs,
    )
    event_point = cast(Point, event_points.iloc[0])
    axes.scatter(
        [event_point.x],
        [event_point.y],
        marker="*",
        s=150,
        facecolor="#d1495b",
        edgecolor="#2b2526",
        linewidth=0.7,
        zorder=5,
    )
    axes.annotate(
        "2011 Tōhoku event",
        (event_point.x, event_point.y),
        xytext=(7, 7),
        textcoords="offset points",
        fontsize=8,
        color="#2b2526",
        zorder=6,
    )

    station_points = _project_points(
        [Point(shift_longitude(station.longitude), station.latitude) for station in atlas.stations],
        config.display_crs,
    )
    projected_station_points = cast(Iterable[BaseGeometry], station_points)
    for station, geometry in zip(atlas.stations, projected_station_points, strict=True):
        point = cast(Point, geometry)
        is_dart = station.station_type == "dart"
        axes.scatter(
            [point.x],
            [point.y],
            marker="^" if is_dart else "o",
            s=44 if is_dart else 38,
            facecolor="#f2b134" if is_dart else "#2a9d8f",
            edgecolor="#202623",
            linewidth=0.6,
            zorder=4,
        )
        axes.annotate(
            station.station_id,
            (point.x, point.y),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=7,
            color="#202623",
            zorder=5,
        )

    axes.set_aspect("equal", adjustable="datalim")
    axes.margins(x=0.015, y=0.04)
    axes.set_axis_off()
    axes.set_title(
        "Pacific evidence map",
        loc="left",
        fontsize=17,
        fontweight="bold",
        color="#17242b",
        pad=14,
    )
    axes.text(
        0.0,
        -0.015,
        "NCEI published hourly travel-time contours; not a continuous field\n"
        "Equal Earth, central meridian 160°W · preliminary_storyboard_evidence",
        transform=axes.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        color="#394850",
    )
    axes.legend(
        handles=[
            Line2D([], [], color="#46789f", linewidth=1.0, label="Published contours (h)"),
            Line2D(
                [],
                [],
                marker="^",
                linestyle="none",
                markerfacecolor="#f2b134",
                markeredgecolor="#202623",
                label="DART candidate",
            ),
            Line2D(
                [],
                [],
                marker="o",
                linestyle="none",
                markerfacecolor="#2a9d8f",
                markeredgecolor="#202623",
                label="Coastal candidate",
            ),
        ],
        loc="lower right",
        frameon=True,
        framealpha=0.95,
        fontsize=8,
    )

    png, svg = _save_figure(figure, output_stem, dpi=config.figure_dpi)
    return PlotFiles(
        plot_id="01_pacific_evidence_map",
        png=png,
        svg=svg,
        projection=config.display_crs,
        units="hours from earthquake origin",
        input_parts=len(coastline_inputs) + len(atlas.contours),
        output_parts=len(coastline_parts) + len(contour_parts),
    )
