import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT name, type, rarity FROM items WHERE type='armour'")
for row in c.fetchall()[:15]:
    print(row)
