import sqlite3, json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

c.execute("SELECT id, slug, name, giver, prerequisite_slug FROM quests WHERE giver = 'Eloise'")
eloise_quests = c.fetchall()
print("Eloise Quests:")
for r in eloise_quests:
    print(f"  {r[0]} | {r[1]} | {r[2]} | Prereq: {r[4]}")

# Check which items are required in Eloise quests
c.execute("""
    SELECT q.slug, q.name, qo.required_item 
    FROM quests q 
    JOIN quest_objectives qo ON q.id = qo.quest_id 
    WHERE q.giver = 'Eloise' AND qo.required_item IS NOT NULL AND qo.required_item != ''
""")
for r in c.fetchall():
    print("Eloise required item:", r)
