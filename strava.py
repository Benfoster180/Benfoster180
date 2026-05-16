import os
from datetime import datetime
from dotenv import load_dotenv
from stravalib.client import Client

load_dotenv()

ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise Exception("Missing STRAVA_ACCESS_TOKEN in .env")

client = Client(access_token=ACCESS_TOKEN)

current_year = datetime.now().year

# pull more activities so we can filter properly
activities = client.get_activities(limit=200)

year_activities = [
    a for a in activities
    if a.start_date.year == current_year
]

if not year_activities:
    print("No activities found for this year.")
    exit()


#Logic Just for Jui Jitsu
def Check_Jui_Jitsu(type, name):
    if str(type) == str("Workout") and str(name[0:3]).lower() == "jui":
        return True

     
#Logic to get most recent workout and check for Jui_Jitsu 
latest = year_activities[0] 
most_recent_name = Check_Jui_Jitsu(latest.type.root, latest.name)

if most_recent_name == True:
    most_recent_workout = "Jui-Jitsu"
else:
    most_recent_workout = latest.type

num_of_runs = 0
kms_ran = 0
Jui_Jitsu_Sessions = 0
num_gym_sessions = 0

for i in range(len(year_activities)):
    if year_activities[i].type.root == "Workout":
        check = Check_Jui_Jitsu(year_activities[i].type.root, year_activities[i].name)
        if check == True:
            Jui_Jitsu_Sessions += 1
    elif year_activities[i].type.root == "Run": 
        num_of_runs +=1 
        kms_ran += year_activities[i].distance
    
    elif year_activities[i].type.root == "WeightTraining": 
        num_gym_sessions +=1 
     


workout_dic = {
    "most_recent": most_recent_workout,
    "runs": num_of_runs,
    "run_kms": str(f"{kms_ran/ 1000:.2f} km"),
    "Jui_Jitsu_Sessions": Jui_Jitsu_Sessions,
    "Jui_Jitsu_Time": str(int(Jui_Jitsu_Sessions) * 2),
    "Gym_Sessions": num_gym_sessions
}

print(workout_dic)
