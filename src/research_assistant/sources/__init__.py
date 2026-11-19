"""Menggabungkan hasil pencarian dari semua sumber aktif dan membuang duplikat, memasok kolam Paper ke lapisan agent."""

from __future__ import annotations

import logging

from research_assistant.models import Paper
from research_assistant.sources.arxiv import ArxivClient
from research_assistant.sources.openalex import OpenAlexClient
from research_assistant.sources.semantic_scholar import SemanticScholarClient

logger = logging.getLogger(__name__)

# Urutan prioritas: record yang muncul lebih dulu dipertahankan, field kosongnya
# diisi dari duplikat sumber berikutnya.
SOURCE_ORDER = ("openalex", "semantic_scholar", "arxiv")

_MERGEABLE = ("year", "venue", "doi", "url", "abstract", "citations", "arxiv_id")


def _is_empty(value: object) -> bool:
    return value is None or value == ""


def _fill_missing(base: Paper, other: Paper) -> None:
    """Mengisi field kosong ``base`` dari ``other`` (gabung kelengkapan); ambil daftar penulis yang lebih panjang."""
    for name in _MERGEABLE:
        if _is_empty(getattr(base, name)) and not _is_empty(getattr(other, name)):
            setattr(base, name, getattr(other, name))
    if len(other.authors) > len(base.authors):
        base.authors = other.authors


def merge_dedup(papers: list[Paper]) -> list[Paper]:
    """Menyatukan duplikat lintas sumber berdasarkan ``dedup_key`` (DOI→arXiv→judul), mempertahankan urutan kemunculan pertama dan menggabungkan field dari duplikatnya."""
    merged: dict[str, Paper] = {}
    order: list[str] = []
    for paper in papers:
        key = paper.dedup_key()
        if key not in merged:
            merged[key] = paper
            order.append(key)
        else:
            _fill_missing(merged[key], paper)
    return [merged[key] for key in order]


def _rank(papers: list[Paper]) -> list[Paper]:
    """Mengurutkan paper citations terbanyak lebih dulu; yang tak punya data citations ditaruh di akhir."""
    return sorted(papers, key=lambda p: (p.citations is None, -(p.citations or 0)))


def search_all(
    query: str,
    per_source: int = 8,
    enabled: tuple[str, ...] = SOURCE_ORDER,
    *,
    openalex_mailto: str | None = None,
    semantic_scholar_api_key: str | None = None,
) -> list[Paper]:
    """Mencari ``query`` di tiap sumber aktif (dibatasi ``per_source``), menggabung-deduplikasi hasilnya, lalu mengurutkannya per citations; kegagalan satu sumber dicatat dan dilewati tanpa menggagalkan sumber lain."""
    clients = {
        "openalex": lambda: OpenAlexClient(mailto=openalex_mailto),
        "semantic_scholar": lambda: SemanticScholarClient(api_key=semantic_scholar_api_key),
        "arxiv": lambda: ArxivClient(),
    }

    collected: list[Paper] = []
    for name in SOURCE_ORDER:  # jaga urutan prioritas apa pun urutan ``enabled``
        if name not in enabled:
            continue
        try:
            client = clients[name]()
            collected.extend(client.search(query, per_source))
        except Exception:  # noqa: BLE001 — satu sumber gagal tak boleh menggagalkan lainnya
            logger.exception("Pencarian sumber %r gagal; dilewati", name)

    return _rank(merge_dedup(collected))
