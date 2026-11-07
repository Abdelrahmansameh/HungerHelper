import sqlite3, requests
from bs4 import BeautifulSoup
import re

# 1. Check local DB
conn = sqlite3.connect(r'C:\Users\PC\Documents\HungerHelper\hunger_helper.db')
c = conn.cursor()
c.execute("SELECT id, slug, name, giver, prerequisite_slug, location FROM quests WHERE name LIKE '%sinai%' OR slug LIKE '%sinai%'")
quests = c.fetchall()
print("LOCAL DB QUESTS:")
for q in quests:
    print(q)
    c.execute("SELECT id, quest_id, obj_id, description, required_item FROM quest_objectives WHERE quest_id = ?", (q[0],))
    for obj in c.fetchall():
        print("  OBJ:", obj)

# 2. Check live website
url = "https://hunger-companion.com/quests/down-from-mount-sinai"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
print(f"\nLIVE URL ({r.status_code}):")
if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')
    for div in soup.find_all(['p', 'div', 'span', 'li', 'h1', 'h2', 'h3']):
        text = div.get_text().strip()
        if any(w in text.lower() for w in ['key', 'door', 'locked', 'book', 'silver', 'gold', 'bronze', 'requirement', 'undercroft']):
            if len(text) < 300 and '\n' not in text:
                print("  SITE:", text)
