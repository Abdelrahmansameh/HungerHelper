import urllib.request
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://hunger-companion.com/characters'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

with open('characters_page.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved characters_page.html")
# Look for Hugo and Gabriel
for match in re.finditer(r'(Hugo|Gabriel)[^<]{0,200}', html, re.IGNORECASE):
    print(match.group(0))
    print('-'*20)
