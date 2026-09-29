"""
workflow.py — Thin wrapper that initializes state and kicks off the
orchestrator. Keeps the UI layer decoupled from agent internals.
"""

from __future__ import annotations

from app.core.state import AgentState, InputMode
from app.agents.orchestrator import orchestrate


def run_workflow(
    input_mode: InputMode,
    user_prompt: str,
    csv_file_path: str | None = None,
) -> AgentState:
    """
    Entry point for the entire pipeline.

    Parameters
    ----------
    input_mode : InputMode
        TEXT or CSV.
    user_prompt : str
        The user's topic or question.
    csv_file_path : str, optional
        Absolute path to the uploaded CSV (required when mode is CSV).

    Returns
    -------
    AgentState
        Final state with `final_report` and `status_messages` populated.
    """
    state = AgentState(
        input_mode=input_mode,
        user_prompt=user_prompt,
        csv_file_path=csv_file_path,
    )

    state.add_status("🚀 Workflow started")
    state = orchestrate(state)
    return state
