with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    cr = f.read().replace("\r\n", "\n")

old_cr = """def render_talent_build_card(build_query: str, is_french: bool = True) -> str:
    \"\"\"
    Embeds the user's saved preset build from mastery_build_summary.png
    Shows talent tree and icons summary directly.
    \"\"\"
    summary_path = os.path.join(ROOT_DIR, "mastery_build_summary.png")
    if os.path.exists(summary_path):
        out_path = os.path.join(OUT_DIR, "build_thrust-master.jpg")
        im = Image.open(summary_path).convert("RGB")
        im.save(out_path, quality=95)
        return out_path

    # Fallback to canvas
    canvas, draw = create_base_canvas("BUILD PRÉFAIT : MAÎTRE D'ESTOC", tag="TALENTS & MAÎTRISES")
    out_path = os.path.join(OUT_DIR, "build_thrust-master.jpg")
    canvas.convert("RGB").save(out_path, quality=95)
    return out_path"""

new_cr = """def render_talent_build_card(build_query: str, is_french: bool = True) -> str:
    \"\"\"
    Embeds the user's saved preset build from Hunger Companion talent trees.
    Shows the 5 disciplines (Cunning, Physiology, Survival, Martial, Arms)
    and the user's active 91-point build.
    \"\"\"
    card_path = os.path.join(OUT_DIR, "build_official_tree.jpg")
    if os.path.exists(card_path):
        return card_path
    from create_talent_tree_card import create_talent_tree_master_card
    return create_talent_tree_master_card()"""

if old_cr in cr:
    cr = cr.replace(old_cr, new_cr)
    with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
        f.write(cr)
    print("SUCCESS: card_renderer.py updated for official talent build card!")
else:
    print("WARNING: Old render_talent_build_card not found")

with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    gk = f.read().replace("\r\n", "\n")

old_gk_talent = """def answer_talent_advice_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    \"\"\"Recommend optimal talent distributions and builds based on user preference.\"\"\"
    lowered = query.lower()
    if not any(w in lowered for w in ["talent", "talents", "build", "arbre", "competence", "compétence", "stats"]):
        return None

    is_spear_thrust = any(w in lowered for w in ["spear", "lance", "thrust", "estoc", "zweihander", "hallebarde"])

    if is_french:
        if is_spear_thrust:
            spoken = "Pour un build Estoc avec la Lance ou le Zweihänder, maximisez la Maîtrise d'Estoc pour +15% d'allonge et la Récupération d'Énergie."
            display = (
                f"⚡ **BUILD RECOMMANDÉ : MAÎTRE D'ESTOC (SPEAR / ZWEI)**\\n\\n"
                f"1. 🗡️ **Maîtrise d'Allonge & Pénétration :** +15% dégâts d'estoc et perce l'armure moyenne.\\n"
                f"2. 🛡️ **Parade Parfaite :** Réduit le coût de garde de 5 à 3 points d'endurance.\\n"
                f"3. 🏃 **Endurance & Agilité :** +20% régénération d'énergie au sprint, idéal pour kiter les Brutes.\\n"
                f"4. 🩸 **Frappe Précise :** 2 coups suffisent pour abattre un joueur sans armure."
            )
        else:
            spoken = "Je vous conseille deux orientations : le build Maître d'Estoc pour infliger de lourds dégâts à distance, ou le build Pillard pour maximiser votre récolte de butin."
            display = (
                f"⚡ **CONSEILS DE TALENTS & BUILDS TACTIQUES :**\\n\\n"
                f"🗡️ **Option 1 : Maître d'Estoc (Combat Polyvalent)**\\n"
                f"• Synergie idéale avec Lance (48.3 estoc) et Zweihänder (52 estoc).\\n"
                f"• Priorité : Régénération d'endurance + Réduction du coût de garde.\\n\\n"
                f"🎒 **Option 2 : Pillard Rapide (Farm & Quêtes)**\\n"
                f"• Vitesse de fouille des conteneurs (+25%).\\n"
                f"• Capacité de portage accrue pour ramener plus d'argent et de sacs de farine.\\n"
                f"• Résistance accrue aux saignements."
            )
    else:
        if is_spear_thrust:
            spoken = "For a Thrust build with Spear or Zweihänder, prioritize Thrust Mastery for +15% range damage and Stamina Recovery."
            display = (
                f"⚡ **RECOMMENDED BUILD : THRUST MASTER (SPEAR / ZWEI)**\\n\\n"
                f"1. 🗡️ **Reach & Penetration :** +15% thrust damage, pierces medium armor.\\n"
                f"2. 🛡️ **Perfect Guard :** Reduces guard cost from 5 to 3 stamina.\\n"
                f"3. 🏃 **Stamina Agility :** +20% sprint stamina recovery, essential for kiting Brutes.\\n"
                f"4. 🩸 **Lethal Thrust :** Down unarmored targets in just 2 hits."
            )
        else:
            spoken = "I recommend two archetypes: Thrust Master for combat dominance with Spear/Zwei, or Swift Scavenger for loot efficiency."
            display = (
                f"⚡ **TACTICAL TALENT & BUILD GUIDANCE :**\\n\\n"
                f"🗡️ **Archetype 1 : Thrust Master (Combat)**\\n"
                f"• Synergizes with Spear (48.3 thrust) and Zweihänder (52 thrust).\\n"
                f"• Focus: Stamina recovery & guard efficiency.\\n\\n"
                f"🎒 **Archetype 2 : Swift Scavenger (Farm & Quests)**\\n"
                f"• +25% search speed on containers.\\n"
                f"• Increased carry capacity for bullion and quest materials.\\n"
                f"• Bleed resistance."
            )

    return {"spoken_text": spoken, "display_text": display}"""

new_gk_talent = """def answer_talent_advice_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    \"\"\"Answers queries regarding the user's authentic Hunger Companion talent build (91 points).\"\"\"
    lowered = query.lower()
    if not any(w in lowered for w in ["talent", "talents", "build", "arbre", "competence", "compétence", "stats", "maîtrise", "maitrise"]):
        return None

    from co_pilot.card_renderer import render_talent_build_card
    card_path = render_talent_build_card(query, is_french)

    if is_french:
        spoken = (
            "Voici votre arbre de talents officiel à 91 points : "
            "37 points en Arms avec Deft Strikes à 5 sur 5 pour le Zweihänder, "
            "36 points en Survival avec Surgeon à 5 sur 5, et 18 points en Physiology. Fiche transmise."
        )
        display = (
            "🌲 **VOTRE ARBRE DE TALENTS ACTUEL (91 POINTS DÉPENSÉS) :**\\n\\n"
            "• 🗡️ **ARMS (37 / 71) — Focus Armes Lourdes & Mêlée :**\\n"
            "  - **Deft Strikes (5/5) :** -25% d'énergie sur les attaques légères à 2 mains (parfait pour le Zweihänder).\\n"
            "  - Paliers I à VII complétés avec **Maîtrise Tier VIII d'Armes débloquée**.\\n\\n"
            "• 💉 **SURVIVAL (36 / 78) — Résilience & Soutien d'Escouade :**\\n"
            "  - **Surgeon (5/5) :** Relève les coéquipiers au sol 25% plus vite en combat.\\n"
            "  - Soins au feu de camp, résistance et **Maîtrise Tier VIII de Survie débloquée**.\\n\\n"
            "• 🏃 **PHYSIOLOGY (18 / 83) — Mobilité & Vitalité :**\\n"
            "  - Sprint prolongé (5/5), Vitalité max (5/5), Agilité au saut (5/5), Coagulation (3/5).\\n\\n"
            "• 🔒 **MARTIAL (0/74) & CUNNING (0/72) :** Aucun point investi (focus pur mêlée et survie).\\n\\n"
            "💡 *Fiche haute résolution reproduisant fidèlement l'arbre Hunger Companion jointe ci-dessous.*"
        )
    else:
        spoken = (
            "Here is your official 91-point Hunger Companion talent build: "
            "37 points in Arms with Deft Strikes at 5 out of 5 for two-handed melee, "
            "36 points in Survival with Surgeon at 5 out of 5, and 18 points in Physiology. Card dispatched."
        )
        display = (
            "🌲 **YOUR CURRENT TALENT BUILD (91 POINTS ALLOCATED) :**\\n\\n"
            "• 🗡️ **ARMS (37 / 71) :** Deft Strikes (5/5) -25% energy for 2H melee + Tier VIII Mastery.\\n"
            "• 💉 **SURVIVAL (36 / 78) :** Surgeon (5/5) +25% revive speed + Tier VIII Mastery.\\n"
            "• 🏃 **PHYSIOLOGY (18 / 83) :** Sprint stamina (5/5), Max health (5/5), Jump agility (5/5), Clotting (3/5).\\n"
            "• 🔒 **MARTIAL (0/74) & CUNNING (0/72) :** 0 points allocated."
        )

    return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}"""

if old_gk_talent in gk:
    gk = gk.replace(old_gk_talent, new_gk_talent)
    with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
        f.write(gk)
    print("SUCCESS: game_knowledge.py updated for official talent build query!")
else:
    print("WARNING: Old answer_talent_advice_query not found in game_knowledge.py")
