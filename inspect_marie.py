import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT name, slug FROM items WHERE name LIKE '%marie%' OR name LIKE '%rozier%'")
print("Matches:", c.fetchall())

# Also check fuzzy or companion_items_cache
c.execute("SELECT name, slug FROM companion_items_cache WHERE name LIKE '%marie%' OR name LIKE '%rozier%'")
print("Cache matches:", c.fetchall())
