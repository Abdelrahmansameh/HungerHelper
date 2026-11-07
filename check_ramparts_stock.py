import sqlite3, json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

# Get all items in standard quests
with open('data/all_tracker_data.json', 'r', encoding='utf-8') as f:
    t = json.load(f)

main_quests = {q['slug']: q for q in t.get('quests', []) if q.get('kind') == 'standard'}

# Check all items sold by Outer Ramparts merchants:
c.execute("""
    SELECT DISTINCT ni.item_name, n.name, n.location 
    FROM npc_items ni 
    JOIN npcs n ON ni.npc_slug = n.slug 
    WHERE n.location LIKE '%Ramparts%'
""")
ramparts_stock = c.fetchall()
print("Outer Ramparts Merchants Stock:")
for itm, npc, loc in sorted(ramparts_stock):
    print(f"  {npc:20} | {itm}")
