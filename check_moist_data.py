import json
import sqlite3

print("--- Checking all_tracker_data.json for moist ---")
with open("data/all_tracker_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print("Keys in all_tracker_data:", list(data.keys()) if isinstance(data, dict) else f"list of {len(data)}")

# If it's a dict or list, search
text = json.dumps(data)
import re
for m in re.finditer(r'moist', text, re.IGNORECASE):
    start = max(0, m.start() - 200)
    end = min(len(text), m.end() + 300)
    print("Match in all_tracker_data:\n", text[start:end])
    print("="*40)
    break

# Let's inspect hunger_helper.db items table for moist-pouch
conn = sqlite3.connect("hunger_helper.db")
cur = conn.cursor()
cur.execute("SELECT * FROM items WHERE slug='moist-pouch' OR name LIKE '%Moist%'")
print("Items row:", cur.fetchall())

# Let's check companion_items_cache
cur.execute("SELECT * FROM companion_items_cache WHERE slug='moist-pouch'")
print("companion_items_cache row:", cur.fetchall())

# Let's check cosmetics or crafting tables in hunger_helper.db
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in hunger_helper.db:", [t[0] for t in cur.fetchall()])
