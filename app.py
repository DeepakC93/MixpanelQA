import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide")
st.title("📊 Mixpanel Events Comparator — Side by Side View")


# ---------------------- Utility Functions ----------------------
def read_file(uploaded):
    if uploaded is None:
        return None

    if uploaded.name.endswith(".csv"):
        return pd.read_csv(uploaded)
    elif uploaded.name.endswith(".json"):
        data = json.load(uploaded)
        return pd.json_normalize(data)
    else:
        st.error("Only CSV and JSON formats supported.")
        return None


def get_param_list(value):
    """Convert PRD 'Params' field into a clean list."""
    if pd.isna(value):
        return []
    return [p.strip() for p in value.replace("\n", "").replace('"', "").split(",") if p.strip()]


def colored_label(text, color):
    """Return HTML colored chip-style label."""
    return f"<span style='background-color:{color}; padding:4px 8px; border-radius:8px; margin-right:4px; color:white; font-size:13px;'>{text}</span>"


# ---------------------- File Upload ----------------------
prd_file = st.file_uploader("Upload PRD (CSV/JSON)", type=["csv", "json"])
android_file = st.file_uploader("Upload Android Events (CSV/JSON)", type=["csv", "json"])
ios_file = st.file_uploader("Upload iOS Events (CSV/JSON)", type=["csv", "json"])

prd_df = read_file(prd_file)
android_df = read_file(android_file)
ios_df = read_file(ios_file)

if prd_df is None or android_df is None or ios_df is None:
    st.stop()

if "Event name" not in prd_df.columns or "Params" not in prd_df.columns:
    st.error("PRD must contain columns: Event name, Par
