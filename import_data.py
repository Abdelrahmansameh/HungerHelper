import requests, json, re, os
from bs4 import BeautifulSoup
from database import get_connection

BASE_URL = 'https://hunger-companion.com'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

def fetch_html(path):
    url = f'{BASE_URL}{path}'
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text

def parse_quest_tree():
    html = fetch_html('/quests/tree')
    soup = BeautifulSoup(html, 'html.parser')
    quests = []
    for a in soup.select('a[data-quest]'):
        slug = a.get('data-quest')
        after = a.get('data-after')
        name = a.get('href').split('/')[-1] if a.get('href') else slug
        quests.append({'slug': slug, 'after': after, 'name': name})
    return quests

def store_quests(tree):
    conn = get_connection()
    cur = conn.cursor()
    for q in tree:
        cur.execute(
            "INSERT OR IGNORE INTO quests (slug, name, prerequisite_slug) VALUES (?,?,?)",
            (q['slug'], q['name'], q['after'] if q['after'] else None)
        )
    conn.commit()
    conn.close()

def fetch_and_store_objectives():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, slug FROM quests')
    for quest_id, slug in cur.fetchall():
        # each quest page url: /quests/<slug>
        page_path = f'/quests/{slug}'
        html = fetch_html(page_path)
        soup = BeautifulSoup(html, 'html.parser')
        # objectives are li elements with class containing 'obj'
        for li in soup.select('li[class*="obj"]'):
            obj_id = li.get('data-obj-id') or li.get('data-obj')
            desc = li.get_text(strip=True)
            # try to find required item from links inside the li
            req_item = None
            a = li.find('a', href=True)
            if a and '/items/' in a['href']:
                req_item = a['href'].split('/')[-1]
            cur.execute(
                "INSERT OR IGNORE INTO quest_objectives (quest_id, obj_id, description, required_item) VALUES (?,?,?,?)",
                (quest_id, obj_id, desc, req_item)
            )
    conn.commit()
    conn.close()

def fetch_and_store_items():
    conn = get_connection()
    cur = conn.cursor()
    # collect distinct required_item slugs from objectives
    cur.execute('SELECT DISTINCT required_item FROM quest_objectives WHERE required_item IS NOT NULL')
    items = [row['required_item'] for row in cur.fetchall()]
    for slug in items:
        try:
            resp = requests.get(f'{BASE_URL}/api/item-card/', params={'slug': slug}, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            continue
        name = data.get('name')
        type_ = data.get('type')
        rarity = data.get('rarity')
        cur.execute("INSERT OR IGNORE INTO items (slug, name, type, rarity) VALUES (?,?,?,?)",
                    (slug, name, type_, rarity))
        item_id = cur.lastrowid
        # handle drops if present
        for drop in data.get('drops', []):
            location = drop.get('location')
            prob = drop.get('chance')
            source = drop.get('source')
            cur.execute(
                "INSERT INTO item_drops (item_id, location, drop_rate, source) VALUES (?,?,?,?)",
                (item_id, location, prob, source)
            )
    conn.commit()
    conn.close()

if __name__ == '__main__':
    print('Downloading quest tree…')
    tree = parse_quest_tree()
    print(f'Found {len(tree)} quests')
    store_quests(tree)
    print('Fetching and storing objectives…')
    fetch_and_store_objectives()
    print('Fetching and storing item data…')
    fetch_and_store_items()
    print('Import complete.')
