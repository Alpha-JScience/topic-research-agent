MVP Implementation Specification

### 1. MVP Scope

**Goal:** Build and deploy a working web app within 3–5 days that demonstrates the core hypothesis: users will actively use multiple output formats and depth levels on a single topic.

**MVP Hypothesis:** Users will select at least 2 output formats and at least 1 non-default depth level per topic session.

**What is IN the MVP:**
- Topic input with IT/General classification
- All 8 output format options (toggleable)
- All 6 depth levels (toggleable)
- DeepSeek API integration with OpenAI SDK
- CSV-based topic database with reload
- Light-mode Streamlit UI
- Deployed on Alibaba Cloud (Function Compute)
- `.secret.toml` configuration

**What is OUT of the MVP:**
- User accounts, saved history, sharing
- OpenAI fallback (deferred to post-MVP)
- Free alternative APIs (deferred)
- Streaming output
- Mobile-responsive design beyond Streamlit defaults

### 2. Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Alibaba Cloud (Function Compute)          │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                   Python Web App                       │   │
│  │  ┌─────────┐    ┌──────────┐    ┌──────────────────┐ │   │
│  │  │ ui.py   │───▶│ app.py   │───▶│  LLM Client      │ │   │
│  │  │Streamlit│    │ Router   │    │  (OpenAI SDK)    │ │   │
│  │  │(light)  │◀───│ + CSV    │◀───│  DeepSeek        │ │   │
│  │  └─────────┘    │ Loader   │    │  api.deepseek.com│ │   │
│  │                 └──────────┘    └──────────────────┘ │   │
│  │                        │                               │   │
│  │                   ┌────▼────┐                          │   │
│  │                   │topics   │                          │   │
│  │                   │.csv     │                          │   │
│  │                   └─────────┘                          │   │
│  └───────────────────────────────────────────────────────┘   │
│  HTTP Trigger → Public URL                                  │
└─────────────────────────────────────────────────────────────┘
```

### 4. Module Specifications

#### 4.1 `app.py` — Core Logic

**Responsibilities:**
- Load `.toml` and environment variables
- Initialize OpenAI client pointed at DeepSeek base URL
- Load and parse `topics.csv`
- Classify topic into IT/General domain
- Construct system prompt based on format + depth + domain
- Call LLM API
- Return structured response

**Key functions:**

```python
def load_config() -> dict:
    """Load .secret.toml with env var override precedence."""

def load_topics_csv(path: str = "topics.csv") -> pd.DataFrame:
    """Load and validate the topic-subject database."""

def classify_topic(topic: str, topics_df: pd.DataFrame) -> str:
    """Return 'IT/AI' or 'General' via keyword match, fallback to LLM."""

def build_system_prompt(domain: str, formats: list[str], depth: str) -> str:
    """Construct the system prompt with format and depth instructions."""

def call_llm(system_prompt: str, user_topic: str) -> str:
    """Call DeepSeek API via OpenAI SDK, handle errors and retries."""
```

**System prompt template (critical):**

```
You are a Topic Research Agent specialized in {domain} topics.

DEPTH LEVEL: {depth}
{format_instructions}

RULES:
- For IT/AI topics: use precise technical terminology, reference 
  real tools/frameworks, and ensure quiz questions test conceptual 
  understanding not trivia.
- For General topics: use accessible language, real-world analogies, 
  and avoid unexplained jargon.
- If uncertain about a fact, state "According to current understanding..." 
  rather than presenting speculation as fact.
- For MCQ quizzes: provide exactly 4 options (A-D), mark the correct 
  answer, and include a one-sentence rationale.
- For fact tables: use Markdown table syntax with clear column headers.
```

#### 4.2 `ui.py` — Streamlit Interface (Light Mode)

**Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  🔬 Topic Research Agent                                    │
│  Instant research in your format, at your depth.            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📝 Enter a topic:                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ [e.g., "Transformer attention mechanism"]            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  🏷️ Subject (auto-detected):  [IT/AI] [General] [Override] │
│                                                              │
│  📊 Output Format (select all that apply):                   │
│  ☐ Paragraph  ☐ Bullet  ☐ Fact Table  ☐ Quick Summary      │
│  ☐ Practical Example  ☐ Quiz MCQ-4  ☐ Q&A                  │
│  ☐ Default (General)                                        │
│                                                              │
│  🔍 Depth Level:                                             │
│  ○ General (default)  ○ Medium  ○ Detailing                 │
│  ○ Conceptual  ○ Theoretical  ○ Paragraphical              │
│                                                              │
│  ┌──────────────────────┐                                   │
│  │   🚀 Generate        │                                   │
│  └──────────────────────┘                                   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  📄 Results                                                  │
│  [Rendered output sections with format-specific styling]     │
└─────────────────────────────────────────────────────────────┘
```


#### 4.3 `topics.csv` — Subject Database

**Initial content (seed with ~50 topics):**

```csv
topic_keyword,subject_category,prompt_prefix,example_hints
transformer,IT/AI,"Focus on attention mechanism, self-attention, and positional encoding","BERT, GPT, ViT"
neural network,IT/AI,"Focus on layer types, activation functions, and backpropagation","CNN, RNN, MLP"
docker,IT/AI,"Focus on containerization, images, and orchestration","Kubernetes, Compose"
api,IT/AI,"Focus on REST, endpoints, authentication, and versioning","REST, GraphQL, gRPC"
sorting algorithm,IT/AI,"Focus on time complexity, stability, and use cases","QuickSort, MergeSort"
photosynthesis,General,"Focus on light-dependent and light-independent reactions","chlorophyll, Calvin cycle"
French Revolution,General,"Focus on causes, key events, and lasting impact","Bastille, Napoleon"
supply chain,General,"Focus on logistics, inventory, and resilience","bullwhip effect, JIT"
cognitive bias,General,"Focus on heuristics, decision-making, and examples","confirmation bias, anchoring"
```

### 5. Verification Checklist

| # | Test | Expected Result |
|---|---|---|
| 1 | Enter "transformer attention" with IT/AI auto-detect | Classification badge shows "IT/AI" |
| 2 | Select only "Quiz MCQ-4" and "General" depth | Output contains 4 MCQs with answers |
| 3 | Select "Fact Table" + "Practical Example" | Markdown table renders + example paragraph |
| 4 | Enter "photosynthesis" | Classification shows "General" |
| 5 | Reload topics.csv with new keyword | New keyword affects classification |
| 6 | Remove API key from `..toml` | Graceful error message, no crash |
| 7 | Deploy to Function Compute | Public URL loads Streamlit UI |
| 8 | Measure response time | DeepSeek flash returns < 15s |