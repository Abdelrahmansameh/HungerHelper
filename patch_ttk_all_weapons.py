import os

p = "co_pilot/game_knowledge.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target_start = """    # 1. SPECIALIZED FIREARM TTK (e.g. Deux Pistol)
    is_deux = ("deux" in lowered or "pistolet" in lowered) and not ("deux mains" in lowered or "deux-mains" in lowered)
    if is_deux:
        from co_pilot.card_renderer import render_item_card
        card_path = render_item_card("deux")"""

# Let's inspect where the firearm block ends:
end_marker = """    # Detect enemy target
    target_creature = "brute"
    target_hp = 900
    creature_name = "Brute" """

assert target_start in text, "target_start not found"
start_idx = text.find(target_start)
end_idx = text.find(end_marker)
assert start_idx != -1 and end_idx != -1, "indices not found"

replacement_block = """    # 1. FIREARMS TTK & COMBAT MATCHUPS (Auster, Deux, LongBoy, Cavalier, etc.)
    firearm_detected = None
    for fn in ["auster", "deux", "longboy", "long boy", "cavalier", "marengo", "borodino", "morgan", "snub", "vepr", "pistolet", "fusil"]:
        if fn in lowered and not ("deux mains" in lowered or "deux-mains" in lowered):
            firearm_detected = "longboy" if fn in ["longboy", "long boy", "fusil"] else "deux" if fn in ["deux", "pistolet"] else fn
            break

    if firearm_detected:
        from co_pilot.card_renderer import render_item_card
        card_path = render_item_card(firearm_detected)

        # Firearm profiles
        if firearm_detected == "auster":
            f_name = "Auster (Pistolet Peu Commun)"
            f_dmg = 48
            f_clip = 2
            f_rate = "0.25s (Double-tap ultra-rapide)"
            f_reload = "12.6s"
            f_ammo = "Munitions Rudes"
            h_green_head, h_green_body = 2, 3
            combo_green = "1 tir tête (78 dmg) + 1 tir corps (39 dmg) = K.O. en 0.25 seconde chrono !"
            green_tactics = "L'Auster possède une cadence entre deux tirs de 0.25s : un enchaînement tête puis torse abat un joueur en armure verte instantanément sans le laisser réagir !"
            h_naked_head, h_naked_body = 2, 3
            h_blue_head, h_blue_body = 2, 4
            h_legend_head, h_legend_body = 5, 5
            h_brute_head, h_brute_body = 10, 19
            h_drooler_head, h_drooler_body = 5, 10
        elif firearm_detected == "longboy":
            f_name = "LongBoy (Fusil Rare)"
            f_dmg = 58
            f_clip = 1
            f_rate = "Tir unique à longue portée"
            f_reload = "6.5s"
            f_ammo = "Munitions Lourdes"
            h_green_head, h_green_body = 1, 2
            combo_green = "1 tir en pleine tête (104 dmg) = ONE-SHOT MORTEL EN PLEINE TÊTE !"
            green_tactics = "Le LongBoy inflige 58 dégâts de base : une tête one-shot les armures vertes à distance !"
            h_naked_head, h_naked_body = 1, 2
            h_blue_head, h_blue_body = 2, 2
            h_legend_head, h_legend_body = 3, 4
            h_brute_head, h_brute_body = 8, 16
            h_drooler_head, h_drooler_body = 4, 8
        else:
            # Deux default
            f_name = "Deux (Pistolet Rare)"
            f_dmg = 54
            f_clip = 2
            f_rate = "2.0s entre tirs"
            f_reload = "8.6s"
            f_ammo = "Munitions Rudes"
            h_green_head, h_green_body = 2, 3
            combo_green = "1 tir tête (86 dmg) + 1 tir corps (44 dmg) = K.O. en 2.0 secondes !"
            green_tactics = "Le Deux dispose de 2 canons rotatifs. Visez la tête puis le buste pour abattre la cible avant le rechargement !"
            h_naked_head, h_naked_body = 1, 2
            h_blue_head, h_blue_body = 2, 3
            h_legend_head, h_legend_body = 4, 4
            h_brute_head, h_brute_body = 9, 17
            h_drooler_head, h_drooler_body = 5, 9

        # Target detection
        is_green = any(w in lowered for w in ["verte", "vert", "cuir", "leather", "uncommon", "non-commun", "non commune", "en vert"])
        is_naked = any(w in lowered for w in ["sans armure", "nu", "naked", "no armour", "aucune"])
        is_blue = any(w in lowered for w in ["bleue", "bleu", "rare", "sapeur", "sapper", "en bleu"])
        is_legend = any(w in lowered for w in ["légendaire", "legendaire", "legendary", "lourde", "heavy", "en or", "en jaune"])
        is_brute = any(w in lowered for w in ["brute", "gros"])
        is_drooler = any(w in lowered for w in ["baveux", "drooler"])

        if is_green or any(w in lowered for w in ["joueur", "personne", "mec", "pvp"]):
            if is_naked:
                t_name = "Joueur Sans Armure (100 PV)"
                t_head, t_body = h_naked_head, h_naked_body
                combo_note = f"Headshot mortel en {t_head} tir !"
                tactics = "Cible non casquée : visez le haut du corps pour un abattage immédiat."
            elif is_blue:
                t_name = "Joueur en Armure Bleue (Cuirasse de Sapeur)"
                t_head, t_body = h_blue_head, h_blue_body
                combo_note = f"{t_head} tirs tête ou {t_body} tirs buste."
                tactics = "Visez impérativement la tête pour contourner la plaque de sapeur."
            elif is_legend:
                t_name = "Joueur en Armure Légendaire Complète"
                t_head, t_body = h_legend_head, h_legend_body
                combo_note = f"{t_head} tirs tête ou {t_body} tirs buste."
                tactics = "Repli tactique recommandé après vos tirs initiaux pour recharger à couvert."
            else:
                t_name = "Joueur en Armure Verte (Cuirasse & Casque de Cuir)"
                t_head, t_body = h_green_head, h_green_body
                combo_note = combo_green
                tactics = green_tactics
        elif is_brute:
            t_name = "Brute (Monstre - 900 PV)"
            t_head, t_body = h_brute_head, h_brute_body
            combo_note = f"{t_head} tirs tête ou {t_body} tirs buste."
            tactics = "Gardez vos distances et tirez dans la tête lorsqu'elle charge."
        elif is_drooler:
            t_name = "Baveux (Drooler - 450 PV)"
            t_head, t_body = h_drooler_head, h_drooler_body
            combo_note = f"{t_head} tirs tête ou {t_body} tirs buste."
            tactics = "Éliminez-le rapidement à distance avant qu'il ne crache son bile acide."
        else:
            t_name = "Joueur en Armure Verte (Cuirasse & Casque de Cuir)"
            t_head, t_body = h_green_head, h_green_body
            combo_note = combo_green
            tactics = green_tactics

        if is_french:
            spoken = f"Avec le {f_name.split('(')[0].strip()}, il faut {t_head} tirs en pleine tête ou {t_body} tirs dans le buste pour tuer un {t_name}. Fiche transmise."
            display = (
                f"🎯 **SIMULATEUR DE TIR & TTK : {f_name.upper()} vs {t_name.upper()}**\\n\\n"
                f"• 🔫 **Arme :** **{f_name}** — Dégâts : **{f_dmg} par balle** ({f_ammo})\\n"
                f"• ⚡ **Cadence & Chargeur :** {f_clip} balles (Cadence : {f_rate} | Rechargement : {f_reload})\\n"
                f"• 🎯 **Cible :** **{t_name}**\\n"
                f"• 💥 **Tirs en Pleine Tête (Headshots) :** **{t_head} tirs**\\n"
                f"• 🛡️ **Tirs dans le Buste (Body Shots) :** **{t_body} tirs**\\n"
                f"• ⚡ **Combo d'Élimination Optimale :** **{combo_note}**\\n\\n"
                f"💡 **Conseil Tactique :** {tactics}\\n\\n"
                f"🖼️ *Fiche d'arme Hunger Companion jointe ci-dessous.*"
            )
        else:
            spoken = f"With the {f_name.split('(')[0].strip()}, it takes {t_head} headshots or {t_body} bodyshots to down a {t_name}."
            display = f"🎯 **GUNPLAY TTK : {f_name.upper()} vs {t_name.upper()}**\\n• Head: **{t_head} shots** | Body: **{t_body} shots**"

        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    """

text = text[:start_idx] + replacement_block + text[end_idx:]

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("Firearms TTK successfully patched for Auster, Deux, LongBoy and all targets!")
