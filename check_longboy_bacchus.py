import urllib.request
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding="utf-8")

req = urllib.request.Request("https://hunger-companion.com/items/longboy", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")
print("Longboy page length:", len(html))

# Find section with id "uses-skins" or skins
skins_div = soup.find(id="uses-skins") or soup.find(id="skins") or soup.find(id="uses-cosmetics")
if skins_div:
    print(skins_div.prettify())
else:
    # search for bacchus
    idx = html.lower().find("bacchus")
    if idx != -1:
        print("Found bacchus:\n", html[max(0, idx-200):min(len(html), idx+1500)])
