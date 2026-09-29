"""
web_search.py — DuckDuckGo-based web search tool.
No API key required; perfect for MVP.
"""

from __future__ import annotations

from duckduckgo_search import DDGS
from app.core.config import settings


def search_web(query: str, max_results: int | None = None) -> str:
    """
    Search the web and return a formatted string of results.

    Returns
    -------
    str
        Concatenated snippets with titles and URLs.
    """
    max_results = max_results or settings.search.max_results
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
    except Exception as exc:
        return f"[Web search failed: {exc}]"

    if not results:
        return "No web results found for this query."

    parts: list[str] = []
    for i, r in enumerate(results, 1):
        parts.append(
            f"**Result {i}:** {r.get('title', 'Untitled')}\n"
            f"URL: {r.get('href', '')}\n"
            f"{r.get('body', '')}\n"
        )
    return "\n---\n".join(parts)
