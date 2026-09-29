import os
import pandas as pd
import toml
from openai import OpenAI
from typing import List, Dict, Any

# Paths
CONFIG_PATH = os.path.join(os.path.dirname(
    __file__), ".streamlit", ".secret.toml")
CSV_PATH = os.path.join(os.path.dirname(__file__), "topics.csv")


def load_config() -> Dict[str, Any]:
    """Load .secret.toml with environment variable override precedence."""
    config = {
        "Ai Platform 1": {
            "base_url": "https://api.Ai Platform",
            "api_key": "your-key-paste",
            "model": "choice model"
        },
        "app": {
            "max_tokens": 4096,
            "temperature": 0.7
        }
    }

    if os.path.exists(CONFIG_PATH):
        try:
            loaded = toml.load(CONFIG_PATH)
            if "deepseek" in loaded:
                config["deepseek"].update(loaded["deepseek"])
            if "app" in loaded:
                config["app"].update(loaded["app"])
        except Exception as e:
            print(f"Warning: Could not load {CONFIG_PATH}: {e}")

    # Environment variables take highest precedence
    config["deepseek"]["base_url"] = os.getenv(
        "DEEPSEEK_BASE_URL", config["deepseek"]["base_url"])
    config["deepseek"]["api_key"] = os.getenv(
        "DEEPSEEK_API_KEY", config["deepseek"]["api_key"])
    config["deepseek"]["model"] = os.getenv(
        "DEEPSEEK_MODEL", config["deepseek"]["model"])

    max_tokens_env = os.getenv("MAX_TOKENS")
    if max_tokens_env:
        config["app"]["max_tokens"] = int(max_tokens_env)

    temp_env = os.getenv("TEMPERATURE")
    if temp_env:
        config["app"]["temperature"] = float(temp_env)

    return config


def load_topics_csv(path: str = CSV_PATH) -> pd.DataFrame:
    """Load and validate the topic-subject database."""
    try:
        df = pd.read_csv(path)
        required_cols = {"topic_keyword", "subject_category",
                         "prompt_prefix", "example_hints"}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"CSV must contain columns: {required_cols}")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["topic_keyword", "subject_category", "prompt_prefix", "example_hints"])


def classify_topic(topic: str, topics_df: pd.DataFrame) -> str:
    """Return 'IT/AI' or 'General' via keyword match, fallback to General."""
    topic_lower = topic.lower()
    for _, row in topics_df.iterrows():
        if str(row["topic_keyword"]).lower() in topic_lower:
            return str(row["subject_category"])
    return "General"


def build_system_prompt(domain: str, formats: List[str], depth: str) -> str:
    """Construct the system prompt with format and depth instructions."""
    format_instructions = "Provide the output in the following formats:\n" + \
        "\n".join([f"- {f}" for f in formats])

    return f"""You are a Topic Research Agent specialized in {domain} topics.

DEPTH LEVEL: {depth}
OUTPUT FORMATS REQUESTED:
{format_instructions}

RULES:
- For IT/AI topics: use precise technical terminology, reference real tools/frameworks, and ensure quiz questions test conceptual understanding not trivia.
- For General topics: use accessible language, real-world analogies, and avoid unexplained jargon.
- If uncertain about a fact, state "According to current understanding..." rather than presenting speculation as fact.
- For MCQ quizzes: provide exactly 4 options (A-D), mark the correct answer, and include a one-sentence rationale.
- For fact tables: use Markdown table syntax with clear column headers.
- Ensure the response length and detail align with the requested depth level.
"""


def call_llm(system_prompt: str, user_topic: str, config: Dict[str, Any]) -> str:
    """Call DeepSeek API via OpenAI SDK, handle errors gracefully."""
    api_key = config["deepseek"]["api_key"]
    if not api_key or api_key == "sk-your-deepseek-key-here":
        return "⚠️ **Configuration Error:** DeepSeek API key is not configured. Please set the `DEEPSEEK_API_KEY` environment variable or update `.streamlit/.secret.toml`."

    client = OpenAI(
        api_key=api_key,
        base_url=config["deepseek"]["base_url"]
    )

    try:
        response = client.chat.completions.create(
            model=config["deepseek"]["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Topic: {user_topic}"}
            ],
            temperature=config["app"]["temperature"],
            max_tokens=config["app"]["max_tokens"],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ **API Error:** Failed to generate response. Details: {str(e)}"
