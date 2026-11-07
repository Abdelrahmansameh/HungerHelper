import sys, urllib.request, json
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def get_links(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        soup = BeautifulSoup(resp.read().decode("utf-8", errors="ignore"), "html.parser")
        items = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/items/") or href.startswith("/weapons/") or href.startswith("/containers/") or href.startswith("/bestiary/") or href.startswith("/characters/"):
                items.append((href, a.get_text(strip=True)))
        return items

for path in ["/weapons", "/bags", "/containers", "/bestiary", "/characters"]:
    items = get_links(f"https://hunger-companion.com{path}")
    print(f"=== {path}: {len(items)} items ===")
    for href, text in items[:10]:
        print(f"  {href} -> {text}")
