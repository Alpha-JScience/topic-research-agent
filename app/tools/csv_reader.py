"""
csv_reader.py — Reads a CSV file and returns a statistical summary
so the LLM analyst isn't overwhelmed by raw rows.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


def read_and_summarize_csv(file_path: str | Path, max_rows_preview: int = 10) -> str:
    """
    Parse a CSV and return a human-readable summary string.

    Includes:
    - Shape (rows × cols)
    - Column names and dtypes
    - Basic descriptive statistics for numeric columns
    - A preview of the first N rows
    """
    path = Path(file_path)
    if not path.exists():
        return f"[Error: File not found at {path}]"

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        return f"[Error reading CSV: {exc}]"

    if df.empty:
        return "[The uploaded CSV file is empty.]"

    lines: list[str] = []

    # Shape
    lines.append(f"## CSV Summary\n")
    lines.append(f"- **Rows:** {len(df)}")
    lines.append(f"- **Columns:** {len(df.columns)}\n")

    # Column info
    lines.append("### Columns")
    for col in df.columns:
        lines.append(f"- `{col}` ({df[col].dtype})")
    lines.append("")

    # Numeric stats
    numeric_cols = df.select_dtypes(include="number").columns
    if not numeric_cols.empty:
        lines.append("### Descriptive Statistics (Numeric)")
        stats = df[numeric_cols].describe().to_markdown()
        lines.append(stats)
        lines.append("")

    # Preview
    lines.append(f"### First {min(max_rows_preview, len(df))} Rows Preview")
    lines.append(df.head(max_rows_preview).to_markdown(index=False))

    return "\n".join(lines)
