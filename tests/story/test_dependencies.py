from importlib.metadata import version


def test_static_story_geospatial_dependencies_are_exact() -> None:
    assert version("geopandas") == "1.1.4"
    assert version("matplotlib") == "3.11.2"


def test_story_analysis_namespace_imports() -> None:
    import analysis.story

    assert analysis.story.__doc__ == "Story-only descriptive analysis."
