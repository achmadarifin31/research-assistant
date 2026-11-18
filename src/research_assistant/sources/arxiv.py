"""Mencari paper di arXiv dan mengubah respons Atom menjadi record Paper."""

from __future__ import annotations

from research_assistant.models import Paper


class ArxivClient:
    name = "arxiv"

    def search(self, query: str, limit: int) -> list[Paper]:
        raise NotImplementedError
