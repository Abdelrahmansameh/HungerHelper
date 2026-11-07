import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()
c.execute("SELECT slug, name_en, category FROM companion_items_cache WHERE slug = 'peasant-s-burden-spear'")
print('peasant-s-burden-spear in db:', c.fetchone())
c.execute("SELECT slug, name_en, category FROM companion_items_cache WHERE slug = 'metallurgist-recipe-spear'")
print('metallurgist-recipe-spear in db:', c.fetchone())
