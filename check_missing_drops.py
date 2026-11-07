import json
import urllib.request
import time
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("data/high_rate_drops.json", "r", encoding="utf-8") as f:
    done = json.load(f)

with open("data/all_hunger_items_cards.json", "r", encoding="utf-8") as f:
    all_items = json.load(f)

targets = [k for k, v in all_items.items() if v.get("c") == "schema" or "recipe" in k or "schema" in k]
missing = [t for t in targets if t not in done]

print(f"Done: {len(done)}, Missing: {len(missing)}")
print("Sample missing:", missing[:15])

# Let's test why one missing failed
headers = {"User-Agent": "Mozilla/5.0"}
for m in missing[:5]:
    url = f"https://hunger-companion.com/items/{m}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            print(f"[OK] {m} -> status {resp.status}")
    except Exception as e:
        print(f"[FAIL] {m} -> {e}")
