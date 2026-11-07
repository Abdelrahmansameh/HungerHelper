import sqlite3

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

for m in ['Sarlat Farm', 'Jacques Bridge', 'Sombre Forest']:
    print(f"\n=== {m} LOOT TITLES ===")
    c.execute("SELECT title, count(*) FROM map_points WHERE map_name = ? GROUP BY title ORDER BY count(*) DESC", (m,))
    for row in c.fetchall():
        print(f"  {row[0]}: {row[1]}")
