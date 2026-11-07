import json

with open("data/all_skins_summary.json", "r", encoding="utf-8") as f:
    skins = json.load(f)

matches = []
for s in skins:
    kw = s.get("keywords", "").lower()
    if "moist" in kw or "pouch" in kw:
        matches.append(s)

print(f"Total skins matching 'moist' or 'pouch': {len(matches)}")
for m in matches:
    print(m["name"], "->", m["type"], "->", m["keywords"])
