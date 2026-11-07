import sqlite3, json, re

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

with open('data/all_tracker_data.json', 'r', encoding='utf-8') as f:
    t = json.load(f)

main_quests = {q['slug']: q for q in t.get('quests', []) if q.get('kind') == 'standard'}

# Unique narrative / lore items to exclude
unique_exclude = {
    'agarwood-necklace',
    'catechisme-of-christian-doctrine-1567',
    'census-of-1806',
    'course-in-agriculture-rozier',
    'course-in-civil-architecture-rondelet',
    'mortuary-record',
    'natural-history-general-and-particular-buffon',
    'the-spirit-of-the-laws-montesquieu',
    'de-molay-s-diary',
    'quarantine-diary',
    'filthy-francois-secret-diary',
    'family-ring',
    'fantine-s-handkerchief',
    'louis-mother-s-locket',
    'piro-s-lens',
    'red-ribbon',
    'golden-leaf-tobacco',
    'preserved-hand',
    'spanish-shako',
    'votive-candle',
    'jacques-bridge-spring-sample',
    'sarlat-farm-spring-sample',
    'sombre-forest-spring-sample'
}

# Get NPC info
c.execute("SELECT slug, name, location FROM npcs")
npc_info = {r[0]: {'name': r[1], 'loc': r[2]} for r in c.fetchall()}

# Get NPC stock
c.execute("SELECT npc_slug, item_name, price_copper, price_silver, category FROM npc_items")
npc_rows = c.fetchall()

cleaned_npc_stock = []
for npc_slug, raw_name, pc, ps, cat in npc_rows:
    cleaned = re.sub(r'^\d+', '', raw_name).strip()
    cleaned_npc_stock.append((npc_slug, cleaned, pc, ps, cat))

# Get all required items in main quests with their exact quest objective text / quantity
main_items_detail = {}
for q_slug, q in main_quests.items():
    for obj in q.get('objectives', []):
        html = obj.get('html', '')
        item_slugs = re.findall(r'/items/([a-z0-9\-]+)', html)
        # Parse quantity e.g. "Find 20x ..." or "Deliver 15x ..."
        qty_match = re.search(r'(\d+)x', html)
        qty = int(qty_match.group(1)) if qty_match else 1
        
        for slug in item_slugs:
            if slug in unique_exclude:
                continue
            if slug not in main_items_detail:
                main_items_detail[slug] = []
            main_items_detail[slug].append({
                'quest_slug': q_slug,
                'quest_title': q['title'],
                'giver': q.get('npc_name', 'Unknown'),
                'qty': qty,
                'raw_text': re.sub(r'<[^>]+>', '', html).strip()
            })

# Get item info
c.execute("SELECT slug, name, type, rarity FROM items")
item_db = {r[0]: (r[1], r[2], r[3]) for r in c.fetchall()}

buyable_items = {}
loot_only_items = {}

for slug, q_list in main_items_detail.items():
    name, itype, rarity = item_db.get(slug, (slug.replace('-', ' ').title(), 'misc', 'common'))
    
    # check merchant stock
    sellers = []
    for npc_slug, cleaned_name, pc, ps, cat in cleaned_npc_stock:
        if (cleaned_name.lower() == name.lower() or 
            cleaned_name.lower() == slug.replace('-', ' ').lower()):
            npc = npc_info.get(npc_slug, {'name': npc_slug.title(), 'loc': 'Unknown'})
            sellers.append({
                'npc_slug': npc_slug,
                'npc_name': npc['name'],
                'npc_loc': npc['loc'],
                'price_copper': pc,
                'price_silver': ps,
                'category': cat
            })
            
    total_qty_needed = sum(q['qty'] for q in q_list)
    quests_str = ", ".join([f"{q['quest_title']} ({q['qty']}x from {q['giver']})" for q in q_list])
    
    item_data = {
        'slug': slug,
        'name': name,
        'type': itype,
        'rarity': rarity,
        'total_qty': total_qty_needed,
        'quests': q_list,
        'sellers': sellers
    }
    
    if sellers:
        buyable_items[slug] = item_data
    else:
        loot_only_items[slug] = item_data

print("=== BUYABLE MAIN QUEST ITEMS ===")
print(f"Count: {len(buyable_items)}")
for slug, d in sorted(buyable_items.items(), key=lambda x: x[1]['name']):
    sellers_str = "; ".join([f"{s['npc_name']} ({s['npc_loc']}, {s['price_silver']}s {s['price_copper']}c)" for s in d['sellers']])
    print(f"* {d['name']} - Need {d['total_qty']}x - Vendors: {sellers_str}")
    for q in d['quests']:
        print(f"    -> Quest: {q['quest_title']} ({q['giver']})")

print("\n=== LOOT-ONLY MAIN QUEST ITEMS (CANNOT BE BOUGHT) ===")
print(f"Count: {len(loot_only_items)}")
for slug, d in sorted(loot_only_items.items(), key=lambda x: (x[1]['type'], x[1]['name'])):
    print(f"* {d['name']} [{d['type']}] - Need {d['total_qty']}x")
    for q in d['quests']:
        print(f"    -> Quest: {q['quest_title']} ({q['giver']})")
