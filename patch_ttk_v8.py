# -*- coding: utf-8 -*-
import os
import math
import sqlite3

def patch_game_knowledge():
    with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
        content = f.read()

    fn_start = "def answer_combat_ttk_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:"
    fn_next = "def answer_squad_item_needs_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:"
    
    s_idx = content.find(fn_start)
    e_idx = content.find(fn_next)
    assert s_idx != -1 and e_idx != -1, f"Indices not found: {s_idx}, {e_idx}"

    new_fn = '''def answer_combat_ttk_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Calculates exact strikes / hits required to down enemies based on weapon and armor/creature HP."""
    lowered = query.lower()
    is_hit_query = any(w in lowered for w in [
        "combien de coups", "combien de coup", "combien d'attaques", "combien dattaque",
        "combien de frappes", "how many hits", "how many strikes", "how many blows",
        "combien de tirs", "combien de tir", "combien de tire", "combien de balles", "combien de balle",
        "how many shots", "how many bullets", "pour tuer", "tuer la brute", "tuer le baveux",
        "kill the brute", "kill drooler", "tuer une personne", "tuer un joueur", "tuer quelqu'un",
        "tuer en vert", "tuer en bleu", "joueur en vert", "joueur en cuir", "en combien de coup",
        "en combien de tire", "en combien de coups", "en combien de tir", "en combien de hit",
        "combien de hit", "combien de hits", "how many hit", "hit to kill", "htk", "ttk"
    ])
    if not is_hit_query:
        return None

    from universal_v8_engine import render_pure_english_melee_card
    from co_pilot.card_renderer import render_weapon_card

    # 1. FIREARMS
    firearm_match = None
    for fn in ["auster", "deux", "longboy", "long boy", "cavalier", "marengo", "pistolet", "fusil"]:
        if fn in lowered and not ("deux mains" in lowered or "deux-mains" in lowered):
            firearm_match = "longboy" if fn in ["longboy", "long boy", "fusil"] else "deux" if fn in ["deux", "pistolet"] else fn
            break

    if firearm_match:
        card_path = render_weapon_card(firearm_match, is_french=False)
        is_green = any(w in lowered for w in ["verte", "vert", "cuir", "leather", "uncommon", "en vert"])
        is_naked = any(w in lowered for w in ["sans armure", "nu", "naked", "no armour"])
        is_blue = any(w in lowered for w in ["bleue", "bleu", "blue", "rare", "sapeur", "sapper", "en bleu", "en blue"])
        is_legend = any(w in lowered for w in ["légendaire", "legendaire", "legendary", "lourde", "heavy", "en or"])
        is_brute = any(w in lowered for w in ["brute", "gros"]) and not any(w in lowered for w in ["joueur", "player"])
        is_drooler = any(w in lowered for w in ["baveux", "drooler"]) and not any(w in lowered for w in ["joueur", "player"])

        f_name = "LongBoy" if firearm_match == "longboy" else "Deux" if firearm_match == "deux" else "Auster"
        f_dmg = 58 if firearm_match == "longboy" else 54 if firearm_match == "deux" else 48
        
        if is_naked:
            t_name, t_head, t_body = "Naked Player (100 HP)", 1, 2
        elif is_blue:
            t_name, t_head, t_body = "Blue / Sapper Armor Player (160 HP)", 2, 4
        elif is_legend:
            t_name, t_head, t_body = "Legendary Armor Player (200 HP)", 3, 5
        elif is_brute:
            t_name, t_head, t_body = "Brute (900 HP)", 9, 18
        elif is_drooler:
            t_name, t_head, t_body = "Drooler (450 HP)", 5, 10
        else:
            t_name, t_head, t_body = "Green Armor Player (140 HP)", 2, 3

        if is_french:
            spoken = f"Avec {f_name}, il faut {t_head} tir(s) dans la tête ou {t_body} tir(s) au corps pour neutraliser un {t_name}."
            display = (
                f"🎯 **SIMULATEUR DE TIR & HTK : {f_name.upper()} vs {t_name.upper()}**\\n\\n"
                f"• 🔫 **Arme :** **{f_name}** — Dégâts : **{f_dmg}**\\n"
                f"• 🎯 **Cible :** **{t_name}**\\n"
                f"• 💥 **Tirs Tête (Headshots) :** **{t_head} tir(s)**\\n"
                f"• 🛡️ **Tirs Corps (Body) :** **{t_body} tir(s)**\\n\\n"
                f"🖼️ *Fiche d'arme Hunger Companion jointe ci-dessous.*"
            )
        else:
            spoken = f"With {f_name}, it takes {t_head} headshot(s) or {t_body} body shot(s) to eliminate a {t_name}."
            display = (
                f"🎯 **FIREARM HTK SIMULATOR : {f_name.upper()} vs {t_name.upper()}**\\n\\n"
                f"• 🔫 **Weapon :** **{f_name}** — Base Damage : **{f_dmg}**\\n"
                f"• 🎯 **Target :** **{t_name}**\\n"
                f"• 💥 **Headshots :** **{t_head} shot(s)**\\n"
                f"• 🛡️ **Body Shots :** **{t_body} shot(s)**\\n\\n"
                f"🖼️ *(Authentic weapon card attached below)*"
            )
        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    # 2. MELEE WEAPONS TTK
    # Target detection
    is_naked = any(w in lowered for w in ["sans armure", "nu", "naked", "no armour"])
    is_green = any(w in lowered for w in ["verte", "vert", "cuir", "leather", "uncommon", "en vert"])
    is_blue = any(w in lowered for w in ["bleue", "bleu", "blue", "rare", "sapeur", "sapper", "en bleu", "en blue"])
    is_epic = any(w in lowered for w in ["violet", "violette", "pourpre", "épique", "epique", "en violet", "epic"])
    is_legend = any(w in lowered for w in ["légendaire", "legendaire", "legendary", "doré", "dore", "jaune", "en or"])
    is_player = any(w in lowered for w in ["joueur", "player", "mec", "gars", "cible", "personne", "en bleu", "en blue", "en vert", "nu", "sans armure", "en or", "legendaire", "légendaire"])
    is_brute = any(w in lowered for w in ["brute", "gros"]) and not is_player
    is_drooler = any(w in lowered for w in ["baveux", "drooler"]) and not is_player

    if is_naked:
        target_name = "Naked Player (100 HP)"
        target_hp = 100
    elif is_blue:
        target_name = "Blue / Sapper Armor Player (160 HP)"
        target_hp = 160
    elif is_epic:
        target_name = "Epic Reinforced Armor Player (180 HP)"
        target_hp = 180
    elif is_legend:
        target_name = "Legendary Armor Player (200 HP)"
        target_hp = 200
    elif is_brute:
        target_name = "Brute Elite Creature (900 HP)"
        target_hp = 900
    elif is_drooler:
        target_name = "Drooler Creature (450 HP)"
        target_hp = 450
    else:
        target_name = "Green Leather Armor Player (140 HP)"
        target_hp = 140

    # Weapon detection - NEVER default to spear!
    w_slug = "longsword"
    w_name = "Longsword"

    if any(w in lowered for w in ["club", "gourdin", "massue"]):
        w_slug, w_name = "club", "Club"
    elif any(w in lowered for w in ["shortsword", "short-sword", "short sword", "epee courte", "épée courte"]):
        w_slug, w_name = "short-sword", "Short Sword"
    elif any(w in lowered for w in ["zweihander", "zweihänder", "zwei", "deux mains", "deux-mains"]):
        w_slug, w_name = "zweihander", "Zweihänder"
    elif any(w in lowered for w in ["hallebarde", "halberd"]):
        w_slug, w_name = "halberd", "Halberd"
    elif any(w in lowered for w in ["sabre", "saber"]):
        w_slug, w_name = "sabre", "Saber"
    elif any(w in lowered for w in ["rapier", "rapiere", "rapière"]):
        w_slug, w_name = "rapier", "Rapier"
    elif any(w in lowered for w in ["war-axe", "war axe", "hache de guerre"]):
        w_slug, w_name = "war-axe", "War Axe"
    elif any(w in lowered for w in ["axe", "hache"]):
        w_slug, w_name = "axe", "Axe"
    elif any(w in lowered for w in ["mace", "masse"]):
        w_slug, w_name = "mace", "Mace"
    elif any(w in lowered for w in ["dagger", "dague"]):
        w_slug, w_name = "dagger", "Dagger"
    elif any(w in lowered for w in ["spear", "lance"]):
        w_slug, w_name = "spear", "Spear"
    elif any(w in lowered for w in ["longsword", "long sword", "epee", "épée"]):
        w_slug, w_name = "longsword", "Longsword"

    # Query DB for weapon stats
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM weapons WHERE slug LIKE ? OR name_en LIKE ? LIMIT 1", (f"%{w_slug}%", f"%{w_name}%"))
    w_row = c.fetchone()
    conn.close()

    if w_row:
        w_dict = dict(w_row)
        light_dmg = float(w_dict.get("light_damage", 34.0))
        heavy_dmg = float(w_dict.get("heavy_damage", 45.0))
        thrust_dmg = float(w_dict.get("thrust_damage", 20.0))
        rarity = w_dict.get("rarity_en", "Common").capitalize()
    else:
        light_dmg, heavy_dmg, thrust_dmg, rarity = 34.0, 43.0, 17.0, "Common"

    # Calculations: Head hits (crit 1.5x on heavy) vs Body hits
    crit_dmg = heavy_dmg * 1.5 if heavy_dmg > 0 else light_dmg * 1.5
    head_hits = max(1, math.ceil(target_hp / crit_dmg))
    body_hits = max(1, math.ceil(target_hp / light_dmg))
    heavy_hits = max(1, math.ceil(target_hp / heavy_dmg))

    # Generate 100% English authentic card
    card_path = render_pure_english_melee_card(w_slug)

    if is_french:
        spoken = f"Avec {w_name}, il faut {head_hits} coup(s) à la tête ou {body_hits} coup(s) au corps pour neutraliser un {target_name}."
        display = (
            f"⚔️ **SIMULATEUR DE COMBAT & HTK : {w_name.upper()} vs {target_name.upper()}**\\n\\n"
            f"• 🗡️ **Arme :** **{w_name}** ({rarity})\\n"
            f"• 🎯 **Cible :** **{target_name}**\\n"
            f"• 💥 **Coups à la Tête (Critique x1.5) :** **{head_hits} frappe(s)**\\n"
            f"• 🛡️ **Coups au Corps :** **{body_hits} coup(s) légers** (ou **{heavy_hits} frappe(s) lourdes**)\\n"
            f"• ⚡ **Conseil Tactique PvP :** Visez la tête pour briser la garde et neutraliser rapidement l'ennemi.\\n\\n"
            f"🖼️ *Fiche d'arme Hunger Companion jointe ci-dessous.*"
        )
    else:
        spoken = f"With {w_name}, it takes {head_hits} headshot(s) or {body_hits} body hit(s) to eliminate a {target_name}."
        display = (
            f"⚔️ **COMBAT SIMULATOR & HTK : {w_name.upper()} vs {target_name.upper()}**\\n\\n"
            f"• 🗡️ **Weapon :** **{w_name}** ({rarity})\\n"
            f"• 🎯 **Target :** **{target_name}**\\n"
            f"• 💥 **Headshots (Crit x1.5) :** **{head_hits} strike(s)**\\n"
            f"• 🛡️ **Body Hits :** **{body_hits} light hit(s)** (or **{heavy_hits} heavy strike(s)**)\\n"
            f"• ⚡ **Tactical Advice :** Prioritize heavy overheads to stagger and finish with rapid light strikes.\\n\\n"
            f"🖼️ *(Authentic Hunger Companion weapon dossier attached below)*"
        )
    return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}
'''

    new_content = content[:s_idx] + new_fn + "\n\n" + content[e_idx:]
    with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully patched game_knowledge.py with V8 TTK logic!")

if __name__ == "__main__":
    patch_game_knowledge()
