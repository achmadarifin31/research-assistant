"""Mendefinisikan antarmuka ``Source`` yang dipatuhi tiap klien dan util pemanggilan HTTP dengan retry/backoff."""

from __future__ import annotations

from typing import Protocol

from research_assistant.models import Paper


class Source(Protocol):
    """Antarmuka seragam tiap klien sumber."""

    name: str

    def search(self, query: str, limit: int) -> list[Paper]:
        """Cari paper untuk query, kembalikan hingga ``limit`` record Paper."""
        ...


def request_with_backoff(*args, **kwargs):
    """Panggil HTTP dengan retry + exponential backoff (tangani 429)."""
    raise NotImplementedError
