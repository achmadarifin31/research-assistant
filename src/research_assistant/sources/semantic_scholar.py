"""Mencari paper di Semantic Scholar dan mengubah respons menjadi record Paper, menangani rate limit 429 dengan retry/backoff."""

from __future__ import annotations

from typing import Any

from research_assistant.models import Paper
from research_assistant.sources.base import request_with_backoff

_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
_FIELDS = "title,authors,year,venue,abstract,citationCount,externalIds,openAccessPdf,url"


def _url(paper: dict[str, Any]) -> str | None:
    oa = paper.get("openAccessPdf") or {}
    return oa.get("url") or paper.get("url")


def _to_paper(paper: dict[str, Any]) -> Paper:
    external = paper.get("externalIds") or {}
    authors = [a["name"] for a in paper.get("authors", []) if a.get("name")]
    return Paper(
        source="semantic_scholar",
        title=paper.get("title") or "",
        authors=authors,
        year=paper.get("year"),
        venue=paper.get("venue") or None,
        doi=external.get("DOI"),
        url=_url(paper),
        abstract=paper.get("abstract"),
        citations=paper.get("citationCount"),
        arxiv_id=external.get("ArXiv"),
    )


class SemanticScholarClient:
    name = "semantic_scholar"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    def search(self, query: str, limit: int) -> list[Paper]:
        """Memanggil Semantic Scholar paper/search dengan ``query`` dan mengembalikan hingga ``limit`` Paper (pakai header x-api-key bila diset)."""
        params = {"query": query, "limit": max(1, min(limit, 100)), "fields": _FIELDS}
        headers = {"x-api-key": self.api_key} if self.api_key else {}
        response = request_with_backoff("GET", _BASE_URL, params=params, headers=headers)
        data = response.json().get("data") or []
        return [_to_paper(p) for p in data[:limit]]
