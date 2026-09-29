"""
streamlit_app.py — Beautiful, readable UI for Topic Research Agent v2.

Run with:
    streamlit run ui/streamlit_app.py
"""

from __future__ import annotations
from app.core.config import settings
from app.core.workflow import run_workflow
from app.core.state import InputMode
import streamlit as st
import sys
from pathlib import Path

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Topic Research Agent v2",
    page_icon="🔬",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar — Input Mode Toggle
# ---------------------------------------------------------------------------
st.sidebar.title("⚙️ Configuration")

input_mode_label = st.sidebar.radio(
    "Select Input Mode",
    options=["📝 Text Topic", "📊 CSV File"],
    index=0,
)

input_mode = InputMode.TEXT if "Text" in input_mode_label else InputMode.CSV

st.sidebar.divider()
st.sidebar.caption(f"**Model:** `{settings.llm.model}`")
st.sidebar.caption(f"**Base URL:** `{settings.llm.base_url}`")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
st.title("🔬 Topic Research Agent v2")
st.markdown(
    "Research any topic via **web search** or analyze your own **CSV data** — "
    "delivered as a clean, readable report."
)

# --- Input widgets ---
user_prompt = st.text_area(
    "💬 Enter your topic or question",
    placeholder="e.g. What are the latest trends in renewable energy?",
    height=100,
)

csv_file = None
if input_mode == InputMode.CSV:
    csv_file = st.file_uploader(
        "📂 Upload a CSV file",
        type=["csv"],
        help="Your file will be analyzed by the Data Analyst agent.",
    )

# --- Run button ---
run_clicked = st.button("🚀 Generate Research Report",
                        type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------
if run_clicked:
    # --- Validation ---
    if not user_prompt.strip() and input_mode == InputMode.TEXT:
        st.warning("Please enter a topic or question.")
        st.stop()

    if input_mode == InputMode.CSV and csv_file is None:
        st.warning("Please upload a CSV file.")
        st.stop()

    # --- Save uploaded CSV to data/raw/ ---
    csv_path: str | None = None
    if csv_file is not None:
        save_dir = settings.data_raw
        save_dir.mkdir(parents=True, exist_ok=True)
        csv_path = str(save_dir / csv_file.name)
        with open(csv_path, "wb") as f:
            f.write(csv_file.getbuffer())

    # --- Run workflow with live status ---
    with st.status("🧠 Agents are working…", expanded=True) as status_box:
        state = run_workflow(
            input_mode=input_mode,
            user_prompt=user_prompt,
            csv_file_path=csv_path,
        )

        # Show each status message as it was recorded
        for msg in state.status_messages:
            st.write(msg)

        status_box.update(label="✅ Report Ready!",
                          state="complete", expanded=False)

    # --- Render the final report ---
    st.divider()
    st.subheader("📄 Final Report")
    st.markdown(state.final_report)

    # --- Download button ---
    st.download_button(
        label="⬇️ Download Report as Markdown",
        data=state.final_report,
        file_name="research_report.md",
        mime="text/markdown",
    )
