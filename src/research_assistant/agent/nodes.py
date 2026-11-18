"""Node loop agent yang membaca dan memperbarui AgentState: plan, search, reflect, dan synthesize."""

from __future__ import annotations

from research_assistant.agent.state import AgentState


def plan(state: AgentState) -> AgentState:
    """Pecah topik menjadi subpertanyaan (structured output)."""
    raise NotImplementedError


def search(state: AgentState) -> AgentState:
    """Isi pool dari subpertanyaan via search_all (dedup)."""
    raise NotImplementedError


def reflect(state: AgentState) -> AgentState:
    """Nilai kecukupan pool; usulkan query baru / tandai celah / set done."""
    raise NotImplementedError


def synthesize(state: AgentState) -> AgentState:
    """Susun cited brief grounded hanya dari pool (dwibahasa + IEEE)."""
    raise NotImplementedError


def should_continue(state: AgentState) -> str:
    """Edge bersyarat: lanjut loop atau berhenti (penjaga budget)."""
    raise NotImplementedError
