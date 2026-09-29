"""
app.py — Simple CLI entry point for testing without the UI.
"""

from __future__ import annotations
from app.core.workflow import run_workflow
from app.core.state import InputMode

import sys
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main() -> None:
    print("=" * 60)
    print("  Topic Research Agent v2 — CLI Mode")
    print("=" * 60)

    mode_input = input("\nChoose input mode [1 = Text, 2 = CSV]: ").strip()
    if mode_input == "2":
        mode = InputMode.CSV
        csv_path = input("Enter path to CSV file: ").strip()
    else:
        mode = InputMode.TEXT
        csv_path = None

    prompt = input("Enter your topic / question: ").strip()

    print("\n⏳ Running workflow…\n")
    state = run_workflow(
        input_mode=mode,
        user_prompt=prompt,
        csv_file_path=csv_path,
    )

    # Print status log
    print("\n--- Status Log ---")
    for msg in state.status_messages:
        print(f"  {msg}")

    # Print final report
    print("\n--- Final Report ---\n")
    print(state.final_report)


if __name__ == "__main__":
    main()
