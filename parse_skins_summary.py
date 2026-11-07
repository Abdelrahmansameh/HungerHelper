import json
import urllib.request
from bs4 import BeautifulSoup
import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

with open("data/all_skins_summary.json", "r", encoding="utf-8") as f:
    skins = json.load(f)

print(f"Total skins in database: {len(skins)}")

# Let's count by type
types = {}
for s in skins:
    t = s.get("type", "unknown")
    types[t] = types.get(t, 0) + 1
print("Skin types:", types)

# Check skins for character, weapon, bag
print("\nSample weapon skins:")
for s in [x for x in skins if x.get("type") == "weapon"][:8]:
    print(s["name"], "->", s["keywords"], "->", s["image"])

print("\nSample character/outfit skins:")
for s in [x for x in skins if x.get("type") in ["outfit", "character", "survivor", "hero"]][:8]:
    print(s["name"], "->", s["keywords"], "->", s["image"])
