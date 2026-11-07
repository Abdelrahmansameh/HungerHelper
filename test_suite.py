import os
import sys
import unittest
import sqlite3
import time

# Ensure project root is in path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from co_pilot.brain import CoPilotBrain
import universal_v8_engine as stored_cards
import json

class HungerHelperMasterTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("=" * 70)
        print("INITIALIZING HUNGER HELPER MASTER REGRESSION TEST SUITE")
        print("=" * 70)
        cls.brain = CoPilotBrain()

    def _assert_valid_response(self, query: str, res: dict, expected_keywords: list, min_images: int = 1):
        spoken = res.get("spoken_text", "")
        display = res.get("display_text", "")
        img_att = res.get("image_attachment")
        img_atts = res.get("image_attachments") or ([img_att] if img_att else [])

        # 1. Non-empty response
        self.assertTrue(bool(spoken or display), f"Query '{query}' produced empty response!")

        # 2. Zero corrupted characters (tofu \ufffd)
        self.assertNotIn("\ufffd", spoken, f"Query '{query}' has corrupted character in spoken text!")
        self.assertNotIn("\ufffd", display, f"Query '{query}' has corrupted character in display text!")
        self.assertNotIn("[] []", spoken, f"Query '{query}' has tofu boxes in spoken text!")
        self.assertNotIn("[] []", display, f"Query '{query}' has tofu boxes in display text!")

        # 3. Expected keywords
        combined = (spoken + " " + display).lower()
        for kw in expected_keywords:
            self.assertIn(kw.lower(), combined, f"Query '{query}' missing expected keyword: '{kw}'")

        # 4. Attachments validation
        if min_images > 0:
            self.assertGreaterEqual(len(img_atts), min_images, f"Query '{query}' expected at least {min_images} image(s), got {len(img_atts)}")
            for p in img_atts:
                self.assertTrue(os.path.exists(p), f"Attachment does not exist on disk: {p}")
                self.assertGreater(os.path.getsize(p), 5000, f"Attachment file is too small / empty: {p}")

    # -----------------------------------------------------------------------
    # DOMAIN 1: MELEE WEAPONS & 2-HANDED ARSENAL
    # -----------------------------------------------------------------------
    def test_01_spear_stats(self):
        res = self.brain.process_message("t1", "Abdallah", "stats de la spear")
        self._assert_valid_response("stats de la spear", res, ["Spear", "thrust", "heavy", "damage"], min_images=1)

    def test_02_club_damage(self):
        res = self.brain.process_message("t1", "Abdallah", "degats du club")
        self._assert_valid_response("degats du club", res, ["Club", "damage"], min_images=1)

    def test_03_pricker_damage(self):
        res = self.brain.process_message("t1", "Abdallah", "montre moi les degat du pricker")
        self._assert_valid_response("montre moi les degat du pricker", res, ["Pricker", "damage"], min_images=1)

    def test_04_two_handed_arsenal(self):
        res = self.brain.process_message("t1", "Abdallah", "montre moi tout les armes a 2 main melee")
        self._assert_valid_response("montre moi tout les armes a 2 main melee", res, ["Zweihander", "Halberd"], min_images=1)

    # -----------------------------------------------------------------------
    # DOMAIN 2: FIREARMS & BALLISTICS
    # -----------------------------------------------------------------------
    def test_05_marengo_htk(self):
        res = self.brain.process_message("t1", "Abdallah", "quel est le htk du marengo")
        self._assert_valid_response("quel est le htk du marengo", res, ["Marengo", "damage"], min_images=1)

    def test_06_le_deux_price_and_vendor(self):
        res = self.brain.process_message("t1", "Abdallah", "combien vaut le deux")
        self._assert_valid_response("combien vaut le deux", res, ["Deux", "silver"], min_images=1)

    def test_07_drak_firearm(self):
        res = self.brain.process_message("t1", "Abdallah", "montre moi les degat du drak")
        self._assert_valid_response("montre moi les degat du drak", res, ["Drak", "damage"], min_images=1)

    def test_08_lasher_firearm(self):
        res = self.brain.process_message("t1", "Abdallah", "les degat du lash")
        self._assert_valid_response("les degat du lash", res, ["Lasher", "damage"], min_images=1)

    # -----------------------------------------------------------------------
    # DOMAIN 3: COSMETIC SKINS & DROPS
    # -----------------------------------------------------------------------
    def test_09_rapier_skins(self):
        res = self.brain.process_message("t1", "Abdallah", "montre moi les skins de la rapier")
        self._assert_valid_response("montre moi les skins de la rapier", res, ["Loup", "Basilisk"], min_images=2)

    def test_10_spear_peasant_burden_drop(self):
        res = self.brain.process_message("t1", "Abdallah", "ou je peux trouver le skin de la spear peasant")
        self._assert_valid_response("ou je peux trouver le skin de la spear peasant", res, ["Peasant's Burden", "Dreg Farmer", "Garnier"], min_images=1)

    def test_11_axe_skins(self):
        res = self.brain.process_message("t1", "Abdallah", "montre moi les skins de la axe")
        self._assert_valid_response("montre moi les skins de la axe", res, ["Padre's Reply", "Recluse"], min_images=2)

    # -----------------------------------------------------------------------
    # DOMAIN 4: CRAFTING RECIPES & SCHEMAS
    # -----------------------------------------------------------------------
    def test_12_metallurgist_recipe_spear(self):
        res = self.brain.process_message("t1", "Abdallah", "metallurgist recipe spear")
        self._assert_valid_response("metallurgist recipe spear", res, ["Spear", "Recipe"], min_images=1)

    def test_13_cook_recipe_brioche(self):
        res = self.brain.process_message("t1", "Abdallah", "cook recipe brioche")
        self._assert_valid_response("cook recipe brioche", res, ["Brioche", "Recipe"], min_images=1)

    def test_14_artificer_recipe_damascus(self):
        res = self.brain.process_message("t1", "Abdallah", "artificer recipe damascus armour plate")
        self._assert_valid_response("artificer recipe damascus armour plate", res, ["Damascus", "Recipe"], min_images=1)

    # -----------------------------------------------------------------------
    # DOMAIN 5: BAGS & CAPACITY (ALL 29 BAGS)
    # -----------------------------------------------------------------------
    def test_15_coldstream_pack_slots(self):
        res = self.brain.process_message("t1", "Abdallah", "combien de slots a coldstream pack")
        self._assert_valid_response("combien de slots a coldstream pack", res, ["Coldstream Pack", "22", "slots", "280 silver"], min_images=1)

    def test_16_ludwigs_drumcase_slots(self):
        res = self.brain.process_message("t1", "Abdallah", "ludwig's drumcase")
        self._assert_valid_response("ludwig's drumcase", res, ["Ludwig's Drumcase", "12", "slots"], min_images=1)

    def test_17_moist_pouch_bag(self):
        res = self.brain.process_message("t1", "Abdallah", "montre moi moist pouch")
        self._assert_valid_response("montre moi moist pouch", res, ["Moist Pouch", "10", "slots"], min_images=1)

    # -----------------------------------------------------------------------
    # DOMAIN 6: ITEMS & RESALE VALUES (700 ITEMS)
    # -----------------------------------------------------------------------
    def test_18_heavy_ammo_cost(self):
        res = self.brain.process_message("t1", "Abdallah", "combien coute heavy ammo")
        self._assert_valid_response("combien coute heavy ammo", res, ["Heavy Ammunition", "2 silver 0 copper"], min_images=1)

    def test_19_heavy_ammo_location(self):
        res = self.brain.process_message("t1", "Abdallah", "ou est ce que je peux trouver heavy ammo")
        self._assert_valid_response("ou est ce que je peux trouver heavy ammo", res, ["Heavy Ammunition", "Voyant", "Munitions Crate"], min_images=1)

    def test_20_flour_resale(self):
        res = self.brain.process_message("t1", "Abdallah", "farine")
        self._assert_valid_response("farine", res, ["Flour", "3 copper"], min_images=1)

    # -----------------------------------------------------------------------
    # DOMAIN 7: HERO KITS & ABILITIES
    # -----------------------------------------------------------------------
    def test_21_marie_ult(self):
        res = self.brain.process_message("t1", "Abdallah", "c'est quoi l'ult de marie")
        self._assert_valid_response("c'est quoi l'ult de marie", res, ["Acid Flask", "Marie"], min_images=1)

    def test_22_marie_passive(self):
        res = self.brain.process_message("t1", "Abdallah", "passive de marie")
        self._assert_valid_response("passive de marie", res, ["Alchemical Pouch", "Marie"], min_images=1)

    def test_23_eva_ult(self):
        res = self.brain.process_message("t1", "Abdallah", "c'est quoi l'ult d'eva")
        self._assert_valid_response("c'est quoi l'ult d'eva", res, ["Flashbang", "Eva"], min_images=1)

    def test_24_otto_passive(self):
        res = self.brain.process_message("t1", "Abdallah", "passif de otto")
        self._assert_valid_response("passif de otto", res, ["Armor Smith", "Otto"], min_images=1)

    def test_25_hugo_ult(self):
        res = self.brain.process_message("t1", "Abdallah", "ult de hugo")
        self._assert_valid_response("ult de hugo", res, ["War Cry", "Hugo"], min_images=1)

    # -----------------------------------------------------------------------
    # DOMAIN 8: BESTIARY & MONSTERS
    # -----------------------------------------------------------------------
    def test_26_brute_stats(self):
        res = self.brain.process_message("t1", "Abdallah", "stats de la brute")
        self._assert_valid_response("stats de la brute", res, ["Brute", "900", "Back Criticals"], min_images=1)

    def test_27_pale_lady_hp(self):
        res = self.brain.process_message("t1", "Abdallah", "combien de pv a la pale lady")
        self._assert_valid_response("combien de pv a la pale lady", res, ["Pale Lady", "900", "Stagger"], min_images=1)

    def test_28_bloater_weakpoint(self):
        res = self.brain.process_message("t1", "Abdallah", "donne moi le point faible des bloater")
        self._assert_valid_response("donne moi le point faible des bloater", res, ["Bloat", "Acid Sacs"], min_images=1)

    # -----------------------------------------------------------------------
    # DOMAIN 9: TRAPS, STATUS EFFECTS & GATHERING
    # -----------------------------------------------------------------------
    def test_29_explosive_trap(self):
        res = self.brain.process_message("t1", "Abdallah", "explosive trap")
        self._assert_valid_response("explosive trap", res, ["Explosive Trap", "60", "4 m", "115"], min_images=1)

    def test_30_light_bleed_status(self):
        res = self.brain.process_message("t1", "Abdallah", "c'est quoi light bleed")
        self._assert_valid_response("c'est quoi light bleed", res, ["Light Bleed", "Bleed Timed"], min_images=1)

    def test_31_garlic_bulb_gathering(self):
        res = self.brain.process_message("t1", "Abdallah", "ou trouver garlic bulb")
        self._assert_valid_response("ou trouver garlic bulb", res, ["Garlic Bulb", "90 %", "2-6"], min_images=1)

    def test_32_munitions_crate_container(self):
        res = self.brain.process_message("t1", "Abdallah", "munitions crate")
        self._assert_valid_response("munitions crate", res, ["Munitions Crate", "646"], min_images=1)

    # -----------------------------------------------------------------------
    # DOMAIN 10: MAPS & DUNGEON NAVIGATION
    # -----------------------------------------------------------------------
    def test_33_sombre_blank_map(self):
        res = self.brain.process_message("t1", "Abdallah", "carte sans indication sombre")
        self._assert_valid_response("carte sans indication sombre", res, ["Sombre Forest", "blank"], min_images=1)

    def test_34_sarlat_clean_map(self):
        res = self.brain.process_message("t1", "Abdallah", "sarlat")
        self._assert_valid_response("sarlat", res, ["Sarlat Farm", "blank"], min_images=1)

    def test_35_piro_lens_location(self):
        res = self.brain.process_message("t1", "Abdallah", "piro's lens")
        self._assert_valid_response("piro's lens", res, ["Piro's Lens", "Rat's Nest Cave", "Jacques Bridge"], min_images=1)

    def test_36_piro_convoy_location(self):
        res = self.brain.process_message("t1", "Abdallah", "ou est la quete piro's nest")
        self._assert_valid_response("ou est la quete piro's nest", res, ["Piro's Convoy", "Jacques Bridge", "848.20"], min_images=1)

    def test_37_jacques_folly_dungeon(self):
        res = self.brain.process_message("t1", "Abdallah", "donjon jacques folly")
        self._assert_valid_response("donjon jacques folly", res, ["Jacques Folly", "1680.4"], min_images=1)

    # -----------------------------------------------------------------------
    # DOMAIN 11: STASH SCANNER & DUAL IMAGES
    # -----------------------------------------------------------------------
    def test_38_stash_dual_images(self):
        res = self.brain.process_message("t1", "Abdallah", "analyse mon stash pour vendre")
        self._assert_valid_response("analyse mon stash pour vendre", res, ["STASH", "EXP RULE", "PRESERVED"], min_images=2)

    # -----------------------------------------------------------------------
    # DOMAIN 12: CANONICAL GAME LORE & WORLDBUILDING
    # -----------------------------------------------------------------------
    def test_39_lore_the_hunger(self):
        res = self.brain.process_message("t1", "Abdallah", "c'est quoi the hunger")
        self._assert_valid_response("c'est quoi the hunger", res, ["Hunger", "Calamity"], min_images=1)

    def test_40_lore_mr_sweet(self):
        res = self.brain.process_message("t1", "Abdallah", "who is mr sweet")
        self._assert_valid_response("who is mr sweet", res, ["Sweet", "Broker"], min_images=1)

    def test_41_lore_chateau_sanctuary(self):
        res = self.brain.process_message("t1", "Abdallah", "histoire du chateau")
        self._assert_valid_response("histoire du chateau", res, ["Château", "Sanctuary"], min_images=1)


    # -----------------------------------------------------------------------
    # DOMAIN 13: ADVANCED ARSENAL & COMBAT HTK DISPATCHER (SCREENSHOT FIXES)
    # -----------------------------------------------------------------------
    def test_42_borodino_typo_htk(self):
        res = self.brain.process_message("t1", "Abdallah", "combien de coup avec un borondi pour uer du violet")
        self._assert_valid_response("combien de coup avec un borondi pour uer du violet", res, ["Borodino", "180 HP", "headshot", "body"], min_images=1)
        self.assertEqual(stored_cards.render_pure_english_firearm_card('borodino'), res.get("image_attachment", ""))

    def test_43_volcan_damage(self):
        res = self.brain.process_message("t1", "Abdallah", "les degats de volcan")
        self._assert_valid_response("les degats de volcan", res, ["Volcan", "36", "Refined Ammunition"], min_images=1)
        self.assertEqual(stored_cards.render_pure_english_firearm_card('volcan'), res.get("image_attachment", ""))

    def test_44_two_handed_melee_english(self):
        res = self.brain.process_message("t1", "Abdallah", "show me every 2 hand melee")
        self._assert_valid_response("show me every 2 hand melee", res, ["2-HANDED MELEE ARSENAL", "Zweihänder", "Halberd"], min_images=1)
        self.assertEqual(stored_cards.render_two_handed_melee_overview_card(), res.get("image_attachment", ""))
        self.assertNotIn("Handkerchief", res.get("display_text", ""))

    def test_45_one_handed_melee_english(self):
        res = self.brain.process_message("t1", "Abdallah", "show me every 1 hand melee")
        self._assert_valid_response("show me every 1 hand melee", res, ["1-HANDED MELEE ARSENAL", "Sabre", "Rapier", "Mace"], min_images=1)
        self.assertEqual(stored_cards.render_one_handed_melee_overview_card(), res.get("image_attachment", ""))

    def test_46_grey_armor_tier_htk(self):
        res = self.brain.process_message("t1", "Abdallah", "combien de coup avec la mace pour tuer du gris")
        self._assert_valid_response("combien de coup avec la mace pour tuer du gris", res, ["Mace", "120 HP"], min_images=1)
        self.assertEqual(stored_cards.render_pure_english_melee_card('mace'), res.get("image_attachment", ""))



    # -----------------------------------------------------------------------
    # DOMAIN 14: MULTI-SKINS, CHARACTER DOSSIERS & BESTIARY MAPS (LATEST USER FIXES)
    # -----------------------------------------------------------------------
    def test_47_dagger_all_8_skins(self):
        res = self.brain.process_message("t1", "Abdallah", "show me dagger skins")
        self._assert_valid_response("show me dagger skins", res, ["ALL OFFICIAL SKINS FOR DAGGER", "Sindle", "Tenebris", "Stag", "Emperor's Talon", "Golgotha", "Trident", "Misericorde"], min_images=8)
        self.assertGreaterEqual(len(res.get("image_attachments", [])), 8)
        with open(os.path.join(ROOT_DIR, "data", "full_companion_skins.json"), encoding="utf-8") as source:
            skins = json.load(source)
        dagger_skins = []
        for skin in skins.values():
            if skin.get("target", "").lower() == "dagger" and skin["name"].strip() not in {s["name"].strip() for s in dagger_skins}:
                dagger_skins.append(skin)
        self.assertIn(stored_cards.render_weapon_skins_showcase_sheet("Dagger", dagger_skins),
                      res.get("image_attachments", []))

    def test_48_otto_prestige_skins(self):
        res = self.brain.process_message("t1", "Abdallah", "show me otto prestige skins")
        self._assert_valid_response("show me otto prestige skins", res, ["OFFICIAL PRESTIGE SKINS : OTTO", "Siegebreaker", "Black Reiter"], min_images=2)
        self.assertEqual(len(res.get("image_attachments", [])), 2)
        self.assertNotIn("Eva", res.get("display_text", ""))
        self.assertNotIn("Mademoiselle Rouge", res.get("display_text", ""))

    def test_49_farmer_dreg_spawn_map(self):
        res = self.brain.process_message("t1", "Abdallah", "where can i find farmer dreg")
        self._assert_valid_response("where can i find farmer dreg", res, ["Farmer Dreg", "Garnier's Farm", "Peasant's Burden", "100% ALWAYS"], min_images=1)
        self.assertIn("dynamic_farmer_dreg_map.jpg", res.get("image_attachment", ""))
        self.assertNotIn("DREG HEAD", res.get("display_text", "").split("•")[0])

    def test_50_creatures_all_20_spawns_map(self):
        res = self.brain.process_message("t1", "Abdallah", "show me a map with all the brute and drooler spawns")
        self._assert_valid_response("show me a map with all the brute and drooler spawns", res, ["ALL 20 CREATURE", "Droolers", "Brutes", "Farmer Dreg"], min_images=1)
        self.assertIn("dynamic_creatures_map.jpg", res.get("image_attachment", ""))

    def test_51_universal_bestiary_sombre_drooler(self):
        res = self.brain.process_message("t1", "Abdallah", "drooler map sombre forest")
        self._assert_valid_response("drooler map sombre forest", res, ["SOMBRE FOREST", "21 confirmed spawner points", "9.8 per raid"], min_images=1)
        self.assertIn("dynamic_creatures_map.jpg", res.get("image_attachment", ""))

    def test_52_universal_bestiary_jacques_brute(self):
        res = self.brain.process_message("t1", "Abdallah", "brute map jacques bridge")
        self._assert_valid_response("brute map jacques bridge", res, ["JACQUES BRIDGE", "20 confirmed spawner points", "9.3 per raid"], min_images=1)
        self.assertIn("dynamic_creatures_map.jpg", res.get("image_attachment", ""))

    def test_53_universal_bestiary_sarlat_bloat(self):
        res = self.brain.process_message("t1", "Abdallah", "bloat map sarlat farm")
        self._assert_valid_response("bloat map sarlat farm", res, ["SARLAT FARM", "17 confirmed spawner points", "BLOAT SPAWNS"], min_images=1)
        self.assertIn("dynamic_creatures_map.jpg", res.get("image_attachment", ""))

    def test_54_peasant_burden_drop_intel(self):
        res = self.brain.process_message("t1", "Abdallah", "peasant burden")
        self._assert_valid_response("peasant burden", res, ["Dreg Farmer", "100% Always Drop", "Garnier's Farm", "1 in 20 raids"], min_images=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
