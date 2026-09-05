"""Acquire approved source contracts into an immutable local raw-data cache."""

from __future__ import annotations

import hashlib
import tempfile
import tomllib
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import cast
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen


@dataclass(frozen=True, slots=True)
class SourceContract:
    """Source identity and acquisition requirements from the TOML contract."""

    source_id: str
    source_class: str
    availability: str
    url: str
    local_path: PurePosixPath
    format: str
    publisher: str
    expected_content_signature: str
    expected_prefix: str
    units: str
    crs: str
    horizontal_datum: str
    vertical_datum: str
    coordinate_order: str
    temporal_semantics: str
    station_metadata: str
    reason: str


@dataclass(frozen=True, slots=True)
class ResponseMetadata:
    """Response metadata retained by callers that write run evidence."""

    content_type: str
    headers: dict[str, str]


@dataclass(frozen=True, slots=True)
class AcquisitionResult:
    """Outcome for exactly one source contract."""

    source_id: str
    status: str
    local_path: PurePosixPath
    bytes: int
    sha256: str
    reason: str


Fetcher = Callable[[str, Path, float], ResponseMetadata]
MAX_FETCH_ATTEMPTS = 3
PREFIX_WINDOW_BYTES = 64 * 1024
CONTRACT_FIELDS: tuple[str, ...] = (
    "source_id",
    "source_class",
    "availability",
    "url",
    "local_path",
    "format",
    "publisher",
    "expected_content_signature",
    "expected_prefix",
    "units",
    "crs",
    "horizontal_datum",
    "vertical_datum",
    "coordinate_order",
    "temporal_semantics",
    "station_metadata",
    "reason",
)


class ContractError(ValueError):
    """Raised when a source-contract TOML file violates the acquisition contract."""


def load_contracts(path: Path) -> tuple[SourceContract, ...]:
    """Load and validate every exact source contract from a TOML file."""
    try:
        document = cast(dict[str, object], tomllib.loads(path.read_text(encoding="utf-8")))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ContractError(f"could not read {path}: {error}") from error

    raw_assets = document.get("assets")
    if not isinstance(raw_assets, dict):
        raise ContractError("missing [assets] tables")
    assets = cast(dict[str, object], raw_assets)
    contracts: list[SourceContract] = []
    for name, raw_values in assets.items():
        if not isinstance(raw_values, dict):
            raise ContractError(f"asset {name!r} must be a TOML table")
        asset = cast(dict[str, object], raw_values)
        values: dict[str, object | None] = {
            field: asset.get(field) for field in CONTRACT_FIELDS
        }
        missing = [field for field, value in values.items() if not isinstance(value, str)]
        if missing:
            raise ContractError(f"asset {name!r} missing string fields: {', '.join(missing)}")
        strings = {field: value for field, value in values.items() if isinstance(value, str)}
        availability = strings["availability"]
        if availability not in {"approved", "blocked"}:
            raise ContractError(f"asset {name!r} has unsupported availability {availability!r}")
        local_path_value = strings["local_path"]
        local_path = PurePosixPath(local_path_value)
        if availability == "blocked" and local_path_value != "not-downloaded":
            raise ContractError(f"blocked asset {name!r} must use local_path 'not-downloaded'")
        if availability == "approved" and (
            local_path_value == "not-downloaded"
            or local_path.is_absolute()
            or ".." in local_path.parts
            or "\\" in local_path_value
        ):
            raise ContractError(f"approved asset {name!r} needs a safe relative local_path")
        parsed_url = urlparse(strings["url"])
        if parsed_url.scheme != "https" or not parsed_url.netloc:
            raise ContractError(f"asset {name!r} needs an absolute HTTPS url")
        contracts.append(
            SourceContract(
                source_id=strings["source_id"],
                source_class=strings["source_class"],
                availability=availability,
                url=strings["url"],
                local_path=local_path,
                format=strings["format"],
                publisher=strings["publisher"],
                expected_content_signature=strings["expected_content_signature"],
                expected_prefix=strings["expected_prefix"],
                units=strings["units"],
                crs=strings["crs"],
                horizontal_datum=strings["horizontal_datum"],
                vertical_datum=strings["vertical_datum"],
                coordinate_order=strings["coordinate_order"],
                temporal_semantics=strings["temporal_semantics"],
                station_metadata=strings["station_metadata"],
                reason=strings["reason"],
            )
        )
    return tuple(sorted(contracts, key=lambda contract: contract.source_id))


def _sha256(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            size += len(chunk)
            digest.update(chunk)
    return size, digest.hexdigest()


def _matches_prefix(path: Path, expected_prefix: str) -> bool:
    with path.open("rb") as source:
        return source.read(PREFIX_WINDOW_BYTES).lstrip().startswith(expected_prefix.encode("utf-8"))


def _result(
    contract: SourceContract, status: str, size: int, digest: str, reason: str
) -> AcquisitionResult:
    return AcquisitionResult(
        source_id=contract.source_id,
        status=status,
        local_path=contract.local_path,
        bytes=size,
        sha256=digest,
        reason=reason,
    )


def download_url(url: str, destination: Path, timeout_seconds: float) -> ResponseMetadata:
    """Stream one HTTPS response to a caller-owned temporary destination."""
    with urlopen(url, timeout=timeout_seconds) as response:  # noqa: S310 - contracts are HTTPS.
        with destination.open("wb") as target:
            while chunk := response.read(1024 * 1024):
                target.write(chunk)
        return ResponseMetadata(
            content_type=response.headers.get_content_type(),
            headers=dict(response.headers.items()),
        )


def _fetch_with_retries(
    fetcher: Fetcher, url: str, destination: Path, timeout_seconds: float
) -> ResponseMetadata:
    for attempt in range(MAX_FETCH_ATTEMPTS):
        try:
            return fetcher(url, destination, timeout_seconds)
        except (TimeoutError, URLError) as error:
            if isinstance(error, HTTPError) or attempt == MAX_FETCH_ATTEMPTS - 1:
                raise
    raise AssertionError("bounded fetch loop must return or raise")


def acquire_source(
    contract: SourceContract,
    root: Path,
    fetcher: Fetcher = download_url,
    timeout_seconds: float = 30.0,
) -> AcquisitionResult:
    """Acquire one approved contract without replacing a conflicting raw file."""
    if contract.availability == "blocked":
        return _result(contract, "blocked", 0, "not-downloaded", contract.reason)

    destination = root / contract.local_path
    if destination.exists():
        size, digest = _sha256(destination)
        if size and _matches_prefix(destination, contract.expected_prefix):
            return _result(contract, "cached", size, digest, "not applicable")
        return _result(contract, "quarantined", size, digest, "existing_checksum_conflict")

    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=f".{destination.name}.", dir=destination.parent, delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)
    try:
        _fetch_with_retries(fetcher, contract.url, temporary_path, timeout_seconds)
        size, digest = _sha256(temporary_path)
        if not size:
            return _result(contract, "quarantined", 0, "not-downloaded", "empty_response")
        if not _matches_prefix(temporary_path, contract.expected_prefix):
            return _result(
                contract, "quarantined", size, digest, "content_signature_mismatch"
            )
        temporary_path.replace(destination)
        return _result(contract, "downloaded", size, digest, "not applicable")
    except (HTTPError, OSError, URLError) as error:
        return _result(contract, "quarantined", 0, "not-downloaded", f"download_failed: {error}")
    finally:
        temporary_path.unlink(missing_ok=True)


def acquire_all(
    contracts: Sequence[SourceContract],
    root: Path,
    fetcher: Fetcher = download_url,
) -> tuple[AcquisitionResult, ...]:
    """Acquire every contract independently in deterministic source-ID order."""
    return tuple(
        acquire_source(contract, root, fetcher)
        for contract in sorted(contracts, key=lambda item: item.source_id)
    )
