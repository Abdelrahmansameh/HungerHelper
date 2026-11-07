import re

with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    brain_code = f.read()

# Replace character handling in brain.py
old_char_section = """        # -------------------------------------------------------------------
        # 1. CHARACTER & TACTICAL ABILITIES (e.g. "tactical de marie", "capacité de marie")
        # -------------------------------------------------------------------
        if any(w in lowered for w in ["tactical", "tactique", "capacité", "capacite", "ability", "personnage", "survivor"]) and any(w in lowered for w in ["marie", "jean", "claude"]):
            char_key = "marie"
            if "jean" in lowered: char_key = "jean"
            elif "claude" in lowered: char_key = "claude"
            
            card_path = render_character_card(char_key)
            if is_french:
                if char_key == "marie":
                    spoken = "Le tactical de Marie est Médecine de Terrain : soin rapide de 45 PV et réduction des saignements. Fiche visuelle transmise."
                else:
                    spoken = f"Voici la fiche tactique complète pour {char_key.title()}. Fiche visuelle transmise."
                display = f"⚔️ **PROFIL TACTIQUE : {char_key.upper()}**\\n*(Fiche de combat complète générée ci-dessous)*"
            else:
                spoken = f"Marie's tactical is Field Triage: heals 45 HP and halves bleed duration. Visual card dispatched."
                display = f"⚔️ **TACTICAL PROFILE : {char_key.upper()}**\\n*(Combat card attached below)*"
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}"""

new_char_section = """        # -------------------------------------------------------------------
        # 1. CHARACTER & TACTICAL ABILITIES (All 6 Official Heroes: Eva, Gabriel, Hugo, Marie, Otto, Serine)
        # -------------------------------------------------------------------
        hero_names = ["serine", "serene", "gabriel", "hugo", "otto", "marie", "eva"]
        hero_keywords = ["tactical", "tactique", "capacité", "capacite", "ability", "personnage", "survivor", "hero", "héros", "classe", "sort", "pouvoir", "competence", "compétence", "profil", "fiche"]
        
        matched_hero = None
        for h in hero_names:
            if h in lowered:
                matched_hero = "serine" if h == "serene" else h
                break

        if matched_hero and any(w in lowered for w in hero_keywords):
            card_path = render_character_card(matched_hero)
            
            hero_spoken_fr = {
                "eva": "Eva est la chasseresse vagabonde : Marathon réduit la perte d'endurance, Lightfoot élimine les bruits de pas et Blind aveugle l'ennemi. Fiche visuelle transmise.",
                "gabriel": "Gabriel est le soldat de fortune : Charge renforce les coups en sprint, Line Infantry fortifie la défense et Sadist redonne de la vigueur. Fiche visuelle transmise.",
                "hugo": "Hugo est le berserker maniaque : Taste of Blood accélère les frappes sur cible saignante, Zealot booste les dégâts et Maniac résiste aux stuns. Fiche transmise.",
                "marie": "Marie est la nonne guerrière : Gentle Touch accélère les soins de 50%, Vespers dissipe le poison et Mending Prayer restaure 45 PV. Fiche transmise.",
                "otto": "Otto est le sapeur d'élite : Maintenance préserve la durabilité d'armure, Field Repairs répare les plaques et Masterwork renforce l'armure. Fiche transmise.",
                "serine": "Serine est l'empoisonneuse vaudou : Vodou Spirit confère 30% d'immunité poison, Rush est une ruée corrosive et Vodou Bomb inflige des dégâts de zone toxiques. Fiche transmise."
            }
            hero_spoken_en = {
                "eva": "Eva is the Vagabond Huntress: Marathon reduces stamina drain, Lightfoot silences footsteps, and Blind disorients enemies. Visual card dispatched.",
                "gabriel": "Gabriel is the Soldier of Fortune: Charge buffs sprint attacks, Line Infantry boosts defense, and Sadist restores vigor. Visual card dispatched.",
                "hugo": "Hugo is the Maniac: Taste of Blood speeds attacks against bleeding foes, Zealot boosts damage, and Maniac provides stun resistance. Visual card dispatched.",
                "marie": "Marie is the Warrior Nun: Gentle Touch speeds healing by 50%, Vespers clears poison, and Mending Prayer heals 45 HP. Visual card dispatched.",
                "otto": "Otto is the Sergeant-at-Arms: Maintenance preserves armor durability, Field Repairs mends armor plates, and Masterwork fortifies defenses. Visual card dispatched.",
                "serine": "Serine is the Vodou Poisoner: Vodou Spirit grants poison resistance, Rush is a corrosive dash, and Vodou Bomb deals area toxic damage. Visual card dispatched."
            }
            
            if is_french:
                spoken = hero_spoken_fr.get(matched_hero, f"Voici la fiche tactique officielle pour {matched_hero.title()}. Fiche visuelle transmise.")
                display = f"⚔️ **PROFIL OFFICIEL DU HÉROS : {matched_hero.upper()} (HUNGER COMPANION)**\\n*(Fiche de personnage complète et compétences générées ci-dessous)*"
            else:
                spoken = hero_spoken_en.get(matched_hero, f"Here is the official tactical profile for {matched_hero.title()}. Visual card dispatched.")
                display = f"⚔️ **OFFICIAL HERO PROFILE : {matched_hero.upper()} (HUNGER COMPANION)**\\n*(Full combat sheet and abilities attached below)*"
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}"""

brain_norm = brain_code.replace("\r\n", "\n")
old_norm = old_char_section.replace("\r\n", "\n")
new_norm = new_char_section.replace("\r\n", "\n")

if old_norm in brain_norm:
    brain_norm = brain_norm.replace(old_norm, new_norm)
    with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
        f.write(brain_norm)
    print("SUCCESS: brain.py updated with all 6 heroes!")
else:
    print("WARNING: Old hero section not found in brain.py")

# Update game_knowledge.py for hit query variations & Auster/Deux reload details
with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    gk_code = f.read()

gk_norm = gk_code.replace("\r\n", "\n")

old_ttk_green = """            else: # Green / Default player
                t_name, t_head, t_body = "Joueur en Armure Verte (Cuirasse & Casque de Cuir)", 2, 3
                combo = "1 tir tête (78 dmg) + 1 tir buste (39 dmg) = 117 dmg = K.O. EN 0.25 SECONDE CHRONO !"
                tactics = "L'Auster tire ses 2 cartouches en 0.25s. Un combo tête puis buste abat un joueur en vert avant qu'il ne puisse lever son arme !" """

new_ttk_green = """            else: # Green / Default player
                t_name, t_head, t_body = "Joueur en Armure Verte (Cuirasse & Casque de Cuir - 120 PV)", 2, 3
                combo = "2 tirs tête = K.O. en 0.25s SANS recharger ! (Corps : 3 tirs, oblige à 12.6s de rechargement)"
                tactics = "Le chargeur ne contient que 2 balles ! Visez impérativement la tête : 2 balles en 0.25s tuent le joueur. Au corps, 2 balles ne font que 96 dégâts, vous obligeant à subir un rechargement complet de 12.6 secondes avant le 3ème tir !" """

old_gk_hit = """        "combien de coups", "combien de coup", "combien d'attaques", "combien dattaque",
        "combien de frappes", "how many hits", "how many strikes", "how many blows",
        "combien de tirs", "combien de tir", "combien de balles", "combien de balle",
        "how many shots", "how many bullets", "pour tuer", "tuer la brute", "tuer le baveux",
        "kill the brute", "kill drooler", "tuer une personne", "tuer un joueur", "tuer quelqu'un",
        "tuer en vert", "tuer en bleu", "joueur en vert", "joueur en cuir" """

new_gk_hit = """        "combien de coups", "combien de coup", "combien d'attaques", "combien dattaque",
        "combien de frappes", "how many hits", "how many strikes", "how many blows",
        "combien de tirs", "combien de tir", "combien de tire", "combien de balles", "combien de balle",
        "how many shots", "how many bullets", "pour tuer", "tuer la brute", "tuer le baveux",
        "kill the brute", "kill drooler", "tuer une personne", "tuer un joueur", "tuer quelqu'un",
        "tuer en vert", "tuer en bleu", "joueur en vert", "joueur en cuir", "en combien de coup",
        "en combien de tire", "en combien de coups", "en combien de tir" """

if old_ttk_green.strip() in gk_norm:
    gk_norm = gk_norm.replace(old_ttk_green.strip(), new_ttk_green.strip())
    print("SUCCESS: game_knowledge.py updated with Auster reload & green armor TTK!")

if old_gk_hit.strip() in gk_norm:
    gk_norm = gk_norm.replace(old_gk_hit.strip(), new_gk_hit.strip())
    print("SUCCESS: game_knowledge.py hit query keywords expanded!")

with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
    f.write(gk_norm)
