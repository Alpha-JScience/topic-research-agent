

from __future__ import annotations

import sys
from pathlib import Path
from dataclasses import dataclass, field

# Python 3.11+ ships tomllib; older versions need the tomli backport
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

# ---------------------------------------------------------------------------
# Resolve the project root (two levels up from this file)
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SECRETS_PATH = PROJECT_ROOT / ".secrets.toml"


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    base_url: str
    model: str


@dataclass(frozen=True)
class SearchConfig:
    max_results: int = 5


@dataclass(frozen=True)
class Settings:
    llm: LLMConfig
    search: SearchConfig = field(default_factory=SearchConfig)
    project_root: Path = PROJECT_ROOT
    data_raw: Path = PROJECT_ROOT / "data" / "raw"
    data_processed: Path = PROJECT_ROOT / "data" / "processed"


def load_settings(path: Path | None = None) -> Settings:
    """Read .secrets.toml and return a frozen Settings object."""
    path = path or SECRETS_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found at {path}. "
            "Copy .secrets.toml.example → .secrets.toml and fill in your keys."
        )

    with open(path, "rb") as f:
        raw = tomllib.load(f)

    llm_raw = raw.get("llm", {})
    llm = LLMConfig(
        api_key=llm_raw.get("api_key", ""),
        base_url=llm_raw.get("base_url", "https://api.openai.com/v1"),
        model=llm_raw.get("model", "gpt-oss-120b"),
    )

    search_raw = raw.get("search", {})
    search = SearchConfig(
        max_results=search_raw.get("max_results", 5),
    )

    return Settings(llm=llm, search=search)


# ---------------------------------------------------------------------------
# Module-level singleton — import this everywhere
# ---------------------------------------------------------------------------
settings: Settings = load_settings()
