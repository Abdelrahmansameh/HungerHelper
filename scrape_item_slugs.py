import urllib.request
from bs4 import BeautifulSoup
import json
import time

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://hunger-companion.com/items"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")

item_slugs = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.startswith("/items/") and "#" not in href:
        slug = href.replace("/items/", "").strip("/")
        if slug and slug not in item_slugs:
            item_slugs.append(slug)

print(f"Total unique item slugs found on /items: {len(item_slugs)}")

# Filter schemas, recipes, weapons, and special drops
schemas = [s for s in item_slugs if "schema" in s or any(w in s for w in ["peasant", "wand", "solstice", "loup", "basilisk", "partisan", "hybernia", "burden"])]
recipes = [s for s in item_slugs if "recipe" in s]

print(f"Schemas ({len(schemas)}):", schemas[:15])
print(f"Recipes ({len(recipes)}):", recipes[:20])

with open("data/all_hunger_item_slugs.json", "w", encoding="utf-8") as f:
    json.dump(item_slugs, f, indent=2)
print("Saved all item slugs to data/all_hunger_item_slugs.json!")
