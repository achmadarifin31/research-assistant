"""Uji integrasi yang memanggil tiap sumber live satu per satu (butuh jaringan).

Jalankan dengan: uv run pytest -m integration

Akses anonim (tanpa API key / mailto) berbagi kuota per-IP, sehingga sumber
bisa membalas 429/503 saat kuota habis. Kondisi itu di-skip, bukan dianggap
gagal — isi OPENALEX_MAILTO / SEMANTIC_SCHOLAR_API_KEY untuk akses lebih stabil.
"""

from typing import Callable

import pytest

from research_assistant.models import Paper
from research_assistant.sources.arxiv import ArxivClient
from research_assistant.sources.base import RetryableHTTPError
from research_assistant.sources.openalex import OpenAlexClient
from research_assistant.sources.semantic_scholar import SemanticScholarClient

pytestmark = pytest.mark.integration

QUERY = "VGG-Face personality"


def _search_or_skip(name: str, search: Callable[[], list[Paper]]) -> list[Paper]:
    try:
        return search()
    except RetryableHTTPError as exc:
        pytest.skip(f"{name} tidak tersedia (rate limit/koneksi: {exc})")


def _assert_valid(results: list[Paper]) -> None:
    assert len(results) >= 1
    first = results[0]
    assert isinstance(first, Paper)
    assert first.title  # field wajib terisi
    assert first.source


def test_openalex_live():
    _assert_valid(_search_or_skip("OpenAlex", lambda: OpenAlexClient().search(QUERY, 3)))


def test_arxiv_live():
    results = _search_or_skip("arXiv", lambda: ArxivClient().search(QUERY, 3))
    _assert_valid(results)
    assert results[0].arxiv_id  # id arXiv harus terekstrak


def test_semantic_scholar_live():
    _assert_valid(_search_or_skip("Semantic Scholar", lambda: SemanticScholarClient().search(QUERY, 3)))
