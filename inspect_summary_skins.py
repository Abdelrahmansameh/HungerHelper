import json

with open("data/all_skins_summary.json", "r", encoding="utf-8") as f:
    skins = json.load(f)

print(f"Total skins in all_skins_summary.json: {len(skins)}")
for s in skins:
    if "peasant" in s.get("name", "").lower() or "spear" in s.get("subject", "").lower():
        print(s)
