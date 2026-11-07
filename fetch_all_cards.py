import urllib.request
import json
import concurrent.futures
import time

with open("data/all_hunger_item_slugs.json", "r", encoding="utf-8") as f:
    slugs = json.load(f)

print(f"Total slugs to query: {len(slugs)}")
headers = {"User-Agent": "Mozilla/5.0"}

results = {}

def fetch_card(slug):
    url = f"https://hunger-companion.com/api/item-card/{slug}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            data["slug"] = slug
            return slug, data
    except Exception as e:
        return slug, None

t0 = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(fetch_card, s) for s in slugs]
    for fut in concurrent.futures.as_completed(futures):
        s, d = fut.result()
        if d:
            results[s] = d

t1 = time.time()
print(f"Fetched {len(results)}/{len(slugs)} items in {t1 - t0:.2f} seconds!")

with open("data/all_hunger_items_cards.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)

# Analyze categories
cats = {}
for s, d in results.items():
    c = d.get("c", "unknown")
    cats[c] = cats.get(c, 0) + 1

print("\nCategories breakdown:")
for c, cnt in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {c}: {cnt}")
