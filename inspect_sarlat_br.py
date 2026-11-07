import sqlite3

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

c.execute("SELECT id, title, point_type, x, y FROM map_points WHERE map_name = 'Sarlat Farm' AND x > 2500 AND y > 2500")
rows = c.fetchall()
print(f"Points in bottom-right of Sarlat Farm: {len(rows)}")
for r in rows:
    print(r)
