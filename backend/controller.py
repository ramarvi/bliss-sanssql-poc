# backend/controller.py

from metadata_loader import load_glossary, load_schema
from llm_adapter import generate_sql_with_llm

# 🧠 Load glossary and schema at startup
glossary = load_glossary()
schema = load_schema()

# 🧱 Rule-based fallback logic (temporary placeholder)
def rule_based_sql(question: str, glossary: dict) -> str:
    for term in glossary:
        if term in question.lower():
            return glossary[term]["sql_expression"]
    return "-- No match found in glossary"

# 🎯 Main orchestrator for generating SQL from question
def generate_sql_response(question: str) -> dict:
    return {
        "rule_based_sql": rule_based_sql(question, glossary),
        "llm_sql": generate_sql_with_llm(question)
    }
