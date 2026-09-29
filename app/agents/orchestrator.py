"""
orchestrator.py — The Manager agent that decides which sub-agents to
invoke based on the input mode (TEXT vs CSV).
"""

from __future__ import annotations

from app.core.state import AgentState, InputMode
from app.agents.researcher import run_researcher
from app.agents.analyst import run_analyst
from app.agents.writer import run_writer


def orchestrate(state: AgentState) -> AgentState:
    """
    Route the workflow:
      TEXT → Researcher → Writer
      CSV  → Analyst → (optional Researcher) → Writer
    """
    state.add_status("🧠 Orchestrator: Planning workflow…")

    if state.input_mode == InputMode.TEXT:
        # Pure web research flow
        state = run_researcher(state)

    elif state.input_mode == InputMode.CSV:
        # Data analysis flow
        state = run_analyst(state)

        # Optionally enrich with web context if user provided a meaningful prompt
        if state.user_prompt.strip():
            state.add_status(
                "🧠 Orchestrator: Adding web context to CSV analysis…")
            state = run_researcher(state)

    else:
        state.add_status(f"⚠️ Unknown input mode: {state.input_mode}")
        state.final_report = "Error: Unknown input mode."
        return state

    # Always finish with the writer
    state = run_writer(state)

    state.add_status("🎉 Orchestrator: Workflow complete!")
    return state
