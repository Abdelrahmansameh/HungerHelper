import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

loot_items = [
    'Flour', 'Charcoal', 'Damp Rag', 'China Bowl', 'Opium', 'Opium Pipe', 
    'Arsenic', 'Glass Vial', 'Silver Dish',
    'Dreg Head', 'Waif Head', 'Shambler Hand', 'Bloat Spine', 'Brute Foot', 'Drooler Jaw'
]

print("=== CHECKING DROP RATES IN item_drops ===")
for item_name in loot_items:
    c.execute("""
        SELECT i.name, idr.source, idr.drop_rate, idr.location 
        FROM item_drops idr 
        JOIN items i ON idr.item_id = i.id 
        WHERE LOWER(i.name) = LOWER(?)
    """, (item_name,))
    rows = c.fetchall()
    if rows:
        print(f"\n{item_name}:")
        for r in rows:
            print(f"  Container: {r[1]} | Rate: {r[2]*100:.1f}% | Map: {r[3]}")
    else:
        print(f"\n{item_name}: (No rows in item_drops table)")
