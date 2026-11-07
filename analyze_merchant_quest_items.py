import sqlite3
import re

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

# Get all items in the game
c.execute("SELECT slug, name, type, rarity FROM items")
all_items = {r[0]: (r[1], r[2], r[3]) for r in c.fetchall()}

# Get all required items in quest objectives
c.execute("""
    SELECT DISTINCT qo.required_item, q.name, q.giver 
    FROM quest_objectives qo 
    JOIN quests q ON qo.quest_id = q.id 
    WHERE qo.required_item IS NOT NULL AND qo.required_item != ''
""")
quest_items = {}
for req, q_title, q_npc in c.fetchall():
    if req not in quest_items:
        quest_items[req] = []
    quest_items[req].append((q_title, q_npc))

# Get all NPC items
c.execute("SELECT npc_slug, item_name, price_copper, price_silver, category FROM npc_items")
npc_rows = c.fetchall()

# Clean item names: remove leading digits
cleaned_npc_stock = []
for npc_slug, raw_name, pc, ps, cat in npc_rows:
    cleaned = re.sub(r'^\d+', '', raw_name).strip()
    cleaned_npc_stock.append((npc_slug, cleaned, raw_name, pc, ps, cat))

print(f"Total quest items required across quests: {len(quest_items)}")
print(f"Total NPC shop offerings: {len(cleaned_npc_stock)}")

# Let's see which quest items match any NPC shop item
matched_quest_items = {}
unmatched_quest_items = {}

for req_slug, quests in quest_items.items():
    item_info = all_items.get(req_slug)
    item_display_name = item_info[0] if item_info else req_slug.replace('-', ' ').title()
    
    # Check if this item is sold by any merchant
    found_merchants = []
    for npc_slug, cleaned_name, raw_name, pc, ps, cat in cleaned_npc_stock:
        # direct match or cleaned match
        if (cleaned_name.lower() == item_display_name.lower() or 
            cleaned_name.lower() == req_slug.replace('-', ' ').lower() or
            cleaned_name.lower().replace('-', ' ') == req_slug.replace('-', ' ').lower()):
            found_merchants.append((npc_slug, cleaned_name))
            
    if found_merchants:
        matched_quest_items[req_slug] = (item_display_name, quests, found_merchants)
    else:
        unmatched_quest_items[req_slug] = (item_display_name, quests)

print("\n================ QUEST ITEMS SOLD BY MERCHANTS ================")
print(f"Count: {len(matched_quest_items)}")
for slug, (name, quests, merchants) in sorted(matched_quest_items.items()):
    merchant_names = set(m[0] for m in merchants)
    print(f"- {name} (slug: {slug})")
    print(f"    Merchants: {', '.join(merchant_names)}")
    print(f"    Quests: {', '.join(q[0] for q in quests[:3])}")

print("\n================ QUEST ITEMS NOT SOLD BY MERCHANTS (LOOT ONLY) ================")
print(f"Count: {len(unmatched_quest_items)}")
sample_loot = list(sorted(unmatched_quest_items.items()))
for slug, (name, quests) in sample_loot[:25]:
    item_type = all_items.get(slug, ('Unknown', 'Unknown', 'Unknown'))[1]
    print(f"- {name} [Type: {item_type}] -> {quests[0][0]}")

print(f"\n... and {len(unmatched_quest_items) - 25} more items.")
