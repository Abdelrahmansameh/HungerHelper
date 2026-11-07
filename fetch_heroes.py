import urllib.request
import re

for hero in ['gabriel', 'hugo']:
    url = f'https://hunger-companion.com/characters/{hero}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            with open(f'{hero}_page.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Saved {hero}_page.html, size: {len(content)}")
    except Exception as e:
        print(f"Failed {url}: {e}")
