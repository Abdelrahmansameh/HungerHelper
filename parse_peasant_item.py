import urllib.request
from bs4 import BeautifulSoup
import json

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://hunger-companion.com/items/peasant-s-burden-spear"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")

# Let's see the main sections
print("H1:", soup.find("h1").text.strip() if soup.find("h1") else "None")

# Find how to get it section
print("\n--- HOW TO GET IT ---")
for el in soup.find_all(["section", "div"], class_=lambda c: c and any(k in str(c) for k in ["obtain", "get", "drop", "info", "creature", "item"])):
    t = el.get_text(separator=" | ", strip=True)
    if "creature" in t.lower() or "dreg" in t.lower() or "farmer" in t.lower() or "sells for" in t.lower():
        print(f"[{el.name}.{el.get('class')}] -> {t[:300]}")

# Also find all text in the body to inspect structure
print("\n--- TEXT SNIPPETS ---")
for p in soup.find_all(["p", "li", "span", "a"]):
    txt = p.get_text(strip=True)
    if any(k in txt.lower() for k in ["dreg", "farmer", "sells", "always", "spawn", "schema", "recipe"]):
        print(f"[{p.name}] {txt}")
