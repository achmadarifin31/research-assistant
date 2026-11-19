"""Unit test offline untuk dedup lintas sumber dan rekonstruksi abstrak OpenAlex."""

from research_assistant.models import Paper, normalize_doi
from research_assistant.sources import merge_dedup
from research_assistant.sources.openalex import reconstruct_abstract


def test_normalize_doi_strips_url_and_lowercases():
    assert normalize_doi("https://doi.org/10.1/ABC") == "10.1/abc"
    assert normalize_doi("doi:10.1/AbC") == "10.1/abc"
    assert normalize_doi(None) is None
    assert normalize_doi("  ") is None


def test_dedup_by_doi_merges_and_fills_fields():
    # Sumber prioritas lebih tinggi lebih dulu tapi field tak lengkap.
    a = Paper(source="openalex", title="Deep Face", doi="https://doi.org/10.1/x",
              authors=["A. One"], abstract=None, citations=None)
    # Duplikat (DOI sama, kapitalisasi beda) membawa field yang hilang.
    b = Paper(source="semantic_scholar", title="Deep Face", doi="10.1/X",
              authors=["A. One", "B. Two"], abstract="isi abstrak", citations=42)

    merged = merge_dedup([a, b])

    assert len(merged) == 1
    kept = merged[0]
    assert kept.source == "openalex"  # record pertama dipertahankan
    assert kept.abstract == "isi abstrak"  # field kosong terisi dari duplikat
    assert kept.citations == 42
    assert kept.authors == ["A. One", "B. Two"]  # daftar penulis terpanjang


def test_dedup_by_title_when_no_identifier():
    a = Paper(source="arxiv", title="A Study: Of  Faces!")
    b = Paper(source="openalex", title="a study of faces")
    assert len(merge_dedup([a, b])) == 1


def test_distinct_papers_not_merged():
    a = Paper(source="openalex", title="Faces", doi="10.1/a")
    b = Paper(source="openalex", title="Voices", doi="10.1/b")
    assert len(merge_dedup([a, b])) == 2


def test_reconstruct_abstract_orders_words_by_position():
    inverted = {"Deep": [0], "learning": [1], "faces": [3], "for": [2]}
    assert reconstruct_abstract(inverted) == "Deep learning for faces"


def test_reconstruct_abstract_empty_returns_none():
    assert reconstruct_abstract(None) is None
    assert reconstruct_abstract({}) is None
