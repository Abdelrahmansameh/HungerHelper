import urllib.request
from bs4 import BeautifulSoup
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

req = urllib.request.Request("https://hunger-companion.com/skins", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")

# Let's inspect skin links and figures on the skins page
skins_data = []

figures = soup.find_all("figure", class_=lambda c: c and "skg__c" in c)
if not figures:
    figures = soup.find_all("div", class_=lambda c: c and "sk-t" in c) or soup.find_all("a", class_=lambda c: c and "sk-t" in c)

print(f"Found {len(figures)} skin elements on /skins")

for f in figures:
    # get skin attributes
    href = f.get("href", "")
    data_t = f.get("data-t", "")
    data_s = f.get("data-s", "")
    data_r = f.get("data-r", "")
    data_o = f.get("data-o", "")
    data_n = f.get("data-n", "")
    img = f.find("img")
    img_src = img.get("src", "") if img else ""
    name_el = f.find("span", class_="sk-t__n") or f.find("b")
    name = name_el.text.strip() if name_el else f.get("title", "")
    if not name and data_n:
        name = data_n.split()[0].title()
    skins_data.append({
        "name": name,
        "type": data_t,
        "subject": data_s,
        "rarity": data_r,
        "obtain": data_o,
        "image": img_src,
        "keywords": data_n,
        "link": href
    })

print(f"Scraped {len(skins_data)} skins. First 5:")
for s in skins_data[:5]:
    print(s)

with open("data/all_skins_summary.json", "w", encoding="utf-8") as out:
    json.dump(skins_data, out, ensure_ascii=False, indent=2)
