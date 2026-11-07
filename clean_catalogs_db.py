import sqlite3
import json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

# 1. Clean bags_full
c.execute('SELECT slug, name, rarity, slots, sell_silver, sell_copper FROM bags_full')
bags = c.fetchall()
for slug, name, rarity, slots, s_s, s_c in bags:
    clean_name = name
    if "Attach" in clean_name:
        clean_name = "Attache's Fold"
    elif "Moist Pouch" in clean_name:
        clean_name = "Moist Pouch"
    elif "Hunting Sling" in clean_name:
        clean_name = "Hunting Sling"
    elif "Silver Pocket" in clean_name:
        clean_name = "Silver Pocket"
    
    if clean_name != name:
        print(f"Updating bag: {name} -> {clean_name}")
        c.execute('UPDATE bags_full SET name = ? WHERE slug = ?', (clean_name, slug))

# 2. Clean status_effects_full
c.execute('SELECT slug, name, effect_type, raw_json FROM status_effects_full')
effects = c.fetchall()
for slug, name, eff_type, raw in effects:
    clean_eff = eff_type
    try:
        data = json.loads(raw)
        desc = data.get('desc', '')
        desc = desc.replace('\u00d7', 'x').replace('×', 'x')
        desc = desc.replace('\ufffd', '')
        clean_eff = desc
    except Exception:
        clean_eff = clean_eff.replace('\ufffd', '')
    c.execute('UPDATE status_effects_full SET effect_type = ? WHERE slug = ?', (clean_eff, slug))

# 3. Clean gathering_full
c.execute('SELECT slug, name, yield_range, raw_json FROM gathering_full')
nodes = c.fetchall()
for slug, name, y_range, raw in nodes:
    clean_yield = y_range
    try:
        data = json.loads(raw)
        raw_y = data.get('yield', '')
        clean_y = raw_y.replace('\u00d7', '').replace('×', '').replace('\u2013', '-').replace('–', '-').replace('\ufffd', '-').strip()
        if clean_y.startswith('-'):
            clean_y = clean_y[1:]
        clean_yield = clean_y
    except Exception:
        pass
    c.execute('UPDATE gathering_full SET yield_range = ? WHERE slug = ?', (clean_yield, slug))

conn.commit()
conn.close()
print("Cleaned tables successfully.")
