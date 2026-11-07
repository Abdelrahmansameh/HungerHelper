import sqlite3, json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

c.execute("SELECT slug, name_en, category, rarity, base_value, sell_silver, sell_copper, best_creature, raw_json FROM companion_items_cache WHERE slug LIKE '%peasant%' OR slug LIKE '%spear%'")
rows = c.fetchall()
for r in rows:
    print(r[0], '|', r[1], '|', r[2], '|', r[3], '| Base:', r[4], f'({r[5]}s {r[6]}c)', '| Creature:', r[7])
    if r[8]:
        try:
            rj = json.loads(r[8])
            print('   rj keys:', list(rj.keys()))
        except:
            pass
