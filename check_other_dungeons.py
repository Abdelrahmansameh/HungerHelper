import sqlite3

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

# Check Jacques Bridge points around Fort Sang Rouge
c.execute("SELECT id, title, x, y FROM map_points WHERE map_name = 'Jacques Bridge' AND x < 1200 AND y > 2400")
print("Jacques Bridge Fort Sang Rouge area:")
for r in c.fetchall():
    print(" ", r)

# Check Sombre Forest The Pit area
c.execute("SELECT id, title, x, y FROM map_points WHERE map_name = 'Sombre Forest' AND x BETWEEN 2400 AND 2900 AND y BETWEEN 1800 AND 2200")
print("Sombre Forest The Pit area:")
for r in c.fetchall():
    print(" ", r)
