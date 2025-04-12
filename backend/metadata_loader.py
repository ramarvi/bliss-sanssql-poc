import csv
import yaml
import os

# 📘 Loads glossary from CSV file located in the metadata/ folder
def load_glossary(path="metadata/glossary.csv"):
    glossary = {}
    if not os.path.exists(path):
        raise FileNotFoundError(f"Glossary file not found: {path}")

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            term = row["term"].strip().lower()
            glossary[term] = {
                "sql_expression": row["sql_expression"],
                "notes": row.get("notes", "")
            }
    return glossary

# 📘 Loads ERD/schema metadata from YAML (for joins, types, structure)
def load_schema(path="metadata/erd.yaml"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Schema/ERD file not found: {path}")

    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# ✅ Convenience utility to load both
def load_metadata():
    return {
        "glossary": load_glossary(),
        "schema": load_schema()
    }
