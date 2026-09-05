import hashlib
from dataclasses import replace
from email.message import Message
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError, URLError

import pytest

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
    assert (tmp_path / contract.local_path).with_name("sample.json.sha256").read_text() == (
        f"{result.sha256}\n"
    )


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
    assert result.reason == "missing_checksum_record"
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


def sample_contract(**changes: str | PurePosixPath) -> SourceContract:
    """Build a valid compact contract for focused acquisition tests."""
    contract = SourceContract(
        source_id="sample", source_class="event", availability="approved",
        url="https://example.test/sample.json", local_path=PurePosixPath("data/raw/sample.json"),
        format="json", publisher="fixture", expected_content_signature="fixture JSON object",
        expected_prefix="{", units="not applicable", crs="not applicable",
        horizontal_datum="not applicable", vertical_datum="not applicable",
        coordinate_order="not applicable", temporal_semantics="not applicable",
        station_metadata="not applicable", reason="not applicable",
    )
    return replace(contract, **changes)


def test_acquire_source_quarantines_tampered_bytes_with_a_stale_checksum(tmp_path: Path) -> None:
    contract = sample_contract()
    acquire_source(contract, tmp_path, fetcher=fixture_fetcher(b'{"ok":true}'))
    (tmp_path / contract.local_path).write_bytes(b'{"ok":false}')

    result = acquire_source(contract, tmp_path, fetcher=fixture_fetcher(b'{"ok":true}'))

    assert result.status == "quarantined"
    assert result.reason == "checksum_record_mismatch"


def test_acquire_source_does_not_clobber_a_race_created_destination(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    contract = sample_contract()
    target = tmp_path / contract.local_path
    import pipeline.acquisition as acquisition

    real_link = acquisition.os.link

    def race_link(source: str | Path, destination: str | Path, *args: object) -> None:
        if Path(destination) == target:
            target.write_bytes(b"race-winner")
            raise FileExistsError
        real_link(source, destination, *args)

    monkeypatch.setattr(acquisition.os, "link", race_link)
    result = acquire_source(contract, tmp_path, fetcher=fixture_fetcher(b'{"ok":true}'))

    assert result.status == "quarantined"
    assert target.read_bytes() == b"race-winner"


def test_acquire_all_isolates_a_malformed_local_parent(tmp_path: Path) -> None:
    bad = sample_contract(source_id="bad", local_path=PurePosixPath("blocked-parent/child.json"))
    good = sample_contract(source_id="good", local_path=PurePosixPath("data/good.json"))
    (tmp_path / "blocked-parent").write_text("not a directory", encoding="utf-8")

    results = acquire_all((bad, good), tmp_path, fetcher=fixture_fetcher(b'{"ok":true}'))

    assert [result.status for result in results] == ["quarantined", "downloaded"]


def test_acquire_source_quarantines_a_symlink_destination_outside_root(tmp_path: Path) -> None:
    contract = sample_contract(local_path=PurePosixPath("data/sample.json"))
    outside = tmp_path.parent / f"{tmp_path.name}-outside"
    outside.mkdir()
    (tmp_path / "data").symlink_to(outside, target_is_directory=True)

    result = acquire_source(contract, tmp_path, fetcher=fixture_fetcher(b'{"ok":true}'))

    assert result.status == "quarantined"
    assert result.reason == "destination_outside_root"


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ('source_id = "usgs-tohoku-origin-csv"', 'source_id = ""', "blank fields"),
        (
            'expected_prefix = "time,latitude,longitude,depth"',
            'expected_prefix = " "',
            "blank fields",
        ),
        (
            'local_path = "data/raw/usgs/official20110311054624120_30.csv"',
            'local_path = "."',
            "safe relative",
        ),
        (
            'source_id = "ncei-ttt-tohoku-layer17-metadata"',
            'source_id = "usgs-tohoku-origin-csv"',
            "duplicate source_id",
        ),
        (
            'local_path = "data/raw/ncei/ttt_contours_2011_tohoku_layer17.metadata.json"',
            'local_path = "data/raw/usgs/official20110311054624120_30.csv"',
            "namespace collision",
        ),
    ],
)
def test_load_contracts_rejects_invalid_contract_values(
    tmp_path: Path, old: str, new: str, message: str
) -> None:
    config = tmp_path / "invalid.toml"
    config.write_text(
        Path("config/tohoku-data-proof.toml").read_text(encoding="utf-8").replace(old, new, 1),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=message):
        load_contracts(config)


@pytest.mark.parametrize(("code", "attempts"), [(408, 2), (429, 2), (500, 2), (404, 1)])
def test_acquire_source_retries_only_transient_http_errors(
    tmp_path: Path, code: int, attempts: int
) -> None:
    calls = 0

    def fetcher(url: str, destination: Path, timeout_seconds: float) -> ResponseMetadata:
        nonlocal calls
        del url, timeout_seconds
        calls += 1
        if calls == 1:
            raise HTTPError("https://example.test", code, "error", Message(), None)
        destination.write_bytes(b'{"ok":true}')
        return ResponseMetadata(content_type="application/json", headers={})

    result = acquire_source(sample_contract(), tmp_path, fetcher=fetcher)

    assert calls == attempts
    assert result.status == ("downloaded" if code != 404 else "quarantined")


def test_acquire_all_isolates_a_non_utf8_checksum_record(tmp_path: Path) -> None:
    bad = sample_contract(source_id="bad", local_path=PurePosixPath("data/bad.json"))
    good = sample_contract(source_id="good", local_path=PurePosixPath("data/good.json"))
    acquire_source(bad, tmp_path, fetcher=fixture_fetcher(b'{"ok":true}'))
    (tmp_path / "data/bad.json.sha256").write_bytes(b"\xff")

    results = acquire_all((bad, good), tmp_path, fetcher=fixture_fetcher(b'{"ok":true}'))

    assert [result.status for result in results] == ["quarantined", "downloaded"]
    assert results[0].reason == "invalid_checksum_record"


def test_acquire_source_rolls_back_its_sidecar_after_raw_publication_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    contract = sample_contract()
    import pipeline.acquisition as acquisition

    real_link = acquisition.os.link

    def fail_raw_link(source: str | Path, destination: str | Path, *args: object) -> None:
        if Path(destination) == tmp_path / contract.local_path:
            raise OSError("injected raw publication failure")
        real_link(source, destination, *args)

    monkeypatch.setattr(acquisition.os, "link", fail_raw_link)
    failed = acquire_source(contract, tmp_path, fetcher=fixture_fetcher(b'{"ok":true}'))

    assert failed.status == "quarantined"
    assert not (tmp_path / contract.local_path).exists()
    assert not (tmp_path / "data/raw/sample.json.sha256").exists()
    monkeypatch.setattr(acquisition.os, "link", real_link)
    recovered = acquire_source(contract, tmp_path, fetcher=fixture_fetcher(b'{"ok":true}'))
    assert recovered.status == "downloaded"


def test_load_contracts_rejects_raw_sidecar_namespace_collision(tmp_path: Path) -> None:
    config = tmp_path / "collision.toml"
    source = Path("config/tohoku-data-proof.toml").read_text(encoding="utf-8")
    config.write_text(
        source.replace(
            'local_path = "data/raw/ncei/ttt_contours_2011_tohoku_layer17.metadata.json"',
            'local_path = "data/raw/usgs/official20110311054624120_30.csv.sha256"',
            1,
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="namespace collision"):
        load_contracts(config)
