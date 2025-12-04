import json
from tabulate import tabulate

def compare_events(android_json, ios_json):
    # Convert JSON strings → dict
    android = json.loads(android_json)
    ios = json.loads(ios_json)

    # Get all unique keys across both
    all_keys = set(android.keys()) | set(ios.keys())

    rows = []
    for key in sorted(all_keys):
        a_val = android.get(key, "-")
        i_val = ios.get(key, "-")
        match = "✓" if a_val == i_val else "✗"
        rows.append([key, a_val, i_val, match])

    print("\n" + tabulate(rows, headers=["Field", "Android", "iOS", "Match"], tablefmt="grid"))


# ------------------------------
# EXAMPLE USAGE
# ------------------------------

android_event = """
{
    "app_device_id": "m.174D4E04-4C16-477F-ADF0-BE064B691E65",
    "build_version": "11702",
    "course_id": 1,
    "device_type": "Android",
    "part_id": "6924548d141112db388ad071",
    "platform": "Android",
    "session_id": "68e3433454eb187b6601dc1c",
    "subject_id": "66a3c9b9189bd8a4b4dcf463",
    "video_id": "692460c00ededf7363e6594d",
    "video_type": "general"
}
"""

ios_event = """
{
    "app_device_id": "m.174D4E04-4C16-477F-ADF0-BE064B691E65",
    "build_version": "11702",
    "course_id": 1,
    "device_type": "iPhone",
    "part_id": "6924548d141112db388ad071",
    "platform": "iOS",
    "session_id": "68e3433454eb187b6601dc1c",
    "subject_id": "66a3c9b9189bd8a4b4dcf463",
    "video_id": "692460c00ededf7363e6594d",
    "video_type": "general"
}
"""

compare_events(android_event, ios_event)
