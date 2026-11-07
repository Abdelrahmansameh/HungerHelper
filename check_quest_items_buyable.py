import sqlite3
import json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

# Get all required items in quest objectives
c.execute("SELECT DISTINCT required_item FROM quest_objectives WHERE required_item IS NOT NULL AND required_item != ''")
req_items = [r[0] for r in c.fetchall()]

# Also get all items sold by NPCs
c.execute("SELECT DISTINCT item_name FROM npc_items")
npc_sold_items = set([r[0] for r in c.fetchall()])

print(f"Total distinct required items in quest_objectives: {len(req_items)}")
print(f"Total distinct items sold by NPCs: {len(npc_sold_items)}")

buyable = []
not_buyable = []

for item in req_items:
    # check exact match or case-insensitive match
    matches = [sold for sold in npc_sold_items if sold.strip().lower() == item.strip().lower()]
    if matches:
        buyable.append((item, matches[0]))
    else:
        not_buyable.append(item)

print(f"\nQuest items BUYABLE from merchants: {len(buyable)}")
for item, match in sorted(buyable):
    print(f"  [BUYABLE] {item}")

print(f"\nQuest items NOT BUYABLE from merchants (Must be found in raid / looted): {len(not_buyable)}")
for item in sorted(not_buyable):
    print(f"  [LOOT-ONLY] {item}")
