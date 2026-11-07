with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

import re
matches = re.findall(r'id:\s*6,[\s\S]*?id:\s*7,', s)
if matches:
    print(matches[0][:1500])
else:
    print("Not found")
