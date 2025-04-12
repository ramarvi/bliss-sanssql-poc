# rule_engine.py

"""
🔧 Rule Engine
-------------
Simple keyword-based SQL generation using ERD metadata.
This module is meant to be a fallback or helper before invoking the LLM.
"""

from typing import Dict, List
import re


# Simple rule-based fallback (not as intelligent as LLM)

def extract_relevant_tables_and_columns(question: str, erd: dict) -> list:
    """
    Try to find relevant tables/columns based on keywords in the question.
    """
    matches = []
    lowered = question.lower()

    for table, props in erd.items():
        for col in props.get("columns", []):
            if col.lower() in lowered or table.lower() in lowered:
                matches.append((table, col))

    return matches

def rule_based_sql(question: str, erd: dict) -> str:
    """
    Generate naive SQL using pattern-based inference from ERD.
    """
    matches = extract_relevant_tables_and_columns(question, erd)

    if not matches:
        return "-- No rule-based SQL generated"

    # Use first match for fallback demo
    table = matches[0][0]
    where_clauses = [f"{col} IS NOT NULL" for _, col in matches]
    where_clause = " AND ".join(where_clauses)

    return f"SELECT * FROM {table} WHERE {where_clause};"
