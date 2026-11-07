import sqlite3

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

c.execute("SELECT n.name, ni.item_name, ni.cost, ni.currency FROM npc_items ni JOIN npcs n ON ni.npc_id = n.id WHERE n.location LIKE '%Ramparts%'")
rows = c.fetchall()
print(f"Outer Ramparts merchant stock ({len(rows)} items):")
for r in rows:
    if any(k in r[1].lower() for k in ['opium', 'pipe', 'bowl', 'candle', 'key', 'flour', 'charcoal', 'saltpetre', 'rag', 'balm']):
        print(" ", r)
