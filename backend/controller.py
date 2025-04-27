# 📦 controller.py
# Orchestrates SQL generation + validation

from metadata_loader import load_erd, load_glossary, load_schema_metadata
from rule_engine import rule_based_sql
from llm_adapter import generate_sql_with_llm
from sql_validator import validate_and_format_sql  # 🆕 Import validator

# 📦 Load metadata at startup (shared across requests)
erd = load_erd()
glossary = load_glossary()
schema_metadata = load_schema_metadata()

def extract_matched_terms(question: str, glossary: dict) -> list:
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
    Main orchestration function:
    - Generate SQL using rule engine + LLM
    - Validate + format LLM SQL
    - Detect matched business terms
    """
    rule_sql = rule_based_sql(question, erd)

    # LLM SQL generation
    llm_sql_raw = generate_sql_with_llm(question, erd, glossary, schema_metadata)

    # Validate and format LLM SQL
    validation_result = validate_and_format_sql(llm_sql_raw)

    if validation_result["success"]:
        final_llm_sql = validation_result["formatted_sql"]
        validation_status = "Validated ✅"
    else:
        final_llm_sql = llm_sql_raw
        validation_status = f"Validation Failed ⚠️: {validation_result['error']}"

    matched_terms = extract_matched_terms(question, glossary)

    return {
        "rule_based_sql": rule_sql,
        "llm_sql": final_llm_sql,
        "matched_terms": matched_terms,
        "validation_status": validation_status
    }
