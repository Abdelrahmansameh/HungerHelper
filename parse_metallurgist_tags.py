import urllib.request
from bs4 import BeautifulSoup
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://hunger-companion.com/items/metallurgist-recipe-spear"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")

print("--- METALLURGIST RECIPE SPEAR LINKS ---")
for a in soup.find_all("a", href=True):
    href = a["href"]
    if "#obtain" in href or "bestiary" in href or "vendor" in href or "#unlocks" in href:
        print(f"href='{href}', text='{a.get_text(separator=' ', strip=True)}', parent='{a.parent.get_text(separator=' | ', strip=True)}'")
