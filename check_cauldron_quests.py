import sqlite3, json

# Check the Cauldron items from our list:
# 1. Saltpetre (Bare Necessities - Eloise) -> Needed before Cauldron! Put in CANNOT BUY!
# 2. Tallow Balm (Bare Necessities - Eloise) -> Needed before Cauldron! Put in CANNOT BUY!
# 3. Fresh Egg (Gardon's Gambit - Louis) -> When does Gardon's Gambit happen?
# 4. Hartshorn (Of Blight & Bezoars - Piro) -> When does Of Blight and Bezoars happen?
# 5. Bezoar (Of Blight & Bezoars - Piro) -> When does Of Blight and Bezoars happen?

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

for q_name in ["Bare Necessities", "Gardon's Gambit", "Of Blight and Bezoars"]:
    c.execute("SELECT id, slug, name, giver, prerequisite_slug FROM quests WHERE name LIKE ?", (f"%{q_name}%",))
    print(c.fetchall())
