"""Mendefinisikan record ``Paper`` seragam untuk hasil semua sumber, dipakai lapisan sumber, sitasi, dan agent sebagai kontrak data bersama."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_DOI_PREFIX = re.compile(r"^(https?://(dx\.)?doi\.org/|doi:)", re.IGNORECASE)
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_WS = re.compile(r"\s+")
_ARXIV_VERSION = re.compile(r"v\d+$", re.IGNORECASE)


def normalize_doi(doi: str | None) -> str | None:
    """Menyeragamkan DOI (buang prefiks URL/``doi:``, lowercase) agar bisa dibandingkan sebagai kunci dedup; mengembalikan None bila kosong."""
    if not doi:
        return None
    cleaned = _DOI_PREFIX.sub("", doi.strip()).strip().lower()
    return cleaned or None


def normalize_arxiv_id(arxiv_id: str | None) -> str | None:
    """Menyeragamkan id arXiv (ambil segmen terakhir, buang sufiks versi ``vN``, lowercase) sebagai kunci dedup cadangan."""
    if not arxiv_id:
        return None
    tail = arxiv_id.strip().rstrip("/").split("/")[-1].lower()
    tail = _ARXIV_VERSION.sub("", tail)
    return tail or None


def normalize_title(title: str | None) -> str | None:
    """Menyeragamkan judul (lowercase, buang tanda baca, rapatkan spasi) untuk dedup cadangan saat DOI & id arXiv kosong."""
    if not title:
        return None
    lowered = _PUNCT.sub(" ", title.strip().lower())
    collapsed = _WS.sub(" ", lowered).strip()
    return collapsed or None


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
        """Memberi kunci identitas paper untuk dedup: DOI → id arXiv → judul ternormalisasi; dipakai ``merge_dedup`` menyatukan duplikat lintas sumber."""
        doi = normalize_doi(self.doi)
        if doi:
            return f"doi:{doi}"
        arxiv = normalize_arxiv_id(self.arxiv_id)
        if arxiv:
            return f"arxiv:{arxiv}"
        title = normalize_title(self.title)
        if title:
            return f"title:{title}"
        return f"id:{id(self)}"  # fallback: tak bisa dibandingkan -> selalu unik
