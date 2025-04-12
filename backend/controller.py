# 📦 controller.py
# This file orchestrates the core backend logic by routing incoming natural language questions
# through both a rule-based SQL generator and an LLM-based generator using ERD and schema context.

from metadata_loader import load_erd, load_glossary, load_schema_metadata
from rule_engine import rule_based_sql
from llm_adapter import generate_sql_with_llm

# 📦 Load metadata at startup (shared across requests)
erd = load_erd()
glossary = load_glossary()
schema_metadata = load_schema_metadata()


def extract_matched_terms(question: str, glossary: dict) -> list:
    """
    Identify which glossary terms or synonyms were mentioned in the user's question.
    Returns a list of matched terms for highlighting or UI display.
    """
    matched = set()
    q_lower = question.lower()

    for entry in glossary.values():
        term = entry["term"].lower()
        synonyms = [s.lower() for s in entry.get("synonyms", [])]

        if term in q_lower or any(s in q_lower for s in synonyms):
            matched.add(entry["term"])

    return sorted(matched)


def generate_sql_response(question: str) -> dict:
    """
    Main orchestration function to generate SQL queries from a user's natural language question.
    It uses both rule-based logic and LLM-based generation.
    """
    # 🧠 Step 1: Try rule-based SQL generation
    rule_sql = rule_based_sql(question, erd)

    # 🤖 Step 2: Use LLM with ERD + glossary context
    llm_sql = generate_sql_with_llm(question, erd, glossary, schema_metadata)

    # 🧩 Step 3: Detect glossary terms that match
    matched_terms = extract_matched_terms(question, glossary)

    # 📤 Return all results
    return {
        "rule_based_sql": rule_sql,
        "llm_sql": llm_sql,
        "matched_terms": matched_terms
    }
