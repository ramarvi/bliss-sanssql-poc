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
You are a helpful assistant that translates natural language questions into SQL queries.

## Database Schema (ERD):
{erd_context}

## Business Glossary:
{glossary_context}

## Column Metadata:
{schema_context}

### User Question:
{question}

### SQL Query:
Write a syntactically correct SQL query using the tables and columns provided.
If a term in the question maps to glossary or schema columns, use them appropriately.
Return only the SQL code.
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
