"""
researcher.py — Uses the LLM + web_search tool to gather information
about a given topic.
"""

from __future__ import annotations

from openai import OpenAI
from app.core.config import settings
from app.core.state import AgentState
from app.tools.web_search import search_web

SYSTEM_PROMPT = """\
You are a thorough Research Agent. Your job is to:
1. Understand the user's topic/question.
2. Use the provided web search results as your evidence base.
3. Produce a structured research brief with key facts, statistics, and sources.

Rules:
- Cite URLs when referencing specific claims.
- Highlight important numbers in **bold**.
- Use bullet points for lists.
- If the search results are insufficient, say so clearly.
"""


def run_researcher(state: AgentState) -> AgentState:
    """Search the web and ask the LLM to synthesize findings."""
    state.add_status("🔍 Researcher: Searching the web…")

    raw_results = search_web(state.user_prompt)
    state.add_status(
        f"🔍 Researcher: Found web results ({len(raw_results)} chars)")

    client = OpenAI(api_key=settings.llm.api_key,
                    base_url=settings.llm.base_url)

    response = client.chat.completions.create(
        model=settings.llm.model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Topic: {state.user_prompt}\n\n"
                    f"--- Web Search Results ---\n{raw_results}"
                ),
            },
        ],
        temperature=0.3,
    )

    state.research_findings = response.choices[0].message.content or ""
    state.add_status("✅ Researcher: Done")
    return state
