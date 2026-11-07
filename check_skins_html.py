import urllib.request
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding="utf-8")

req = urllib.request.Request("https://hunger-companion.com/skins", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")

# Check if there are figcaption or mats on /skins
figures = soup.find_all("figure")
print(f"Figures on /skins: {len(figures)}")
if figures:
    for f in figures[:3]:
        print(f.prettify()[:600])

# Check how mats are stored on /skins
mats = soup.find_all(class_=lambda c: c and "mat" in c)
print(f"Mats on /skins: {len(mats)}")
