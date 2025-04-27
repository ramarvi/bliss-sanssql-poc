# streamlit_app.py

import streamlit as st
import requests
import pandas as pd
import sys
import os

# Add backend folder to path to load glossary
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from metadata_loader import load_glossary

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(
    page_title="BLISS – Self-Serve SQL",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar collapsed by default
)

# ----------------------------
# Title and Intro
# ----------------------------
st.title("🌟 BLISS – Business Language Interface for Self-Serve SQL")
st.caption("Ask business questions in plain English. Get SQL instantly, validate, visualize, and export.")
st.divider()

# ----------------------------
# Business Question Input
# ----------------------------
st.subheader("Enter your business question")
question = st.text_input(
    label="Business Question",
    value="",  # Empty by default
    label_visibility="collapsed",
    placeholder="e.g. Show top campaigns by open rate last month"
)

# ----------------------------
# Load glossary
# ----------------------------
glossary = load_glossary()

# ----------------------------
# Submit to backend if question entered
# ----------------------------
if question.strip():
    try:
        response = requests.post(
            "http://localhost:8000/generate_sql",
            json={"question": question}
        )
        data = response.json()

        llm_sql = data.get("llm_sql", "")
        matched_terms = data.get("matched_terms", [])
        rule_sql = data.get("rule_based_sql", "")

        # Divider after question
        st.divider()

        # ----------------------------
        # Generated SQL Preview
        # ----------------------------
        st.markdown("#### 🧠 LLM-Generated SQL")
        st.code(llm_sql, language="sql")

        # ----------------------------
        # Trustworthiness Panel
        # ---------------------------- 
        with st.expander("✅ Trust Summary", expanded=False):
            st.markdown(f"**Terms Matched:** {', '.join(matched_terms) if matched_terms else 'None'}")

        # ----------------------------
        # Expandable SQL Editor
        # ----------------------------
        with st.expander("✍️ Edit generated SQL before running (optional)", expanded=False):
            editable_sql = st.text_area(
                "Edit SQL below if needed:",
                value=llm_sql,
                height=200,
                label_visibility="collapsed"
            )

        # ----------------------------
        # Run Query Button
        # ----------------------------
        run_query = st.button("🚀 Run Query")
        
        if run_query and editable_sql.strip():
            try:
                run_response = requests.post(
                    "http://localhost:8000/run_sql",
                    json={"sql_query": editable_sql}
                )
                run_response.raise_for_status()
                run_data = run_response.json()

                if "error" in run_data:
                    st.error(f"🚨 Error executing SQL: {run_data['error']}")
                else:
                    # Show results
                    st.success("✅ Download Ready!")
                    df = pd.DataFrame(run_data.get("rows", []), columns=run_data.get("columns", []))
                    st.dataframe(df, use_container_width=True)

                    # CSV download button
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📁 Download Results as CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"🚨 Error contacting backend: {e}")

    except Exception as e:
        st.error(f"🚨 Error contacting backend: {e}")

else:
    st.info("👆 Please enter a business question above to get started.")

# ----------------------------
# (Optional) Sidebar - Business Glossary
# ----------------------------
with st.sidebar:
    st.header("📘 Business Glossary")
    if st.checkbox("Show full glossary", value=False):
        if glossary:
            glossary_df = pd.DataFrame([
                {
                    "Term": entry["term"],
                    "Table": entry["table"],
                    "Column": entry["column"],
                    "Description": entry["description"],
                    "Synonyms": ", ".join(entry["synonyms"]) if entry.get("synonyms") else "—"
                }
                for entry in glossary.values()
            ])
            st.dataframe(glossary_df, use_container_width=True)
