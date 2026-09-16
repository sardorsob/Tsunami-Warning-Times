from importlib.metadata import version
from pathlib import Path


def test_static_story_geospatial_dependencies_are_exact() -> None:
    assert version("geopandas") == "1.1.4"
    assert version("matplotlib") == "3.11.2"


def test_story_analysis_namespace_imports() -> None:
    import analysis.story

    assert analysis.story.__doc__ == "Story-only descriptive analysis."


def test_story_notebook_is_a_thin_read_only_view() -> None:
    source = Path("notebooks/story/tohoku_storyboard_eda.py").read_text(encoding="utf-8")
    for forbidden in (
        "analysis.story.plots",
        "observation.csv",
        "station.csv",
        "mlflow",
        ".write_text(",
        "print(",
    ):
        assert forbidden not in source
