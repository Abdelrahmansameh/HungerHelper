import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0'}

eloise_chain = [
    'a-warm-welcome',
    'making-dough',
    'the-gavroche-family',
    'last-embers',
    'mapping-the-front',
    'bare-necessities',
    'ink-in-the-ashes',
    'pushing-back-the-shadows',
    'down-from-mount-sinai',
    'crossing-the-threshold',
    'a-touch-of-bribery'
]

for slug in eloise_chain:
    url = f"https://hunger-companion.com/quests/{slug}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        # find Guide section
        text = soup.get_text()
        guide_idx = text.find('Guide')
        guide_snip = text[guide_idx:guide_idx+400] if guide_idx != -1 else "No guide section"
        print(f"=== {slug} ===")
        print(guide_snip.strip())
        print()
