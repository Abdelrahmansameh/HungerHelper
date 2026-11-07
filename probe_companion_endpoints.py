import sys, urllib.request, json
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

endpoints = [
    "/weapons",
    "/bags",
    "/containers",
    "/skins",
    "/bestiary",
    "/crafting",
    "/characters",
    "/compendium"
]

for ep in endpoints:
    url = f"https://hunger-companion.com{ep}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            title = soup.find("title").text.strip() if soup.find("title") else ""
            h1 = soup.find("h1").text.strip() if soup.find("h1") else ""
            # find all links on page
            links = [a["href"] for a in soup.find_all("a", href=True)]
            sub_links = [l for l in links if l.startswith(ep) or (ep == "/bestiary" and "/bestiary/" in l)]
            print(f"{ep}: status 200, title='{title}', h1='{h1}', total_links={len(links)}, sub_links={len(sub_links)}")
    except Exception as e:
        print(f"{ep}: ERROR {e}")
