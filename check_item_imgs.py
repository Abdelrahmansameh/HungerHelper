import urllib.request
from bs4 import BeautifulSoup
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://hunger-companion.com/items/peasant-s-burden-spear"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")
imgs = soup.find_all("img")
print(f"Total imgs: {len(imgs)}")
for im in imgs:
    print(im.get("src"), im.get("alt"))
