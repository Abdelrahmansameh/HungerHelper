import os, requests

HEADERS = {'User-Agent': 'Mozilla/5.0'}
BASE_URL = 'https://hunger-companion.com'

ITEM_MAP = {
    'flour': '/media/items/T_UI_Item_CoarseFlour.png',
    'charcoal': '/media/items/T_UI_Item_Charcoal.png',
    'saltpetre': '/media/items/T_UI_Item_SaltPetre.png',
    'damp_rag': '/media/items/T_UI_Item_DampRag.png',
    'tallow_balm': '/media/items/T_UI_Item_TallowBalm.png',
    'china_bowl': '/media/items/T_UI_Item_Bowl.png',
    'opium_pipe': '/media/items/T_UI_Item_OpiumPipe.png',
    'opium': '/media/items/T_UI_Item_Opium.png',
    'votive_candle': '/media/items/T_UI_Item_VotiveCandle.png',
    'book_census': '/media/items/T_UI_Item_FamilyRegister.png',
    'book_rozier': '/media/items/T_UI_Item_GrainRecord.png',
    'book_catechisme': '/media/items/T_UI_Item_ChristianDoctrine.png',
    'book_montesquieu': '/media/items/T_UI_Item_FortificationBlueprint.png',
    'book_buffon': '/media/items/T_UI_Item_TitheLedger.png',
    'book_rondelet': '/media/items/T_UI_Item_SawmillReport.png',
    'silver_key': '/media/items/T_UI_Item_Key_Unique_Bloodbox.png',
    'gold_key': '/media/items/T_UI_Item_Key_Unique_Bloodbox.png'
}

TARGET_DIRS = [
    r'C:\Users\PC\Documents\HungerHelper\assets\items',
    r'C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee\assets\items'
]

for d in TARGET_DIRS:
    os.makedirs(d, exist_ok=True)

for name, rel_url in ITEM_MAP.items():
    url = BASE_URL + rel_url
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        for d in TARGET_DIRS:
            dest = os.path.join(d, f"{name}.png")
            with open(dest, 'wb') as f:
                f.write(r.content)
        print(f"Downloaded correct image for {name} ({len(r.content)} bytes)")
    else:
        print(f"FAILED to download {name}: {r.status_code}")

print("Done downloading exact official item images!")
