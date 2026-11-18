"""Menggabungkan hasil pencarian dari semua sumber aktif dan membuang duplikat, memasok kolam Paper ke lapisan agent."""

from __future__ import annotations

from research_assistant.models import Paper


def merge_dedup(papers: list[Paper]) -> list[Paper]:
    """Gabungkan & buang duplikat berdasarkan dedup_key (DOI → arXiv id → judul)."""
    raise NotImplementedError


def search_all(
    query: str,
    per_source: int = 8,
    enabled: tuple[str, ...] = ("openalex", "semantic_scholar", "arxiv"),
    *,
    openalex_mailto: str | None = None,
    semantic_scholar_api_key: str | None = None,
) -> list[Paper]:
    """Cari di semua sumber aktif lalu dedup hasilnya."""
    raise NotImplementedError
