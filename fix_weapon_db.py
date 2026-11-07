import sqlite3

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

c.execute("UPDATE weapons SET name_fr = 'Rapière' WHERE slug = 'rapier'")
c.execute("UPDATE weapons SET name_fr = 'Hache de guerre' WHERE slug = 'war-axe'")
conn.commit()

c.execute("SELECT slug, name_en, name_fr FROM weapons WHERE slug IN ('rapier', 'war-axe')")
print("Updated weapons in DB:", c.fetchall())
conn.close()
