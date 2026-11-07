import urllib.request
from bs4 import BeautifulSoup
import json

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://hunger-companion.com/items"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")

# Look at category tabs or filters
filters = soup.find_all(["a", "button"], class_=lambda c: c and any(k in str(c) for k in ["filter", "tab", "nav", "pill", "category", "cat"]))
print(f"Found {len(filters)} filter elements")
for f in filters[:30]:
    print(f.name, f.get("class"), f.get("href"), f.get_text(strip=True))

# Look for data attributes or script JSON tags
scripts = soup.find_all("script")
print(f"Found {len(scripts)} scripts")
for s in scripts:
    if s.string and any(k in s.string for k in ["items", "schemas", "recipes", "peasant"]):
        print("Script snippet:", s.string[:200])
