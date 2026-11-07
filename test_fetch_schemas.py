import urllib.request
from bs4 import BeautifulSoup
import json
import sys

headers = {"User-Agent": "Mozilla/5.0"}

urls = [
    "https://hunger-companion.com/items/schemas",
    "https://hunger-companion.com/items/recipes",
    "https://hunger-companion.com/items/peasant-s-burden-spear",
    "https://hunger-companion.com/creatures/dreg",
    "https://hunger-companion.com/creatures/farmer"
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            title = soup.find("title")
            h1 = soup.find("h1")
            print(f"[OK] {url} -> Title: {title.text if title else 'No title'} | H1: {h1.text.strip() if h1 else 'No H1'}")
    except Exception as e:
        print(f"[FAIL] {url} -> {e}")
