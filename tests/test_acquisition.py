import hashlib
from pathlib import Path, PurePosixPath
from urllib.error import URLError

from pipeline.acquisition import (
    ResponseMetadata,
    SourceContract,
    acquire_all,
    acquire_source,
    load_contracts,
)


def fixture_fetcher(payload: bytes):
    """Return a fetcher that writes fixture bytes to its requested destination."""

    def fetcher(url: str, destination: Path, timeout_seconds: float) -> ResponseMetadata:
        del url, timeout_seconds
        destination.write_bytes(payload)
        return ResponseMetadata(content_type="application/json", headers={})

    return fetcher


def test_acquire_source_writes_verified_bytes_atomically(tmp_path: Path) -> None:
    contract = SourceContract(
        source_id="sample",
        source_class="event",
        availability="approved",
        url="https://example.test/sample.json",
        local_path=PurePosixPath("data/raw/sample.json"),
        format="json",
        publisher="fixture",
        expected_content_signature="fixture JSON object",
        expected_prefix="{",
        units="not applicable",
        crs="not applicable",
        horizontal_datum="not applicable",
        vertical_datum="not applicable",
        coordinate_order="not applicable",
        temporal_semantics="not applicable",
        station_metadata="not applicable",
        reason="not applicable",
    )

    payload = (Path(__file__).parent / "fixtures/acquisition/sample.json").read_bytes().rstrip()
    result = acquire_source(contract, tmp_path, fetcher=fixture_fetcher(payload))

    assert result.status == "downloaded"
    assert result.bytes == 11
    assert result.sha256 == hashlib.sha256(payload).hexdigest()
    assert (tmp_path / contract.local_path).read_bytes() == payload


def test_acquire_source_reuses_a_verified_cache_without_fetching(tmp_path: Path) -> None:
    contract = SourceContract(
        source_id="sample",
        source_class="event",
        availability="approved",
        url="https://example.test/sample.json",
        local_path=PurePosixPath("data/raw/sample.json"),
        format="json",
        publisher="fixture",
        expected_content_signature="fixture JSON object",
        expected_prefix="{",
        units="not applicable",
        crs="not applicable",
        horizontal_datum="not applicable",
        vertical_datum="not applicable",
        coordinate_order="not applicable",
        temporal_semantics="not applicable",
        station_metadata="not applicable",
        reason="not applicable",
    )
    payload = b'{"ok":true}'
    acquire_source(contract, tmp_path, fetcher=fixture_fetcher(payload))

    def unfetched(url: str, destination: Path, timeout_seconds: float) -> ResponseMetadata:
        del url, destination, timeout_seconds
        raise AssertionError("cache reuse must not fetch")

    result = acquire_source(contract, tmp_path, fetcher=unfetched)

    assert result.status == "cached"
    assert result.sha256 == hashlib.sha256(payload).hexdigest()


def test_acquire_source_quarantines_an_invalid_existing_file(tmp_path: Path) -> None:
    contract = SourceContract(
        source_id="sample",
        source_class="event",
        availability="approved",
        url="https://example.test/sample.json",
        local_path=PurePosixPath("data/raw/sample.json"),
        format="json",
        publisher="fixture",
        expected_content_signature="fixture JSON object",
        expected_prefix="{",
        units="not applicable",
        crs="not applicable",
        horizontal_datum="not applicable",
        vertical_datum="not applicable",
        coordinate_order="not applicable",
        temporal_semantics="not applicable",
        station_metadata="not applicable",
        reason="not applicable",
    )
    target = tmp_path / contract.local_path
    target.parent.mkdir(parents=True)
    target.write_bytes(b"unexpected")

    result = acquire_source(contract, tmp_path, fetcher=fixture_fetcher(b'{"ok":true}'))

    assert result.status == "quarantined"
    assert result.reason == "existing_checksum_conflict"
    assert target.read_bytes() == b"unexpected"


def test_acquire_all_isolates_a_transient_source_failure_in_source_id_order(tmp_path: Path) -> None:
    contracts = (
        SourceContract(
            source_id="z-fails",
            source_class="event",
            availability="approved",
            url="https://example.test/fails",
            local_path=PurePosixPath("data/raw/fails.json"),
            format="json",
            publisher="fixture",
            expected_content_signature="fixture JSON object",
            expected_prefix="{",
            units="not applicable",
            crs="not applicable",
            horizontal_datum="not applicable",
            vertical_datum="not applicable",
            coordinate_order="not applicable",
            temporal_semantics="not applicable",
            station_metadata="not applicable",
            reason="not applicable",
        ),
        SourceContract(
            source_id="a-downloads",
            source_class="event",
            availability="approved",
            url="https://example.test/downloads",
            local_path=PurePosixPath("data/raw/downloads.json"),
            format="json",
            publisher="fixture",
            expected_content_signature="fixture JSON object",
            expected_prefix="{",
            units="not applicable",
            crs="not applicable",
            horizontal_datum="not applicable",
            vertical_datum="not applicable",
            coordinate_order="not applicable",
            temporal_semantics="not applicable",
            station_metadata="not applicable",
            reason="not applicable",
        ),
    )

    def fetcher(url: str, destination: Path, timeout_seconds: float) -> ResponseMetadata:
        del timeout_seconds
        if url.endswith("fails"):
            raise URLError("temporary outage")
        destination.write_bytes(b'{"ok":true}')
        return ResponseMetadata(content_type="application/json", headers={})

    results = acquire_all(contracts, tmp_path, fetcher=fetcher)

    assert [result.source_id for result in results] == ["a-downloads", "z-fails"]
    assert [result.status for result in results] == ["downloaded", "quarantined"]


def test_acquire_source_never_fetches_a_blocked_contract(tmp_path: Path) -> None:
    contract = SourceContract(
        source_id="blocked",
        source_class="event",
        availability="blocked",
        url="https://example.test/blocked",
        local_path=PurePosixPath("not-downloaded"),
        format="unknown",
        publisher="fixture",
        expected_content_signature="unknown",
        expected_prefix="not applicable",
        units="unknown",
        crs="unknown",
        horizontal_datum="unknown",
        vertical_datum="unknown",
        coordinate_order="unknown",
        temporal_semantics="unknown",
        station_metadata="not applicable",
        reason="source access is blocked",
    )

    def must_not_fetch(url: str, destination: Path, timeout_seconds: float) -> ResponseMetadata:
        del url, destination, timeout_seconds
        raise AssertionError("blocked contracts must never fetch")

    result = acquire_source(contract, tmp_path, fetcher=must_not_fetch)

    assert result.status == "blocked"
    assert result.reason == "source access is blocked"


def test_load_contracts_preserves_the_approved_source_contract_fields() -> None:
    contracts = load_contracts(Path("config/tohoku-data-proof.toml"))

    event = next(
        contract for contract in contracts if contract.source_id == "usgs-tohoku-origin-csv"
    )
    blocked = next(contract for contract in contracts if contract.availability == "blocked")

    assert len(contracts) == 15
    assert event.expected_content_signature.startswith("One CSV row")
    assert event.expected_prefix == "time,latitude,longitude,depth"
    assert event.crs == "WGS84 horizontal coordinates"
    assert event.temporal_semantics == "origin timestamp is UTC; record update is source metadata"
    assert event.station_metadata == "not applicable"
    assert event.reason == "not applicable"
    assert blocked.reason != "not applicable"


def test_acquire_source_limits_the_prefix_identity_check_to_a_leading_window(
    tmp_path: Path,
) -> None:
    contract = SourceContract(
        source_id="sample",
        source_class="event",
        availability="approved",
        url="https://example.test/sample.json",
        local_path=PurePosixPath("data/raw/sample.json"),
        format="json",
        publisher="fixture",
        expected_content_signature="fixture JSON object",
        expected_prefix="{",
        units="not applicable",
        crs="not applicable",
        horizontal_datum="not applicable",
        vertical_datum="not applicable",
        coordinate_order="not applicable",
        temporal_semantics="not applicable",
        station_metadata="not applicable",
        reason="not applicable",
    )

    result = acquire_source(contract, tmp_path, fetcher=fixture_fetcher(b" " * 65_536 + b"{}"))

    assert result.status == "quarantined"
    assert result.reason == "content_signature_mismatch"
