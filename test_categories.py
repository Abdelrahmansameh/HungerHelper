import sqlite3

conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()

def get_loot_categories(map_name):
    c.execute("SELECT id, title, x, y FROM map_points WHERE map_name = ?", (map_name,))
    rows = c.fetchall()
    
    cats = {
        'bullion': [],      # Hard to find: Opium Pipe (13.7%) - Bullion Box, Jewellery Box
        'wall_cabinet': [], # Hard to find: China Bowl (16.1%) - Wall Cabinet
        'medicinals': [],   # Hard to find: Opium (47.6%) - Jacque's Medicinals
        'tooling_bin': [],  # Medium: Saltpetre (18.9%) - Tooling Bin
        'stone_grave': [],  # Medium: Damp Rag (23.8%) - Stone Grave
        'ash_pile': [],     # Common: Charcoal (52.6%) - Pile of Ash
        'flour_sack': [],   # Common: Flour (47.6%) - Flour Sack
    }
    
    seen_coords = set()
    for pid, title, x, y in rows:
        t = title.lower()
        coord_key = (round(x, 1), round(y, 1))
        
        # Prioritize assigning coordinate to the most specific container
        if 'jacque' in t and 'medicinal' in t:
            if coord_key not in seen_coords:
                cats['medicinals'].append((x, y, title))
                seen_coords.add(coord_key)
        elif 'bullion' in t or 'jeweller' in t:
            if coord_key not in seen_coords:
                cats['bullion'].append((x, y, title))
                seen_coords.add(coord_key)
        elif 'wall cabinet' in t:
            if coord_key not in seen_coords:
                cats['wall_cabinet'].append((x, y, title))
                seen_coords.add(coord_key)
        elif 'tooling bin' in t:
            if coord_key not in seen_coords:
                cats['tooling_bin'].append((x, y, title))
                seen_coords.add(coord_key)
        elif 'stone grave' in t:
            if coord_key not in seen_coords:
                cats['stone_grave'].append((x, y, title))
                seen_coords.add(coord_key)
        elif 'pile of ash' in t:
            if coord_key not in seen_coords:
                cats['ash_pile'].append((x, y, title))
                seen_coords.add(coord_key)
        elif 'flour sack' in t:
            if coord_key not in seen_coords:
                cats['flour_sack'].append((x, y, title))
                seen_coords.add(coord_key)
                
    return cats

for m in ['Sarlat Farm', 'Jacques Bridge', 'Sombre Forest']:
    cats = get_loot_categories(m)
    print(f"\n{m}:")
    for k, v in cats.items():
        print(f"  {k}: {len(v)} points")
