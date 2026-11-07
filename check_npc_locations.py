import requests
from bs4 import BeautifulSoup

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0'})

r = s.get('https://hunger-companion.com/npcs')
if r.ok:
    soup = BeautifulSoup(r.text, 'html.parser')
    for card in soup.select('.npc-card, .fh-b, article, li'):
        text = card.get_text(separator=' | ')
        if any(name in text for name in ['Louis', 'Piro', 'Moreau', 'Sweet', 'Reynauld']):
            print(text[:200])
            print("---")
