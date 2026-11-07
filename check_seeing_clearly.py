import sys, json
sys.stdout.reconfigure(encoding='utf-8')

tracker = json.load(open('data/all_tracker_data.json', encoding='utf-8'))

for q in tracker.get('quests', []):
    if 'clearly' in q.get('title', '').lower() or 'lens' in str(q).lower() or 'piro' in q.get('npc_slug', '').lower():
        print("QUEST:", q.get('title'), "| NPC:", q.get('npc_name'), "| Kind:", q.get('kind'))
        for obj in q.get('objectives', []):
            print("  obj:", obj.get('html'))

for pt in tracker.get('points', []):
    if 'lens' in pt.get('title', '').lower() or 'clearly' in str(pt).lower():
        print("POINT:", pt)
