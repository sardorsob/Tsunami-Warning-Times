from pathlib import Path

from pipeline.acquisition import load_contracts
from pipeline.provenance import validate_manifest


def test_story_map_context_is_one_exact_public_domain_asset() -> None:
    contracts = load_contracts(Path("config/story-map-context.toml"))

    assert len(contracts) == 1
    contract = contracts[0]
    assert contract.source_id == "natural-earth-coastline-110m-v4.1.0"
    assert contract.url == (
        "https://naturalearth.s3.amazonaws.com/110m_physical/"
        "ne_110m_coastline.zip"
    )
    assert contract.local_path.as_posix() == (
        "data/raw/natural-earth/ne_110m_coastline_v4.1.0.zip"
    )
    assert contract.expected_prefix == "PK"


def test_story_source_manifest_is_valid() -> None:
    result = validate_manifest(Path("artifacts/provenance/story-source-manifest.csv"))

    assert result.records == 1
