import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

c.execute("SELECT id, slug, name, type, rarity FROM items LIMIT 10")
for r in c.fetchall():
    print("item sample:", r)

c.execute("SELECT id, npc_slug, item_name, price_copper, price_silver, category FROM npc_items LIMIT 10")
for r in c.fetchall():
    print("npc_item sample:", r)
