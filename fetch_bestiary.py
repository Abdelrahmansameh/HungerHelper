import urllib.request
import os

url = "https://hunger-companion.com/bestiary"
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("utf-8")
        with open("bestiary_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Downloaded bestiary_page.html successfully! Length:", len(html))
except Exception as e:
    print("Error fetching bestiary:", e)
