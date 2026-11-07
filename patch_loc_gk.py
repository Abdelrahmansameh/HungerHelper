# -*- coding: utf-8 -*-
with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    text = f.read()

old_loc_part = '''    # 3. Dynamic POI Search in Database (map_points)
    img_path, intel = generate_location_poi_map(query)
    title = intel.get("title", "Rep\ufffdre Tactique")
    m_name = intel.get("map_name", "Sarlat Farm")
    if is_french:
        spoken = f"Le rep\ufffdre pour {title} sur {m_name} est affich\ufffd sur la carte tactique transmise."
        display = f"\U0001f4cd **LOCALISATION : {title.upper()} ({m_name.upper()})**\\n\\n" + "\\n".join(intel.get("drops", []))
    else:
        spoken = f"Location for {title} on {m_name} marked on map."
        display = f"\U0001f4cd **LOCATION : {title.upper()} ({m_name.upper()})**"
    return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}'''

# Find block
s_idx = text.find("# 3. Dynamic POI Search in Database (map_points)")
assert s_idx != -1, "POI Search block not found"
end_idx = text.find("return {\"spoken_text\": spoken, \"display_text\": display, \"image_attachment\": img_path}", s_idx)
end_idx += len("return {\"spoken_text\": spoken, \"display_text\": display, \"image_attachment\": img_path}")

new_loc_part = '''    # 2.5 Item Location & Raid Drops (e.g. "ou est ce que je peux trouver heavy ammo")
    if any(w in lowered for w in ["ammo", "munition", "munitions", "flour", "farine", "charcoal", "charbon", "saltpetre", "salpetre", "bezoar", "chiffon", "balm", "baume"]):
        from co_pilot.companion_intel import get_companion_item_intel
        from co_pilot.card_renderer import render_item_card
        
        cand_slug = "heavy-ammunition" if any(w in lowered for w in ["heavy ammo", "munitions lourdes", "heavy ammunition"]) else "flour" if "farine" in lowered or "flour" in lowered else "charcoal" if "charbon" in lowered or "charcoal" in lowered else "saltpetre"
        intel = get_companion_item_intel(cand_slug)
        if intel:
            card_p = render_item_card(intel["name_en"], rarity=intel.get("rarity", "Common"),
                                      sell_silver=intel.get("sell_silver", 0), sell_copper=intel.get("sell_copper", 2),
                                      item_type=intel.get("category", "Ammunition"), desc=intel.get("lore_desc", "Essential raid ammunition."),
                                      best_source=intel.get("best_container", "Munitions Crate (1/108)"), drop_rate="High",
                                      buy_vendor=intel.get("vendor_buy", "Voyant the Rifleman, Piro, Reynauld (0s 2c)"))
            spoken = f"{intel['name_en']} can be purchased at Chateau Hub from Voyant the Rifleman, Piro, and Reynauld, or scavenged from Munitions Crates in raid."
            display = (
                f"📦 **LOOT & VENDOR LOCATIONS : {intel['name_en'].upper()}**\\n\\n"
                f"• 🏰 **Château Hub Traders :** Available from **{intel.get('vendor_buy', 'Voyant the Rifleman, Piro, Reynauld')}** (0 Silver, 2 Copper).\\n"
                f"• 📦 **Best Raid Containers :** **{intel.get('best_container', 'Munitions Crate (1/108)')}** on Sarlat Farm, Jacques Bridge, and Sombre Forest.\\n"
                f"• 👾 **Creature Drop :** Scavenged from Brutes (1/52 drop rate).\\n\\n"
                f"*(Authentic Hunger Companion item card attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_p}

    # 3. Dynamic POI Search in Database (map_points & Piro's Convoy)
    img_path, intel = generate_location_poi_map(query)
    title = intel.get("title", "Tactical Waypoint")
    m_name = intel.get("map_name", "Jacques Bridge")
    drops_txt = "\\n".join(intel.get("drops", []))
    spoken = f"Location for {title} on {m_name} marked on map."
    display = f"📍 **LOCATION : {title.upper()} ({m_name.upper()})**\\n\\n{drops_txt}"
    return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}'''

text = text[:s_idx] + new_loc_part + text[end_idx:]

with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] game_knowledge.py updated with item location handling!")
