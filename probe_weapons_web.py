import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}
for slug in ["borodino", "volcan", "vepr"]:
    url = f"https://hunger-companion.com/items/{slug}"
    try:
        r = requests.get(url, headers=headers, timeout=6)
        print(f"=== {slug} ({r.status_code}) ===")
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            print("Title:", soup.title.get_text() if soup.title else "No title")
            # find stats
            stats_div = soup.find("div", class_="stats") or soup.find("section", class_="stats")
            if stats_div:
                print("Stats div:", stats_div.get_text(strip=True)[:200])
            main = soup.find("main") or soup.body
            if main:
                text = main.get_text(separator=" ", strip=True)
                print("Main sample:", text[:300])
    except Exception as e:
        print(f"Error {slug}: {e}")
