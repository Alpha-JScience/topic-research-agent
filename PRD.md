# 📄 Product Requirements Document (PRD) - Version 2

## 1. Overview
**Product:** Topic Research Agent v2
**Objective:** Evolve the agent from a purely web-search-based text generator into a hybrid research tool that can ingest, analyze, and synthesize both live web data and user-provided structured data (CSV), delivered through a highly readable, modern UI.

## 2. Problem Statement
In V1, the agent could only research topics via web search. Users could not incorporate their own proprietary datasets, financial reports, or survey data into the research. Furthermore, the text output was dense and lacked visual hierarchy, making it hard to read.

## 3. Key Features (V2)
1. **Dual-Input Toggle:** A UI toggle allowing users to choose between "Free Text Topic" (Web Search) or "Data File Analysis" (CSV Upload).
2. **CSV Data Ingestion & Analysis:** The `Analyst` agent can parse CSVs, extract key statistics, and identify trends.
3. **Smart Orchestration:** The `Orchestrator` agent dynamically routes tasks based on the input type (e.g., if CSV is uploaded, it prioritizes the `Analyst` over the `Researcher`).
4. **Enhanced Readable UI Output:** The `Writer` agent formats the final output using strict Markdown guidelines (headers, bullet points, bold text, tables) for maximum readability.

## 4. User Stories
* **As a user**, I want to toggle between typing a topic and uploading a CSV, so I can use the tool for both general research and specific data analysis.
* **As a user**, I want the system to analyze my CSV file and combine it with web context, so I can get a comprehensive report.
* **As a user**, I want the final report to use clear headings, bullet points, and bold text, so I can skim and understand the insights quickly without reading walls of text.

## 5. UI/UX Requirements (The "Easy Readable" Output)
To achieve the "best user interface output", the `Writer` agent must be prompted to output strictly formatted Markdown. The UI must render this beautifully.
* **Visual Hierarchy:** Use `H2` and `H3` headers to break down sections.
* **Scannability:** Use bullet points for lists. Never use paragraphs longer than 3-4 sentences.
* **Data Highlighting:** Use **bold text** for key metrics, numbers, and conclusions.
* **Tabular Data:** If the CSV contains structured data, the Writer must output Markdown tables.
* **UI Elements:** The frontend should render Markdown natively, support code blocks if necessary, and show a loading state (e.g., "🔍 Researching web...", "📊 Analyzing CSV...").
