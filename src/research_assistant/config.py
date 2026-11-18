"""Memuat kredensial & setting dari ``.env`` dan menyediakannya sebagai objek Settings yang dipakai klien sumber, agent, dan UI."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Setting runtime untuk satu sesi agent."""

    openai_api_key: str | None = None
    openalex_mailto: str | None = None
    semantic_scholar_api_key: str | None = None

    # Toggle sumber
    enable_openalex: bool = True
    enable_semantic_scholar: bool = True
    enable_arxiv: bool = True

    # Budget loop
    model: str = "gpt-4o-mini"
    max_rounds: int = 3
    per_source: int = 8
    top_k: int = 20
    languages: tuple[str, ...] = ("id", "en")

    @classmethod
    def from_env(cls) -> "Settings":
        """Bangun Settings dari environment (.env)."""
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openalex_mailto=os.getenv("OPENALEX_MAILTO"),
            semantic_scholar_api_key=os.getenv("SEMANTIC_SCHOLAR_API_KEY"),
        )
