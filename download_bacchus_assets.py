import urllib.request
import os

os.makedirs("assets/items", exist_ok=True)
os.makedirs("assets/skins", exist_ok=True)

downloads = [
    ("https://hunger-companion.com/media/items/T_UI_Item_MoistPouch.png", "assets/items/T_UI_Item_MoistPouch.png"),
    ("https://hunger-companion.com/media/renders/ID_HipBag_Common01.webp", "assets/items/ID_HipBag_Common01.webp"),
    ("https://hunger-companion.com/media/skins/Skin_Longboy_01a.webp", "assets/skins/Skin_Longboy_01a.webp"),
    ("https://hunger-companion.com/media/items/T_UI_Item_RoyalJelly.png", "assets/items/T_UI_Item_RoyalJelly.png"),
    ("https://hunger-companion.com/media/items/T_UI_Item_PolishedRod.png", "assets/items/T_UI_Item_PolishedRod.png"),
    ("https://hunger-companion.com/media/items/T_UI_Item_WhitePearl.png", "assets/items/T_UI_Item_WhitePearl.png"),
    ("https://hunger-companion.com/media/items/T_UI_Item_IvoryTusk.png", "assets/items/T_UI_Item_IvoryTusk.png"),
    ("https://hunger-companion.com/media/renders/ID_Weap_Pistol_Common02.webp", "assets/items/ID_Weap_Pistol_Common02.webp"),
]

for url, target in downloads:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            with open(target, "wb") as f:
                f.write(data)
            print(f"Downloaded {target} ({len(data)} bytes)")
    except Exception as e:
        print(f"Error {url}: {e}")
