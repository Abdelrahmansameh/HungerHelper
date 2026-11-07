import json, sqlite3, re

with open('data/all_tracker_data.json', 'r', encoding='utf-8') as f:
    t = json.load(f)
quests = t.get('quests', [])

main_quests = [q for q in quests if q.get('kind') == 'standard']

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

# Get all items in the game
c.execute("SELECT slug, name, type, rarity FROM items")
all_items = {r[0]: (r[1], r[2], r[3]) for r in c.fetchall()}

# Get all NPC items
c.execute("SELECT npc_slug, item_name, price_copper, price_silver, category FROM npc_items")
npc_rows = c.fetchall()

cleaned_npc_stock = []
for npc_slug, raw_name, pc, ps, cat in npc_rows:
    cleaned = re.sub(r'^\d+', '', raw_name).strip()
    cleaned_npc_stock.append((npc_slug, cleaned, raw_name, pc, ps, cat))

print(f"Main (standard) quests count: {len(main_quests)}")

# Extract required items from main quests
main_quest_items = {} # item_slug -> list of {quest_title, qty, type}
for q in main_quests:
    q_title = q.get('title')
    for obj in q.get('objectives', []):
        okeys = obj.get('okeys', [])
        html = obj.get('html', '')
        # extract item slug from href="/items/..." or okeys
        item_slugs = re.findall(r'/items/([a-z0-9\-]+)', html)
        if not item_slugs:
            for k in okeys:
                if '|ID_' in k:
                    # e.g. "a-warm-welcome|ID_..."
                    pass
        for s in set(item_slugs):
            if s not in main_quest_items:
                main_quest_items[s] = []
            main_quest_items[s].append(q_title)

print(f"Total unique item slugs in main quests: {len(main_quest_items)}")

# Classify items:
# 1. Is it unique quest collectible / narrative item?
# 2. Is it buyable from merchant?
# 3. Is it not buyable (raid loot only)?

results = []
for slug, q_list in main_quest_items.items():
    item_info = all_items.get(slug, (slug.replace('-', ' ').title(), 'unknown', 'unknown'))
    name, itype, rarity = item_info
    
    # Check if buyable
    merchants = []
    for npc_slug, cleaned_name, raw_name, pc, ps, cat in cleaned_npc_stock:
        if (cleaned_name.lower() == name.lower() or 
            cleaned_name.lower() == slug.replace('-', ' ').lower()):
            merchants.append((npc_slug, pc, ps))
            
    is_unique_quest_item = (itype == 'quest_item' or 
                            any(w in slug for w in ['book', 'diary', 'sample', 'locket', 'necklace', 'lens', 'record', 'doctrine', 'census', 'handkerchief', 'ring']) or
                            'diary' in name.lower() or 'sample' in name.lower() or 'record' in name.lower())
    
    results.append({
        'slug': slug,
        'name': name,
        'type': itype,
        'rarity': rarity,
        'quests': list(set(q_list)),
        'merchants': list(set(merchants)),
        'is_unique': is_unique_quest_item,
        'buyable': len(merchants) > 0
    })

print("\n--- ALL MAIN QUEST ITEMS ---")
for r in sorted(results, key=lambda x: (x['is_unique'], not x['buyable'], x['name'])):
    u_tag = "[UNIQUE/NARRATIVE]" if r['is_unique'] else "[REGULAR]"
    b_tag = f"[BUYABLE: {len(r['merchants'])} vendors]" if r['buyable'] else "[LOOT-ONLY]"
    print(f"{u_tag} {b_tag} {r['name']} ({r['slug']}) - Type: {r['type']} - Quests: {', '.join(r['quests'])}")
