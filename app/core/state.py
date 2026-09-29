from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from typing import Optional, Literal


class WorkflowState(BaseModel):
    """Shared state management for the workflow."""
    input_mode: Literal["TEXT", "CSV"] = "TEXT"
    user_prompt: str = ""
    csv_file_path: Optional[str] = None

    # Intermediate data collected by agents
    web_research: Optional[str] = None
    csv_analysis: Optional[str] = None

    # Final output
    final_report: Optional[str] = None
    status: str = "INITIALIZED"


"""
state.py — Pydantic model that holds all data flowing through the workflow.
"""


class InputMode(str, Enum):
    TEXT = "text"
    CSV = "csv"


class AgentState(BaseModel):
    """Mutable state bag passed between agents in the workflow."""

    # --- Input ---
    input_mode: InputMode = InputMode.TEXT
    user_prompt: str = ""
    csv_file_path: Optional[str] = None

    # --- Intermediate outputs ---
    research_findings: str = ""
    csv_analysis: str = ""

    # --- Final output ---
    final_report: str = ""

    # --- Status tracking for the UI ---
    status_messages: list[str] = Field(default_factory=list)

    def add_status(self, msg: str) -> None:
        self.status_messages.append(msg)
