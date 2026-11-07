# -*- coding: utf-8 -*-
import os

with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    text = f.read()

fn_start = "def answer_combat_ttk_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:"
fn_next = "def answer_squad_item_needs_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:"

s_idx = text.find(fn_start)
e_idx = text.find(fn_next)
assert s_idx != -1 and e_idx != -1

new_ttk_fn = '''def answer_combat_ttk_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Calculates exact strikes / hits required to down enemies based on weapon and armor/creature HP."""
    lowered = query.lower()
    is_hit_query = any(w in lowered for w in [
        "combien de coups", "combien de coup", "combien d'attaques", "combien dattaque",
        "combien de frappes", "how many hits", "how many strikes", "how many blows",
        "combien de tirs", "combien de tir", "combien de balles", "combien de balle",
        "how many shots", "how many bullets", "pour tuer", "tuer la brute", "tuer le baveux",
        "kill the brute", "kill drooler", "tuer une personne", "tuer un joueur", "tuer quelqu'un",
        "tuer en vert", "tuer en bleu", "joueur en vert", "joueur en cuir"
    ])
    if not is_hit_query:
        return None

    from co_pilot.card_renderer import render_weapon_card

    # 1. FIREARMS (Auster, Deux, LongBoy, Cavalier, Pistolet, Fusil)
    firearm_match = None
    for fn in ["auster", "deux", "longboy", "long boy", "cavalier", "marengo", "pistolet", "fusil"]:
        if fn in lowered and not ("deux mains" in lowered or "deux-mains" in lowered):
            firearm_match = "longboy" if fn in ["longboy", "long boy", "fusil"] else "deux" if fn in ["deux", "pistolet"] else fn
            break

    if firearm_match:
        card_path = render_weapon_card(firearm_match, is_french)

        # Detect player target / armor
        is_green = any(w in lowered for w in ["verte", "vert", "cuir", "leather", "uncommon", "non-commun", "non commune", "en vert"])
        is_naked = any(w in lowered for w in ["sans armure", "nu", "naked", "no armour", "aucune"])
        is_blue = any(w in lowered for w in ["bleue", "bleu", "rare", "sapeur", "sapper", "en bleu"])
        is_legend = any(w in lowered for w in ["légendaire", "legendaire", "legendary", "lourde", "heavy", "en or"])
        is_brute = any(w in lowered for w in ["brute", "gros"])
        is_drooler = any(w in lowered for w in ["baveux", "drooler"])

        if firearm_match == "auster":
            f_name = "Auster (Pistolet Peu Commun)"
            f_dmg = 48
            f_clip = 2
            f_rate = "0.25s (Double-tap ultra-rapide)"
            f_reload = "12.6s"
            f_ammo = "Munitions Rudes"
            if is_naked:
                t_name, t_head, t_body = "Joueur Sans Armure (100 PV)", 1, 2
                combo = "1 tir tête (96 dmg) = neutralisation quasi instantanée !"
                tactics = "Visez la tête non protégée pour un tir mortel immédiat."
            elif is_blue:
                t_name, t_head, t_body = "Joueur en Armure Bleue (Sapeur)", 2, 4
                combo = "2 tirs tête (134 dmg) = K.O. en 0.25s."
                tactics = "Le blindage absorbe les tirs au corps. Double-tapez impérativement le casque !"
            elif is_legend:
                t_name, t_head, t_body = "Joueur en Armure Légendaire", 5, 5
                combo = "Nécessite au moins 3 rechargements complets."
                tactics = "Évitez le duel frontal rapproché face à une plaque légendaire avec l'Auster."
            elif is_brute:
                t_name, t_head, t_body = "Brute (900 PV)", 10, 19
                combo = "10 balles en pleine tête."
                tactics = "Tirez pendant qu'elle prépare sa charge puis esquivez."
            elif is_drooler:
                t_name, t_head, t_body = "Baveux (Drooler - 450 PV)", 5, 10
                combo = "5 balles tête ou 10 corps."
                tactics = "Abattez-le à distance avant ses projections d'acide."
            else: # Green / Default player
                t_name, t_head, t_body = "Joueur en Armure Verte (Cuirasse & Casque de Cuir)", 2, 3
                combo = "1 tir tête (78 dmg) + 1 tir buste (39 dmg) = 117 dmg = K.O. EN 0.25 SECONDE CHRONO !"
                tactics = "L'Auster tire ses 2 cartouches en 0.25s. Un combo tête puis buste abat un joueur en vert avant qu'il ne puisse lever son arme !"

        elif firearm_match == "longboy":
            f_name = "LongBoy (Fusil de Tireur d'Élite)"
            f_dmg = 58
            f_clip = 1
            f_rate = "Tir unique longue portée"
            f_reload = "6.5s"
            f_ammo = "Munitions Lourdes"
            if is_naked:
                t_name, t_head, t_body = "Joueur Sans Armure (100 PV)", 1, 2
                combo = "1 tir en pleine tête (116 dmg) = ONE-SHOT MORTEL !"
                tactics = "One-shot net à n'importe quelle distance."
            elif is_blue:
                t_name, t_head, t_body = "Joueur en Armure Bleue (Sapeur)", 2, 2
                combo = "1 tir tête (81 dmg) + 1 tir corps (40 dmg) = K.O."
                tactics = "Rechargez à couvert entre deux tirs."
            elif is_legend:
                t_name, t_head, t_body = "Joueur en Armure Légendaire", 3, 4
                combo = "3 tirs tête ou 4 corps."
                tactics = "Exploitez votre portée supérieure."
            elif is_brute:
                t_name, t_head, t_body = "Brute (900 PV)", 8, 16
                combo = "8 tirs tête."
                tactics = "Snipez la tête depuis un promontoire élevé."
            elif is_drooler:
                t_name, t_head, t_body = "Baveux (Drooler - 450 PV)", 4, 8
                combo = "4 tirs tête."
                tactics = "One-tap de précision."
            else:
                t_name, t_head, t_body = "Joueur en Armure Verte (Cuirasse & Casque de Cuir)", 1, 2
                combo = "1 tir en pleine tête (104 dmg) = ONE-SHOT MORTEL EN PLEINE TÊTE !"
                tactics = "Le LongBoy inflige 104 dégâts en headshot sur armure verte : one-shot garanti sans rémission !"

        else: # Deux default
            f_name = "Deux (Pistolet Rare)"
            f_dmg = 54
            f_clip = 2
            f_rate = "2.0s entre tirs"
            f_reload = "8.6s"
            f_ammo = "Munitions Rudes"
            if is_naked:
                t_name, t_head, t_body = "Joueur Sans Armure (100 PV)", 1, 2
                combo = "1 tir tête (108 dmg) = ONE-SHOT MORTEL !"
                tactics = "Une seule balle en pleine tête neutralise la cible."
            elif is_blue:
                t_name, t_head, t_body = "Joueur en Armure Bleue (Sapeur)", 2, 3
                combo = "2 tirs tête ou 1 tête + 2 corps."
                tactics = "Visez la tête pour surmonter la plaque de sapeur."
            elif is_legend:
                t_name, t_head, t_body = "Joueur en Armure Légendaire", 4, 4
                combo = "4 tirs tête ou 4 corps."
                tactics = "Désengagez après vos 2 premiers tirs pour recharger."
            elif is_brute:
                t_name, t_head, t_body = "Brute (900 PV)", 9, 17
                combo = "9 balles tête ou 17 corps."
                tactics = "Gardez vos distances et visez le crâne."
            elif is_drooler:
                t_name, t_head, t_body = "Baveux (Drooler - 450 PV)", 5, 9
                combo = "5 balles tête ou 9 corps."
                tactics = "Éliminez-le rapidement à distance."
            else:
                t_name, t_head, t_body = "Joueur en Armure Verte (Cuirasse & Casque de Cuir)", 2, 3
                combo = "1 tir tête (86 dmg) + 1 tir corps (44 dmg) = K.O. en 2.0 secondes !"
                tactics = "Le Deux possède 2 canons. Enchaînez 1 tir tête puis 1 tir corps pour abattre votre cible avant les 8.6s de rechargement !"

        if is_french:
            spoken = f"Avec l'{f_name.split()[0]}, il faut {t_head} tirs en pleine tête ou {t_body} tirs dans le buste pour tuer un {t_name}. Fiche d'arme transmise."
            display = (
                f"🎯 **SIMULATEUR DE TIR & TTK : {f_name.upper()} vs {t_name.upper()}**\\n\\n"
                f"• 🔫 **Arme :** **{f_name}** — Dégâts de base : **{f_dmg} par balle** ({f_ammo})\\n"
                f"• 🎯 **Cible :** **{t_name}**\\n"
                f"• 💥 **Tirs en Pleine Tête (Headshots) :** **{t_head} tirs**\\n"
                f"• 🛡️ **Tirs dans le Buste (Body Shots) :** **{t_body} tirs**\\n"
                f"• ⚡ **Combo d'Élimination Optimale :** **{combo}**\\n\\n"
                f"💡 **Conseil Tactique :** {tactics}\\n\\n"
                f"🖼️ *Fiche d'arme Hunger Companion jointe ci-dessous.*"
            )
        else:
            spoken = f"With the {f_name.split()[0]}, it takes {t_head} headshots or {t_body} bodyshots to down a {t_name}."
            display = f"🎯 **GUNPLAY TTK : {f_name.upper()} vs {t_name.upper()}**\\n• Head: **{t_head} shots** | Body: **{t_body} shots**"

        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    # 2. MELEE WEAPONS TTK
    target_creature = "brute"
    target_hp = 900
    creature_name = "Brute"
    weakness_note = "Vulnérable aux attaques dans le dos et au saignement."

    if any(w in lowered for w in ["baveux", "drooler"]):
        target_creature = "drooler"
        target_hp = 450
        creature_name = "Baveux (Drooler)"
        weakness_note = "Faible résistance aux frappes d'estoc rapides."
    elif any(w in lowered for w in ["pitchskin", "peau de poix"]):
        target_creature = "pitchskin"
        target_hp = 1400
        creature_name = "Pitchskin (Miniboss)"
        weakness_note = "Sensible aux attaques dans le dos et à l'attrition."
    elif any(w in lowered for w in ["verte", "vert", "cuir", "leather", "uncommon"]):
        target_creature = "player_green"
        target_hp = 120
        creature_name = "Joueur en Armure Verte (Cuir)"
        weakness_note = "Peu de réduction contre les coups lourds contondants ou d'estoc."
    elif any(w in lowered for w in ["sans armure", "nu", "naked"]):
        target_creature = "player_naked"
        target_hp = 100
        creature_name = "Joueur Sans Armure"
        weakness_note = "Aucune résistance aux dégâts : 1 à 2 frappes suffisent."

    # Detect weapon
    w_slug = "spear"
    w_name = "Lance (Spear)"
    thrust_dmg = 48.3
    light_dmg = 45.0
    heavy_dmg = 68.0

    if any(w in lowered for w in ["zweihander", "zweihänder", "zwei", "deux mains", "deux-mains"]):
        w_slug, w_name = "zweihander", "Zweihänder"
        thrust_dmg, light_dmg, heavy_dmg = 52.0, 52.0, 82.0
    elif any(w in lowered for w in ["hallebarde", "halberd"]):
        w_slug, w_name = "halberd", "Hallebarde"
        thrust_dmg, light_dmg, heavy_dmg = 50.6, 46.0, 70.0
    elif any(w in lowered for w in ["sabre", "épée", "epee"]):
        w_slug, w_name = "sabre", "Sabre de cavalerie"
        thrust_dmg, light_dmg, heavy_dmg = 34.0, 34.0, 50.0
    elif any(w in lowered for w in ["dague", "dagger"]):
        w_slug, w_name = "dagger", "Dague de rôdeur"
        thrust_dmg, light_dmg, heavy_dmg = 28.0, 24.0, 42.0
    elif any(w in lowered for w in ["hache", "axe"]):
        w_slug, w_name = "axe", "Hache de guerre"
        thrust_dmg, light_dmg, heavy_dmg = 15.0, 30.0, 44.0

    card_path = render_weapon_card(w_slug, is_french)

    hits_thrust = math.ceil(target_hp / thrust_dmg)
    hits_heavy = math.ceil(target_hp / heavy_dmg)
    hits_backstab = math.ceil(target_hp / (thrust_dmg * 2.0))

    if is_french:
        spoken = f"Avec la {w_name}, il faut {hits_thrust} coups d'estoc ou {hits_heavy} coups lourds pour neutraliser un {creature_name}. Fiche d'arme transmise."
        display = (
            f"⚔️ **SIMULATEUR DE COMBAT & TTK : {w_name.upper()} vs {creature_name.upper()}**\\n\\n"
            f"• 🎯 **Points de Vie Cible :** **{target_hp} PV**\\n"
            f"• 🗡️ **Dégâts d'Estoc :** **{thrust_dmg}** ➡️ **{hits_thrust} coups d'estoc** de face\\n"
            f"• 💥 **Attaque Lourde :** **{heavy_dmg}** ➡️ **{hits_heavy} coups lourds**\\n"
            f"• 🩸 **Frappe dans le Dos (Critique x2) :** **{hits_backstab} coups seulement !**\\n\\n"
            f"💡 **Conseil Tactique :** {weakness_note}\\n\\n"
            f"🖼️ *Fiche d'arme Hunger Companion jointe ci-dessous.*"
        )
    else:
        spoken = f"With the {w_name}, it takes {hits_thrust} thrusts or {hits_heavy} heavy attacks to down {creature_name}."
        display = (
            f"⚔️ **COMBAT TTK SIMULATOR : {w_name.upper()} vs {creature_name.upper()}**\\n\\n"
            f"• 🎯 **Target Health :** **{target_hp} HP**\\n"
            f"• 🗡️ **Thrust Hits :** **{hits_thrust} hits**\\n"
            f"• 💥 **Heavy Attacks :** **{hits_heavy} hits**\\n"
            f"• 🩸 **Backstab (x2 Crit) :** **{hits_backstab} hits only !**\\n\\n"
            f"💡 **Tactical Tip :** {weakness_note}"
        )
    return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}
'''

text = text[:s_idx] + new_ttk_fn + "\n\n# ---------------------------------------------------------------------------\n# 12. SQUAD QUEST & ITEM NEEDS CHECKER\n# ---------------------------------------------------------------------------\n\n" + text[e_idx:]

with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] game_knowledge.py fixed successfully.")
