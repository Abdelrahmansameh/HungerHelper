import os

p = "co_pilot/game_knowledge.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = """def answer_combat_ttk_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    \"\"\"Calculates exact strikes / hits required to down enemies based on weapon and creature HP.\"\"\"
    lowered = query.lower()
    is_hit_query = any(w in lowered for w in [
        "combien de coups", "combien de coup", "combien d'attaques", "combien dattaque",
        "combien de frappes", "how many hits", "how many strikes", "how many blows",
        "tuer la brute", "tuer le baveux", "kill the brute", "kill drooler"
    ])
    if not is_hit_query:
        return None"""

replacement = """def answer_combat_ttk_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    \"\"\"Calculates exact strikes / hits required to down enemies based on weapon and creature HP.\"\"\"
    lowered = query.lower()
    is_hit_query = any(w in lowered for w in [
        "combien de coups", "combien de coup", "combien d'attaques", "combien dattaque",
        "combien de frappes", "how many hits", "how many strikes", "how many blows",
        "combien de tirs", "combien de tir", "combien de balles", "combien de balle",
        "how many shots", "how many bullets", "pour tuer", "tuer la brute", "tuer le baveux",
        "kill the brute", "kill drooler", "tuer une personne", "tuer un joueur", "tuer quelqu'un"
    ])
    if not is_hit_query:
        return None

    # 1. SPECIALIZED FIREARM TTK (e.g. Deux Pistol)
    is_deux = ("deux" in lowered or "pistolet" in lowered) and not ("deux mains" in lowered or "deux-mains" in lowered)
    if is_deux:
        from co_pilot.card_renderer import render_item_card
        card_path = render_item_card("deux")

        # Player targets with armours
        is_green = any(w in lowered for w in ["verte", "vert", "cuir", "leather", "uncommon", "non-commun", "non commune"])
        is_naked = any(w in lowered for w in ["sans armure", "nu", "naked", "no armour", "aucune"])
        is_blue = any(w in lowered for w in ["bleue", "bleu", "rare", "sapeur", "sapper"])
        is_legend = any(w in lowered for w in ["légendaire", "legendaire", "legendary", "lourde", "heavy"])
        is_brute = any(w in lowered for w in ["brute", "gros"])
        is_drooler = any(w in lowered for w in ["baveux", "drooler"])

        if is_green:
            t_name = "Joueur en Armure Verte (Cuirasse & Casque de Cuir)"
            t_head = 2
            t_body = 3
            combo_note = "1 tir en pleine tête (86 dégâts) + 1 tir corps (44 dégâts) = K.O. en 2 secondes !"
            tactics = "Le Deux dispose de 2 balles dans son canon rotatif. En enchaînant un tir tête suivi d'un tir corps, vous abattez votre cible sans devoir subir les 8.6s de rechargement !"
        elif is_naked:
            t_name = "Joueur Sans Armure (100 PV)"
            t_head = 1
            t_body = 2
            combo_note = "1 tir en pleine tête inflige 108 dégâts = ONE-SHOT MORTEL IMMÉDIAT !"
            tactics = "Une seule balle dans la tête neutralise instantanément une cible non casquée."
        elif is_blue:
            t_name = "Joueur en Armure Bleue (Cuirasse de Sapeur)"
            t_head = 2
            t_body = 3
            combo_note = "2 tirs tête ou 1 tête + 2 corps."
            tactics = "Visez impérativement la tête pour minimiser l'impact de la plaque de sapeur."
        elif is_legend:
            t_name = "Joueur en Armure Légendaire Complète"
            t_head = 4
            t_body = 4
            combo_note = "4 tirs tête ou 4 tirs buste (8 tirs dans les jambes)."
            tactics = "Contre une armure légendaire, désengagez après vos 2 premiers tirs pour recharger à l'abri."
        elif is_brute:
            t_name = "Brute (900 PV)"
            t_head = 9
            t_body = 17
            combo_note = "9 balles dans la tête ou 17 balles dans le corps."
            tactics = "Gardez vos distances et visez la tête pendant qu'elle charge son coup lourd."
        elif is_drooler:
            t_name = "Baveux (Drooler - 450 PV)"
            t_head = 5
            t_body = 9
            combo_note = "5 balles dans la tête ou 9 balles dans le corps."
            tactics = "Éliminez-le rapidement à distance avant qu'il ne crache son bile acide."
        else:
            t_name = "Joueur Standard en Armure Moyenne"
            t_head = 2
            t_body = 3
            combo_note = "2 tirs tête ou 1 tir tête + 1 tir corps."
            tactics = "Le double tir tête/corps garantit une élimination avant le rechargement."

        if is_french:
            spoken = f"Avec le Deux, il faut {t_head} tirs en pleine tête ou {t_body} tirs dans le buste pour tuer un {t_name}. Fiche tactique transmise."
            display = (
                f"🎯 **SIMULATEUR DE TIR & TTK : DEUX vs {t_name.upper()}**\\n\\n"
                f"• 🔫 **Arme :** **Deux (Pistolet Rare)** — Dégâts : **54 par balle** (Munitions Rudes)\\n"
                f"• 🎯 **Cible :** **{t_name}**\\n"
                f"• 💥 **Tirs en Pleine Tête (Headshots) :** **{t_head} tirs**\\n"
                f"• 🛡️ **Tirs dans le Buste (Body Shots) :** **{t_body} tirs**\\n"
                f"• ⚡ **Combo d'Élimination Optimale :** **{combo_note}**\\n\\n"
                f"💡 **Conseil Tactique :** {tactics}\\n\\n"
                f"🖼️ *Fiche d'arme Hunger Companion jointe ci-dessous.*"
            )
        else:
            spoken = f"With the Deux pistol, it takes {t_head} headshots or {t_body} bodyshots to down a {t_name}."
            display = f"🎯 **GUNPLAY TTK : DEUX vs {t_name.upper()}**\\n• Head: **{t_head} shots** | Body: **{t_body} shots**"

        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}"""

assert target in text, "target not found"
text = text.replace(target, replacement, 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("Combat TTK firearms & armour support patched successfully!")
