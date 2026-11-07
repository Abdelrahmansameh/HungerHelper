# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect("hunger_helper.db")
c = conn.cursor()

c.execute("UPDATE companion_items_cache SET category = 'Ingrédient & Matériau (Materials)' WHERE slug LIKE '%flour%'")
c.execute("UPDATE companion_items_cache SET category = 'Objet de Quête (Quest Items)' WHERE slug LIKE '%ring%'")
c.execute("UPDATE companion_items_cache SET category = 'Arme à Feu (Pistols)' WHERE slug = 'deux' OR slug = 'auster'")
c.execute("UPDATE companion_items_cache SET category = 'Arme de Mêlée (Melee)' WHERE slug = 'zweihander'")

conn.commit()
print("Cleaned companion_items_cache successfully.")
conn.close()
