import sqlite3, re

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

keywords = ['tallow', 'saltpetre', 'longboy', 'ammunition', 'wine', 'mead', 'needle', 'branch', 'egg', 'bloodbag', 'bezoar', 'hartshorn']
c.execute("SELECT npc_slug, item_name, price_copper, price_silver FROM npc_items")
for slug, item_name, pc, ps in c.fetchall():
    if any(k in item_name.lower() for k in keywords):
        print(f"{slug:20} | {item_name:30} | {ps}s {pc}c")
