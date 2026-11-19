"""Unit test offline untuk format penulis dan entri IEEE (ID/EN)."""

from research_assistant.citations.ieee import format_authors, format_entry
from research_assistant.models import Paper


def test_initials_and_single_author():
    assert format_authors(["Saif M. Mohammad"]) == "S. M. Mohammad"
    assert format_authors(["Achmad Nurs Syururi Arifin"]) == "A. N. S. Arifin"


def test_two_authors_conjunction_per_language():
    authors = ["Ada Lovelace", "Alan Turing"]
    assert format_authors(authors, "id") == "A. Lovelace dan A. Turing"
    assert format_authors(authors, "en") == "A. Lovelace and A. Turing"


def test_three_authors_use_comma_and_conjunction():
    authors = ["A One", "B Two", "C Three"]
    assert format_authors(authors, "en") == "A. One, B. Two, and C. Three"


def test_more_than_six_authors_truncated_et_al():
    authors = [f"Name{i} Sur{i}" for i in range(7)]
    assert format_authors(authors) == "N. Sur0, et al."


def test_format_entry_with_doi():
    paper = Paper(
        source="openalex", title="Deep Face", authors=["A One", "B Two"],
        venue="J. Faces", year=2024, doi="https://doi.org/10.1/ABC",
    )
    entry = format_entry(1, paper, "id")
    assert entry == '[1] A. One dan B. Two, "Deep Face," J. Faces, 2024. doi: 10.1/abc'


def test_format_entry_fallback_arxiv_then_url():
    arxiv = Paper(source="arxiv", title="On Faces", authors=["C Three"], year=2013, arxiv_id="1309.6352")
    assert format_entry(2, arxiv, "en").endswith("arXiv:1309.6352")

    url_only = Paper(source="openalex", title="No DOI", authors=["D Four"], url="http://x/y")
    entry = format_entry(3, url_only, "en")
    assert entry.endswith("[Online]. Available: http://x/y")


def test_format_entry_omits_missing_fields_cleanly():
    paper = Paper(source="arxiv", title="Bare", authors=[])  # tanpa penulis/venue/tahun/id
    assert format_entry(4, paper, "id") == '[4] "Bare."'
