import sqlite3
conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT slug, name FROM items WHERE name LIKE '%trap%'")
rows = c.fetchall()
print("Matches for '%trap%':", rows)
conn.close()
