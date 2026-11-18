"""Memformat penulis dan entri daftar pustaka gaya IEEE (ID/EN) serta menomori ulang sitasi sesuai urutan kemunculan di brief.

Format entri:
    [n] F. Last, dan F. Last, "Judul," Venue, tahun. doi: 10.x/...
("dan" untuk ID, "and" untuk EN; fallback ke arXiv id atau URL bila tak ada DOI).
"""

from __future__ import annotations

from research_assistant.models import Paper


def format_authors(authors: list[str], lang: str = "id") -> str:
    """Format daftar penulis gaya IEEE (F. Last), konjungsi per bahasa."""
    raise NotImplementedError


def format_entry(number: int, paper: Paper, lang: str = "id") -> str:
    """Format satu entri daftar pustaka IEEE."""
    raise NotImplementedError


def renumber(brief_text: str) -> tuple[str, list[int]]:
    """Tetapkan ulang nomor [n] sesuai urutan kemunculan di brief final."""
    raise NotImplementedError
