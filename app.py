import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mixpanel Comparison Tool", layout="wide")

st.title("📊 Mixpanel Event Comparison Tool")

st.markdown("""
Upload **PRD**, **Android Events**, and **iOS Events** to compare parameters, 
identify missing fields, and check extra values across platforms.
""")

# ------------------------------------------------------------------------------------
# FILE UPLOAD SECTION
# ------------------------------------------------------------------------------------

prd_file = st.file_uploader("Upload PRD (CSV or Excel)", type=["csv", "xlsx"])
android_file = st.file_uploader("Upload Android Events (JSON or CSV)", type=["json", "csv"])
ios_file = st.file_uploader("Upload iOS Events (JSON or CSV)", type=["json", "csv"])

# ------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------------------------------

def load_file(file):
    if file is None:
        return None
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    if file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    if file.name.endswith(".json"):
        return pd.read_json(file)
    return None


def compare_params(prd_params, ios_params, android_params):
    prd_set = set(prd_params)
    ios_set = set(ios_params)
    android_set = set(android_params)

    return {
        "Missing in iOS": list(prd_set - ios_set),
        "Missing in Android": list(prd_set - android_set),
        "Extra in iOS": list(ios_set - prd_set),
        "Extra in Android": list(android_set - prd_set),
    }

# ------------------------------------------------------------------------------------
# PROCESS WHEN ALL FILES ARE UPLOADED
# ------------------------------------------------------------------------------------

if prd_file and android_file and ios_file:

    prd_df = load_file(prd_file)
    android_df = load_file(android_file)
    ios_df = load_file(ios_file)

    # Basic validation
    required_cols = ["Event name", "Params"]

    if not all(col in prd_df.columns for col in required_cols):
        st.error("PRD must contain columns: Event name, Params")
        st.stop()

    st.success("Files loaded successfully!")

    st.header("🔍 Event-wise Comparison")

    # Output table
    output_rows = []

    for _, row in prd_df.iterrows():
        event = row["Event name"]
        prd_params = [p.strip() for p in str(row["Params"]).split(",")]

        ios_event = ios_df[ios_df["event"] == event]
        android_event = android_df[android_df["event"] == event]

        ios_params = list(ios_event.columns) if not ios_event.empty else []
        android_params = list(android_event.columns) if not android_event.empty else []

        comparison = compare_params(prd_params, ios_params, android_params)

        output_rows.append({
            "Event": event,
            "PRD Params": ", ".join(prd_params),
            "Missing in iOS": ", ".join(comparison["Missing in iOS"]) or "—",
            "Missing in Android": ", ".join(comparison["Missing in Android"]) or "—",
            "Extra in iOS": ", ".join(comparison["Extra in iOS"]) or "—",
            "Extra in Android": ", ".join(comparison["Extra in Android"]) or "—",
        })

    output_df = pd.DataFrame(output_rows)

    st.dataframe(output_df, use_container_width=True)

else:
    st.info("Upload all three files to begin comparison.")

