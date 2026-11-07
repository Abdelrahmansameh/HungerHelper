with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    text = f.read().replace("\r\n", "\n")

start_marker = "# 0.45 MAP & TACTICAL NAVIGATION ROUTER"
end_marker = "# 0.5 COMBAT TTK & HIT CALCULATOR"

idx_start = text.find(start_marker)
idx_end = text.find(end_marker)

print("idx_start:", idx_start, "idx_end:", idx_end)

if idx_start != -1 and idx_end != -1:
    new_snippet = """# 0.40 PIRO'S LENS VS PIRO'S CONVOY ROUTER (ABSOLUTE PRIORITY)
        # -------------------------------------------------------------------
        if any(w in lowered for w in ["lens", "lentille", "piro's lens", "piros lens", "seeing clearly"]):
            from co_pilot.map_generator import generate_location_poi_map
            from co_pilot.card_renderer import render_item_card
            img_path, intel = generate_location_poi_map("piro's lens")
            card_p = render_item_card("Piro's Lens", rarity="Uncommon", item_type="Quest Item", is_french=is_french)
            spoken = "Piro's Lens is located in the subterranean Rat's Nest Cave at Jacques Bridge South-East ruins."
            display = (
                "🔍 **QUEST ITEM LOCATION : PIRO'S LENS (QUEST: SEEING CLEARLY)**\\n\\n"
                "• 📍 **Cave Entrance :** `X: 1602.00, Y: 3552.00` (Subterranean Rat's Nest Cave).\\n"
                "• 🎯 **Exact Item Coordinates :** `X: 1491.15, Y: 3535.74` (on the ground inside).\\n"
                "• 📜 **Quest Giver :** Piro (The Leper Physician at Chateau Hub) — Quest *Seeing Clearly*.\\n"
                "• 🔒 **Security Protocol :** Keep in **Secure Pouch** (Non-droppable quest item).\\n\\n"
                "*(Authentic tactical cave map & item card attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachments": [img_path, card_p], "image_attachment": img_path}

        elif any(w in lowered for w in ["convoy", "convoi", "remains of the day", "return to the convoy"]) or ("piro" in lowered and any(w in lowered for w in ["ruine", "ruins", "charette", "wagon", "site", "quete", "quête"])):
            from co_pilot.map_generator import generate_location_poi_map
            img_path, intel = generate_location_poi_map("piro's convoy")
            spoken = "Piro's Convoy ruins are situated on the Jacques Bridge southwest riverbank road."
            display = (
                "📍 **QUEST LOCATION : PIRO'S CONVOY RUINS (JACQUES BRIDGE)**\\n\\n"
                "• 📍 **Wagon Coordinates :** `X: 848.20, Y: 3084.90` (Southwest Riverbank Road).\\n"
                "• 📜 **Quests :** *Remains of the Day* & *Return to the Convoy*.\\n"
                "• 🎁 **Objective :** Retrieve Crude Ampoules from the overturned supply cart.\\n\\n"
                "*(Tactical convoy recon map attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}

        # -------------------------------------------------------------------
        # 0.45 MAP & TACTICAL NAVIGATION ROUTER
        # Handles pure blank base maps & dungeon layouts
        # -------------------------------------------------------------------
        is_dungeon = any(w in lowered for w in ["dungeon", "donjon", "folly", "pit", "puits", "entree", "entrée", "entrées", "entrances"])
        is_pure_map_query = (
            any(w in lowered for w in ["map", "carte", "plan"]) and
            not any(w in lowered for w in [
                "poi", "point", "trouver", "drop", "coffre", "container", "clef", "clé", "key",
                "creature", "créature", "baveux", "brute", "drooler", "farm", "route", "speedrun",
                "guide", "tactique", "stratégie", "strat", "skin", "arme", "weapon", "degat"
            ])
        ) or any(w in lowered for w in ["carte sans indication", "map sans indication", "blank map", "pure map", "carte de base"])

        if is_dungeon:
            from universal_v8_engine import render_authentic_dungeon_card
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

        elif is_pure_map_query:
            from universal_v8_engine import get_pure_blank_map
            is_jb = any(w in lowered for w in ["jaque", "jaques", "jacques", "jb", "pont jacques", "jacques bridge"])
            is_sf = any(w in lowered for w in ["sarlat", "sf", "ferme de sarlat", "sarlat farm", "moulin"])
            is_sombre = any(w in lowered for w in ["sombre", "forest", "foret", "forêt", "sombre forest"])

            if is_sombre or "sombre" in lowered:
                p_map = get_pure_blank_map("sombre")
                spoken = "Official blank vintage Sombre Forest map dispatched."
                display = (
                    "🗺️ **OFFICIAL MAP : SOMBRE FOREST (AUTHENTIC BLANK BASE MAP)**\\n\\n"
                    "• 📍 **Zone :** Deep wilderness, Lumberjack Camps & Ancient Monoliths.\\n"
                    "• 🧭 **Format :** 100% clean vintage map from Hunger Companion (zero pins, zero overlays, no sidebars).\\n\\n"
                    "🖼️ *(Authentic 4096x4096 clean base map attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}
            elif is_sf or "sarlat" in lowered:
                p_map = get_pure_blank_map("sarlat")
                spoken = "Official blank vintage Sarlat Farm map dispatched."
                display = (
                    "🗺️ **OFFICIAL MAP : SARLAT FARM (AUTHENTIC BLANK BASE MAP)**\\n\\n"
                    "• 📍 **Zone :** Farmlands, Windmill & Central Granary Clusters.\\n"
                    "• 🧭 **Format :** 100% clean vintage map from Hunger Companion (zero pins, zero overlays, no sidebars).\\n\\n"
                    "🖼️ *(Authentic 4096x4096 clean base map attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}
            elif is_jb or "jacques" in lowered or "jaque" in lowered or "jb" in lowered:
                p_map = get_pure_blank_map("jacques")
                spoken = "Official blank vintage Jacques Bridge map dispatched."
                display = (
                    "🗺️ **OFFICIAL MAP : JACQUES BRIDGE (AUTHENTIC BLANK BASE MAP)**\\n\\n"
                    "• 📍 **Zone :** Fortified bridge, garrison ruins & East riverbank.\\n"
                    "• 🧭 **Format :** 100% clean vintage map from Hunger Companion (zero pins, zero overlays, no sidebars).\\n\\n"
                    "🖼️ *(Authentic 4096x4096 clean base map attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}
        
        """
    text = text[:idx_start] + new_snippet + text[idx_end:]
    with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Replaced map routing block successfully!")
else:
    print("Error: Could not locate markers in brain.py")
