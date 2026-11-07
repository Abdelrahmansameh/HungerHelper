import sqlite3, json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

# Get all 48 standard quests and their prerequisites
with open('data/all_tracker_data.json', 'r', encoding='utf-8') as f:
    t = json.load(f)

main_quests = {q['slug']: q for q in t.get('quests', []) if q.get('kind') == 'standard'}

print("=== ALL STANDARD QUESTS & PREREQUISITES ===")
c.execute("SELECT slug, name, giver, prerequisite_slug FROM quests")
db_quests = {r[0]: (r[1], r[2], r[3]) for r in c.fetchall()}

for slug, q in main_quests.items():
    db_info = db_quests.get(slug, (q['title'], q.get('npc_name'), None))
    print(f"Slug: {slug:30} | Title: {db_info[0]:30} | Giver: {str(db_info[1]):15} | Prereq: {str(db_info[2])}")
