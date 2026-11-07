import requests
from bs4 import BeautifulSoup
import os

url = "https://hunger-companion.com/npcs/eloise"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
try:
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")
        img_tags = soup.find_all("img")
        print(f"Found {len(img_tags)} img tags on {url}")
        target_img = None
        for img in img_tags:
            src = img.get("src", "")
            print("  Image src:", src)
            if "eloise" in src.lower() or "npc" in src.lower() or "character" in src.lower():
                target_img = src
                break
        if not target_img and img_tags:
            # First content image
            target_img = img_tags[0].get("src")
            
        if target_img:
            if target_img.startswith("/"):
                target_img = "https://hunger-companion.com" + target_img
            print("Downloading Eloise image from:", target_img)
            img_data = requests.get(target_img, timeout=10).content
            out_file = os.path.abspath("assets/eloise_avatar.png")
            with open(out_file, "wb") as f:
                f.write(img_data)
            print("Saved Eloise avatar to:", out_file)
    else:
        print("Failed to fetch, status code:", resp.status_code)
except Exception as e:
    print("Error:", e)
