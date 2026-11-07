import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

for itm in ['Saltpetre', 'Tallow Balm']:
    c.execute("""
        SELECT i.name, idr.source, idr.drop_rate, idr.location 
        FROM item_drops idr 
        JOIN items i ON idr.item_id = i.id 
        WHERE LOWER(i.name) = LOWER(?)
    """, (itm,))
    print(f"\n{itm}:")
    for r in c.fetchall():
        print(f"  Container: {r[1]} | Rate: {r[2]*100:.1f}% | Map: {r[3]}")
