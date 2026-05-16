import os
from datetime import datetime
from stravalib.client import Client

print("🚀 Starting Strava README update...")

ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise Exception("Missing STRAVA_ACCESS_TOKEN")

client = Client(access_token=ACCESS_TOKEN)

current_year = datetime.now().year

print("📡 Fetching activities...")

activities = list(client.get_activities(limit=200))

year_activities = [
    a for a in activities
    if a.start_date and a.start_date.year == current_year
]

print(f"📊 Year activities: {len(year_activities)}")

# counters
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

current_year = datetime.now().year

print("📦 Stats calculated")

# -----------------------------
# BUILD MARKDOWN BLOCK
# -----------------------------
start = "<!-- STRAVA_START -->"
end = "<!-- STRAVA_END -->"

stats_block = f"""
{start}

## 🏃 Strava Stats ({current_year}) (Auto-updated)

- 🏃 Runs: {runs}, Distance: {round(kms, 2)} km
- 🏋️ Gym sessions: {gym}
- 🥋 Jiu Jitsu sessions: {jui}

{end}
"""

# -----------------------------
# UPDATE README
# -----------------------------
repo_root = os.getenv("GITHUB_WORKSPACE", os.getcwd())
readme_path = os.path.join(repo_root, "README.md")

print("📝 Updating README:", readme_path)

if not os.path.exists(readme_path):
    raise Exception("README.md not found")

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

if start in content and end in content:
    before = content.split(start)[0]
    after = content.split(end)[1]
    new_content = before + stats_block + after
else:
    # fallback append
    new_content = content + "\n\n" + stats_block

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✅ README successfully updated")
