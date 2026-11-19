"""Unit test offline untuk penomoran ulang sitasi sesuai urutan kemunculan."""

from research_assistant.citations import CitationStore, build_bibliography, renumber
from research_assistant.models import Paper


def _pool() -> list[Paper]:
    return [
        Paper(source="openalex", title="Paper A", doi="10.1/a"),
        Paper(source="openalex", title="Paper B", doi="10.1/b"),
        Paper(source="openalex", title="Paper C", doi="10.1/c"),
    ]


def test_renumber_by_appearance_and_drops_uncited():
    store = CitationStore.of_pool(_pool())  # nomor kerja 1=A, 2=B, 3=C
    # Draf merujuk C lalu A (B tak dikutip); nomor kerja acak.
    draft = "Klaim pertama [3]. Klaim kedua [1]. Lagi soal C [3]."

    text, cited = renumber(draft, store)

    assert text == "Klaim pertama [1]. Klaim kedua [2]. Lagi soal C [1]."
    assert [p.title for p in cited] == ["Paper C", "Paper A"]  # urut kemunculan


def test_renumber_handles_grouped_markers():
    store = CitationStore.of_pool(_pool())
    text, cited = renumber("Gabungan [2, 3] lalu [1].", store)
    assert text == "Gabungan [1, 2] lalu [3]."
    assert [p.title for p in cited] == ["Paper B", "Paper C", "Paper A"]


def test_renumber_drops_hallucinated_numbers():
    store = CitationStore.of_pool(_pool())
    text, cited = renumber("Nyata [2], karangan [99].", store)
    assert text == "Nyata [1], karangan ."  # nomor di luar pool dibuang
    assert [p.title for p in cited] == ["Paper B"]


def test_build_bibliography_only_cited_in_order():
    store = CitationStore.of_pool(_pool())
    _, cited = renumber("Lihat [3] dan [1].", store)
    biblio = build_bibliography(cited, "en")
    assert biblio.splitlines()[0] == "## References"
    assert '[1] "Paper C." doi: 10.1/c' in biblio
    assert '[2] "Paper A." doi: 10.1/a' in biblio
    assert "Paper B" not in biblio  # tak dikutip -> tak masuk daftar
