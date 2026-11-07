import urllib.request
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding="utf-8")

req = urllib.request.Request("https://hunger-companion.com/characters/marie", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")
articles = soup.find_all("article", class_=lambda c: c and "chx" in c)
print(f"Marie has {len(articles)} skins!")
for a in articles:
    h3 = a.find("h3")
    rar = a.find(class_=lambda c: c and "rar" in c)
    mats = a.find_all("li")
    m_info = []
    for m in mats:
        img = m.find("img")
        b = m.find("b")
        span = m.find(class_="chx-mn")
        m_info.append((span.text if span else "", b.text if b else "x1", img.get("src") if img else ""))
    print("  Skin:", h3.text if h3 else "", rar.text if rar else "", "Mats:", m_info)
