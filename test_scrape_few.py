import sys, urllib.request, json, time
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

headers = {"User-Agent": "Mozilla/5.0"}

test_slugs = [
    "metallurgist-recipe-spear",
    "peasant-s-burden-spear",
    "cook-recipe-brioche",
    "gunsmith-recipe-volcan",
    "artificer-recipe-damascus-armour-plate"
]

for slug in test_slugs:
    url = f"https://hunger-companion.com/items/{slug}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            print("=" * 50)
            print("SLUG:", slug)
            # Find How to get it
            for div in soup.find_all(["div", "section"]):
                txt = div.get_text(separator=" | ", strip=True)
                if any(w in txt for w in ["Placed in the world", "creature Best:", "In vendor stock", "sells to vendors:"]):
                    print("  INFO:", txt[:200])
        time.sleep(0.5)
    except Exception as e:
        print("ERROR on", slug, e)
