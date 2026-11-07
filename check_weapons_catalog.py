import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_weapons_catalog():
    url = "https://hunger-companion.com/weapons"
    r = requests.get(url, headers=HEADERS, timeout=8)
    if r.status_code != 200:
        print(f"Error fetching {url}: {r.status_code}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    weapon_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/items/") and href not in weapon_links:
            weapon_links.append(href)

    print(f"Found {len(weapon_links)} weapon URLs in /weapons: {weapon_links}")
    return weapon_links

if __name__ == "__main__":
    scrape_weapons_catalog()
