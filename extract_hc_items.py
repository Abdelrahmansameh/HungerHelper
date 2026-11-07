import urllib.request
from bs4 import BeautifulSoup
import json

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://hunger-companion.com/items"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")
for s in soup.find_all("script"):
    if s.string and "window.HC_ITEMS" in s.string:
        print("Found HC_ITEMS script! Length:", len(s.string))
        # Let's save it to a file so we can inspect it completely
        with open("data/hc_items_script.js", "w", encoding="utf-8") as out:
            out.write(s.string)
        print("Saved to data/hc_items_script.js")
        break
