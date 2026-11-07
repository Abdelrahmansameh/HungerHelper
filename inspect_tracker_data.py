import json

with open("data/all_tracker_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

points = data.get("points", [])
for p in points[:15]:
    print(p)

types = set(p.get("type") for p in points)
print("\nUnique types:", types)
