# llm_adapter.py

import os
import requests
from metadata_loader import load_erd, load_glossary, load_schema_metadata

# Load metadata for prompt generation
erd = load_erd()
glossary = load_glossary()
schema_metadata = load_schema_metadata()

def format_prompt(question, erd, glossary, schema_metadata):
    """
    Formats a system prompt for the LLM using ERD, glossary, and schema metadata.
    Helps the model generate more accurate and relevant SQL queries.
    """

    # 🧱 ERD (Entity Relationship Diagram) context
    erd_lines = []
    for table, details in erd.items():
        pk = details.get("primary_key", "unknown")
        cols = ", ".join(details.get("columns", []))
        erd_lines.append(f"- {table} (PK: {pk}): {cols}")

        # Handle joins if available
        joins = details.get("joins", [])
        for join in joins:
            table_name = join.get("table")
            join_key = join.get("on")
            if table_name and join_key:
                erd_lines.append(f"  ↪ joins with {table_name} on {join_key}")

    erd_context = "\n".join(erd_lines)

    # 📖 Glossary context with synonyms
    glossary_lines = []
    for entry in glossary.values():
        synonyms = f"(synonyms: {', '.join(entry['synonyms'])})" if entry.get("synonyms") else ""
        glossary_lines.append(
            f"- {entry['term']} → {entry['table']}.{entry['column']} {synonyms} — {entry['description']}"
        )
    glossary_context = "\n".join(glossary_lines)

    # 🧠 Schema Metadata context (optional)
    schema_lines = []
    if schema_metadata:
        for table, columns in schema_metadata.items():
            for col, desc in columns.items():
                schema_lines.append(f"- {table}.{col}: {desc}")
    schema_context = "\n".join(schema_lines) if schema_lines else "No additional schema metadata available."

    # 🧪 Compose the final prompt
    prompt = f"""
You are a precise and reliable assistant that translates business questions into SQL queries.
    
## Database Schema (ERD)
{erd_context}

## Business Glossary
Use this glossary to map business terms in the question to the appropriate tables or columns:
{glossary_context}

## Column Metadata
Each table and its columns with data types:
{schema_context}

## Rules:
- Only use the tables and columns that exist in the provided schema.
- If terms in the user question match glossary definitions or column names, use them confidently.
- Use proper SQL syntax and aliases for clarity.
- Prefer INNER JOINs unless otherwise implied.
- Do not explain the query. Only return the SQL code.

### User Question:
{question}

### SQL Query:
"""

    return prompt.strip()


def clean_sql_output(sql: str) -> str:
    """
    Cleans up LLM-generated SQL to remove problematic characters.
    """
    return sql.strip().replace("`", "").replace("'", "")


def generate_sql_with_llm(question, erd, glossary, schema_metadata={}):
    """
    Calls the local Mistral LLM using the formatted prompt to generate SQL.
    """
    prompt = format_prompt(question, erd, glossary, schema_metadata)

    # 🧪 Local LLM (Mistral) Inference via Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        raw_sql = response.json().get("response", "").strip()
        return clean_sql_output(raw_sql)
    else:
        return f"-- ERROR: LLM call failed ({response.status_code})"
