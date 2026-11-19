"""Memformat penulis dan entri daftar pustaka gaya IEEE (ID/EN) serta menomori ulang sitasi sesuai urutan kemunculan di brief.

Format entri:
    [n] F. Last, dan F. Last, "Judul," Venue, tahun. doi: 10.x/...
("dan" untuk ID, "and" untuk EN; fallback ke arXiv id atau URL bila tak ada DOI).
"""

from __future__ import annotations

import re

from research_assistant.citations.store import CitationStore
from research_assistant.models import Paper, normalize_doi

MAX_AUTHORS = 6  # lebih dari ini -> penulis pertama + "et al." (gaya IEEE)

_CITE = re.compile(r"\[([\d][\d,\s]*)\]")
_HEADING = {"id": "Daftar Pustaka", "en": "References"}


def _initials(name: str) -> str:
    """Mengubah nama penuh menjadi bentuk IEEE 'F. Last' (nama depan jadi inisial, nama belakang utuh)."""
    tokens = name.split()
    if len(tokens) <= 1:
        return name.strip()
    surname = tokens[-1]
    given_initials = []
    for part in tokens[:-1]:
        # Tangani nama bertanda hubung: "Jean-Pierre" -> "J.-P."
        chunks = [c for c in part.split("-") if c]
        given_initials.append("-".join(f"{c[0].upper()}." for c in chunks))
    return " ".join([*given_initials, surname])


def format_authors(authors: list[str], lang: str = "id") -> str:
    """Merangkai daftar penulis gaya IEEE: inisial 'F. Last', konjungsi per bahasa, dan 'et al.' bila lebih dari enam penulis."""
    names = [_initials(a) for a in authors if a and a.strip()]
    if not names:
        return ""
    if len(names) > MAX_AUTHORS:
        return f"{names[0]}, et al."

    conjunction = "dan" if lang == "id" else "and"
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} {conjunction} {names[1]}"
    return ", ".join(names[:-1]) + f", {conjunction} {names[-1]}"


def _identifier(paper: Paper, lang: str) -> str:
    """Membangun penutup entri: DOI bila ada, lalu fallback id arXiv, lalu URL (berlabel per bahasa)."""
    doi = normalize_doi(paper.doi)
    if doi:
        return f"doi: {doi}"
    if paper.arxiv_id:
        return f"arXiv:{paper.arxiv_id}"
    if paper.url:
        online = "Daring" if lang == "id" else "Online"
        available = "Tersedia" if lang == "id" else "Available"
        return f"[{online}]. {available}: {paper.url}"
    return ""


def format_entry(number: int, paper: Paper, lang: str = "id") -> str:
    """Memformat satu entri daftar pustaka IEEE bernomor ``number``; field kosong (venue/tahun/identifier) dilewati tanpa merusak tanda baca."""
    authors = format_authors(paper.authors, lang)
    body = f"{authors}, " if authors else ""

    meta = [m for m in (paper.venue, str(paper.year) if paper.year else None) if m]
    if meta:
        # Koma di dalam kutip karena masih ada venue/tahun yang menyusul.
        body += f'"{paper.title}," ' + ", ".join(meta) + "."
    else:
        # Tak ada info lanjutan -> tutup judul dengan titik.
        body += f'"{paper.title}."'

    identifier = _identifier(paper, lang)
    if identifier:
        body += f" {identifier}"
    return f"[{number}] {body}"


def renumber(brief_text: str, store: CitationStore) -> tuple[str, list[Paper]]:
    """Menomori ulang penanda ``[n]`` pada brief menurut urutan kemunculan, membuang nomor tak dikenal, dan mengembalikan teks baru + daftar paper terkutip berurut (dasar daftar pustaka)."""
    old_to_new: dict[int, int] = {}
    cited: list[Paper] = []

    def replace(match: re.Match[str]) -> str:
        raw = match.group(1).replace(" ", "")
        mapped: list[int] = []
        for token in raw.split(","):
            if not token:
                continue
            old = int(token)
            paper = store.get(old)
            if paper is None:
                continue  # nomor halusinasi / di luar pool -> buang
            if old not in old_to_new:
                cited.append(paper)
                old_to_new[old] = len(cited)
            mapped.append(old_to_new[old])
        if not mapped:
            return ""  # seluruh isi penanda tak valid -> hapus penanda
        return "[" + ", ".join(str(n) for n in mapped) + "]"

    return _CITE.sub(replace, brief_text), cited


def build_bibliography(papers: list[Paper], lang: str = "id") -> str:
    """Merakit blok daftar pustaka lengkap: heading per bahasa + entri bernomor 1..k, hanya memuat paper yang diberikan (sumber terkutip)."""
    heading = _HEADING.get(lang, _HEADING["id"])
    lines = [f"## {heading}", ""]
    lines += [format_entry(i, paper, lang) for i, paper in enumerate(papers, start=1)]
    return "\n".join(lines)
