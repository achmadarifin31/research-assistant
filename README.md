# Research Agent

Agent riset yang, dari satu topik, menghasilkan **cited brief IEEE dwibahasa (Indonesia & Inggris)** dengan sitasi terverifikasi. Dibangun dengan **OpenAI** (LLM), **LangGraph** (loop plan → search → reflect → synthesize), dan **Streamlit** (UI). Sumber literatur: **OpenAlex**, **Semantic Scholar**, dan **arXiv**.

## Struktur proyek

```
src/research_assistant/   # kode sumber (package)
  models.py               # schema Paper + dedup
  config.py               # setting & kredensial
  sources/                # klien OpenAlex / Semantic Scholar / arXiv
  citations/              # CitationStore + formatter IEEE
  agent/                  # state, node, graph LangGraph
  ui/                     # aplikasi Streamlit
tests/                    # unit (offline) + integration (live API)
docs/                     # dokumentasi
streamlit_app.py          # entry point UI
```

## Setup

Butuh [uv](https://docs.astral.sh/uv/) dan Python 3.12+.

```bash
# 1. Install dependensi + buat virtualenv
uv sync

# 2. Siapkan kredensial
cp .env.example .env      # lalu isi OPENAI_API_KEY (wajib)
```

## Menjalankan

```bash
uv run streamlit run streamlit_app.py
```

## Pengujian

```bash
uv run pytest                      # semua test
uv run pytest -m "not integration" # hanya test offline (tanpa jaringan)
uv run pytest -m integration       # hanya test live API
```

## Status

Dalam pengembangan: lapisan sumber literatur (OpenAlex, Semantic Scholar, arXiv) beserta penggabungan & deduplikasi hasil.
