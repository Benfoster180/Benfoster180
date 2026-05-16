import os
import json
from datetime import datetime
from stravalib.client import Client

print("🚀 Script starting...")

ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise Exception("Missing STRAVA_ACCESS_TOKEN")

print("🔐 Token loaded successfully")

client = Client(access_token=ACCESS_TOKEN)

current_year = datetime.now().year

print("📡 Fetching activities from Strava...")

try:
    activities = list(client.get_activities(limit=200))
except Exception as e:
    print("❌ Failed to fetch activities:", e)
    raise

print(f"📊 Total activities fetched: {len(activities)}")

year_activities = [
    a for a in activities
    if a.start_date and a.start_date.year == current_year
]

print(f"📅 Activities this year: {len(year_activities)}")

runs = 0
kms = 0
gym = 0
jui = 0


def is_jui(activity):
    name = (activity.name or "").lower()
    return (
        getattr(activity.type, "root", "") == "Workout"
        and name.startswith("jui")
    )


for a in year_activities:

    activity_type = getattr(a.type, "root", "")

    if activity_type == "Run":
        runs += 1
        if a.distance:
            kms += a.distance / 1000

    elif activity_type == "WeightTraining":
        gym += 1

    elif activity_type == "Workout" and is_jui(a):
        jui += 1


stats = {
    "year": current_year,
    "runs": runs,
    "run_km": round(kms, 2),
    "gym_sessions": gym,
    "jui_jitsu_sessions": jui
}

print("📦 Final stats:", stats)

# ✅ Always write to repo root (GitHub Actions safe)
repo_root = os.getenv("GITHUB_WORKSPACE", os.getcwd())
file_path = os.path.join(repo_root, "strava_stats.json")

print("📝 Writing to:", file_path)

try:
    with open(file_path, "w") as f:
        json.dump(stats, f, indent=2)

    print("✅ SUCCESS: strava_stats.json created")

    print("📁 Files in workspace:", os.listdir(repo_root))

except Exception as e:
    print("❌ File write failed:", e)
    raise