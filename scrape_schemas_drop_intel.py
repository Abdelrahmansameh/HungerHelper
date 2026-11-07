import urllib.request
from bs4 import BeautifulSoup
import json
import concurrent.futures
import time
import os
import re

headers = {"User-Agent": "Mozilla/5.0"}

with open("data/all_hunger_items_cards.json", "r", encoding="utf-8") as f:
    all_items = json.load(f)

# Select schemas and recipes
targets = [k for k, v in all_items.items() if v.get("c") == "schema" or "recipe" in k or "schema" in k]
print(f"Total targets to scrape drop intel for: {len(targets)}")

def scrape_item_drops(slug):
    url = f"https://hunger-companion.com/items/{slug}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return slug, None

    soup = BeautifulSoup(html, "html.parser")
    
    # 1. Title, Category, Rarity
    h1 = soup.find("h1")
    title = h1.text.strip() if h1 else slug.replace("-", " ").title()
    
    # 2. Extract How to get it
    # Check for creature drops
    creature_drops = []
    # Check placed in world
    placed_drops = []
    # Check vendor buy
    vendors = []
    
    # Text in essentials or obtain section
    essentials = soup.find("section", class_=lambda c: c and "essentials" in str(c).lower()) or soup
    
    # Find all obtain entries
    for sec in soup.find_all("section"):
        sec_text = sec.get_text(separator=" ", strip=True)
        # Check creatures
        if "creature" in sec_text.lower():
            for tr in sec.find_all(["tr", "li", "div"], class_=lambda c: c and any(k in str(c).lower() for k in ["row", "entry", "drop", "item", "creature"])):
                row_t = tr.get_text(separator=" | ", strip=True)
                if any(cr in row_t.lower() for cr in ["dreg", "farmer", "brute", "drooler", "pitchskin", "lady", "hound", "shambler"]):
                    # avoid 1/10000+ container low rates if possible, but keep specific mob names
                    creature_drops.append(row_t)
                    
        # Check placed in world / loose loot
        if "placed" in sec_text.lower() or "world" in sec_text.lower():
            for el in sec.find_all(["tr", "li", "div"]):
                t = el.get_text(separator=" | ", strip=True)
                if "placed in the world" in t.lower() or "fixed spot" in t.lower():
                    placed_drops.append(t)
                    
        # Check vendor stock
        if "vendor" in sec_text.lower() or "marchand" in sec_text.lower():
            for el in sec.find_all(["tr", "li", "div"]):
                t = el.get_text(separator=" | ", strip=True)
                if "in vendor stock" in t.lower() or "from vendors" in t.lower():
                    vendors.append(t)

    # Clean duplicates
    creature_drops = list(dict.fromkeys(creature_drops))
    placed_drops = list(dict.fromkeys(placed_drops))
    vendors = list(dict.fromkeys(vendors))
    
    return slug, {
        "title": title,
        "slug": slug,
        "creatures": creature_drops[:5],
        "placed": placed_drops[:5],
        "vendors": vendors[:5]
    }

print("Starting concurrent drop scrape...")
t0 = time.time()
drop_results = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(scrape_item_drops, s) for s in targets]
    for fut in concurrent.futures.as_completed(futures):
        s, res = fut.result()
        if res:
            drop_results[s] = res

t1 = time.time()
print(f"Scraped drop intel for {len(drop_results)} items in {t1 - t0:.2f} seconds!")

with open("data/all_schemas_drop_intel.json", "w", encoding="utf-8") as out:
    json.dump(drop_results, out, indent=2, ensure_ascii=False)

print("Saved data/all_schemas_drop_intel.json!")

# Check Peasant's Burden and Spear Recipe
for k in ["peasant-s-burden-spear", "metallurgist-recipe-spear", "bacchus-wand-longboy", "solstice-vepr"]:
    if k in drop_results:
        print(f"\nDrop intel for {k}:")
        print(json.dumps(drop_results[k], indent=2, ensure_ascii=False))
