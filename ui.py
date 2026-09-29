from app import load_config, load_topics_csv, classify_topic, build_system_prompt, call_llm
import streamlit as st
import sys
import os

# Ensure local imports work seamlessly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Topic Research Agent",
                   page_icon="🔬", layout="centered")

# Initialize session state
if "config" not in st.session_state:
    st.session_state.config = load_config()
if "topics_df" not in st.session_state:
    st.session_state.topics_df = load_topics_csv()


def reload_data():
    st.session_state.config = load_config()
    st.session_state.topics_df = load_topics_csv()


st.title("🔬 Topic Research Agent")
st.caption(
    "Instant, multi-format research briefs on any topic — from AI to Art History.")
st.markdown("---")

# 1. Topic Input
topic = st.text_input(
    "📝 Enter a topic:", placeholder='e.g., "Transformer attention mechanism" or "Photosynthesis"')

# 2. Subject Classification (with override)
detected_domain = classify_topic(
    topic, st.session_state.topics_df) if topic else "General"

st.markdown("🏷️ **Subject (auto-detected):**")
domain = st.radio(
    "Select Domain:",
    ["IT/AI", "General"],
    index=0 if detected_domain == "IT/AI" else 1,
    horizontal=True
)

# 3. Output Format Toggle
st.markdown("📊 **Output Format** (select all that apply):")
formats = st.multiselect(
    "Choose formats:",
    ["Paragraph", "Bullet", "Concise Fact Table", "Quick Summary",
        "Practical Relevant Example", "Quiz MCQ-4", "Question with Answer", "Default (General)"],
    default=["Default (General)"]
)

# 4. Depth Level Toggle
st.markdown("🔍 **Depth Level:**")
depth = st.radio(
    "Select depth:",
    ["General (Default)", "Medium", "Detailing",
     "Conceptual", "Theoretical", "Paragraphical"],
    index=0,
    horizontal=True
)

# 5. Generate Action
if st.button("🚀 Generate", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    elif not formats:
        st.warning("Please select at least one output format.")
    else:
        with st.spinner("Researching and formatting your topic..."):
            system_prompt = build_system_prompt(domain, formats, depth)
            result = call_llm(system_prompt, topic, st.session_state.config)

            st.markdown("---")
            st.subheader("📄 Results")
            st.markdown(result)

# Sidebar for admin/reload actions
with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("🔄 Reload Topics CSV & Config"):
        reload_data()
        st.success("Reloaded successfully!")

    st.markdown("---")
    st.markdown("### About")
    st.markdown("Powered by DeepSeek API.")
    st.markdown("Optimized for Alibaba Cloud Function Compute.")
