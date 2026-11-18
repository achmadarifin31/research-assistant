"""Mendefinisikan ``AgentState`` yang dialirkan dan diperbarui antar node sepanjang loop agent."""

from __future__ import annotations

from typing import TypedDict

from research_assistant.models import Paper


class AgentState(TypedDict, total=False):
    # Parameter dari UI
    topic: str
    languages: list[str]
    max_rounds: int
    per_source: int
    top_k: int

    # Progres loop
    round: int
    subquestions: list[str]  # pertanyaan putaran ini
    asked: list[str]  # semua yang pernah diajukan (cegah berulang)
    pool: list[Paper]  # kolam kandidat Paper (sudah dedup)
    gaps: list[str]  # celah hasil refleksi
    done: bool  # sinyal berhenti loop

    # Keluaran
    brief: str
    log: list[str]  # baris status untuk UI
