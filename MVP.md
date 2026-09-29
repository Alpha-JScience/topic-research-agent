# 🚀 Minimum Viable Product (MVP) Plan

## 1. Updated Project Structure
To support the UI requirement, we need to add a `ui/` directory to your existing structure.

```text
topic-research-agent/
│
├── app/
│   ├── __init__.py
│   ├── app.py               
│   ├── agents/
│   │   ├── orchestrator.py     # UPDATED: Handles input type routing
│   │   ├── researcher.py       
│   │   ├── analyst.py          # UPDATED: Processes CSV data
│   │   └── writer.py           # UPDATED: Enforces strict readable Markdown
│   ├── core/
│   │   ├── workflow.py         
│   │   └── state.py            # UPDATED: Stores input_type and file_path
│   └── tools/
│       ├── web_search.py       
│       └── csv_reader.py       # UPDATED: Robust CSV parsing & basic stats
│
├── ui/                         # NEW: Frontend for the toggle and output
│   └── streamlit_app.py        # UI implementation (Streamlit recommended for MVP)
│
├── tests/
│   ├── test_agents.py
│   └── test_workflow.py
│
├── requirements.txt            # Add: streamlit, pandas, python-magic (for file validation)
└── README.md
```


## 2. Step-by-Step Implementation Guide

### Phase 1: Core State & Tools (`app/core/` & `app/tools/`)
1. **Update `state.py`**: Add fields to the shared state:
   * `input_mode`: Enum (`TEXT`, `CSV`).
   * `user_prompt`: String.
   * `csv_file_path`: String (nullable).
2. **Upgrade `csv_reader.py`**: 
   * Use `pandas` to read the CSV.
   * Implement a tool that returns a summary: column names, data types, row count, and basic statistical summary (mean, min, max for numeric columns) so the LLM doesn't get overwhelmed by raw data.

### Phase 2: Agent Logic (`app/agents/`)
1. **Upgrade `orchestrator.py`**:
   * Add logic to check `state.input_mode`.
   * If `CSV`, pass the file path to the `Analyst` first. 
   * If `TEXT`, pass the prompt to the `Researcher`.
   * *Pro-tip:* Allow a hybrid mode where the Analyst summarizes the CSV, and the Researcher finds web context *about* the CSV data.
2. **Upgrade `analyst.py`**:
   * Give it the `csv_reader` tool.
   * Prompt it to extract 3-5 key insights from the data.
3. **Upgrade `writer.py` (Crucial for UI)**:
   * Update the system prompt to enforce the "Easy Readable" rules.
   * *Prompt snippet:* "You are an expert report writer. You must format your output using strict Markdown. Use H2 (##) for main sections, H3 (###) for subsections. Use bullet points for lists. Bold all key numbers and metrics. Keep paragraphs under 3 sentences. If presenting data, use Markdown tables."

### Phase 3: Workflow Orchestration (`app/core/workflow.py`)
1. Update the Magentic workflow to accept the `input_mode` and `csv_file_path` as initial inputs.
2. Ensure the workflow passes the `Analyst`'s CSV summary to the `Writer` as context, rather than the raw CSV.

### Phase 4: User Interface (`ui/streamlit_app.py`)
*Recommendation: Use **Streamlit** for the MVP as it integrates perfectly with Python backends and renders Markdown beautifully out-of-the-box.*

**UI Layout Requirements:**
1. **Sidebar / Top Bar:** 
   * A `st.radio` or `st.toggle` for "Input Mode": `[ 📝 Text Topic ]` vs `[ 📊 CSV File ]`.
2. **Main Input Area:**
   * If Text: `st.text_area` for the topic.
   * If CSV: `st.file_uploader` (accepts `.csv`). Save uploaded file to `data/raw/`.
3. **Execution Button:** "Generate Research Report".
4. **Loading State:** Use `st.status` or `st.spinner` to show agent progress (e.g., "Orchestrator routing...", "Analyst reading CSV...", "Writer formatting...").
5. **Output Area:** 
   * Use `st.markdown()` to render the Writer's output. Streamlit automatically handles the H2, H3, bolding, and tables, fulfilling the "best readable UI" requirement.

## 3. Definition of Done (MVP)
The MVP is complete when:
- [ ] A user can select "Text" and get a well-formatted web-researched report.
- [ ] A user can select "CSV", upload a file, and get a report analyzing that specific data.
- [ ] The Orchestrator successfully routes the workflow based on the toggle selection without crashing.
- [ ] The final output renders with clear headers, bullet points, and bold text in the UI (no walls of text).
- [ ] The system gracefully handles errors (e.g., uploading a non-CSV file, uploading an empty CSV).
