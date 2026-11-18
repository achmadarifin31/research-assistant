"""Menerima input topik, menampilkan progres loop, lalu merender brief dengan tombol unduh.

Jalankan via entry point root: ``uv run streamlit run streamlit_app.py``.
"""

from __future__ import annotations

import streamlit as st

from research_assistant.config import Settings


def render_sidebar() -> Settings:
    """Sidebar: API key, model, toggle sumber, bahasa, budget putaran."""
    raise NotImplementedError


def main() -> None:
    """Titik masuk UI Streamlit."""
    st.set_page_config(page_title="Research Agent", page_icon="📚")
    st.title("📚 Research Agent")
    st.info("Antarmuka belum diimplementasikan.")


if __name__ == "__main__":
    main()
