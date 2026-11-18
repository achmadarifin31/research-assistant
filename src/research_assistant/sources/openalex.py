"""Mencari paper di OpenAlex dan mengubah respons menjadi record Paper, termasuk merekonstruksi abstrak dari inverted index."""

from __future__ import annotations

from research_assistant.models import Paper


class OpenAlexClient:
    name = "openalex"

    def __init__(self, mailto: str | None = None) -> None:
        self.mailto = mailto

    def search(self, query: str, limit: int) -> list[Paper]:
        raise NotImplementedError


def reconstruct_abstract(inverted_index: dict[str, list[int]]) -> str:
    """Rekonstruksi teks abstrak dari inverted index OpenAlex."""
    raise NotImplementedError
