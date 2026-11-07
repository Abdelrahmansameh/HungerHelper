import re

with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    gk = f.read().replace("\r\n", "\n")

# Find the start of melee weapons handling in answer_combat_ttk_query
start_idx = gk.find("# 2. MELEE WEAPONS TTK")
if start_idx != -1:
    end_idx = gk.find("return {\"spoken_text\": spoken, \"display_text\": display, \"image_attachment\": card_path}", start_idx)
    end_idx = gk.find("\n", end_idx) + 1

    new_melee_section = """    # 2. MELEE WEAPONS TTK
    from overhaul_all_cards import render_clean_melee_card

    # Detect Target Armor Tier or Creature
    is_player = any(w in lowered for w in ["joueur", "player", "personne", "cible", "mec", "gars", "en bleu", "en blue", "en vert", "nu", "sans armure"])
    is_naked = any(w in lowered for w in ["sans armure", "nu", "naked", "no armour"])
    is_green = any(w in lowered for w in ["verte", "vert", "cuir", "leather", "uncommon", "en vert"])
    is_blue = any(w in lowered for w in ["bleue", "bleu", "blue", "rare", "sapeur", "sapper", "en bleu", "en blue"])
    is_epic = any(w in lowered for w in ["violet", "violette", "pourpre", "épique", "epique", "en violet"])
    is_legend = any(w in lowered for w in ["légendaire", "legendaire", "legendary", "doré", "dore", "jaune", "en or"])
    is_brute = any(w in lowered for w in ["brute", "gros"]) and not is_player
    is_drooler = any(w in lowered for w in ["baveux", "drooler"]) and not is_player

    if is_naked:
        t_name = "Joueur Sans Armure (100 PV)"
        t_hp = 100
        t_head = 2
        t_body = 3
        weakness_note = "Aucune protection : 1 frappe lourde à la tête ou 3 coups de taille suffisent."
    elif is_blue:
        t_name = "Joueur en Armure Bleue (Sapeur - 160 PV)"
        t_hp = 160
        t_head = 2
        t_body = 4
        weakness_note = "Le casque de sapeur absorbe l'impact. Enchaînez 1 frappe lourde à la tête + 1 coup de taille."
    elif is_epic:
        t_name = "Joueur en Armure Épique (180 PV)"
        t_hp = 180
        t_head = 3
        t_body = 4
        weakness_note = "Blindage lourd. Visez les brèches du casque."
    elif is_legend:
        t_name = "Joueur en Armure Légendaire (200 PV)"
        t_hp = 200
        t_head = 3
        t_body = 5
        weakness_note = "Armure maximale : privilégiez les attaques d'estoc lourdes à la tête."
    elif is_brute:
        t_name = "Brute Élite (900 PV)"
        t_hp = 900
        t_head = 8
        t_body = 15
        weakness_note = "Vulnérable aux attaques dans le dos (Critique x2)."
    elif is_drooler:
        t_name = "Baveux (Drooler - 450 PV)"
        t_hp = 450
        t_head = 4
        t_body = 8
        weakness_note = "Sensible aux frappes d'estoc rapides."
    else: # Default: Joueur en Armure Verte
        t_name = "Joueur en Armure Verte (Cuir - 140 PV)"
        t_hp = 140
        t_head = 2
        t_body = 3
        weakness_note = "Protection légère : 2 frappes bien placées dont une à la tête suffisent."

    # Detect Weapon
    w_slug = "longsword"
    w_name = "Longsword"
    if any(w in lowered for w in ["zweihander", "zweihänder", "zwei", "deux mains", "deux-mains"]):
        w_slug, w_name = "zweihander", "Zweihänder"
    elif any(w in lowered for w in ["longsword", "long sword", "epee", "épée"]):
        w_slug, w_name = "longsword", "Longsword"
    elif any(w in lowered for w in ["spear", "lance"]):
        w_slug, w_name = "spear", "Lance (Spear)"
    elif any(w in lowered for w in ["hallebarde", "halberd"]):
        w_slug, w_name = "halberd", "Hallebarde"
    elif any(w in lowered for w in ["sabre", "saber"]):
        w_slug, w_name = "sabre", "Sabre"
    elif any(w in lowered for w in ["rapier", "rapière", "rapiere"]):
        w_slug, w_name = "rapier", "Rapière"
    elif any(w in lowered for w in ["war-axe", "war axe", "hache de guerre"]):
        w_slug, w_name = "war-axe", "Hache de Guerre"
    elif any(w in lowered for w in ["axe", "hache"]):
        w_slug, w_name = "axe", "Hache"
    elif any(w in lowered for w in ["mace", "masse"]):
        w_slug, w_name = "mace", "Masse"
    elif any(w in lowered for w in ["short-sword", "short sword"]):
        w_slug, w_name = "short-sword", "Short Sword"
    elif any(w in lowered for w in ["dagger", "dague"]):
        w_slug, w_name = "dagger", "Dague"
    elif any(w in lowered for w in ["club", "gourdin"]):
        w_slug, w_name = "club", "Club"

    card_path = render_clean_melee_card(w_slug, is_french)

    if is_french:
        spoken = f"Avec la {w_name}, il faut {t_head} coups à la tête ou {t_body} coups au corps pour tuer un {t_name}. Fiche d'arme transmise."
        display = (
            f"⚔️ **SIMULATEUR DE COMBAT & TTK : {w_name.upper()} vs {t_name.upper()}**\\n\\n"
            f"• 🗡️ **Arme :** **{w_name}**\\n"
            f"• 🎯 **Cible :** **{t_name}**\\n"
            f"• 💥 **Coups à la Tête (Headshots) :** **{t_head} coups**\\n"
            f"• 🛡️ **Coups au Corps (Body Hits) :** **{t_body} coups**\\n"
            f"• ⚡ **Conseil PvP :** {weakness_note}\\n\\n"
            f"🖼️ *Fiche d'arme Hunger Companion jointe ci-dessous.*"
        )
    else:
        spoken = f"With the {w_name}, it takes {t_head} headshots or {t_body} body hits to down a {t_name}."
        display = f"⚔️ **COMBAT TTK : {w_name.upper()} vs {t_name.upper()}**\\n• Head: **{t_head} hits** | Body: **{t_body} hits**"

    return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}
"""
    gk = gk[:start_idx] + new_melee_section + gk[end_idx:]
    with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
        f.write(gk)
    print("SUCCESS: game_knowledge.py updated for melee TTK and Longsword!")
else:
    print("WARNING: Start of melee section not found!")
