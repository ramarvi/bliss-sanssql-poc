# streamlit_app.py

import streamlit as st
import requests
import pandas as pd
import sys
import os

# Add backend folder to the path for loading glossary
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from metadata_loader import load_glossary

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(page_title="BLISS – Self-Serve SQL", layout="wide")
st.markdown("## 🌟 BLISS – Business Language Interface for Self-Serve SQL")
st.markdown("Ask business questions in plain English. Get SQL instantly from both the LLM and the rule engine.")
st.markdown("---")

# ----------------------------
# Input
# ----------------------------
question = st.text_input(
    "💬 Enter your business question:",
    placeholder="e.g. What were Q1 sales by region in 2022?"
)

# ----------------------------
# Options below input
# ----------------------------
show_matched_terms = st.checkbox("🔍 Show matched business terms", value=True)
show_full_glossary = st.checkbox("📘 Show full business glossary", value=False)
show_dev = st.checkbox("🧪 Show rule-based SQL", value=False)

# ----------------------------
# Load glossary
# ----------------------------
glossary = load_glossary()

# ----------------------------
# Submit to backend
# ----------------------------
if question.strip():
    try:
        response = requests.post(
            "http://localhost:8000/generate_sql",
            json={"question": question}
        )
        data = response.json()

        st.markdown("#### 🧠 LLM-Generated SQL")
        st.code(data.get("llm_sql", ""), language="sql")

        if show_dev:
            st.markdown("#### 📘 Rule-Based SQL")
            st.code(data.get("rule_based_sql", ""), language="sql")

        # Matched terms display
        if show_matched_terms:
            matched_terms = data.get("matched_terms", [])
            if matched_terms:
                st.markdown("#### 🧩 Matched Business Terms")
                st.markdown(", ".join(matched_terms))
            else:
                st.info("⚠️ No matched business terms were detected.")

    except Exception as e:
        st.error(f"🚨 Error contacting backend: {e}")

# ----------------------------
# Glossary Table
# ----------------------------
if show_full_glossary and glossary:
    st.markdown("---")
    st.markdown("### 📘 Full Business Glossary")

    full_df = pd.DataFrame([
        {
            "Term": entry["term"],
            "Table": entry["table"],
            "Column": entry["column"],
            "Description": entry["description"],
            "Synonyms": ", ".join(entry["synonyms"]) if entry.get("synonyms") else "—"
        }
        for entry in glossary.values()
    ])

    st.dataframe(full_df, use_container_width=True)
