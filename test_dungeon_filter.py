import sqlite3

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

def is_dungeon(map_name, x, y):
    if map_name == 'Sarlat Farm':
        # Undercroft dungeon complex in bottom right
        if x > 3100 and y > 2900:
            return True
    elif map_name == 'Jacques Bridge':
        # Fort Sang Rouge dungeon
        if x < 1200 and y > 2400:
            return True
    elif map_name == 'Sombre Forest':
        # The Pit dungeon
        if 2400 <= x <= 2900 and 1800 <= y <= 2200:
            return True
    return False

for m in ['Sarlat Farm', 'Jacques Bridge', 'Sombre Forest']:
    c.execute("SELECT id, title, x, y FROM map_points WHERE map_name = ?", (m,))
    rows = c.fetchall()
    total = len(rows)
    open_world = [r for r in rows if not is_dungeon(m, r[2], r[3])]
    dungeon_count = total - len(open_world)
    print(f"{m}: Total={total}, OpenWorld={len(open_world)}, FilteredDungeon={dungeon_count}")
