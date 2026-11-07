import sqlite3, json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

# Check descriptions of quests and objectives for "merchant", "unlock", "shop", "vendor"
c.execute("""
    SELECT q.name, qo.description 
    FROM quest_objectives qo 
    JOIN quests q ON qo.quest_id = q.id 
    WHERE LOWER(qo.description) LIKE '%merchant%' 
       OR LOWER(qo.description) LIKE '%vendor%' 
       OR LOWER(qo.description) LIKE '%shop%' 
       OR LOWER(qo.description) LIKE '%unlock%'
       OR LOWER(qo.description) LIKE '%buy%'
       OR LOWER(qo.description) LIKE '%speak%'
""")
for r in c.fetchall():
    print(r)
