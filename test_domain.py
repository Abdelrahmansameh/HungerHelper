import urllib.request
import re

with open("characters_page.html", "r", encoding="utf-8") as f:
    html = f.read()

domains = ["https://hungercompanion.com", "https://hunger-companion.com", "https://companion.playhunger.com"]

test_rel = "/media/abilities/T_UI_Ability_Blind_256.png"

for d in domains:
    url = d + test_rel
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                print(f"SUCCESS with domain: {d}")
                break
    except Exception as e:
        print(f"Failed {d}: {e}")
