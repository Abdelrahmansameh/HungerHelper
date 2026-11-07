import urllib.request
from bs4 import BeautifulSoup
import json

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://hunger-companion.com/items"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")

links = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    text = a.get_text(strip=True)
    if "/items/" in href or "schema" in href or "recipe" in href:
        links.append((href, text))

print(f"Found {len(links)} item links on /items")
for l in links[:30]:
    print(l)

# Check categories/filters
cats = soup.find_all(["nav", "div", "ul"], class_=lambda c: c and "cat" in str(c).lower())
for c in cats:
    print("Cat block:", c.get_text(separator=" | ", strip=True)[:200])
