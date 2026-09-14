# pyright: reportUnknownMemberType=false
"""Deterministic static plots for preliminary visual-story evidence.

Pyright's third-party GeoPandas and Matplotlib signatures retain unknown
keyword types; source-owned values and geometry objects remain explicitly typed.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
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

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from pyproj import CRS  # noqa: E402
from shapely.geometry import LineString, MultiLineString, Point  # noqa: E402
from shapely.geometry.base import BaseGeometry  # noqa: E402

from analysis.story.atlas import (  # noqa: E402
    AtlasConfig,
    AtlasError,
    AtlasInputs,
    Coordinate,
    shift_longitude,
    split_at_display_seam,
)


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
