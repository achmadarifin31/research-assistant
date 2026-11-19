"""Memetakan Paper ke nomor sitasi stabil sesuai urutan kemunculan, dipakai saat sintesis menyusun daftar pustaka."""

from __future__ import annotations

from research_assistant.models import Paper


class CitationStore:
    """Memberi nomor kerja stabil ke tiap paper pool (idempoten per ``dedup_key``) agar bisa dirujuk ``[n]`` dalam draf lalu di-renumber."""

    def __init__(self) -> None:
        self._key_to_number: dict[str, int] = {}
        self._number_to_paper: dict[int, Paper] = {}
        self._counter = 0

    @classmethod
    def of_pool(cls, papers: list[Paper]) -> "CitationStore":
        """Membangun store dan menomori seluruh pool berurutan (1..N) sebagai nomor kerja yang dilihat LLM."""
        store = cls()
        for paper in papers:
            store.cite(paper)
        return store

    def cite(self, paper: Paper) -> int:
        """Mengembalikan nomor kerja paper; menetapkan nomor baru bila belum ada (idempoten) sehingga paper sama selalu bernomor sama."""
        key = paper.dedup_key()
        existing = self._key_to_number.get(key)
        if existing is not None:
            return existing
        self._counter += 1
        self._key_to_number[key] = self._counter
        self._number_to_paper[self._counter] = paper
        return self._counter

    def number_of(self, paper: Paper) -> int | None:
        """Mengembalikan nomor kerja paper bila sudah terdaftar, selain itu None."""
        return self._key_to_number.get(paper.dedup_key())

    def get(self, number: int) -> Paper | None:
        """Mengembalikan paper untuk suatu nomor kerja; dipakai renumber memetakan ``[n]`` ke paper."""
        return self._number_to_paper.get(number)

    def numbered_papers(self) -> list[Paper]:
        """Mengembalikan semua paper bernomor urut nomor kerja (bukan subset yang benar-benar dikutip — itu hasil renumber)."""
        return [self._number_to_paper[n] for n in sorted(self._number_to_paper)]

    def __len__(self) -> int:
        return self._counter
