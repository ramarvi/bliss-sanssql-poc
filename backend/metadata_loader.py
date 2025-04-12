# 📄 metadata_loader.py
# Loads ERD, schema metadata, and business glossary from the /metadata folder.

import os
import yaml
import csv

# Define the relative path to the metadata folder (one level up from backend)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'metadata'))

def load_erd(path="erd.yaml"):
    """
    Loads the Entity Relationship Diagram (ERD) YAML file.
    Used to understand tables, primary keys, and join relationships.
    """
    full_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"ERD file not found: {full_path}")

    with open(full_path, "r") as f:
        return yaml.safe_load(f)

def load_schema_metadata(path="schema_metadata.yaml"):
    """
    Loads optional schema metadata (column-level descriptions).
    If the file is missing, fallback to an empty dictionary.
    """
    full_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(full_path):
        print(f"⚠️  Schema metadata file not found at {full_path}. Proceeding with empty metadata.")
        return {}

    with open(full_path, "r") as f:
        return yaml.safe_load(f)

def load_glossary(path="glossary.csv"):
    """
    Loads the business glossary from CSV.
    Returns a dictionary keyed by business term for easy lookups.
    Includes synonyms for mapping natural language queries to schema terms.
    """
    full_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Glossary file not found: {full_path}")

    glossary = {}
    with open(full_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Ensure required fields exist
            if all(k in row for k in ["term", "description", "table", "column"]):
                term = row["term"].strip().lower()
                glossary[term] = {
                    "term": term,
                    "description": row["description"].strip(),
                    "table": row["table"].strip(),
                    "column": row["column"].strip(),
                    "synonyms": [s.strip().lower() for s in row.get("synonyms", "").split(",") if s.strip()]
                }
    return glossary
