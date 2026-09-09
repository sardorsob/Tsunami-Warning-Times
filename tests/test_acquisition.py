import hashlib
import json
from dataclasses import replace
from datetime import UTC, datetime
from email.message import Message
from http.client import IncompleteRead
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError, URLError
from urllib.request import Request

import pytest

from pipeline.acquisition import (
    AcquisitionResult,
    ResponseMetadata,
    SourceContract,
    acquire_all,
    acquire_source,
    load_contracts,
)
from scripts import acquire_tohoku as acquire_script
from scripts.acquire_tohoku import working_tree_status, write_run_evidence


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
    assert result.content_type == "application/json"
    assert result.headers == {}


def test_write_run_evidence_writes_an_immutable_portable_bundle(tmp_path: Path) -> None:
    config = tmp_path / "tohoku.toml"
    config.write_text("[assets]\n", encoding="utf-8")
    approved = sample_contract()
    blocked = replace(
        approved,
        source_id="blocked",
        availability="blocked",
        local_path=PurePosixPath("not-downloaded"),
        url="https://example.test/blocked",
        reason="source access is blocked",
    )
    results = (
        acquire_source(
            approved,
            tmp_path,
            fetcher=fixture_fetcher(b'{"ok":true}'),
        ),
        acquire_source(blocked, tmp_path),
    )

    run_path = write_run_evidence(
        root=tmp_path,
        run_tag="Initial Rerun!",
        config_path=config,
        contracts=(approved, blocked),
        results=results,
        command="uv run python scripts/acquire_tohoku.py --run-tag Initial Rerun!",
        mode="live",
        now_utc=lambda: datetime(2011, 3, 11, 5, 46, tzinfo=UTC),
        git_sha=lambda: "be7f766",
        working_tree=lambda: "dirty",
    )

    assert run_path.name == "2011-03-11__0546__initial-rerun__be7f766"
    assert {path.name for path in run_path.iterdir()} == {
        "config.json",
        "inputs.json",
        "meta.json",
        "metrics.json",
        "notes.md",
        "outputs.json",
    }
    assert json.loads((run_path / "meta.json").read_text(encoding="utf-8")) == {
        "command": "uv run python scripts/acquire_tohoku.py --run-tag Initial Rerun!",
        "evidence_disposition": "implementation-under-review",
        "git_sha": "be7f766",
        "mode": "live",
        "run_id": "2011-03-11__0546__initial-rerun__be7f766",
        "timestamp_utc": "2011-03-11T05:46:00Z",
        "working_tree": "dirty",
    }
    inputs = json.loads((run_path / "inputs.json").read_text(encoding="utf-8"))
    assert [(item["source_id"], item["availability"], item["url"]) for item in inputs] == [
        ("blocked", "blocked", "https://example.test/blocked"),
        ("sample", "approved", "https://example.test/sample.json"),
    ]
    outputs = json.loads((run_path / "outputs.json").read_text(encoding="utf-8"))
    assert outputs[0]["source_id"] == "blocked"
    assert outputs[1]["content_type"] == "application/json"
    assert json.loads((run_path / "metrics.json").read_text(encoding="utf-8")) == {
        "bytes_by_status": {"blocked": 0, "downloaded": 11},
        "status_counts": {"blocked": 1, "downloaded": 1},
        "total_bytes": 11,
        "total_contracts": 2,
        "total_outcomes": 2,
    }
    assert "## Decision" in (run_path / "notes.md").read_text(encoding="utf-8")

    with pytest.raises(FileExistsError):
        write_run_evidence(
            root=tmp_path,
            run_tag="Initial Rerun!",
            config_path=config,
            contracts=(approved, blocked),
            results=results,
            command="test",
            mode="live",
            now_utc=lambda: datetime(2011, 3, 11, 5, 46, tzinfo=UTC),
            git_sha=lambda: "be7f766",
            working_tree=lambda: "dirty",
        )


def test_working_tree_status_ignores_only_generated_run_bundles(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    observed: list[str] = []

    def fake_check_output(command: list[str], **kwargs: object) -> str:
        del kwargs
        observed.extend(command)
        return ""

    monkeypatch.setattr("scripts.acquire_tohoku.subprocess.check_output", fake_check_output)

    assert working_tree_status(tmp_path) == "clean"
    assert observed == [
        "git",
        "status",
        "--porcelain",
        "--untracked-files=all",
        "--",
        ".",
        ":(exclude)artifacts/logs/runs/**",
    ]


def test_read_ioc_api_key_rejects_malformed_values_without_echoing_them(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert hasattr(acquire_script, "read_ioc_api_key")
    loader = acquire_script.read_ioc_api_key
    malformed = "not-a-valid-secret"

    def malformed_key(*args: object, **kwargs: object) -> str:
        del args, kwargs
        return malformed

    monkeypatch.setattr(
        "scripts.acquire_tohoku.subprocess.check_output",
        malformed_key,
    )

    with pytest.raises(ValueError) as error:
        loader()

    assert malformed not in str(error.value)
    assert "128 hexadecimal" in str(error.value)


def test_ioc_keychain_fetcher_routes_the_secret_only_to_the_exact_ioc_host(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert hasattr(acquire_script, "ioc_keychain_fetcher")
    factory = acquire_script.ioc_keychain_fetcher
    loaded = 0
    routed: list[tuple[str, str | None]] = []

    def load_key() -> str:
        nonlocal loaded
        loaded += 1
        return "a" * 128

    def ordinary(url: str, destination: Path, timeout_seconds: float) -> ResponseMetadata:
        del destination, timeout_seconds
        routed.append((url, None))
        return ResponseMetadata(content_type="application/json", headers={})

    def authenticated(
        url: str, destination: Path, timeout_seconds: float, api_key: str
    ) -> ResponseMetadata:
        del destination, timeout_seconds
        routed.append((url, api_key))
        return ResponseMetadata(content_type="application/json", headers={})

    monkeypatch.setattr(acquire_script, "read_ioc_api_key", load_key)
    monkeypatch.setattr(acquire_script, "download_url", ordinary)
    monkeypatch.setattr(acquire_script, "download_ioc_url", authenticated)
    fetcher = factory()

    fetcher("https://example.test/data", tmp_path / "ordinary", 30)
    fetcher(
        "https://api.ioc-sealevelmonitoring.org/v2/research/data",
        tmp_path / "ioc-a",
        30,
    )
    fetcher(
        "https://api.ioc-sealevelmonitoring.org/v2/catalog/ioc/valp",
        tmp_path / "ioc-b",
        30,
    )
    fetcher("https://api.ioc-sealevelmonitoring.org.evil.test/data", tmp_path / "evil", 30)

    assert loaded == 1
    assert routed == [
        ("https://example.test/data", None),
        ("https://api.ioc-sealevelmonitoring.org/v2/research/data", "a" * 128),
        ("https://api.ioc-sealevelmonitoring.org/v2/catalog/ioc/valp", "a" * 128),
        ("https://api.ioc-sealevelmonitoring.org.evil.test/data", None),
    ]


def test_download_ioc_url_uses_header_auth_and_rejects_redirects(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert hasattr(acquire_script, "download_ioc_url")
    assert hasattr(acquire_script, "RejectAuthenticatedRedirects")
    observed: dict[str, object] = {}
    headers = Message()
    headers["Content-Type"] = "application/json"

    class Response:
        status = 200

        def __init__(self) -> None:
            self.headers = headers
            self._reads = [b'{"data":[]}', b""]

        def __enter__(self) -> "Response":
            return self

        def __exit__(self, *args: object) -> None:
            del args

        def read(self, size: int) -> bytes:
            del size
            return self._reads.pop(0)

    class Opener:
        def open(self, request: object, timeout: float) -> Response:
            observed["request"] = request
            observed["timeout"] = timeout
            return Response()

    def fake_build_opener(handler: object) -> Opener:
        observed["handler"] = handler
        return Opener()

    monkeypatch.setattr(acquire_script, "build_opener", fake_build_opener)
    destination = tmp_path / "valp.json"
    metadata = acquire_script.download_ioc_url(
        "https://api.ioc-sealevelmonitoring.org/v2/research/data",
        destination,
        30,
        "a" * 128,
    )

    request = observed["request"]
    assert isinstance(request, Request)
    assert request.get_header("X-api-key") == "a" * 128
    assert request.get_header("Accept") == "application/json"
    assert isinstance(observed["handler"], acquire_script.RejectAuthenticatedRedirects)
    assert observed["timeout"] == 30
    assert destination.read_bytes() == b'{"data":[]}'
    assert metadata.content_type == "application/json"

    with pytest.raises(HTTPError, match="redirect refused"):
        acquire_script.RejectAuthenticatedRedirects().redirect_request(
            request, None, 302, "redirect refused", headers, "https://evil.test"
        )


def test_write_run_evidence_keeps_only_safe_response_header_values(tmp_path: Path) -> None:
    config = tmp_path / "tohoku.toml"
    config.write_text("[assets]\n", encoding="utf-8")
    contract = sample_contract()
    result = replace(
        acquire_source(contract, tmp_path, fetcher=fixture_fetcher(b'{"ok":true}')),
        headers={
            "Authentication-Info": "secret-info",
            "Content-Type": "application/json",
            "ETag": "public-version",
            "X-Auth-Token": "secret-token",
            "X-Unrecognized": "not-implicitly-safe",
        },
    )

    run_path = write_run_evidence(
        root=tmp_path,
        run_tag="header-redaction",
        config_path=config,
        contracts=(contract,),
        results=(result,),
        command="test",
        mode="fixture",
        now_utc=lambda: datetime(2011, 3, 11, 5, 46, tzinfo=UTC),
        git_sha=lambda: "be7f766",
        working_tree=lambda: "clean",
    )

    output = json.loads((run_path / "outputs.json").read_text(encoding="utf-8"))[0]
    assert output["headers"] == {
        "Authentication-Info": "[redacted]",
        "Content-Type": "application/json",
        "ETag": "public-version",
        "X-Auth-Token": "[redacted]",
        "X-Unrecognized": "[redacted]",
    }


def test_write_run_evidence_rejects_duplicate_or_mismatched_source_ids(tmp_path: Path) -> None:
    config = tmp_path / "tohoku.toml"
    config.write_text("[assets]\n", encoding="utf-8")
    contract = sample_contract()
    result = AcquisitionResult(
        source_id="sample",
        status="downloaded",
        local_path=contract.local_path,
        bytes=11,
        sha256="a" * 64,
        reason="not applicable",
    )
    variants = (
        ((contract, contract), (result,), "duplicate contract source_id"),
        ((contract,), (result, result), "duplicate result source_id"),
        ((contract,), (replace(result, source_id="other"),), "source ID sets differ"),
    )

    for contracts, results, message in variants:
        with pytest.raises(ValueError, match=message):
            write_run_evidence(
                root=tmp_path,
                run_tag="invalid",
                config_path=config,
                contracts=contracts,
                results=results,
                command="test",
                mode="fixture",
                now_utc=lambda: datetime(2011, 3, 11, 5, 46, tzinfo=UTC),
                git_sha=lambda: "be7f766",
                working_tree=lambda: "clean",
            )
    assert not (tmp_path / "artifacts/logs/runs").exists()


def test_write_run_evidence_cleans_failed_temp_bundle_and_allows_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = tmp_path / "missing.toml"
    contract = sample_contract()
    result = AcquisitionResult(
        source_id="sample",
        status="downloaded",
        local_path=contract.local_path,
        bytes=11,
        sha256="a" * 64,
        reason="not applicable",
    )
    run_path = tmp_path / "artifacts/logs/runs/2011-03-11__0546__retry__be7f766"

    def write_bundle() -> Path:
        return write_run_evidence(
            root=tmp_path,
            run_tag="retry",
            config_path=config,
            contracts=(contract,),
            results=(result,),
            command="test",
            mode="fixture",
            now_utc=lambda: datetime(2011, 3, 11, 5, 46, tzinfo=UTC),
            git_sha=lambda: "be7f766",
            working_tree=lambda: "clean",
        )

    with pytest.raises(FileNotFoundError):
        write_bundle()
    assert not run_path.exists()

    config.write_text("[assets]\n", encoding="utf-8")
    original_write_json = acquire_script._write_json  # pyright: ignore[reportPrivateUsage]

    def fail_outputs(path: Path, value: object) -> None:
        if path.name == "outputs.json":
            raise OSError("injected write failure")
        original_write_json(path, value)

    monkeypatch.setattr(acquire_script, "_write_json", fail_outputs)
    with pytest.raises(OSError, match="injected write failure"):
        write_bundle()
    assert not run_path.exists()
    runs = run_path.parent
    assert not any(
        path.name.startswith(".2011-03-11__0546__retry__be7f766.") for path in runs.iterdir()
    )

    monkeypatch.setattr(acquire_script, "_write_json", original_write_json)
    assert write_bundle() == run_path


def test_write_run_evidence_respects_an_exclusive_writer_lock(tmp_path: Path) -> None:
    config = tmp_path / "tohoku.toml"
    config.write_text("[assets]\n", encoding="utf-8")
    contract = sample_contract()
    result = AcquisitionResult(
        source_id="sample",
        status="downloaded",
        local_path=contract.local_path,
        bytes=11,
        sha256="a" * 64,
        reason="not applicable",
    )
    runs = tmp_path / "artifacts/logs/runs"
    runs.mkdir(parents=True)
    lock = runs / ".2011-03-11__0546__locked__be7f766.lock"
    lock.write_text("another writer", encoding="utf-8")

    with pytest.raises(FileExistsError):
        write_run_evidence(
            root=tmp_path,
            run_tag="locked",
            config_path=config,
            contracts=(contract,),
            results=(result,),
            command="test",
            mode="fixture",
            now_utc=lambda: datetime(2011, 3, 11, 5, 46, tzinfo=UTC),
            git_sha=lambda: "be7f766",
            working_tree=lambda: "clean",
        )

    assert lock.read_text(encoding="utf-8") == "another writer"
    assert not (runs / "2011-03-11__0546__locked__be7f766").exists()


def test_main_records_the_supplied_programmatic_argv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    contract = sample_contract()
    result = AcquisitionResult(
        source_id="sample",
        status="cached",
        local_path=contract.local_path,
        bytes=11,
        sha256="a" * 64,
        reason="verified immutable cache",
    )
    observed: dict[str, str] = {}

    def fake_load_contracts(path: Path) -> tuple[SourceContract, ...]:
        del path
        return (contract,)

    def fake_acquire_all(*args: object, **kwargs: object) -> tuple[AcquisitionResult, ...]:
        del args, kwargs
        return (result,)

    monkeypatch.setattr(acquire_script, "load_contracts", fake_load_contracts)
    monkeypatch.setattr(acquire_script, "acquire_all", fake_acquire_all)

    def capture_evidence(**kwargs: object) -> Path:
        observed["command"] = str(kwargs["command"])
        return tmp_path / "run"

    monkeypatch.setattr(acquire_script, "write_run_evidence", capture_evidence)
    config = tmp_path / "config with spaces.toml"
    argv = [
        "--config",
        str(config),
        "--root",
        str(tmp_path),
        "--run-tag",
        "Tag With Space",
        "--offline",
    ]

    assert acquire_script.main(argv) == 0
    assert observed["command"] == (
        "uv run python scripts/acquire_tohoku.py --config "
        f"'{config}' --root {tmp_path} --run-tag 'Tag With Space' --offline"
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

    assert len(contracts) == 18
    assert event.expected_content_signature.startswith("One CSV row")
    assert event.expected_prefix == "time,latitude,longitude,depth"
    assert event.crs == "WGS84 horizontal coordinates"
    assert event.temporal_semantics == "origin timestamp is UTC; record update is source metadata"
    assert event.station_metadata == "not applicable"
    assert event.reason == "not applicable"
    assert blocked.reason != "not applicable"
    valparaiso = next(
        contract
        for contract in contracts
        if contract.source_id == "ioc-valparaiso-rad-20110311to20110314"
    )
    assert valparaiso.availability == "approved"
    assert valparaiso.format == "IOC SLSMF v2 research JSON"
    assert "includesensors%5B%5D=rad" in valparaiso.url
    assert "filter_exceeded_neighbours=false" in valparaiso.url


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


def test_acquire_all_retries_and_isolates_incomplete_http_reads(tmp_path: Path) -> None:
    bad = sample_contract(source_id="bad", local_path=PurePosixPath("data/bad.json"))
    good = sample_contract(source_id="good", local_path=PurePosixPath("data/good.json"))
    bad_calls = 0

    def fetcher(url: str, destination: Path, timeout_seconds: float) -> ResponseMetadata:
        nonlocal bad_calls
        del timeout_seconds
        if destination.name.startswith(".bad.json"):
            bad_calls += 1
            raise IncompleteRead(b"partial", 10)
        destination.write_bytes(b'{"ok":true}')
        return ResponseMetadata(content_type="application/json", headers={})

    results = acquire_all((bad, good), tmp_path, fetcher=fetcher)

    assert bad_calls == 3
    assert [result.status for result in results] == ["quarantined", "downloaded"]


def test_load_contracts_rejects_a_nul_local_path(tmp_path: Path) -> None:
    config = tmp_path / "nul-path.toml"
    source = Path("config/tohoku-data-proof.toml").read_text(encoding="utf-8")
    config.write_text(
        source.replace(
            'local_path = "data/raw/usgs/official20110311054624120_30.csv"',
            'local_path = "data/raw/\\u0000payload.csv"',
            1,
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="NUL byte"):
        load_contracts(config)


def test_acquire_all_defensively_isolates_a_nul_path(tmp_path: Path) -> None:
    bad = sample_contract(source_id="bad", local_path=PurePosixPath("data/\x00bad.json"))
    good = sample_contract(source_id="good", local_path=PurePosixPath("data/good.json"))

    results = acquire_all((bad, good), tmp_path, fetcher=fixture_fetcher(b'{"ok":true}'))

    assert [result.status for result in results] == ["quarantined", "downloaded"]
