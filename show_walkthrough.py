with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8", errors="ignore") as f:
    s = f.read()

import re
m = re.search(r'ROUTE WALKTHROUGH', s, re.IGNORECASE)
if m:
    pos = m.start()
    print("Found at pos", pos)
    print(s[pos-200:pos+1500].encode('ascii', 'replace').decode('ascii'))
