"""Mencari paper di OpenAlex dan mengubah respons menjadi record Paper, termasuk merekonstruksi abstrak dari inverted index."""

from __future__ import annotations

from typing import Any

from research_assistant.models import Paper
from research_assistant.sources.base import request_with_backoff

_BASE_URL = "https://api.openalex.org/works"
_USER_AGENT = "research-assistant/0.1"


def reconstruct_abstract(inverted_index: dict[str, list[int]] | None) -> str | None:
    """Menyusun ulang teks abstrak dari ``abstract_inverted_index`` OpenAlex (peta kata→posisi); mengembalikan None bila kosong."""
    if not inverted_index:
        return None
    positions: dict[int, str] = {}
    for word, idxs in inverted_index.items():
        for i in idxs:
            positions[i] = word
    if not positions:
        return None
    ordered = (positions.get(i, "") for i in range(max(positions) + 1))
    text = " ".join(ordered).strip()
    return text or None


def _venue(work: dict[str, Any]) -> str | None:
    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    return source.get("display_name")


def _url(work: dict[str, Any]) -> str | None:
    oa = work.get("open_access") or {}
    if oa.get("oa_url"):
        return oa["oa_url"]
    location = work.get("primary_location") or {}
    return location.get("landing_page_url") or work.get("doi")


def _to_paper(work: dict[str, Any]) -> Paper:
    authors = [
        a["author"]["display_name"]
        for a in work.get("authorships", [])
        if a.get("author", {}).get("display_name")
    ]
    return Paper(
        source="openalex",
        title=work.get("display_name") or "",
        authors=authors,
        year=work.get("publication_year"),
        venue=_venue(work),
        doi=work.get("doi"),
        url=_url(work),
        abstract=reconstruct_abstract(work.get("abstract_inverted_index")),
        citations=work.get("cited_by_count"),
        arxiv_id=None,
    )


class OpenAlexClient:
    name = "openalex"

    def __init__(self, mailto: str | None = None) -> None:
        self.mailto = mailto

    def _user_agent(self) -> str:
        # OpenAlex menolak request tanpa User-Agent; sertakan mailto hanya bila
        # pengguna mengisinya sendiri (polite pool), jangan bocorkan email lain.
        if self.mailto:
            return f"{_USER_AGENT} (mailto:{self.mailto})"
        return _USER_AGENT

    def search(self, query: str, limit: int) -> list[Paper]:
        """Memanggil OpenAlex /works dengan ``query`` dan mengembalikan hingga ``limit`` Paper (User-Agent sopan; ``mailto`` masuk polite pool bila diset)."""
        params: dict[str, Any] = {"search": query, "per_page": max(1, min(limit, 200))}
        if self.mailto:
            params["mailto"] = self.mailto
        headers = {"User-Agent": self._user_agent()}
        response = request_with_backoff("GET", _BASE_URL, params=params, headers=headers)
        results = response.json().get("results", [])
        return [_to_paper(w) for w in results[:limit]]
