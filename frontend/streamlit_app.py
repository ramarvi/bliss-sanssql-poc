# streamlit_app.py

import streamlit as st
import requests

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(page_title="BLISS – Self-Serve SQL", layout="wide")

st.markdown("## 🌟 BLISS – Business Language Interface for Self-Serve SQL")
st.markdown("Ask business questions in plain English. Get SQL instantly from both the LLM and the rule engine.")

# ----------------------------
# Sidebar toggles
# ----------------------------
st.sidebar.header("⚙️ Options")
show_dev = st.sidebar.checkbox("🧪 Show rule-based SQL", value=False)
use_multiline = st.sidebar.checkbox("✍️ Enable multi-line input", value=False)

st.markdown("---")

# ----------------------------
# Question input
# ----------------------------
if use_multiline:
    question = st.text_area(
        "💬 Enter your business question below:",
        placeholder="e.g. What were Q1 sales by region in 2022?",
        height=120
    )
else:
    question = st.text_input(
        "💬 Enter your business question:",
        placeholder="e.g. What were Q1 sales by region in 2022?"
    )

# ----------------------------
# Send to backend
# ----------------------------
if question.strip():
    try:
        response = requests.post(
            "http://localhost:8000/generate_sql",
            json={"question": question}
        )
        data = response.json()

        if show_dev:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🧠 LLM-Generated SQL")
                st.code(data.get("llm_sql", ""), language="sql")
            with col2:
                st.markdown("#### 📘 Rule-Based SQL")
                st.code(data.get("rule_based_sql", ""), language="sql")
        else:
            st.markdown("#### 🧠 LLM-Generated SQL")
            st.code(data.get("llm_sql", ""), language="sql")

    except Exception as e:
        st.error(f"🚨 Error contacting backend: {e}")
else:
    st.info("👆 Type a question above to get started.")
