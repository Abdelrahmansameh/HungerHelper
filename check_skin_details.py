import urllib.request
from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

def get_page(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8", errors="ignore")

# Let's inspect the moist-pouch page around "Skin_Longboy_01a"
pouch_html = get_page("https://hunger-companion.com/items/moist-pouch")
idx = pouch_html.find("Skin_Longboy_01a")
if idx != -1:
    print("Context around Skin_Longboy_01a on moist-pouch page:")
    print(pouch_html[max(0, idx-500):min(len(pouch_html), idx+1000)])

# Let's search where "moist-pouch" or "Moist Pouch" appears in skins
skins_html = get_page("https://hunger-companion.com/skins")
for m in re.finditer(r'moist', skins_html, re.I):
    start = max(0, m.start() - 300)
    end = min(len(skins_html), m.end() + 300)
    print("\n--- Skin match ---")
    print(skins_html[start:end])
