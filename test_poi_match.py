import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

for tok in ['heavy', 'ammo']:
    c.execute("""
        SELECT map_name, title, point_type, x, y, description
        FROM map_points
        WHERE title LIKE ? OR quest_slug LIKE ? OR description LIKE ?
        LIMIT 5
    """, (f"%{tok}%", f"%{tok}%", f"%{tok}%"))
    pts = c.fetchall()
    print(f"Token '{tok}' matched {len(pts)} points:")
    for p in pts:
        print(" ", p)
