import sys, urllib.request
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

url = "https://hunger-companion.com/items/peasant-s-burden-spear"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    soup = BeautifulSoup(resp.read().decode("utf-8", errors="ignore"), "html.parser")
    # print all text under How to get it
    for a in soup.find_all("a", href=True):
        if "bestiary" in a["href"] or "dreg" in a.text.lower() or "obtain" in a["href"]:
            print("Link:", a["href"], "| Text:", a.text.strip(), "| Parent:", a.parent.text.strip())
