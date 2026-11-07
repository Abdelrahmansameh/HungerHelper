import requests
from bs4 import BeautifulSoup
import re

HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Check quest page
url = "https://hunger-companion.com/quests/down-from-mount-sinai"
r = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(r.text, 'html.parser')

with open(r'C:\Users\PC\Documents\HungerHelper\quest_sinai_scraped.txt', 'w', encoding='utf-8') as out:
    out.write("=== ALL TEXT ON QUEST PAGE ===\n")
    for l in soup.stripped_strings:
        out.write(l + "\n")

    books = [
        'census-of-1806',
        'the-spirit-of-the-laws-montesquieu',
        'course-in-agriculture-rozier',
        'course-in-civil-architecture-rondelet',
        'natural-history-general-and-particular-buffon',
        'catechisme-of-christian-doctrine-1567',
        'mortuary-record'
    ]

    out.write("\n=== CHECKING INDIVIDUAL BOOK PAGES ===\n")
    for b in books:
        b_url = f"https://hunger-companion.com/items/{b}"
        res = requests.get(b_url, headers=HEADERS)
        if res.status_code == 200:
            b_soup = BeautifulSoup(res.text, 'html.parser')
            text = " ".join(b_soup.stripped_strings)
            out.write(f"\nITEM: {b}\n")
            out.write(text[:600] + "\n")
        else:
            out.write(f"\nITEM: {b} -> HTTP {res.status_code}\n")

print("Scrape complete, saved to quest_sinai_scraped.txt")
