import urllib.request
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding="utf-8")

for url in ["https://hunger-companion.com/characters/marie", "https://hunger-companion.com/characters/eva"]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        skg = soup.find_all(class_="skg__c")
        print(f"URL {url} -> {len(skg)} skins found!")
        for s in skg[:2]:
            b = s.find("b")
            mats = s.find_all("a", class_="mat")
            mat_list = []
            for m in mats:
                img = m.find("img")
                qty = m.find("i")
                mat_list.append((m.get("title", ""), img.get("src", "") if img else "", qty.text if qty else "1"))
            print("  Skin:", b.text if b else "No name", "Mats:", mat_list)
    except Exception as e:
        print("Error:", url, e)
