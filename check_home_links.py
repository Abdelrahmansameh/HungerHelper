import sys, urllib.request
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request("https://hunger-companion.com", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    soup = BeautifulSoup(resp.read().decode("utf-8", errors="ignore"), "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(" ", strip=True)
        if any(w in href for w in ["recipe", "craft", "compendium", "gathering", "trap", "effect", "item", "sim"]):
            print(f"{href} -> {text}")
