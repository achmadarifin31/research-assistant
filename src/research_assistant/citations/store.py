"""Memetakan Paper ke nomor sitasi stabil sesuai urutan kemunculan, dipakai saat sintesis menyusun daftar pustaka."""

from __future__ import annotations

from research_assistant.models import Paper


class CitationStore:
    """Memetakan Paper → nomor sitasi stabil sesuai urutan kemunculan."""

    def __init__(self) -> None:
        self._by_key: dict[str, int] = {}
        self._papers: list[Paper] = []

    def cite(self, paper: Paper) -> int:
        """Kembalikan nomor sitasi paper; tetapkan baru bila belum ada (idempoten)."""
        raise NotImplementedError

    def cited_papers(self) -> list[Paper]:
        """Daftar paper yang benar-benar dikutip, berurut nomor."""
        raise NotImplementedError
