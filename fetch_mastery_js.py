import urllib.request

req = urllib.request.Request('https://hunger-companion.com/assets/js/mastery.js', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    js_content = resp.read().decode('utf-8', errors='ignore')

with open('mastery.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Saved mastery.js, size:", len(js_content))
