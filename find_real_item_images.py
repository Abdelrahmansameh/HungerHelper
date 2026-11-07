import requests
from bs4 import BeautifulSoup
import re

HEADERS = {'User-Agent': 'Mozilla/5.0'}
items_to_check = [
    'charcoal', 'flour', 'saltpetre', 'damp-rag', 'tallow-balm',
    'china-bowl', 'opium-pipe', 'opium', 'votive-candle',
    'census-of-1806', 'the-spirit-of-the-laws-montesquieu',
    'course-in-agriculture-rozier', 'course-in-civil-architecture-rondelet',
    'natural-history-general-and-particular-buffon', 'catechisme-of-christian-doctrine-1567',
    'bronze-key', 'silver-key', 'gold-key'
]

results = {}
for slug in items_to_check:
    url = f"https://hunger-companion.com/items/{slug}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Look for main item image
            img = soup.find('img', src=re.compile(r'/media/items/'))
            if img:
                results[slug] = img['src']
                print(f"FOUND {slug} -> {img['src']}")
            else:
                # find any media img
                any_img = soup.find('img', src=re.compile(r'/media/'))
                if any_img:
                    results[slug] = any_img['src']
                    print(f"FOUND (alt) {slug} -> {any_img['src']}")
                else:
                    print(f"NO IMG for {slug}")
        else:
            print(f"HTTP {r.status_code} for {slug}")
    except Exception as e:
        print(f"ERROR {slug}: {e}")

print("\nSUMMARY:")
for k, v in results.items():
    print(f"'{k}': '{v}',")
