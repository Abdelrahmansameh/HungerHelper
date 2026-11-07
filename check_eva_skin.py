import urllib.request
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding="utf-8")

req = urllib.request.Request("https://hunger-companion.com/characters/eva", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

idx = html.find("Eva_Cosmetic_02a")
if idx != -1:
    print(html[max(0, idx-200):min(len(html), idx+1200)])
else:
    print("Not found in /characters/eva")
