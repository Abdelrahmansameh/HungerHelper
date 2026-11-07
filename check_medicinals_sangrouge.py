import sqlite3

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

c.execute("SELECT title, map_name, x, y FROM map_points WHERE title LIKE '%Medicinal%'")
print("Medicinals:")
for r in c.fetchall():
    print(" ", r)

c.execute("SELECT id, title, map_name, x, y FROM map_points WHERE map_name = 'Jacques Bridge' AND (title LIKE '%Fort%' OR title LIKE '%Sang%')")
print("Fort Sang Rouge points:")
for r in c.fetchall():
    print(" ", r)
