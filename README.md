
# 📈 BLISS Analytics

Business Language Interface for Self-Serve Analytics

A proof-of-concept (PoC) tool that lets business users ask questions in plain English and instantly get SQL queries and results — powered by an LLM and a lightweight rule engine.

---

## ✅ What This Does

- Translates natural language questions into SQL using:
  - 🤖 A local LLM (Mistral via Ollama)
  - 🧠 A lightweight rule-based SQL generator
- Grounded in structured metadata:
  - ERD (YAML format)
  - Business glossary (CSV with table/column mapping + synonyms)
  - Optional schema metadata
- Clean, human-centered Streamlit UI:
  - Displays matched business terms
  - Allows SQL preview, editing, execution, and CSV export
- Modular backend:
  - Extensible prompt logic and metadata loaders
  - Easily replicable across domain contexts (Marketing, Finance, etc.)

---

## 📐 Design Philosophy and Guiding Principles

BLISS is built for adaptability, collaboration, and practical business value:

| Principle | Description |
|:---------|:------------|
| 📦 Modular | Swappable layers (LLM, rule engine, glossary, UI, DB) |
| 🪶 Lightweight | Local LLMs, no heavy infra or vendor lock-in |
| 📊 Metadata-First | Glossary and ERD drive the engine |
| 🔁 Feedback-Driven | Designed to evolve via user input |
| 🔐 Separation of Concerns | Enables parallel development by different teams |
| 🧩 Extensible | Works across domains by swapping ERD + glossary |

These principles support incremental adoption, low cost, collaborative workflows, and long-term maintainability.

---

## 🧱 Architecture Overview

| Layer                | Status | Highlights |
|---------------------|--------|------------|
| Metadata Loader     | ✅     | Loads YAML + CSV metadata cleanly |
| LLM Prompt Adapter  | ✅     | Structured prompt creation with glossary/ERD |
| Rule Engine         | ✅     | ERD-based keyword matching for basic SQL |
| Controller          | ✅     | Routes question through both engines |
| SQL Execution       | ✅     | DuckDB backend wired and validated |
| Output Visualization| 🔲     | Charting & CSV download polishing planned |
| UI (Streamlit)      | ✅     | Clean UX with SQL editing, matching terms, and execution |

### 🗺️ System Flow

```
User → Streamlit Frontend → FastAPI Backend → 
[LLM Adapter / Rule Engine] →
SQL Validator (sqlglot) →
DuckDB →
Results (Preview, CSV Export)
```

---

## 🛠️ Roadmap

### 🎯 Short-Term Goals

| Area     | Status | Goal |
|----------|--------|------|
| Backend  | ✅     | Run SQL on DuckDB backend |
| Backend  | ✅     | Add SQL validation & formatting (via sqlglot) |
| Frontend | ✅     | Display tabular results from backend |
| Frontend | ✅     | Show matched glossary terms in UI |
| Frontend | ✅     | Add glossary toggle (full glossary + inline) |
| Frontend | 🔲     | Add feedback loop (flag incorrect SQL) |

### 📊 Output Features (Planned)

| Feature         | Benefit |
|----------------|---------|
| 📈 Visual Charts | Plot results for quick insights |
| 📁 CSV Download (Polish) | Export results cleanly with query context |
| 🧠 Term Tracing | Map glossary terms → SQL columns automatically |

---

## ☁️ Cloud & Production Readiness (Optional)

This PoC is modular by design and can scale to production with minimal friction:

| Area              | Goal / Adaptation                                                                 |
|-------------------|-----------------------------------------------------------------------------------|
| 📦 Warehouse Support | Plug into Redshift, BigQuery, or Snowflake via connector module |
| 🔐 User Access     | Integrate company SSO to restrict query access or database schemas |
| 🧩 Metric Layer    | Optional DBT/semantic layer integration for reusable metrics |
| 🧠 Fine-Tuning     | Store feedback for prompt improvement or small LLM tuning |
| 🧪 Evaluation Tools | Add observability: matched terms, SQL validity, latency tracking |

---

## 📁 File Structure

```
bliss-sanssql-poc/
│
├── backend/
│   ├── main.py              # FastAPI app
│   ├── controller.py        # Orchestrates LLM + rule engine
│   ├── llm_adapter.py       # Formats prompt, calls LLM
│   ├── rule_engine.py       # Basic SQL generation from ERD
│   ├── metadata_loader.py   # Loads ERD, glossary, metadata
│   ├── run_sql.py           # Executes SQL via DuckDB
│   ├── sql_validator.py     # Validate & format SQL (via sqlglot)
│
├── metadata/
│   ├── erd.yaml             # Tables, columns, joins
│   ├── glossary.csv         # Business terms → table.column
│   └── schema_metadata.yaml # (Optional) Column descriptions
│
├── frontend/
│   └── streamlit_app.py     # Streamlit UI
│
├── data/
│   ├── dim_campaign.csv
│   ├── dim_customer.csv
│   ├── fact_message_event.csv
│   └── marketing.db         # DuckDB database
```

---

## 🚀 Getting Started

```bash
# 1. Start backend
cd backend
uvicorn main:app --reload

# 2. Run frontend
cd ../frontend
streamlit run streamlit_app.py
```

🔔 Note:  
- Ensure Ollama is running for local LLM inference.  
- Install DuckDB, sqlglot, and other requirements (`pip install -r requirements.txt`).

---

## 🙌 Credits & Notes

- Built by Ram with ChatGPT as a thinking and engineering partner 💬
- Mistral runs locally via Ollama for fast LLM inference
- Designed for modularity, cost-efficiency, and scalability
- A template for vertical-specific, business-friendly, self-serve analytics products

---

## ✅ Status: Working Prototype

- Functional for:
  - Generating SQL from natural language
  - Validating and formatting SQL
  - Executing queries on DuckDB
  - Previewing results
  - Exporting as CSV (basic)
- Coming Next:
  - Visualization of results
  - Feedback and explainability improvements
  - Light productionization options 🚀
