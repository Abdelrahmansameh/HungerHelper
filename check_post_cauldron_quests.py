import sqlite3, json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

# Check all standard quests that have prerequisites after crossing-the-threshold or located in Cauldron
c.execute("""
    SELECT q.id, q.slug, q.name, q.giver, q.prerequisite_slug, q.location 
    FROM quests q 
    WHERE q.prerequisite_slug = 'crossing-the-threshold' 
       OR q.location LIKE '%Cauldron%'
""")
print("Quests after crossing-the-threshold:")
for r in c.fetchall():
    print(r)

# Check all quests given by Cauldron NPCs
c.execute("SELECT slug, name, location FROM npcs WHERE location LIKE '%Cauldron%'")
cauldron_npcs = [r[0] for r in c.fetchall()]
print("\nCauldron NPCs:", cauldron_npcs)

c.execute("SELECT slug, name, giver FROM quests WHERE LOWER(giver) IN (SELECT LOWER(name) FROM npcs WHERE location LIKE '%Cauldron%')")
print("\nQuests given by Cauldron NPCs:", c.fetchall())
