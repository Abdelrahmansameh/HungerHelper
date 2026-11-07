import argparse, json, os, sys
from collections import defaultdict, deque
from database import get_connection

def load_quests():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, slug, name, giver, prerequisite_slug, location FROM quests')
    quests = {row['slug']: dict(row) for row in cur.fetchall()}
    conn.close()
    return quests

def load_objectives():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT quest_id, obj_id, description, required_item FROM quest_objectives')
    objectives = defaultdict(list)
    for row in cur.fetchall():
        objectives[row['quest_id']].append(dict(row))
    conn.close()
    return objectives

def load_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, slug, name, type FROM items')
    items = {row['slug']: dict(row) for row in cur.fetchall()}
    conn.close()
    return items

def load_item_drops():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT item_id, location, drop_rate FROM item_drops')
    drops = defaultdict(list)
    for row in cur.fetchall():
        drops[row['item_id']].append(dict(row))
    conn.close()
    return drops

def resolve_dependencies(selected_slugs, quests):
    """Return full set of quests including prerequisites (DFS)."""
    full = set()
    stack = list(selected_slugs)
    while stack:
        slug = stack.pop()
        if slug in full:
            continue
        full.add(slug)
        prereq = quests.get(slug, {}).get('prerequisite_slug')
        if prereq:
            stack.append(prereq)
    return full

def aggregate_items(selected_quest_ids, objectives, items):
    needed = defaultdict(int)
    for qid in selected_quest_ids:
        for obj in objectives.get(qid, []):
            req = obj.get('required_item')
            if req:
                needed[req] += 1  # count occurrences; can adjust per quest specifics
    return needed

def group_by_location(quests, needed_items, items, item_drops):
    # map location -> list of quests and items that drop there
    loc_map = defaultdict(lambda: {'quests': [], 'items': []})
    for slug, q in quests.items():
        loc = q.get('location') or 'unknown'
        loc_map[loc]['quests'].append(q)
    for slug, qty in needed_items.items():
        item = items.get(slug)
        if not item:
            continue
        # find best location by highest drop chance
        drops = item_drops.get(item['id'], [])
        if not drops:
            continue
        best = max(drops, key=lambda d: d['drop_rate'])
        loc_map[best['location']]['items'].append({'item': item, 'qty': qty, 'chance': best['drop_rate']})
    return loc_map

def generate_plan(loc_map):
    plan = []
    for loc, data in loc_map.items():
        if not data['quests'] and not data['items']:
            continue
        plan.append({'location': loc, 'quests': [q['name'] for q in data['quests']],
                     'items': [{'name': i['item']['name'], 'qty': i['qty'], 'chance': i['chance']} for i in data['items']]})
    return plan

def main():
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    parser = argparse.ArgumentParser(description='Hunger Companion Optimizer')
    parser.add_argument('--all', '--new-wipe', dest='all', action='store_true', help='Plan for all quests (full wipe)')
    parser.add_argument('--quests', nargs='*', help='Specify list of quest slugs to include')
    args = parser.parse_args()

    quests = load_quests()
    objectives = load_objectives()
    items = load_items()
    item_drops = load_item_drops()

    if args.all:
        selected_slugs = set(quests.keys())
    else:
        selected_slugs = set(args.quests or [])
        if not selected_slugs:
            print('No quests specified. Use --all or provide quest slugs.')
            sys.exit(1)

    full_slugs = resolve_dependencies(selected_slugs, quests)
    # map slug to quest id for later lookups
    slug_to_id = {q['slug']: q['id'] for q in quests.values()}
    selected_ids = [slug_to_id[s] for s in full_slugs if s in slug_to_id]

    needed_items = aggregate_items(selected_ids, objectives, items)
    active_quests = {s: quests[s] for s in full_slugs if s in quests}
    loc_map = group_by_location(active_quests, needed_items, items, item_drops)
    plan = generate_plan(loc_map)

    print(json.dumps(plan, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
