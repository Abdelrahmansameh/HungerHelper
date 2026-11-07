import urllib.request
import re
import os

BASE_URL = "https://hunger-companion.com"

with open("damage_sim.html", "r", encoding="utf-8") as f:
    html = f.read()

media_items = set(re.findall(r"/media/items/[a-zA-Z0-9_\-\.]+", html))

os.makedirs("assets/items", exist_ok=True)
os.makedirs("assets/armor", exist_ok=True)

downloaded = 0
for m in media_items:
    fname = os.path.basename(m)
    if "armor" in fname.lower() or "helmet" in fname.lower():
        local_p = os.path.join("assets/armor", fname)
    else:
        local_p = os.path.join("assets/items", fname)

    if os.path.exists(local_p) and os.path.getsize(local_p) > 0:
        continue

    url = BASE_URL + m
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read()
            with open(local_p, "wb") as out_f:
                out_f.write(data)
            downloaded += 1
            print(f"Downloaded: {fname}")
    except Exception as e:
        print(f"Failed {fname}: {e}")

print(f"Done! Downloaded {downloaded} simulation assets.")
