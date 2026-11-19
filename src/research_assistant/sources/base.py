"""Mendefinisikan antarmuka ``Source`` yang dipatuhi tiap klien dan util pemanggilan HTTP dengan retry/backoff."""

from __future__ import annotations

import random
from typing import Protocol

import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt

from research_assistant.models import Paper

DEFAULT_TIMEOUT = 20.0
MAX_ATTEMPTS = 4
MAX_BACKOFF = 30.0
DEFAULT_USER_AGENT = "research-assistant/0.1"


class Source(Protocol):
    """Kontrak klien sumber: tiap klien menyediakan ``name`` dan ``search`` yang mengembalikan daftar Paper seragam."""

    name: str

    def search(self, query: str, limit: int) -> list[Paper]:
        """Mencari paper untuk ``query`` dan mengembalikan hingga ``limit`` record Paper."""
        ...


class RetryableHTTPError(Exception):
    """Menandai kegagalan HTTP sementara (429/5xx/koneksi) yang layak dicoba ulang; ``retry_after`` membawa hint tunggu dari server bila ada."""

    def __init__(self, message: str, retry_after: float | None = None) -> None:
        super().__init__(message)
        self.retry_after = retry_after


def _wait(retry_state) -> float:
    """Menghitung jeda sebelum percobaan berikutnya: hormati ``Retry-After`` bila ada, selain itu exponential backoff + jitter."""
    exc = retry_state.outcome.exception() if retry_state.outcome else None
    if isinstance(exc, RetryableHTTPError) and exc.retry_after is not None:
        # Hormati Retry-After tapi batasi agar tidak tidur berlebihan.
        return min(exc.retry_after, MAX_BACKOFF) + random.random()
    base = 2.0 ** (retry_state.attempt_number - 1)
    return min(base, MAX_BACKOFF) + random.random()


def _parse_retry_after(value: str | None) -> float | None:
    """Mengubah header ``Retry-After`` (detik) menjadi angka; mengabaikan format tanggal HTTP."""
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


@retry(
    reraise=True,
    stop=stop_after_attempt(MAX_ATTEMPTS),
    wait=_wait,
    retry=retry_if_exception_type(RetryableHTTPError),
)
def request_with_backoff(method: str, url: str, **kwargs) -> requests.Response:
    """Memanggil HTTP dengan retry otomatis pada 429/5xx/kesalahan koneksi (exponential backoff + jitter, hormati Retry-After); dipakai semua klien sumber."""
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
    headers = {"User-Agent": DEFAULT_USER_AGENT, **(kwargs.pop("headers", None) or {})}
    kwargs["headers"] = headers
    try:
        response = requests.request(method, url, **kwargs)
    except requests.RequestException as exc:
        raise RetryableHTTPError(str(exc)) from exc

    if response.status_code == 429:
        retry_after = _parse_retry_after(response.headers.get("Retry-After"))
        raise RetryableHTTPError("rate limited (429)", retry_after=retry_after)
    if response.status_code >= 500:
        raise RetryableHTTPError(f"server error ({response.status_code})")

    response.raise_for_status()
    return response
