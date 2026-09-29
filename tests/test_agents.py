"""
test_agents.py — Unit tests for individual agents.
Uses mocking so no real API calls are made.
"""

from unittest.mock import patch, MagicMock
from app.core.state import AgentState, InputMode


def _mock_llm_response(content: str) -> MagicMock:
    """Helper to create a fake OpenAI chat completion response."""
    choice = MagicMock()
    choice.message.content = content
    resp = MagicMock()
    resp.choices = [choice]
    return resp


@patch("app.agents.researcher.OpenAI")
@patch("app.agents.researcher.search_web", return_value="Mock search result about AI.")
def test_run_researcher(mock_search, mock_openai_cls):
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_llm_response(
        "## AI Research\n- **Key fact**: AI is growing."
    )
    mock_openai_cls.return_value = mock_client

    state = AgentState(input_mode=InputMode.TEXT, user_prompt="AI trends")
    from app.agents.researcher import run_researcher

    result = run_researcher(state)
    assert "AI" in result.research_findings
    assert len(result.status_messages) >= 2


@patch("app.agents.analyst.OpenAI")
@patch(
    "app.agents.analyst.read_and_summarize_csv",
    return_value="## CSV Summary\n- Rows: 100",
)
def test_run_analyst(mock_csv, mock_openai_cls):
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_llm_response(
        "## Insights\n- **Trend**: Sales up **20%**."
    )
    mock_openai_cls.return_value = mock_client

    state = AgentState(
        input_mode=InputMode.CSV,
        user_prompt="Analyze sales",
        csv_file_path="/fake/path.csv",
    )
    from app.agents.analyst import run_analyst

    result = run_analyst(state)
    assert "Trend" in result.csv_analysis


@patch("app.agents.writer.OpenAI")
def test_run_writer(mock_openai_cls):
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_llm_response(
        "# Final Report\n## Key Takeaways\n- **Point 1**"
    )
    mock_openai_cls.return_value = mock_client

    state = AgentState(
        input_mode=InputMode.TEXT,
        user_prompt="Test",
        research_findings="Some findings",
    )
    from app.agents.writer import run_writer

    result = run_writer(state)
    assert "Final Report" in result.final_report
