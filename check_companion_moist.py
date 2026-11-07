import json
import urllib.request
import re

# Let's check en_urls.json to see all URLs
with open("en_urls.json", "r", encoding="utf-8") as f:
    urls = json.load(f)
    print("Total URLs:", len(urls))
    cosmetic_urls = [u for u in urls if any(k in u.lower() for k in ["skin", "cosmetic", "craft", "tailor", "recipe", "pouch"])]
    print("Interesting URLs:", cosmetic_urls[:20])

# Let's check hunger-companion.com for moist-pouch
url = "https://hunger-companion.com/items/moist-pouch"
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        print("HTML length for moist-pouch:", len(html))
        # Search for images, recipes, craft, etc. in html
        for line in html.splitlines():
            if any(k in line.lower() for k in ["craft", "recipe", "skin", "cosmetic", "t_ui_item_moistpouch", "webp", "tailor", "used for", "used in"]):
                print("HTML line:", line.strip()[:150])
except Exception as e:
    print("Error fetching moist-pouch page:", e)
