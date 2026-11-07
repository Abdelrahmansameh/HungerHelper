import sys, urllib.request, json
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

for path in ["/recipes", "/gathering", "/traps", "/effects"]:
    url = f"https://hunger-companion.com{path}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            soup = BeautifulSoup(resp.read().decode("utf-8", errors="ignore"), "html.parser")
            items = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if any(href.startswith(p) for p in ["/items/", "/recipes/", "/gathering/", "/traps/", "/effects/"]):
                    items.append((href, a.get_text(" ", strip=True)))
            print(f"=== {path}: {len(items)} items found ===")
            for h, t in items[:5]:
                print(f"  {h} -> {t}")
    except Exception as e:
        print(f"ERROR on {path}: {e}")
