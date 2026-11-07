import sqlite3

conn = sqlite3.connect("hunger_helper.db")
c = conn.cursor()
c.execute("SELECT * FROM quests WHERE prerequisite_slug = 'a-touch-of-bribery'")
for r in c.fetchall():
    print("Quest after A Touch of Bribery:", r)
    c.execute(f"SELECT description FROM quest_objectives WHERE quest_id = {r[0]}")
    print("Objectives:", [row[0] for row in c.fetchall()])
