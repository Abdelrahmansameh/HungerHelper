import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT slug, name_en, name_fr, rarity_en, sell_price, light_damage, heavy_damage FROM weapons")
weapons = c.fetchall()
print(f"Total weapons in DB: {len(weapons)}")
for w in weapons:
    print(w)
