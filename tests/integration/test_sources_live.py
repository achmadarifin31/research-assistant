"""Uji integrasi yang memanggil tiap sumber live satu per satu (butuh jaringan).

Jalankan dengan: uv run pytest -m integration
"""

import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skip(reason="klien OpenAlex belum diimplementasikan")
def test_openalex_live():
    raise NotImplementedError


@pytest.mark.skip(reason="klien Semantic Scholar belum diimplementasikan")
def test_semantic_scholar_live():
    raise NotImplementedError


@pytest.mark.skip(reason="klien arXiv belum diimplementasikan")
def test_arxiv_live():
    raise NotImplementedError
