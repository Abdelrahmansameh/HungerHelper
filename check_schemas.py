import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT id, slug, name, type, rarity FROM items WHERE type = 'schema'")
rows = c.fetchall()
print(f"Total schema items: {len(rows)}")
for r in rows:
    c.execute("SELECT location, drop_rate, source FROM item_drops WHERE item_id = ?", (r[0],))
    drops = c.fetchall()
    print(f"  Item {r[0]}: {r[1]} ({r[2]}) -> Drops: {drops}")

# Let's check all item_drops where drop_rate == 1.0 or drop_rate == 100
c.execute("SELECT items.id, items.slug, items.name, item_drops.location, item_drops.drop_rate, item_drops.source FROM items JOIN item_drops ON items.id = item_drops.item_id WHERE item_drops.drop_rate >= 0.99")
print("\nItems with 100% (or ~1.0) drop rate:")
for r in c.fetchall():
    print("  100% Drop:", r)
