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

print("--- ALL LINKS AND PARENTS IN OBTAIN OR ESSENTIALS ---")
for sec in soup.find_all("section"):
    for a in sec.find_all("a"):
        print(f"Link: href='{a.get('href')}', text='{a.get_text(strip=True)}', parent={a.parent.get_text(separator=' | ', strip=True)}")
