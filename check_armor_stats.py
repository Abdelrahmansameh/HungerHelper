import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

# Search items table for armour
c.execute("SELECT name, category, rarity, stats FROM items WHERE category LIKE '%armour%' OR category LIKE '%armor%' LIMIT 10")
rows = c.fetchall()
print(f"Found {len(rows)} armour items:")
for r in rows:
    print(r)

# Check if there are character base stats or if all heroes share base HP
