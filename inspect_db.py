import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("PRAGMA table_info(items)")
print("Columns in items:", c.fetchall())

c.execute("SELECT slug, name, type, rarity FROM items WHERE type = 'schema'")
schemas = c.fetchall()
print(f"Total schemas: {len(schemas)}")
for s in schemas:
    print(s)
