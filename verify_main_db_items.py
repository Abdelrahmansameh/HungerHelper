import sqlite3, json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

with open('data/all_tracker_data.json', 'r', encoding='utf-8') as f:
    t = json.load(f)
main_slugs = set(q['slug'] for q in t.get('quests', []) if q.get('kind') == 'standard')

print("Main slugs count:", len(main_slugs))

c.execute("""
    SELECT q.slug, q.name, qo.description, qo.required_item 
    FROM quests q 
    JOIN quest_objectives qo ON q.id = qo.quest_id 
    WHERE qo.required_item IS NOT NULL AND qo.required_item != ''
""")
rows = c.fetchall()

main_db_items = {}
for q_slug, q_name, desc, req in rows:
    if q_slug in main_slugs:
        if req not in main_db_items:
            main_db_items[req] = set()
        main_db_items[req].add((q_slug, q_name))

print("Total unique items in main quests from DB:", len(main_db_items))
for item, quests in sorted(main_db_items.items()):
    print(f"  {item}: {quests}")
