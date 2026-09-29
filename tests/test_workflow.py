"""
test_workflow.py — Integration-level tests for the workflow router.
"""

from unittest.mock import patch
from app.core.state import AgentState, InputMode


@patch("app.core.workflow.orchestrate")
def test_run_workflow_text_mode(mock_orch):
    mock_orch.side_effect = lambda s: s  # passthrough

    from app.core.workflow import run_workflow

    state = run_workflow(InputMode.TEXT, "test topic")
    assert state.input_mode == InputMode.TEXT
    assert state.user_prompt == "test topic"
    mock_orch.assert_called_once()


@patch("app.core.workflow.orchestrate")
def test_run_workflow_csv_mode(mock_orch):
    mock_orch.side_effect = lambda s: s

    from app.core.workflow import run_workflow

    state = run_workflow(InputMode.CSV, "analyze this",
                         csv_file_path="/tmp/x.csv")
    assert state.input_mode == InputMode.CSV
    assert state.csv_file_path == "/tmp/x.csv"
