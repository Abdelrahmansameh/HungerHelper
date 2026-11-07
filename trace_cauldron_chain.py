import sqlite3, json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

# Find the exact quest that unlocks the Cauldron
c.execute("SELECT id, slug, name, giver, prerequisite_slug, location FROM quests WHERE slug LIKE '%threshold%' OR location LIKE '%Cauldron%'")
for r in c.fetchall():
    print("Cauldron related quest:", r)

# Trace Eloise chain to Crossing The Threshold
chain = []
curr = 'crossing-the-threshold'
while curr:
    c.execute("SELECT slug, name, giver, prerequisite_slug FROM quests WHERE slug = ?", (curr,))
    row = c.fetchone()
    if row:
        chain.append(row)
        curr = row[3]
    else:
        break

print("\n--- Chain to Crossing The Threshold (Unlocking Cauldron) ---")
for r in reversed(chain):
    print(f"  {r[0]} ({r[1]}) by {r[2]} [Prereq: {r[3]}]")
