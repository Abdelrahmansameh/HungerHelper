import sqlite3
import json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
slugs = ['borodino', 'volcan', 'vepr', 'cavalier', 'morgan', 'snub', 'belier', 'jager', 'swan', 'voir', 'kompas', 'louisville', 'volant', 'brown-betty']
placeholders = ', '.join(['?'] * len(slugs))
c.execute(f"SELECT slug, name_en, category, rarity, combat_stats, raw_json FROM companion_items_cache WHERE slug IN ({placeholders})", slugs)
rows = c.fetchall()
print(f"Found {len(rows)} weapons:")
for r in rows:
    slug, name, cat, rar, combat, raw = r
    data = json.loads(raw) if raw else {}
    print(f"=== {name} ({slug}) [{rar} {cat}] ===")
    print("Combat stats:", combat)
    print("Desc / Raw:", data.get("desc", "")[:120])
    for k in ["damage", "headshot", "range", "rate", "reload", "ammo", "capacity"]:
        if k in data:
            print(f"  {k}: {data[k]}")
conn.close()
