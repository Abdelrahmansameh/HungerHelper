import requests
from bs4 import BeautifulSoup
import re

headers = {"User-Agent": "Mozilla/5.0"}
for slug in ["borodino", "volcan", "vepr", "cavalier", "morgan", "snub"]:
    url = f"https://hunger-companion.com/items/{slug}"
    r = requests.get(url, headers=headers, timeout=6)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        main_text = soup.get_text(separator="\n", strip=True)
        lines = [l for l in main_text.splitlines() if l]
        print(f"\n=================== {slug.upper()} ===================")
        for i, l in enumerate(lines):
            if any(k in l.lower() for k in ["damage", "penetration", "headshot", "range", "rate of fire", "capacity", "reload", "takes"]):
                for j in range(max(0, i-1), min(len(lines), i+4)):
                    print(f"  {lines[j]}")
                print("  ---")
