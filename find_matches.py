with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

import re
for m in re.finditer(r'(\d+):\s*"data:image/jpeg;base64', s):
    pos = m.start()
    print(f"Match at pos {pos}: {s[pos-30:pos+30]}")
