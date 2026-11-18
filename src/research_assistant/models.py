"""Mendefinisikan record ``Paper`` seragam untuk hasil semua sumber, dipakai lapisan sumber, sitasi, dan agent sebagai kontrak data bersama."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Paper:
    """Record seragam hasil tiap sumber literatur."""

    source: str  # "openalex" | "semantic_scholar" | "arxiv"
    title: str
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    venue: str | None = None
    doi: str | None = None  # DOI ternormalisasi — kunci dedup utama
    url: str | None = None
    abstract: str | None = None
    citations: int | None = None
    arxiv_id: str | None = None  # kunci dedup cadangan

    def dedup_key(self) -> str:
        """Kunci dedup: DOI → arXiv id → judul ternormalisasi."""
        raise NotImplementedError


def normalize_doi(doi: str | None) -> str | None:
    """Normalisasi DOI (lowercase, buang prefiks URL)."""
    raise NotImplementedError
