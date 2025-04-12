# 💡 BLISS: Business Language Interface for Self-Serve SQL

BLISS is a proof-of-concept tool that enables business users to ask natural language questions and get instant SQL queries using both rule-based and LLM (Large Language Model) logic.

---

## ✅ Features Completed

### 🔧 Backend
- Modular FastAPI backend
- Metadata loaders for ERD (YAML), business glossary (CSV), and optional schema metadata
- Rule-based SQL generator using ERD context
- LLM SQL generator using contextual prompts (via Ollama/Mistral)
- Unified controller to orchestrate both engines
- Matching glossary terms logic

### 🧑‍💻 Frontend (Streamlit)
- Clean two-pane layout: user input + SQL outputs
- Toggles for:
  - Multi-line input (removed for simplicity)
  - Show matched business terms
  - Show full glossary
- Matched terms displayed based on question
- Glossary rendered as table in UI

---

## 🛍️ Next Steps

### ↺ SQL Execution Layer
- Add SQL execution support using DuckDB or SQLite
- Parse SQL using `sqlglot` for validation + dialect normalization
- Enable query result display (via `st.dataframe`)
- Add chart rendering:
  - Support for bar, line, pie charts
  - Use inferred or selected metrics/dimensions
- Add CSV export:
  - Download button for query results

---

## 📦 Folder Structure

```
📁 backend/
    ├── main.py
    ├── controller.py
    ├── rule_engine.py
    ├── llm_adapter.py
    ├── metadata_loader.py
    └── requirements.txt

📁 frontend/
    └── streamlit_app.py

📁 metadata/
    ├── erd.yaml
    ├── glossary.csv
    └── schema_metadata.yaml (optional)
```

---

## 🚀 How to Run

### Backend
```bash
cd backend
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
streamlit run streamlit_app.py
```

---

## 🧠 LLM Used
- Model: `mistral` (local via [Ollama](https://ollama.com))
- Prompt includes ERD, glossary, schema metadata
- Can be extended to use OpenAI, Claude, etc.

---

## 🏑 Vision

Empower non-technical users to explore data by:
- Asking questions in English
- Understanding how terms map to the database
- Validating and visualizing results
- Creating a bridge between natural language and SQL fluency


