import json

with open("data/high_rate_drops.json", "r", encoding="utf-8") as f:
    drops = json.load(f)

print(f"Total entries in high_rate_drops.json: {len(drops)}")
for k in ["peasant-s-burden-spear", "metallurgist-recipe-spear", "bacchus-wand-longboy", "solstice-vepr"]:
    if k in drops:
        d = drops[k]
        print(f"\n{k} -> Title: {d['title']}, Resale: {d['sell_display']}")
        print("  Drops:", d["summary_intel"])
