Product Requirements Document (PRD)

### 1. Product Overview

**Product Name:** Topic Research Agent

**Tagline:** Instant, multi-format research briefs on any topic — from AI to Art History.

**One-Sentence Positioning:** A Python web application that lets users input any topic and receive structured research outputs in the format and depth they choose, powered by DeepSeek or free LLM APIs.

**Problem Statement:** Learners, students, and professionals waste time manually gathering and formatting research on unfamiliar topics. Existing tools (Google, ChatGPT) produce unstructured walls of text that require further processing to be useful — converting prose to bullet points, extracting key facts, creating practice questions, or finding practical examples. There is no lightweight tool that lets a user say "give me this topic as a fact table" or "quiz me on this" in one click.

**Hypothesis (falsifiable):** If we provide a one-click way to generate topic research in seven distinct output formats at three depth levels, users will use at least two different formats per topic on average, indicating that format flexibility is a core value driver.

### 2. Target Users

| User Segment | Primary Need | Example Scenario |
|---|---|---|
| IT/AI/Software Engineering students | Understand technical concepts deeply, test knowledge | "Explain transformer attention as a fact table, then quiz me with 4 MCQs" |
| General learners (non-IT) | Quick, digestible summaries of unfamiliar topics | "Give me a practical example of supply chain resilience" |
| Educators | Generate teaching materials from topics | "Create a quick summary + 2 MCQs on photosynthesis for my class" |
| Self-directed professionals | Upskill efficiently on new domains | "Detailing-level bullet points on Kubernetes networking" |

### 3. Feature Requirements

#### 3.1 Core Features (MVP)

**F1 — Topic Input & Subject Classification**

User enters a free-text topic. The system classifies it into one of two subject domains:

- **Option 1 (IT/AI/Software Engineering):** Topics related to programming, AI, machine learning, software architecture, data structures, cloud computing, cybersecurity, etc. The agent applies a "technical lens" — precise terminology, code-adjacent examples, and engineering-focused quizzes.
- **Option 2 (General):** Everything else — history, biology, business, arts, philosophy, etc. The agent uses accessible language and real-world analogies.

Classification is performed via a lightweight keyword-matching layer against the CSV subject database, with an LLM fallback for ambiguous topics. The classification result is displayed to the user (with an override toggle).

**F2 — Output Format Toggle (Multiple Choice)**

User selects one or more output formats. Each selected format produces a distinct section in the response:

| Format | Description | Output Type |
|---|---|---|
| Paragraph | Standard prose explanation | Text |
| Bullet | Key points as a bulleted list | Text |
| Concise Fact Table | Structured table with columns like Concept, Definition, Significance | Markdown table |
| Quick Summary | 3–5 sentence TL;DR | Text |
| Practical Relevant Example | Real-world or domain-specific illustration | Text |
| Quiz MCQ-4 | Four multiple-choice questions with 4 options each | Structured Q&A |
| Question with Answer | Short-answer Q&A pairs | Structured Q&A |
| Default (General) | Balanced paragraph + bullets + one example | Mixed |

**F3 — Discussion Depth Level Toggle (Multiple Choice)**

User selects a depth level:

| Level | Description | Target Length |
|---|---|---|
| General (Default) | Balanced, accessible overview | 200–400 words |
| Medium | Standard educational depth | 400–700 words |
| Detailing | Comprehensive with subtopics | 700–1200 words |
| Conceptual | Focus on "why" and mental models | 300–600 words |
| Theoretical | Formal definitions, axioms, frameworks | 500–900 words |
| Paragraphical | Flowing narrative form | 300–500 words |

**F4 — Free LLM Provider Integration**

- **Primary:** DeepSeek API (OpenAI-compatible). Model IDs: `deepseek-flash` or `deepseek-v4-pro`. Base URL: `https://api.deepseek.com`. 
- **Fallback:** OpenAI API key (optional, configured in secrets).
- **Free alternatives (optional layer):** OpenRouter free models (`:free` suffix, 20 RPM / 50 RPD), OVHcloud anonymous tier (no key needed, 2 RPM), or Ollama cloud. 

The system reads configuration from `.toml` (base_url, api_key) and supports environment variable overrides.

**F5 — Topic Subject Database (CSV)**

A reloadable CSV file (`topics.csv`) containing topic-subject mappings used for classification and prompt tailoring. Schema:

```
topic_keyword,subject_category,prompt_prefix,example_hints
transformer,IT/AI,"Focus on architecture, attention mechanism","BERT, GPT"
photosynthesis,General,"Focus on biological process","plants, chlorophyll"
```

The CSV is loaded at startup and can be reloaded without restarting the app.

#### 3.2 Non-Goals (Explicitly Excluded from MVP)

- User authentication or accounts
- Persistent storage of past research (session-only)
- Collaboration or sharing features
- Custom user-uploaded datasets beyond the topic CSV
- Mobile native app
- Billing or usage metering
- Multiple languages (English-only UI and output)

### 4. Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| Format diversity per session | ≥ 2.0 formats used per topic | UI event logging |
| Depth level usage spread | No single level > 60% of selections | UI event logging |
| Classification accuracy | ≥ 85% correct IT vs General | Manual spot-check of 50 topics |
| Response latency | < 15s for DeepSeek flash, non-streaming | API timing |
| App uptime (Alibaba Cloud) | ≥ 99% during demo period | Function Compute metrics |

