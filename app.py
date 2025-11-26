import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mixpanel Comparison Tool", layout="wide")

st.title("📊 Mixpanel Event Comparison Tool (Textbox Version)")

st.markdown("""
Paste Android & iOS event params directly, and upload PRD to compare.
""")

# ------------------------------------------------------------------------------------
# FILE UPLOAD FOR PRD
# ------------------------------------------------------------------------------------

prd_file = st.file_uploader("Upload PRD (CSV or Excel)", type=["csv", "xlsx"])

# ------------------------------------------------------------------------------------
# TEXTBOX INPUT FOR ANDROID & IOS
# ------------------------------------------------------------------------------------

st.subheader("Android Event Params")
android_text = st.text_area(
    "Paste Android event parameters here (comma or newline separated):",
    height=150
)

st.subheader("iOS Event Params")
ios_text = st.text_area(
    "Paste iOS event parameters here (comma or newline separated):",
    height=150
)

# ------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------------------------------

def parse_params(raw):
    if not raw:
        return []
    separators = [",", "\n"]
    for sep in separators:
        raw = raw.replace(sep, ",")
    return [p.strip() for p in raw.split(",") if p.strip()]

def compare_params(prd_params, ios_params, android_params):
    prd_set = set(prd_params)
    ios_set = set(ios_params)
    android_set = set(android_params)

    return {
        "Missing in iOS": sorted(list(prd_set - ios_set)),
        "Missing in Android": sorted(list(prd_set - android_set)),
        "Extra in iOS": sorted(list(ios_set - prd_set)),
        "Extra in Android": sorted(list(android_set - prd_set)),
    }

def load_prd(file):
    if file is None:
        return None
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    if file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    return None

# ------------------------------------------------------------------------------------
# PROCESS WHEN PRD + TEXTBOXES ARE FILLED
# ------------------------------------------------------------------------------------

if prd_file and (android_text or ios_text):

    prd_df = load_prd(prd_file)

    if prd_df is None:
        st.error("PRD file format not supported.")
        st.stop()

    if "Event name" not in prd_df.columns or "Params" not in prd_df.columns:
        st.error("PRD must contain 'Event name' and 'Params' columns.")
        st.stop()

    android_params = parse_params(android_text)
    ios_params = parse_params(ios_text)

    st.success("PRD + Android + iOS inputs loaded!")

    st.header("🔍 Event-wise Comparison")

    output_rows = []

    for _, row in prd_df.iterrows():
        event = row["Event name"]
        prd_params = parse_params(str(row["Params"]))

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
    st.info("Upload PRD and paste Android/iOS params to start comparison.")
