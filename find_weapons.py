import urllib.request
import re

url = "https://hunger-companion.com/simulation/damage"
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("utf-8")
        with open("damage_sim.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Damage sim length:", len(html))
        weaps = re.findall(r"/media/[^\s\"\'<>]+", html)
        print("Media items:", len(weaps))
        for m in set(weaps):
            if any(k in m.lower() for k in ["weap", "sword", "helmet", "armour", "armor", "longsword"]):
                print(m)
except Exception as e:
    print("Error:", e)
