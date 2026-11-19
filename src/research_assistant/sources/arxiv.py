"""Mencari paper di arXiv dan mengubah respons Atom menjadi record Paper."""

from __future__ import annotations

from typing import Any

import feedparser

from research_assistant.models import Paper, normalize_arxiv_id
from research_assistant.sources.base import request_with_backoff

_BASE_URL = "http://export.arxiv.org/api/query"


def _year(entry: Any) -> int | None:
    published = entry.get("published")  # "2024-01-15T..."
    if published and len(published) >= 4 and published[:4].isdigit():
        return int(published[:4])
    return None


def _to_paper(entry: Any) -> Paper:
    authors = [a.get("name") for a in entry.get("authors", []) if a.get("name")]
    title = " ".join((entry.get("title") or "").split())  # rapatkan newline Atom
    return Paper(
        source="arxiv",
        title=title,
        authors=authors,
        year=_year(entry),
        venue="arXiv",
        doi=entry.get("arxiv_doi"),
        url=entry.get("link") or entry.get("id"),
        abstract=" ".join((entry.get("summary") or "").split()) or None,
        citations=None,
        arxiv_id=normalize_arxiv_id(entry.get("id")),  # mis. "1309.6352"
    )


class ArxivClient:
    name = "arxiv"

    def search(self, query: str, limit: int) -> list[Paper]:
        """Memanggil arXiv API dengan ``query`` dan mengubah respons Atom menjadi hingga ``limit`` Paper."""
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max(1, limit),
        }
        response = request_with_backoff("GET", _BASE_URL, params=params)
        feed = feedparser.parse(response.content)
        return [_to_paper(e) for e in feed.entries[:limit]]
