import json
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
import altair as alt

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Midad Explorer", layout="wide")
# ==========================================
# 1. Midad brand (top of page) — Arabic, vivid green gradient, custom font
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Almarai:wght@800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@700&display=swap');
    
    .midad-brand {
        font-size: 34px !important;
        font-weight: 800 !important;
        letter-spacing: 0px !important;
        background: linear-gradient(90deg, #A8E063 0%, #56AB2F 50%, #1B5E20 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Cairo', 'Tajawal', 'Almarai', 'IBM Plex Sans Arabic', sans-serif !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
        padding: 0 !important;
        line-height: 1.6 !important;
        direction: rtl;
    }
</style>
<h1 class="midad-brand">مِداد</h1>
""", unsafe_allow_html=True)

# ==========================================
# 2. Custom CSS — moderate sizing
# ==========================================
st.markdown("""
<style>
    /* Labels */
    label, .stSelectbox label, .stTextInput label, .stNumberInput label {
        font-size: 14px !important;
        font-weight: 500 !important;
    }

    /* Inputs */
    input, .stSelectbox div[data-baseweb="select"] {
        font-size: 14px !important;
    }

    /* Main title (Midad Explorer) */
    h1 {
        font-size: 28px !important;
        margin-top: 10px !important;
        margin-bottom: 10px !important;
    }

    /* Subheader (Data Overview & Dashboard) */
    h3 {
        font-size: 20px !important;
        margin-top: 10px !important;
        margin-bottom: 10px !important;
    }

    /* Markdown paragraphs */
    .stMarkdown p {
        font-size: 14px !important;
    }

    /* Buttons */
    .stButton button {
        font-size: 14px !important;
        padding: 6px 16px !important;
    }

    /* Number input */
    .stNumberInput input {
        font-size: 14px !important;
    }

    /* Metrics */
    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 24px !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] div {
        font-size: 13px !important;
    }

    /* Reduce page padding a bit */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }

    /* Space between vertical blocks */
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.8rem !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Quality indicator ---
quality_path = Path("../data/quality_report.json")
if quality_path.exists():
    report = json.loads(quality_path.read_text())
    if report["status"] == "PASS":
        st.success(f"✅ Data Quality: PASS — last run {report['last_run']}")
    else:
        st.error(f"❌ Data Quality: FAIL — last run {report['last_run']}")
else:
    st.warning("⚠️ No quality report found")


# ==========================================
# Dashboard Brief Section
# ==========================================
st.subheader(" Data Overview & Dashboard")

# Fetch statistics from the API
try:
    stats_resp = requests.get(f"{API_BASE}/dashboard_stats", timeout=5)
    if stats_resp.status_code == 200:
        stats = stats_resp.json()

        # Quick summary metrics
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric(label="Total Records", value=stats.get("total_rows", 0))
        with col_b:
            st.metric(label="Unique Sources", value=len(stats.get("source_counts", {})))

        # Display compact Bar Charts inside an Expander
        with st.expander(" View Detailed Charts & Distribution", expanded=False):

            # First row: Sources and Content Types
            row1_col1, row1_col2 = st.columns(2)

            with row1_col1:
                st.markdown("**Content by Source**")
                if stats.get("source_counts"):
                    source_df = pd.DataFrame(
                        list(stats["source_counts"].items()),
                        columns=["Source", "Count"]
                    )
                    chart = alt.Chart(source_df).mark_bar(color="#4C78A8").encode(
                        x=alt.X("Count:Q", title="Count"),
                        y=alt.Y("Source:N", sort="-x", title=""),
                    ).properties(height=200)
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("No source data available.")

            with row1_col2:
                st.markdown("**Content by Type**")
                if stats.get("content_type_counts"):
                    type_df = pd.DataFrame(
                        list(stats["content_type_counts"].items()),
                        columns=["Type", "Count"]
                    )
                    chart = alt.Chart(type_df).mark_bar(color="#F58518").encode(
                        x=alt.X("Count:Q", title="Count"),
                        y=alt.Y("Type:N", sort="-x", title=""),
                    ).properties(height=200)
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("No content type data available.")

            # Second row: Topics and Difficulty Level
            row2_col1, row2_col2 = st.columns(2)

            with row2_col1:
                st.markdown("**Topics**")
                if stats.get("topic_counts"):
                    topic_df = pd.DataFrame(
                        list(stats["topic_counts"].items()),
                        columns=["Topic", "Count"]
                    )
                    chart = alt.Chart(topic_df).mark_bar(color="#54A24B").encode(
                        x=alt.X("Count:Q", title="Count"),
                        y=alt.Y("Topic:N", sort="-x", title=""),
                    ).properties(height=150)
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("No topic data available.")

            with row2_col2:
                st.markdown("**Difficulty Level Distribution**")
                if stats.get("difficulty_counts"):
                    diff_df = pd.DataFrame(
                        list(stats["difficulty_counts"].items()),
                        columns=["Difficulty", "Count"]
                    )
                    chart = alt.Chart(diff_df).mark_bar(color="#E45756").encode(
                        x=alt.X("Count:Q", title="Count"),
                        y=alt.Y("Difficulty:N", sort="-x", title=""),
                    ).properties(height=150)
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning("⚠️ 'Difficulty' column not found in dataset. Please check column names.")

    else:
        st.error("Could not load dashboard statistics from API.")
except requests.exceptions.ConnectionError:
    st.warning("⚠️ Could not connect to FastAPI to load dashboard stats.")

st.divider()
# ==========================================


# --- Main title ---
st.title("Midad Explorer")

# --- Fetch filter options from API ---
try:
    filters_resp = requests.get(f"{API_BASE}/filters", timeout=5)
    filters = filters_resp.json() if filters_resp.status_code == 200 else {}
except requests.exceptions.ConnectionError:
    filters = {}
    st.error("⚠️ Could not connect to FastAPI. Make sure uvicorn is running on port 8000.")


content_types = [""] + filters.get("content_types", [])
topics = [""] + filters.get("topics", [])
sources = [""] + filters.get("sources", [])

# Four search fields
col1, col2, col3, col4 = st.columns(4)

with col1:
    keyword = st.text_input("Search in keywords", placeholder="e.g., python, agents")

with col2:
    content_type = st.selectbox(
        "Content Type", content_types, format_func=lambda x: x if x else "— select —"
    )

with col3:
    topic = st.selectbox(
        "Topic", topics, format_func=lambda x: x if x else "— select —"
    )

with col4:
    source = st.selectbox(
        "Source", sources, format_func=lambda x: x if x else "— select —"
    )

limit = st.number_input(
    "Number of rows",
    min_value=30,
    max_value=500,
    value=30,
    step=10,
)

# Search button
if st.button("Search"):
    params = {"limit": limit}

    if keyword and keyword.strip():
        params["q"] = keyword.strip()
    if content_type:
        params["content_type"] = content_type
    if topic:
        params["topic"] = topic
    if source:
        params["source"] = source

    try:
        response = requests.get(f"{API_BASE}/content", params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            st.write(f"Number of results: {data['total']}")

            if data["results"]:
                df = pd.DataFrame(data["results"])
                # Set the index to start from 1 instead of 0 for better readability
                df.index = range(1, len(df) + 1)
                st.dataframe(df, use_container_width=True, height=600)
            else:
                st.warning("No matching results found.")
        else:
            st.error(f"API error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Could not connect to FastAPI. Make sure uvicorn is running.")