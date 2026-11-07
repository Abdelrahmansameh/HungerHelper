import json
import sqlite3

with open("data/all_hunger_items_cards.json", "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Total items in all_hunger_items_cards.json: {len(items)}")

# Check SQLite companion_items_cache
conn = sqlite3.connect("hunger_helper.db")
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM companion_items_cache")
count_cache = c.fetchone()[0]
print(f"Total items currently in companion_items_cache: {count_cache}")

# Also check items table
c.execute("SELECT COUNT(*) FROM items")
count_items = c.fetchone()[0]
print(f"Total items in items table: {count_items}")
conn.close()
