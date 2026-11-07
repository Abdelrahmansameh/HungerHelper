import sqlite3
import json
import os

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

print("--- TABLES ---")
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(c.fetchall())

print("\n--- CREATURE DROPS SAMPLE ---")
c.execute("SELECT * FROM creature_drops LIMIT 20")
for r in c.fetchall():
    print(r)

print("\n--- ITEM DROPS SAMPLE ---")
c.execute("SELECT * FROM item_drops WHERE drop_rate > 0.1 LIMIT 20")
for r in c.fetchall():
    print(r)

print("\n--- ITEMS MATCHING RECIPE OR SCHEMA ---")
c.execute("SELECT slug, name, type, rarity FROM items WHERE name LIKE '%recipe%' OR name LIKE '%schema%' OR slug LIKE '%recipe%' OR slug LIKE '%schema%'")
for r in c.fetchall()[:25]:
    print(r)

print("\n--- FULL COMPANION SKINS SAMPLE ---")
if os.path.exists("data/full_companion_skins.json"):
    skins = json.load(open("data/full_companion_skins.json", encoding="utf-8"))
    print("Total skins in JSON:", len(skins))
    # look at peasant's burden
    for k, v in skins.items():
        if "peasant" in k or "burden" in k:
            print("Peasant entry in JSON:", json.dumps(v, indent=2))
            break
