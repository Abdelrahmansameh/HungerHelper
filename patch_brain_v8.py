# -*- coding: utf-8 -*-
import re

with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Map Router (lines 309-358)
old_map_block = '''        if is_map_context or is_dungeon:
            from universal_v7_engine import get_clean_raid_map, render_authentic_dungeon_card
            if is_dungeon:
                img_path = render_authentic_dungeon_card(is_french=is_french)
                spoken = "Jacques Folly subterranean dungeon map dispatched with authentic entrance coordinates."
                display = (
                    "🏰 **DUNGEON ACCESS : JACQUES FOLLY (AUTHENTIC NORTHERN RIDGE SITES)**\\n\\n"
                    "• 📍 **Authentic Location :** Northwest of Vairon Quarry on northern wooded ridge.\\n"
                    "• 🚪 **Official Entrance Coordinates (Jacques Bridge - Raid 2) :**\\n"
                    "  1. **Jacques Folly Main Dungeon Entrance** (X: 1680.4, Y: 197.1)\\n"
                    "  2. **The Last Prisoner Crypt** (X: 1530.5, Y: 315.4)\\n"
                    "• 🔑 **Required Key :** Jacques Folly Key (3 Uses)\\n"
                    "• 📦 **Loot Capacity :** 174 reinforced subterranean containers.\\n\\n"
                    "🖼️ *(Authentic clean map inset attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}

            elif is_jb:
                p_map = get_clean_raid_map(2)
                spoken = "Jacques Bridge clean tactical map dispatched."
                display = (
                    "🗺️ **TACTICAL MAP : JACQUES BRIDGE (RAID 2 - CLEAN MAP)**\\n\\n"
                    "• 📍 **Zone :** Fortified bridge, garrison ruins & East riverbank.\\n"
                    "• 🎯 **Key Sites :** Bastion Crossing, Gavroche Ruins, Jacques Folly Ridge.\\n\\n"
                    "🖼️ *(Clean high-resolution map without sidebars attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}

            elif is_sf:
                p_map = get_clean_raid_map(1)
                spoken = "Sarlat Farm clean tactical map dispatched."
                display = (
                    "🗺️ **TACTICAL MAP : SARLAT FARM (RAID 1 - CLEAN MAP)**\\n\\n"
                    "• 📍 **Zone :** Farmlands, Windmill & Central Granary Clusters.\\n"
                    "• 🌾 **High-Density Flour Route :** Maximum sack clusters at Mill & Granary.\\n\\n"
                    "🖼️ *(Clean high-resolution map without sidebars attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}

            elif is_sombre:
                p_map = get_clean_raid_map(7)
                spoken = "Sombre Forest clean tactical map dispatched."
                display = (
                    "🗺️ **TACTICAL MAP : SOMBRE FOREST (RAID 7 - CLEAN MAP)**\\n\\n"
                    "• 📍 **Zone :** Deep wilderness, Lumberjack Camps & Ancient Monoliths.\\n"
                    "• 🌲 **Threats :** Drooler packs & roaming Brutes.\\n\\n"
                    "🖼️ *(Clean high-resolution map without sidebars attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}'''

new_map_block = '''        if is_map_context or is_dungeon:
            from universal_v8_engine import get_pure_blank_map, render_authentic_dungeon_card
            if is_dungeon:
                img_path = render_authentic_dungeon_card(is_french=is_french)
                spoken = "Jacques Folly subterranean dungeon map dispatched with authentic entrance coordinates."
                display = (
                    "🏰 **DUNGEON ACCESS : JACQUES FOLLY (AUTHENTIC NORTHERN RIDGE SITES)**\\n\\n"
                    "• 📍 **Authentic Location :** Northwest of Vairon Quarry on northern wooded ridge.\\n"
                    "• 🚪 **Official Entrance Coordinates (Jacques Bridge - Raid 2) :**\\n"
                    "  1. **Jacques Folly Main Descent** (X: 1680.4, Y: 197.1)\\n"
                    "  2. **The Last Prisoner Crypt** (X: 1530.5, Y: 315.4)\\n"
                    "• 🔑 **Required Key :** Jacques Folly Key (3 Uses)\\n"
                    "• 📦 **Loot Capacity :** 174 reinforced subterranean containers.\\n\\n"
                    "🖼️ *(Authentic clean map inset attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}

            elif is_jb:
                p_map = get_pure_blank_map("jacques")
                spoken = "Official blank vintage Jacques Bridge map dispatched."
                display = (
                    "🗺️ **OFFICIAL MAP : JACQUES BRIDGE (AUTHENTIC BLANK BASE MAP)**\\n\\n"
                    "• 📍 **Zone :** Fortified bridge, garrison ruins & East riverbank.\\n"
                    "• 🧭 **Format :** 100% clean vintage map from Hunger Companion (zero pins, zero overlays, no sidebars).\\n\\n"
                    "🖼️ *(Authentic 4096x4096 clean base map attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}

            elif is_sf:
                p_map = get_pure_blank_map("sarlat")
                spoken = "Official blank vintage Sarlat Farm map dispatched."
                display = (
                    "🗺️ **OFFICIAL MAP : SARLAT FARM (AUTHENTIC BLANK BASE MAP)**\\n\\n"
                    "• 📍 **Zone :** Farmlands, Windmill & Central Granary Clusters.\\n"
                    "• 🧭 **Format :** 100% clean vintage map from Hunger Companion (zero pins, zero overlays, no sidebars).\\n\\n"
                    "🖼️ *(Authentic 4096x4096 clean base map attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}

            elif is_sombre:
                p_map = get_pure_blank_map("sombre")
                spoken = "Official blank vintage Sombre Forest map dispatched."
                display = (
                    "🗺️ **OFFICIAL MAP : SOMBRE FOREST (AUTHENTIC BLANK BASE MAP)**\\n\\n"
                    "• 📍 **Zone :** Deep wilderness, Lumberjack Camps & Ancient Monoliths.\\n"
                    "• 🧭 **Format :** 100% clean vintage map from Hunger Companion (zero pins, zero overlays, no sidebars).\\n\\n"
                    "🖼️ *(Authentic 4096x4096 clean base map attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}'''

assert old_map_block in content, "Map block not found in brain.py"
content = content.replace(old_map_block, new_map_block)

# 2. Update Character and Skin imports (lines 416, 440, 469)
content = content.replace("from universal_v7_engine import render_clean_character_card", "from universal_v8_engine import render_clean_character_card")
content = content.replace("from universal_v7_engine import render_skins_for_target\n            skin_res = render_skins_for_target(clean_text)\n            \n            if skin_res[\"has_skins\"]:", "from universal_v8_engine import get_universal_skins\n            skin_res = get_universal_skins(clean_text)\n            \n            if skin_res[\"found\"]:")
content = content.replace("from universal_v7_engine import render_universal_stash_analysis", "from universal_v8_engine import render_universal_stash_analysis")

# 3. Update Weapon Query in line 826
old_weapon_block = '''        weapon_res = answer_weapon_query(clean_text, is_french)
        if weapon_res:
            w_target = "spear"
            for wn in ["zweihander", "zwei", "deux mains", "deux-mains", "spear", "lance", "halberd", "hallebarde", "sabre", "dagger", "dague", "axe", "hache"]:
                if wn in lowered:
                    w_target = "zweihander" if wn in ["zwei", "deux mains", "deux-mains"] else wn
                    break
            card_path = render_weapon_card(w_target, is_french)
            weapon_res["image_attachment"] = card_path
            return weapon_res'''

new_weapon_block = '''        weapon_res = answer_weapon_query(clean_text, is_french)
        if weapon_res:
            from universal_v8_engine import render_pure_english_melee_card
            w_target = "longsword"
            weapon_map = {
                "club": "club", "gourdin": "club", "massue": "club",
                "shortsword": "short-sword", "short-sword": "short-sword", "short sword": "short-sword",
                "longsword": "longsword", "long sword": "longsword", "epee": "longsword", "épée": "longsword",
                "spear": "spear", "lance": "spear",
                "zweihander": "zweihander", "zweihänder": "zweihander", "zwei": "zweihander",
                "halberd": "halberd", "hallebarde": "halberd",
                "saber": "sabre", "sabre": "sabre",
                "rapier": "rapier", "rapiere": "rapier", "rapière": "rapier",
                "war-axe": "war-axe", "war axe": "war-axe",
                "axe": "axe", "hache": "axe",
                "mace": "mace", "masse": "mace",
                "dagger": "dagger", "dague": "dagger"
            }
            for k, val in weapon_map.items():
                if k in lowered:
                    w_target = val
                    break
            card_path = render_pure_english_melee_card(w_target)
            weapon_res["image_attachment"] = card_path
            return weapon_res'''

assert old_weapon_block in content, "Weapon block not found in brain.py"
content = content.replace(old_weapon_block, new_weapon_block)

with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully patched co_pilot/brain.py with V8 engine integration!")
