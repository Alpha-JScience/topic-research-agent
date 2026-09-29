"""
analyst.py — Reads a CSV via the csv_reader tool and asks the LLM
to extract key insights and trends.
"""

from __future__ import annotations

from openai import OpenAI
from app.core.config import settings
from app.core.state import AgentState
from app.tools.csv_reader import read_and_summarize_csv

SYSTEM_PROMPT = """\
You are a Data Analyst Agent. You receive a structured summary of a CSV dataset.
Your job is to:
1. Identify the 3-5 most important insights or trends.
2. Note any anomalies, outliers, or missing data patterns.
3. Suggest what the data might imply in the context of the user's question.

Formatting rules:
- Use **bold** for key metrics and numbers.
- Use bullet points and short paragraphs.
- Use Markdown tables when comparing values.
"""


def run_analyst(state: AgentState) -> AgentState:
    """Read the CSV, summarize it, and ask the LLM for insights."""
    state.add_status("📊 Analyst: Reading CSV file…")

    csv_summary = read_and_summarize_csv(state.csv_file_path)
    state.add_status("📊 Analyst: CSV parsed successfully")

    client = OpenAI(api_key=settings.llm.api_key,
                    base_url=settings.llm.base_url)

    user_msg = f"User's question/context: {state.user_prompt}\n\n--- CSV Summary ---\n{csv_summary}"

    response = client.chat.completions.create(
        model=settings.llm.model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.3,
    )

    state.csv_analysis = response.choices[0].message.content or ""
    state.add_status("✅ Analyst: Done")
    return state
