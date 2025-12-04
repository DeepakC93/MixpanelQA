import streamlit as st
import pandas as pd
import json

st.title("Event Comparison (Android vs iOS)")

# ----------- EXPECTED PRD FIELDS -----------
EXPECTED_EVENTS = {
    "Part Started": {
        "fields": ["part_id", "part_type"],
        "notes": "part_type: live / test / general"
    },
    "Part Ended": {
        "fields": ["part_id", "part_status"],
        "notes": "part_status: ended"
    },
    "Live Waiting Status": {
        "fields": ["live_status"],
        "notes": "live_status: waiting"
    },
    "Video Play Event": {
        "fields": ["video_type", "video_id"],
        "notes": "video_type, video_id"
    },
    "Video Playback Duration": {
        "fields": ["playback_duration"],
        "notes": "playback_duration event sent"
    }
}


# ---------- INPUT BOXES ----------
st.subheader("Paste Android JSON")
android_json_text = st.text_area("Android Event JSON", height=200, key="a")

st.subheader("Paste iOS JSON")
ios_json_text = st.text_area("iOS Event JSON", height=200, key="b")

# Try to parse JSON
try:
    android_event = json.loads(android_json_text) if android_json_text.strip() else {}
except:
    android_event = {}
    st.error("Invalid Android JSON")

try:
    ios_event = json.loads(ios_json_text) if ios_json_text.strip() else {}
except:
    ios_event = {}
    st.error("Invalid iOS JSON")


def check_fields(event_json, required_fields):
    """Returns True if all required PRD fields exist."""
    return all(field in event_json for field in required_fields)


# ----------- BUILD TABLE -----------
table_rows = []

for event_name, info in EXPECTED_EVENTS.items():
    required_fields = info["fields"]

    android_ok = check_fields(android_event, required_fields)
    ios_ok = check_fields(ios_event, required_fields)

    table_rows.append({
        "Event": event_name,
        "Android": "✔" if android_ok else "❌",
        "iOS": "✔" if ios_ok else "❌",
        "Notes": info["notes"]
    })

df = pd.DataFrame(table_rows)

st.subheader("✅ Part-Level Events (Covered)")
st.dataframe(df, use_container_width=True)

