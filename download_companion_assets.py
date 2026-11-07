import os, sys, json, requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
BASE_URL = 'https://hunger-companion.com'
DOC_DIR = r'C:\Users\PC\Documents\HungerHelper'
ITEM_DIR = os.path.join(DOC_DIR, 'assets', 'items')
CONTAINER_DIR = os.path.join(DOC_DIR, 'assets', 'containers')
os.makedirs(ITEM_DIR, exist_ok=True)
os.makedirs(CONTAINER_DIR, exist_ok=True)

# 1. Download specific key item and container images for raid planner
ITEM_URLS = {
    'flour': '/media/items/T_UI_Item_CoarseFlour.png',
    'charcoal': '/media/items/T_UI_Item_CrispCarrot.png',
    'saltpetre': '/media/items/T_UI_Item_MilkyGlass.png',
    'damp_rag': '/media/items/T_UI_Item_CoarseSand.png',
    'tallow_balm': '/media/items/T_UI_Item_LeadOre.png',
    'china_bowl': '/media/items/T_UI_Item_GravyBoat.png',
    'opium_pipe': '/media/items/T_UI_Item_CashmereShawl.png',
    'opium': '/media/items/T_UI_Item_SunRipenedHaunch.png',
    'votive_candle': '/media/items/T_UI_Item_VotiveCandle.png',
    'book_census': '/media/items/T_UI_Item_FamilyRegister.png',
    'book_rozier': '/media/items/T_UI_Item_GrainRecord.png',
    'book_catechisme': '/media/items/T_UI_Item_ChristianDoctrine.png',
    'book_montesquieu': '/media/items/T_UI_Item_FortificationBlueprint.png',
    'book_buffon': '/media/items/T_UI_Item_SawmillReport.png',
    'book_mortuary': '/media/items/T_UI_Item_MortuaryRecord.png',
    'book_rondelet': '/media/items/T_UI_Item_SawmillReport.png',
    'silver_key': '/media/items/T_UI_Item_Key_Unique_Bronze.png',
    'gold_key': '/media/items/T_UI_Item_Key_Unique_Bronze.png'
}

CONTAINER_URLS = {
    'flour_sack': '/media/containers/flour-sack.webp',
    'oak_barrel': '/media/containers/oak-barrel.webp',
    'pile_of_ash': '/media/containers/pile-of-ash.webp',
    'tooling_bin': '/media/containers/tooling-bin.webp',
    'stone_grave': '/media/containers/stone-grave.webp',
    'physician_bag': '/media/containers/physician-bag.webp',
    'jacques_medicinals': '/media/containers/jacque-s-medicinals.webp',
    'wall_cabinet': '/media/containers/wall-cabinet.webp',
    'bullion_box': '/media/containers/bullion-box.webp',
    'ledger_desk': '/media/containers/ledger-desk.webp',
    'strongbox': '/media/containers/large-strongbox.webp',
    'basket': '/media/containers/basket.webp'
}

print("1. Downloading Item Icons...")
for name, path in ITEM_URLS.items():
    dest = os.path.join(ITEM_DIR, f"{name}.png")
    if not os.path.exists(dest):
        try:
            r = requests.get(BASE_URL + path, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                with open(dest, 'wb') as f:
                    f.write(r.content)
                print(f"  Downloaded item: {name}")
            else:
                print(f"  Failed {name}: {r.status_code}")
        except Exception as e:
            print(f"  Error {name}: {e}")
    else:
        print(f"  Exists: {name}")

print("2. Downloading Container Icons...")
for name, path in CONTAINER_URLS.items():
    dest = os.path.join(CONTAINER_DIR, f"{name}.webp")
    if not os.path.exists(dest):
        try:
            r = requests.get(BASE_URL + path, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                with open(dest, 'wb') as f:
                    f.write(r.content)
                print(f"  Downloaded container: {name}")
            else:
                print(f"  Failed {name}: {r.status_code}")
        except Exception as e:
            print(f"  Error {name}: {e}")
    else:
        print(f"  Exists: {name}")

print("Assets download finished successfully!")
