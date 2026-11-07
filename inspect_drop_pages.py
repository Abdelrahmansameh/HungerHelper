import urllib.request
from bs4 import BeautifulSoup
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {"User-Agent": "Mozilla/5.0"}

def inspect_page(slug):
    url = f"https://hunger-companion.com/items/{slug}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    print(f"\n=================== {slug} ===================")
    
    # Check all dl, tables, or sections
    for sec in soup.find_all("section"):
        h2 = sec.find(["h2", "h3"])
        print(f"Section [{h2.text.strip() if h2 else 'No title'}]:")
        for item in sec.find_all(["li", "p", "div", "tr"]):
            t = item.get_text(separator=" | ", strip=True)
            if any(w in t.lower() for w in ["drop", "obtain", "creature", "farmer", "sarlat", "farrier", "loose", "rate", "chance", "placed"]):
                print("  ->", t[:150])

inspect_page("peasant-s-burden-spear")
inspect_page("metallurgist-recipe-spear")
