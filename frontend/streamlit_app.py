# streamlit_app.py

import streamlit as st
import requests
import pandas as pd
import os
import sys
import plotly.express as px

# Add backend folder to path to load glossary
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from metadata_loader import load_glossary

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(
    page_title="BLISS – Self-Serve SQL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# Title and Intro
# ----------------------------
st.title("📊 BLISS – Business Language Interface for Self-Serve SQL")
st.caption("Ask business questions in plain English. Get SQL instantly, validate, visualize, and export.")
st.divider()

# ----------------------------
# Initialize Session State
# ----------------------------
if "query_results" not in st.session_state:
    st.session_state.query_results = None
    st.session_state.query_columns = None
    st.session_state.llm_sql = None
    st.session_state.original_question = None

# ----------------------------
# Business Question Input
# ----------------------------
st.subheader("Enter your business question")
question = st.text_input(
    label="Business Question",
    value="",
    label_visibility="collapsed",
    placeholder="e.g. Show top campaigns by open rate last month"
)

if not question.strip():
    st.info("👆 Please type a business question above to get started.")

# ----------------------------
# Load glossary
# ----------------------------
glossary = load_glossary()

# ----------------------------
# SQL Generation (when user presses Enter after typing question)
# ----------------------------
if question.strip() and not st.session_state.llm_sql:
    try:
        response = requests.post(
            "http://localhost:8000/generate_sql",
            json={"question": question}
        )
        data = response.json()

        st.session_state.llm_sql = data.get("llm_sql", "")
        st.session_state.original_question = question

    except Exception as e:
        st.error(f"🚨 Error contacting backend: {e}")

# ----------------------------
# Render Generated SQL + Editable Box + Run Query Button
# ----------------------------
if st.session_state.llm_sql:
    st.divider()
    st.markdown("#### 🧠 LLM-Generated SQL")
    st.code(st.session_state.llm_sql, language="sql")

    with st.expander("✍️ Edit generated SQL before running (optional)", expanded=False):
        edited_sql = st.text_area(
            "Edit SQL if needed:",
            value=st.session_state.llm_sql,
            height=200,
            label_visibility="collapsed"
        )
    # Otherwise fallback
    if "edited_sql" not in st.session_state:
        st.session_state.edited_sql = st.session_state.llm_sql

    # Run Query button
    if st.button("🚀 Run Query"):
        try:
            run_response = requests.post(
                "http://localhost:8000/run_sql",
                json={"sql_query": edited_sql}
            )
            run_data = run_response.json()

            if "error" in run_data:
                st.error(f"🚨 Error executing SQL: {run_data['error']}")
            else:
                st.session_state.query_results = run_data.get("rows", [])
                st.session_state.query_columns = run_data.get("columns", [])

        except Exception as e:
            st.error(f"🚨 Error contacting backend: {e}")

# ----------------------------
# Render Results if Available
# ----------------------------
if st.session_state.query_results and st.session_state.query_columns:
    st.divider()

    df = pd.DataFrame(st.session_state.query_results, columns=st.session_state.query_columns)
    st.dataframe(df, use_container_width=True)

    # Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📁 Download Results as CSV",
        data=csv,
        file_name="query_results.csv",
        mime="text/csv"
    )

    # Optional: Visualize
    with st.expander("📊 Visualize Results (optional)", expanded=False):
        x_axis = st.selectbox("X-Axis", options=df.columns)
        y_axis = st.selectbox("Y-Axis", options=df.columns)
        chart_type = st.selectbox("Chart Type", options=["Bar", "Line", "Scatter"])

        if st.button("📈 Plot Chart"):
            if chart_type == "Bar":
                fig = px.bar(df, x=x_axis, y=y_axis)
            elif chart_type == "Line":
                fig = px.line(df, x=x_axis, y=y_axis)
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_axis, y=y_axis)

            st.plotly_chart(fig, use_container_width=True)

    # Divider
    st.divider()

    # Provide Feedback
    with st.expander("💬 Provide Feedback", expanded=False):
        additional_feedback = st.text_area("Leave additional comments (optional):", "")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Thumbs Up"):
                try:
                    requests.post(
                        "http://localhost:8000/submit_feedback",
                        json={
                            "question": st.session_state.original_question,
                            "generated_sql": st.session_state.llm_sql,
                            "feedback": additional_feedback,
                            "thumbs": "up"
                        }
                    )
                    st.success("✅ Thank you! Your feedback has been recorded.")
                except Exception as e:
                    st.error(f"🚨 Error submitting feedback: {e}")

        with col2:
            if st.button("👎 Thumbs Down"):
                try:
                    requests.post(
                        "http://localhost:8000/submit_feedback",
                        json={
                            "question": st.session_state.original_question,
                            "generated_sql": st.session_state.llm_sql,
                            "feedback": additional_feedback,
                            "thumbs": "down"
                        }
                    )
                    st.success("✅ Thank you! Your feedback has been recorded.")
                except Exception as e:
                    st.error(f"🚨 Error submitting feedback: {e}")

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
