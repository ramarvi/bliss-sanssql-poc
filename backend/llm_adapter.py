# backend/llm_adapter.py

import requests
from metadata_loader import load_schema

# Load schema metadata (used to guide LLM)
schema = load_schema()

# ✅ Format the schema metadata into a string
def format_schema_for_prompt(schema: dict) -> str:
    lines = ["Here is the database schema:\n"]

    # Loop through tables
    for table_name, table_info in schema.get("tables", {}).items():
        lines.append(f"Table: {table_name}")
        for column in table_info.get("columns", []):
            col_name = column["name"]
            col_type = column["type"]
            lines.append(f"  - {col_name} ({col_type})")
        lines.append("")  # Empty line for spacing

    # Include relationships if any
    if "relationships" in schema:
        lines.append("Table Relationships:")
        for rel in schema["relationships"]:
            lines.append(
                f"  - {rel['from_table']}.{rel['from_column']} → {rel['to_table']}.{rel['to_column']}"
            )
        lines.append("")  # Empty line for spacing

    return "\n".join(lines)

# 🧠 Main LLM function: send prompt to local Mistral via Ollama
def generate_sql_with_llm(question: str) -> str:
    schema_context = format_schema_for_prompt(schema)

    prompt = f"""
You are a helpful assistant that writes SQL queries based on user questions.
Use the schema and relationships provided to inform your SQL generation.

{schema_context}

User question:
{question}

Respond with only the SQL query, no explanation.
""".strip()

    try:
        # 💬 Call local Mistral via Ollama API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()

    except requests.exceptions.RequestException as e:
        return f"-- LLM error: {e}"
