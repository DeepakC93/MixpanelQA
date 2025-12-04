import streamlit as st
import json
import pandas as pd

st.title("Event Comparison (Android vs iOS)")

st.write("Paste the JSON for Android and iOS events.")

android_input = st.text_area("Android JSON", height=200)
ios_input = st.text_area("iOS JSON", height=200)

def check_field(data, field):
    return field in data and data[field] not in [None, "", {}]

def check_part_started(data):
    return check_field(data, "part_id") and check_field(data, "part_type")

def check_part_ended(data):
    return check_field(data, "part_status") and data.get("part_status") == "ended"

def check_live_waiting(data):
    return check_field(data, "live_status") and data.get("live_status") == "waiting"

def check_video_play(data):
    return check_field(data, "video_id") and check_field(data, "video_type")

def check_video_playback(data):
    return check_field(data, "playback_duration")

def tick(val):
    return "✔" if val else "❌"

if st.button("Compare"):
    try:
        android_json = json.loads(android_input) if android_input.strip() else {}
        ios_json = json.loads(ios_input) if ios_input.strip() else {}
    except:
        st.error("Invalid JSON format. Please check your input.")
        st.stop()

    results = [
        {
            "Event": "Part Started",
            "Android": tick(check_part_started(android_json)),
            "iOS": tick(check_part_started(ios_json)),
            "Notes": "part_type: live / test / general"
        },
        {
            "Event": "Part Ended",
            "Android": tick(check_part_ended(android_json)),
            "iOS": tick(check_part_ended(ios_json)),
            "Notes": "part_status: ended"
        },
        {
            "Event": "Live Waiting Status",
            "Android": tick(check_live_waiting(android_json)),
            "iOS": tick(check_live_waiting(ios_json)),
            "Notes": "live_status: waiting"
        },
        {
            "Event": "Video Play Event",
            "Android": tick(check_video_play(android_json)),
            "iOS": tick(check_video_play(ios_json)),
            "Notes": "video_type, video_id"
        },
        {
            "Event": "Video Playback Duration",
            "Android": tick(check_video_playback(android_json)),
            "iOS": tick(check_video_playback(ios_json)),
            "Notes": "playback_duration event sent"
        }
    ]

    df = pd.DataFrame(results)
    st.subheader("✅ Par
