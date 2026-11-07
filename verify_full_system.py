import sys
import os

from co_pilot.brain import CoPilotBrain

b = CoPilotBrain()

test_cases = [
    # 1. Hero abilities & profiles
    ("c'est quoi l'ult de marie", "Acid Flask", "character_marie.jpg"),
    ("c'est quoi le passif de marie", "Alchemical Pouch", "character_marie.jpg"),
    ("passive de marie", "Alchemical Pouch", "character_marie.jpg"),
    ("sort de marie", "Healing Salve", "character_marie.jpg"),
    ("c'est quoi l'ult d'eva", "Flashbang", "character_eva.jpg"),
    ("passif d'eva", "Lightfoot", "character_eva.jpg"),
    ("sort d'eva", "Caltrops", "character_eva.jpg"),
    ("c'est quoi l'ult d'otto", "Iron Will", "character_otto.jpg"),
    ("passif d'otto", "Armor Smith", "character_otto.jpg"),
    ("sort d'otto", "Siegebreaker", "character_otto.jpg"),
    ("ult de hugo", "War Cry", "character_hugo.jpg"),
    ("passif de hugo", "Thick Skin", "character_hugo.jpg"),
    ("competence de hugo", "Fortify", "character_hugo.jpg"),
    ("ult de gabriel", "Sadist's Surge", "character_gabriel.jpg"),
    ("passif de gabriel", "Line Infantry", "character_gabriel.jpg"),
    ("ult de serine", "Vodou Bomb", "character_serine.jpg"),
    ("passif de serine", "Vodou Spirit", "character_serine.jpg"),
    ("fiche de marie", "Warrior Nun", "character_marie.jpg"),
    ("fiche de eva", "Vagabond Huntress", "character_eva.jpg"),
    ("skills de otto", "Sergeant-at-Arms", "character_otto.jpg"),

    # 2. Weapon stats & HTK
    ("combien de coup pour tuer un joueur en blue a la longsword", "Longsword", "weapon_card_longsword.jpg"),
    ("combien de coup pour tuer un joueur en vert avec la longsword", "Longsword", "weapon_card_longsword.jpg"),
    ("combien de coup pour tuer un joueur sans armure a la longsword", "Longsword", "weapon_card_longsword.jpg"),
    ("combien de coups avec la zweihander pour tuer la brute", "Zweihänder", "weapon_card_zweihander.jpg"),
    ("quel est le htk du marengo", "Marengo", "firearm_marengo.jpg"),
    ("montre moi les degat de marengo", "Marengo", "firearm_marengo.jpg"),
    ("montre moi les degat du drak", "Drak", "firearm_drak.jpg"),
    ("les degat du lash", "Lasher", "firearm_lasher.jpg"),
    ("montre moi les degat du pricker", "Pricker", "weapon_card_pricker.jpg"),
    ("montre moi tout les armes a 2 main melee", "Zweihänder", "overview_two_handed_weapons.jpg"),
    ("quelle arme a le meilleur estoc", "Zweihander", "weapon_card_zweihander.jpg"),

    # 3. Skins & Crafting
    ("ou est ce que je peux trouver le skin peasant burden", "Peasant's Burden", "skin_spear_peasants_burden.jpg"),
    ("ou je peux trouver le skin de la spear peasant", "Partisan", "skin_spear_partisan.jpg"),
    ("skin peasant burden", "Peasant's Burden", "skin_spear_peasants_burden.jpg"),
    ("skin bacchus wand", "Bacchus' Wand", "skin_longboy_bacchus_wand.jpg"),
    ("skin loup", "Loup", "skin_rapier_loup.jpg"),
    ("skin basilisk", "Basilisk", "skin_rapier_basilisk.jpg"),
    ("skin solstice", "Solstice", "skin_vepr_solstice.jpg"),
    ("montre moi les skin de la spear", "Partisan", "skin_spear_partisan.jpg"),
    ("montre moi les skin de la rapier", "Loup", "skin_rapier_loup.jpg"),
    ("moist pouch sert a craft quel skin", "Bacchus' Wand", "skin_longboy_bacchus_wand.jpg"),

    # 4. Maps (Blank vs POI)
    ("carte de sombre", "SOMBRE FOREST", "blank_sombre_forest.jpg"),
    ("sarlat", "SARLAT FARM", "blank_sarlat_farm.jpg"),
    ("montre moi sarlat", "SARLAT FARM", "blank_sarlat_farm.jpg"),
    ("map jacques bridge", "JACQUES BRIDGE", "blank_jacques_bridge.jpg"),
    ("ou est la quete piro's nest", "Piro's Missing Convoy", "dynamic_piro_convoy_location_map.jpg"),
    ("ou se trouve family gavroche", "Gavroche Family Camp", "dynamic_gavroche_location_map.jpg"),
    ("donjon jacques folly", "Jacques Folly", "dungeon_jacques_folly.jpg"),

    # 5. Items & Quests
    ("combien coute heavy ammo", "Heavy Ammunition", "item_card_heavy_ammunition.jpg"),
    ("ou est ce que je peux trouver heavy ammo", "Heavy Ammunition", "item_card_heavy_ammunition.jpg"),
    ("montre moi moist pouch", "Moist Pouch", "item_card_moist_pouch.jpg"),
    ("combien coute la farine et ou la trouver", "Flour", "item_card_flour.jpg"),
    ("combien coute le family ring", "Family Ring", "item_card_family-ring.jpg"),
    ("quel quete viens apres celle de mr sweet avec les opium pipe china bowl", "Down From Mount Sinai", "quest_card_down-from-mount-sinai.jpg"),
    ("qui a besoin de farine", "Making Dough", "item_card_flour.jpg"),

    # 6. Bestiary
    ("donne moi le point faible des bloater", "Bloat", "creature_bloat.jpg"),
    ("montre moi le shambler", "Shambler", "creature_shambler.jpg"),
    ("tactique contre le baveux", "Drooler", "creature_drooler.jpg"),

    # 7. Mastery tree & Stash
    ("montre moi mon arbre de talent", "TALENT BUILD", "build_all_trees_highlighted.jpg"),
    ("analyse mon stash pour vendre", "STASH & INVENTORY", "stash_highlighted_grid.jpg")
]

print(f"Total test cases to execute: {len(test_cases)}")
failures = []

for idx, (query, expected_keyword, expected_att) in enumerate(test_cases, 1):
    try:
        res = b.process_message("test", "Abdallah", query)
        disp = res.get("display_text", "")
        att = res.get("image_attachment") or (res.get("image_attachments")[0] if res.get("image_attachments") else None)
        att_base = os.path.basename(att) if att else "None"

        # Verification
        kw_ok = expected_keyword.lower() in disp.lower()
        att_ok = expected_att.lower() in att_base.lower() if att else False

        if kw_ok and att_ok:
            status = "PASS"
        else:
            status = "FAIL"
            failures.append({
                "idx": idx,
                "query": query,
                "expected_kw": expected_keyword,
                "got_kw": kw_ok,
                "expected_att": expected_att,
                "got_att": att_base,
                "disp_snippet": disp[:100].replace("\n", " ")
            })

        print(f"[{status}] #{idx:02d}: '{query}' -> Att: {att_base} | Kw: {kw_ok}")
    except Exception as e:
        failures.append({"idx": idx, "query": query, "error": str(e)})
        print(f"[ERROR] #{idx:02d}: '{query}' -> Exception: {e}")

print("=" * 60)
print(f"RESULTS: {len(test_cases) - len(failures)} / {len(test_cases)} PASSED")
if failures:
    print(f"FAILURES ({len(failures)}):")
    for f in failures:
        print(f"  #{f['idx']}: query '{f['query']}' | expected {f.get('expected_att')} / got {f.get('got_att')}")
else:
    print("ALL TESTS PASSED 100% PERFECTLY (60 / 60)!")
print("=" * 60)
