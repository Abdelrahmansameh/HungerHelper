import urllib.request
import os

BASE_URL = "https://hunger-companion.com"

assets_to_download = [
    # Bestiary full renders & faces
    ("/media/bestiary/BP_Brute_Parent__full.webp", "assets/bestiary/brute_full.webp"),
    ("/media/bestiary/BP_Brute_Parent__face.webp", "assets/bestiary/brute_face.webp"),
    ("/media/bestiary/BP_Biter_Parent__full.webp", "assets/bestiary/drooler_full.webp"),
    ("/media/bestiary/BP_Biter_Parent__face.webp", "assets/bestiary/drooler_face.webp"),
    ("/media/bestiary/BP_Bloat_Parent__full.webp", "assets/bestiary/bloat_full.webp"),
    ("/media/bestiary/BP_Dreg_Parent__full.webp", "assets/bestiary/dreg_full.webp"),
    ("/media/bestiary/BP_Shambler_Parent__full.webp", "assets/bestiary/shambler_full.webp"),
    ("/media/bestiary/BP_Waif_Parent__full.webp", "assets/bestiary/waif_full.webp"),

    # Character Skins
    ("/media/skins/Eva_Cosmetic_01a.webp", "assets/characters/eva.webp"),
    ("/media/skins/Gabriel_Cosmetic_01a.webp", "assets/characters/gabriel.webp"),
    ("/media/skins/Hugo_Cosmetic_01a.webp", "assets/characters/hugo.webp"),
    ("/media/skins/Marie_Cosmetic_01a.webp", "assets/characters/marie.webp"),
    ("/media/skins/Abel_Cosmetic_01a.webp", "assets/characters/otto.webp"),
    ("/media/skins/Serine_Cosmetic_01a.webp", "assets/characters/serine.webp"),

    # Ability Icons: Eva
    ("/media/abilities/T_UI_Ability_SteelLegs_256.png", "assets/abilities/eva_passive.png"),
    ("/media/abilities/T_UI_Ability_Lightfoot_256.png", "assets/abilities/eva_q.png"),
    ("/media/abilities/T_UI_Ability_Blind_256.png", "assets/abilities/eva_e.png"),

    # Ability Icons: Gabriel
    ("/media/abilities/T_UI_Ability_Charge_256.png", "assets/abilities/gabriel_passive.png"),
    ("/media/abilities/T_UI_Ability_Brace.png", "assets/abilities/gabriel_q.png"),
    ("/media/abilities/T_UI_Ability_Sadist_256.png", "assets/abilities/gabriel_e.png"),

    # Ability Icons: Hugo
    ("/media/abilities/T_UI_Ability_TasteOfBlood_256.png", "assets/abilities/hugo_passive.png"),
    ("/media/abilities/T_UI_Ability_Zealot_256.png", "assets/abilities/hugo_q.png"),
    ("/media/abilities/T_UI_Ability_Maniac_256.png", "assets/abilities/hugo_e.png"),

    # Ability Icons: Marie
    ("/media/abilities/T_UI_Ability_GentleTouch_256.png", "assets/abilities/marie_passive.png"),
    ("/media/abilities/T_UI_Ability_Vespers_256.png", "assets/abilities/marie_q.png"),
    ("/media/abilities/T_UI_Ability_MendingPrayer_256.png", "assets/abilities/marie_e.png"),

    # Ability Icons: Otto
    ("/media/abilities/T_UI_Ability_Maintenance_256.png", "assets/abilities/otto_passive.png"),
    ("/media/abilities/T_UI_Ability_FieldRepairs_256.png", "assets/abilities/otto_q.png"),
    ("/media/abilities/T_UI_Ability_Masterwork_256.png", "assets/abilities/otto_e.png"),

    # Ability Icons: Serine
    ("/media/abilities/T_UI_Ability_VoudouSpirit_256.png", "assets/abilities/serine_passive.png"),
    ("/media/abilities/T_UI_Ability_Rush_256.png", "assets/abilities/serine_q.png"),
    ("/media/abilities/T_UI_Ability_VoudouBomb_256.png", "assets/abilities/serine_e.png"),
]

for rel_url, local_path in assets_to_download:
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        continue
    url = BASE_URL + rel_url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read()
            with open(local_path, "wb") as f:
                f.write(data)
            print(f"Downloaded: {local_path} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed {url}: {e}")

print("Asset download process completed!")
