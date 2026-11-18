"""Mencari paper di Semantic Scholar dan mengubah respons menjadi record Paper, menangani rate limit 429 dengan retry/backoff."""

from __future__ import annotations

from research_assistant.models import Paper


class SemanticScholarClient:
    name = "semantic_scholar"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    def search(self, query: str, limit: int) -> list[Paper]:
        raise NotImplementedError
