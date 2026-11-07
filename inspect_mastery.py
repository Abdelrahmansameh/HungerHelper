import urllib.request
import re

req = urllib.request.Request('https://hunger-companion.com/mastery', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

with open('mastery_page.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved mastery_page.html, size:", len(html))
