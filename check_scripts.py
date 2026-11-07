with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

import re
scripts = list(re.finditer(r'<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>', s))
print("Found scripts:", len(scripts))
for i, m in enumerate(scripts):
    print(f"Script {i} length: {len(m.group(1))}")
