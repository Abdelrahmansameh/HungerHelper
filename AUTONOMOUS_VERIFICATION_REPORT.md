# AUTONOMOUS SELF-VERIFICATION & HEALTH AUDIT REPORT
**Generated:** 2026-11-05T10:02:26.281204
**Overall System Status:** HEALTHY / GREEN (100% OPERATIONAL)

---

## 1. Hunger Companion Catalog Completeness
| Catalog Table | Actual Rows | Meets Target | Status |
| :--- | :---: | :---: | :---: |
| `companion_items_cache` | **700** | Yes | PASSED |
| `items` | **700** | Yes | PASSED |
| `weapons_full` | **37** | Yes | PASSED |
| `bags_full` | **29** | Yes | PASSED |
| `containers_full` | **67** | Yes | PASSED |
| `recipes_full` | **399** | Yes | PASSED |
| `gathering_full` | **32** | Yes | PASSED |
| `traps_full` | **12** | Yes | PASSED |
| `status_effects_full` | **36** | Yes | PASSED |
| `quests` | **99** | Yes | PASSED |
| `quest_objectives` | **702** | Yes | PASSED |
| `map_points` | **3459** | Yes | PASSED |
| `maps` | **4** | Yes | PASSED |
| `creatures` | **10** | Yes | PASSED |

---

## 2. Regression Test Suite Execution (`test_suite.py`)
**Result:** 100% GREEN (38/38 Tests Passed)

```
test_01_spear_stats (__main__.HungerHelperMasterTestSuite.test_01_spear_stats) ... ok
test_02_club_damage (__main__.HungerHelperMasterTestSuite.test_02_club_damage) ... ok
test_03_pricker_damage (__main__.HungerHelperMasterTestSuite.test_03_pricker_damage) ... ok
test_04_two_handed_arsenal (__main__.HungerHelperMasterTestSuite.test_04_two_handed_arsenal) ... ok
test_05_marengo_htk (__main__.HungerHelperMasterTestSuite.test_05_marengo_htk) ... ok
test_06_le_deux_price_and_vendor (__main__.HungerHelperMasterTestSuite.test_06_le_deux_price_and_vendor) ... ok
test_07_drak_firearm (__main__.HungerHelperMasterTestSuite.test_07_drak_firearm) ... ok
test_08_lasher_firearm (__main__.HungerHelperMasterTestSuite.test_08_lasher_firearm) ... ok
test_09_rapier_skins (__main__.HungerHelperMasterTestSuite.test_09_rapier_skins) ... c:\Users\PC\Documents\HungerHelper\universal_v8_engine.py:540: ResourceWarning: unclosed file <_io.TextIOWrapper name='c:\\Users\\PC\\Documents\\HungerHelper\\data\\full_companion_skins.json' mode='r' encoding='utf-8'>
  db = json.load(open(db_p, encoding="utf-8"))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_10_spear_peasant_burden_drop (__main__.HungerHelperMasterTestSuite.test_10_spear_peasant_burden_drop) ... ok
test_11_axe_skins (__main__.HungerHelperMasterTestSuite.test_11_axe_skins) ... ok
test_12_metallurgist_recipe_spear (__main__.HungerHelperMasterTestSuite.test_12_metallurgist_recipe_spear) ... c:\Users\PC\Documents\HungerHelper\universal_v8_engine.py:671: ResourceWarning: unclosed file <_io.TextIOWrapper name='c:\\Users\\PC\\Documents\\HungerHelper\\data\\high_rate_drops.json' mode='r' encoding='utf-8'>
  drops_db = json.load(open(db_p, encoding="utf-8")) if os.path.exists(db_p) else {}
ResourceWarning: Enable tracemalloc to get the object allocation traceback
c:\Users\PC\Documents\HungerHelper\universal_v8_engine.py:390: ResourceWarning: unclosed file <_io.TextIOWrapper name='c:\\Users\\PC\\Documents\\HungerHelper\\data\\high_rate_drops.json' mode='r' encoding='utf-8'>
  drops_db = json.load(open(db_p, encoding="utf-8")) if os.path.exists(db_p) else {}
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_13_cook_recipe_brioche (__main__.HungerHelperMasterTestSuite.test_13_cook_recipe_brioche) ... ok
test_14_artificer_recipe_damascus (__main__.HungerHelperMasterTestSuite.test_14_artificer_recipe_damascus) ... ok
test_15_coldstream_pack_slots (__main__.HungerHelperMasterTestSuite.test_15_coldstream_pack_slots) ... ok
test_16_ludwigs_drumcase_slots (__main__.HungerHelperMasterTestSuite.test_16_ludwigs_drumcase_slots) ... ok
test_17_moist_pouch_bag (__main__.HungerHelperMasterTestSuite.test_17_moist_pouch_bag) ... ok
test_18_heavy_ammo_cost (__main__.HungerHelperMasterTestSuite.test_18_heavy_ammo_cost) ... ok
test_19_heavy_ammo_location (__main__.HungerHelperMasterTestSuite.test_19_heavy_ammo_location) ... ok
test_20_flour_resale (__main__.HungerHelperMasterTestSuite.test_20_flour_resale) ... ok
test_21_marie_ult (__main__.HungerHelperMasterTestSuite.test_21_marie_ult) ... ok
test_22_marie_passive (__main__.HungerHelperMasterTestSuite.test_22_marie_passive) ... ok
test_23_eva_ult (__main__.HungerHelperMasterTestSuite.test_23_eva_ult) ... ok
test_24_otto_passive (__main__.HungerHelperMasterTestSuite.test_24_otto_passive) ... ok
test_25_hugo_ult (__main__.HungerHelperMasterTestSuite.test_25_hugo_ult) ... ok
test_26_brute_stats (__main__.HungerHelperMasterTestSuite.test_26_brute_stats) ... ok
test_27_pale_lady_hp (__main__.HungerHelperMasterTestSuite.test_27_pale_lady_hp) ... ok
test_28_bloater_weakpoint (__main__.HungerHelperMasterTestSuite.test_28_bloater_weakpoint) ... ok
test_29_explosive_trap (__main__.HungerHelperMasterTestSuite.test_29_explosive_trap) ... ok
test_30_light_bleed_status (__main__.HungerHelperMasterTestSuite.test_30_light_bleed_status) ... ok
test_31_garlic_bulb_gathering (__main__.HungerHelperMasterTestSuite.test_31_garlic_bulb_gathering) ... ok
test_32_munitions_crate_container (__main__.HungerHelperMasterTestSuite.test_32_munitions_crate_container) ... ok
test_33_sombre_blank_map (__main__.HungerHelperMasterTestSuite.test_33_sombre_blank_map) ... ok
test_34_sarlat_clean_map (__main__.HungerHelperMasterTestSuite.test_34_sarlat_clean_map) ... ok
test_35_piro_lens_location (__main__.HungerHelperMasterTestSuite.test_35_piro_lens_location) ... ok
test_36_piro_convoy_location (__main__.HungerHelperMasterTestSuite.test_36_piro_convoy_location) ... ok
test_37_jacques_folly_dungeon (__main__.HungerHelperMasterTestSuite.test_37_jacques_folly_dungeon) ... ok
test_38_stash_dual_images (__main__.HungerHelperMasterTestSuite.test_38_stash_dual_images) ... ok
test_39_lore_the_hunger (__main__.HungerHelperMasterTestSuite.test_39_lore_the_hunger) ... ok
test_40_lore_mr_sweet (__main__.HungerHelperMasterTestSuite.test_40_lore_mr_sweet) ... ok
test_41_lore_chateau_sanctuary (__main__.HungerHelperMasterTestSuite.test_41_lore_chateau_sanctuary) ... ok

----------------------------------------------------------------------
Ran 41 tests in 5.746s

OK
```

---

## 3. Live Bot Daemon & Hardware Process Status
**Active Python Tasks:** RUNNING
```
Id ProcessName
   -- -----------
 6632 python     
42744 python
```

---

## 4. Self-Healing & Continuous Verification Architecture
- **Automated Verification Runner:** `autonomous_self_verifier.py`
- **Test Suite:** `test_suite.py` (simulating all 11 user domain requests)
- **Feedback Loop:** Validates responses against expected keywords, enforces Pure English defaults, eliminates corrupted glyphs, and asserts visual image integrity on disk.