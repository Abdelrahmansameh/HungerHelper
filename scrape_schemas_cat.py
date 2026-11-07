import urllib.request
from bs4 import BeautifulSoup
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://hunger-companion.com/items?cat=schema"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")
schema_links = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.startswith("/items/") and "#" not in href:
        slug = href.replace("/items/", "").strip("/")
        if slug not in schema_links:
            schema_links.append((slug, a.get_text(strip=True)))

print(f"Total schemas listed on /items?cat=schema: {len(schema_links)}")
for s in schema_links[:20]:
    print(s)

with open("data/all_schemas_list.json", "w", encoding="utf-8") as f:
    json.dump(schema_links, f, indent=2)
