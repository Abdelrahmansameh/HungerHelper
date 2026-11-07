import sys, json
sys.stdout.reconfigure(encoding='utf-8')

# Let's check companion_items_cache for all items
import sqlite3
conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

c.execute("SELECT slug, name_en, category, rarity, base_value, sell_silver, sell_copper, best_container, vendor_buy FROM companion_items_cache WHERE category LIKE '%schema%' OR category LIKE '%recipe%' OR slug LIKE '%recipe%' OR slug LIKE '%schema%'")
rows = c.fetchall()
print(f"Total schemas/recipes in db: {len(rows)}")

for r in rows[:15]:
    print(r[0], "|", r[1], "|", r[2], "|", r[3], "| Resale:", f"{r[5]}s {r[6]}c", "| Vendor:", r[8], "| Container:", r[7])
