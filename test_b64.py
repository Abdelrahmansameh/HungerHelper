import re

with open(r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\eloise_raid_planner.html", "r", encoding="utf-8") as f:
    s = f.read()

matches = re.findall(r'(\d+):\s*"data:image/jpeg;base64,([^"]+)"', s)
print("Found maps count:", len(matches))
for idx, b64 in matches:
    print(f"Map {idx}: prefix {b64[:30]} len {len(b64)}")
