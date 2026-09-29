"""
writer.py — Takes research findings and/or CSV analysis and produces
a beautifully formatted, easy-to-read Markdown report.
"""

from __future__ import annotations

from openai import OpenAI
from app.core.config import settings
from app.core.state import AgentState, InputMode

SYSTEM_PROMPT = """\
You are an expert Report Writer. You receive raw research notes and/or data
analysis and turn them into a polished, highly readable Markdown report.

STRICT FORMATTING RULES (follow these exactly):
1. Start with a single H1 (#) title that captures the topic.
2. Use H2 (##) for major sections and H3 (###) for subsections.
3. Use bullet points for every list — never comma-separated inline lists.
4. **Bold** every key metric, number, percentage, and important conclusion.
5. Keep every paragraph to 3 sentences or fewer.
6. If data comparisons exist, use a Markdown table.
7. End with a "## Key Takeaways" section containing 3-5 bolded bullet points.
8. Do NOT output walls of text. Scannability is the #1 priority.
"""


def run_writer(state: AgentState) -> AgentState:
    """Combine all agent outputs into a final readable report."""
    state.add_status("✍️ Writer: Composing final report…")

    client = OpenAI(api_key=settings.llm.api_key,
                    base_url=settings.llm.base_url)

    # Build context depending on input mode
    context_parts: list[str] = []
    if state.input_mode == InputMode.TEXT:
        context_parts.append(
            f"## Research Findings\n{state.research_findings}")
    elif state.input_mode == InputMode.CSV:
        context_parts.append(f"## CSV Data Analysis\n{state.csv_analysis}")
        if state.research_findings:
            context_parts.append(
                f"## Supplementary Web Research\n{state.research_findings}"
            )

    context = "\n\n---\n\n".join(context_parts)

    user_msg = (
        f"Topic / Question: {state.user_prompt}\n\n"
        f"--- Agent Outputs ---\n{context}"
    )

    response = client.chat.completions.create(
        model=settings.llm.model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.4,
    )

    state.final_report = response.choices[0].message.content or ""
    state.add_status("✅ Writer: Report complete")
    return state
