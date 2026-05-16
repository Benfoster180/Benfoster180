import os
import json
from datetime import datetime
from dotenv import load_dotenv
from stravalib.client import Client

load_dotenv()

ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise Exception("Missing STRAVA_ACCESS_TOKEN")

client = Client(access_token=ACCESS_TOKEN)

current_year = datetime.now().year

activities = client.get_activities(limit=200)

year_activities = [
    a for a in activities
    if a.start_date.year == current_year
]

runs = 0
kms = 0
gym = 0
jui = 0


def is_jui(activity):
    return (
        str(activity.type.root) == "Workout"
        and activity.name.lower().startswith("jui")
    )


for a in year_activities:
    if a.type.root == "Run":
        runs += 1
        kms += a.distance / 1000

    elif a.type.root == "WeightTraining":
        gym += 1

    elif a.type.root == "Workout" and is_jui(a):
        jui += 1


stats = {
    "year": current_year,
    "runs": runs,
    "run_km": round(kms, 2),
    "gym_sessions": gym,
    "jui_jitsu_sessions": jui
}

# 🔥 DEBUG (important for GitHub Actions)
print("Stats generated:", stats)
print("Working directory:", os.getcwd())

# ✅ WRITE FILE (this is what fixes your error)
file_path = os.path.join(os.getcwd(), "strava_stats.json")

with open(file_path, "w") as f:
    json.dump(stats, f, indent=2)

print("Saved file:", file_path)