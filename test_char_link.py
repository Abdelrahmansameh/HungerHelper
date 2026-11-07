import json

with open("data/all_skins_summary.json", "r", encoding="utf-8") as f:
    skins = json.load(f)

for s in skins:
    if s.get("type") == "character":
        print(s["name"], "link:", s["link"], "keywords:", s["keywords"])
        print("image:", s["image"])
        print("-" * 30)
        break
