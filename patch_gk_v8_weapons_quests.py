# -*- coding: utf-8 -*-
import os
import re

with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update answer_weapon_query
old_fn_start = "def answer_weapon_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:"
old_fn_end = "def answer_effect_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:"
s_idx = text.find(old_fn_start)
e_idx = text.find(old_fn_end)
assert s_idx != -1 and e_idx != -1, "answer_weapon_query not found in game_knowledge.py"

new_weapon_query = '''def answer_weapon_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Answer queries regarding weapon damage stats, firearms, 2-handed weapons, Pricker, etc."""
    lowered = query.lower()
    from universal_v8_engine import (
        render_pure_english_firearm_card,
        render_pure_english_melee_card,
        render_two_handed_melee_overview_card
    )

    # 0. 2-HANDED MELEE WEAPONS QUERY ("montre moi tout les armes a 2 main melee", "armes a deux mains")
    if any(w in lowered for w in ["2 main", "2 mains", "deux main", "deux mains", "two handed", "2-handed", "two-handed"]) and any(w in lowered for w in ["arme", "armes", "weapon", "weapons", "melee"]):
        card_p = render_two_handed_melee_overview_card()
        spoken = "All 4 official two-handed melee weapons in Hunger dispatched: Zweihander, Halberd, Spear, and War Axe."
        display = (
            "⚔️ **OFFICIAL 2-HANDED MELEE ARSENAL (HUNGER COMPANION)**\\n\\n"
            "• 🥇 **Zweihänder (Legendary)** : 52.0 Thrust | 82.0 Heavy | 52.0 Light (3 hits vs Legendary Armor)\\n"
            "• 🥈 **Halberd (Epic)** : 50.6 Thrust | 70.0 Heavy | 46.0 Light (3 hits vs Legendary Armor)\\n"
            "• 🥉 **Spear (Rare)** : 48.3 Thrust | 58.0 Heavy | 42.0 Light (4 hits vs Legendary Armor)\\n"
            "• 🛡️ **War Axe (Rare)** : 32.0 Thrust | 60.0 Heavy | 40.0 Light (4 hits vs Legendary Armor)\\n\\n"
            "*(Comparative 4-weapon analytical dossier attached below)*"
        )
        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_p}

    # 1. FIREARMS (Marengo, Drak, Lasher, Auster, Deux, Longboy, Cavalier)
    firearms_keys = ["marengo", "drak", "lasher", "lash", "auster", "deux", "longboy", "long boy", "cavalier"]
    for fn in firearms_keys:
        if fn in lowered and not ("deux mains" in lowered or "deux-mains" in lowered):
            fk = "lasher" if fn in ["lasher", "lash"] else "longboy" if "long" in fn else fn
            card_path = render_pure_english_firearm_card(fk, is_french=False)
            
            f_specs = {
                "marengo": ("Marengo (Epic Revolver)", 39, 68, "6 rounds", "0.5s", "3.0s", "Heavy Ammunition", "Voyant the Rifleman (42s 38c)"),
                "drak": ("Drak (Legendary Heavy Rifle)", 107, 192, "1 round", "0.5s", "3.2s", "Exotic Ammunition", "Ambrose's Tithe (Loot exclusive)"),
                "lasher": ("Lasher (Epic Chain Repeater)", 30, 52, "14 rounds", "0.2s", "3.9s", "Heavy Ammunition", "Voyant the Rifleman (86s 36c)"),
                "auster": ("Auster (Uncommon Pistol)", 48, 78, "2 rounds", "0.25s (Double-tap)", "12.6s", "Rough Ammunition", "Octave de Villiers (3s 50c)"),
                "deux": ("Deux (Rare Rotary Pistol)", 54, 86, "2 rounds", "2.0s", "8.6s", "Rough Ammunition", "Voyant the Rifleman (5s 0c)"),
                "longboy": ("LongBoy (Rare Precision Rifle)", 58, 104, "1 round", "Single Shot", "6.5s", "Heavy Ammunition", "Voyant the Rifleman (6s 50c)"),
                "cavalier": ("Cavalier (Uncommon Pistol)", 52, 80, "2 rounds", "1.5s", "9.0s", "Rough Ammunition", "Octave de Villiers")
            }
            fn_title, dmg, head, clip, rate, reload, ammo, vendor = f_specs.get(fk, ("Firearm", 48, 78, "2", "0.5s", "10s", "Ammo", "Chateau"))
            
            spoken = f"{fn_title} deals {dmg} base damage ({head} headshot) chambering {ammo}. Technical dossier dispatched."
            display = (
                f"🎯 **FIREARM BALLISTIC DOSSIER : {fn_title.upper()}**\\n\\n"
                f"• 💥 **Base Damage :** **{dmg} per shot** | 🎯 **Headshot Critical :** **{head} dmg**\\n"
                f"• 🔄 **Magazine Capacity :** **{clip}** | ⚡ **Fire Rate :** **{rate}**\\n"
                f"• ⏱️ **Tactical Reload :** **{reload}** | 📦 **Ammunition :** **{ammo}**\\n"
                f"• 🛒 **Merchant Availability :** {vendor}\\n\\n"
                f"*(Authentic weapon card attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    # 2. MELEE WEAPONS LOOKUP (Pricker, Club, Longsword, Zweihander, Spear, etc.)
    conn = get_db_connection()
    c = conn.cursor()

    is_thrust = any(w in lowered for w in ["thrust", "estoc", "pénétration", "penetration", "perce", "pierce"])
    if is_thrust and any(w in lowered for w in ["meilleur", "meilleure", "plus grand", "plus fort", "best", "highest", "top", "max"]):
        c.execute("SELECT name_en, name_fr, rarity_en, rarity_fr, thrust_damage FROM weapons WHERE thrust_damage > 0 ORDER BY thrust_damage DESC LIMIT 3")
        top3 = c.fetchall()
        conn.close()
        card_path = render_pure_english_melee_card("zweihander")
        spoken = "The weapon with the highest thrust damage is the Legendary Zweihander with 52, followed by the Halberd with 50.6, and the Spear with 48.3."
        top_str = "\\n".join([f"  {idx}. **{r['name_en']}** ({r['rarity_en']}) : **{r['thrust_damage']}** thrust" for idx, r in enumerate(top3, 1)])
        display = (
            f"🏆 **HIGHEST THRUST DAMAGE WEAPONS (HUNGER COMPANION) :**\\n\\n{top_str}\\n\\n"
            f"• 🥇 **Zweihander (Legendary)** : **52** thrust damage\\n"
            f"• 🥈 **Halberd (Epic)** : **50.6** thrust damage\\n"
            f"• 🥉 **Spear (Rare)** : **48.3** thrust damage"
        )
        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    # Match weapon in weapons DB table
    c.execute("SELECT * FROM weapons")
    weapons = c.fetchall()
    conn.close()

    for w_row in weapons:
        w = dict(w_row)
        w_slug = w["slug"]
        w_en = w["name_en"].lower()
        w_fr = w["name_fr"].lower()
        if w_slug in lowered or w_en in lowered or (len(w_fr) >= 4 and w_fr in lowered):
            card_path = render_pure_english_melee_card(w_slug)
            w_name = w["name_en"]
            rarity = w.get("rarity_en", "Common")
            t_dmg = w.get("thrust_damage", 0)
            l_dmg = w.get("light_damage", 0)
            h_dmg = w.get("heavy_damage", 0)
            sell_p = w.get("sell_price", "1 0")

            spoken = f"{w_name} ({rarity}) deals {t_dmg} thrust, {h_dmg} heavy, and {l_dmg} light damage. Card dispatched."
            display = (
                f"🗡️ **MELEE WEAPON PROFILE : {w_name.upper()} ({rarity.upper()})**\\n\\n"
                f"• 🎯 **Thrust Damage :** **{t_dmg}**\\n"
                f"• 💥 **Heavy Strike :** **{h_dmg}**\\n"
                f"• ⚔️ **Light Strike :** **{l_dmg}** (Out of energy: {w.get('light_no_energy', 10)})\\n"
                f"• 💰 **Sell Price :** **{sell_p}**\\n\\n"
                f"*(Authentic directional attack compass card attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    return None
'''

text = text[:s_idx] + new_weapon_query + "\n\n" + text[e_idx:]

with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] game_knowledge.py updated with firearms & 2H weapon query logic!")
