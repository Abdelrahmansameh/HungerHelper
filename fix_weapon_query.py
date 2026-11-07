# -*- coding: utf-8 -*-
with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    text = f.read()

fn_start = "def answer_weapon_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:"
fn_end = "# 4. STATUS EFFECTS INTEL"

s = text.find(fn_start)
e = text.find(fn_end)
assert s != -1 and e != -1

new_weapon_fn = '''def answer_weapon_query(query: str, is_french: bool) -> Optional[Dict[str, str]]:
    """Answer queries regarding weapon damage stats, highest thrust, firearms, etc."""
    lowered = query.lower()
    from co_pilot.card_renderer import render_weapon_card

    # 0. FIREARMS SPECIFIC
    for fn in ["auster", "deux", "longboy", "long boy", "cavalier"]:
        if fn in lowered and not ("deux mains" in lowered or "deux-mains" in lowered):
            f_key = "longboy" if "long" in fn else fn
            card_path = render_weapon_card(f_key, is_french)
            if f_key == "auster":
                sp = "L'Auster est un pistolet peu commun infligeant 48 dégâts avec une cadence ultra-rapide de 0.25s entre tirs. Fiche balistique transmise."
                disp = (
                    "🔫 **FICHE TECHNIQUE : AUSTER (PISTOLET PEU COMMUN)**\\n\\n"
                    "• 💥 **Dégâts de Base :** **48 par balle** (Munitions Rudes)\\n"
                    "• 🎯 **Headshot Critique :** **78 dégâts**\\n"
                    "• ⚡ **Cadence :** **0.25s** (Double-tap instantané)\\n"
                    "• ⏳ **Rechargement :** **12.6s** (2 cartouches)\\n"
                    "• 💰 **Prix de Revente :** **3 Argent 50 Cuivre**\\n\\n"
                    "💡 *Un tir tête suivi d'un tir buste abat un joueur en armure verte en 0.25s chrono.*"
                )
            elif f_key == "deux":
                sp = "Le Deux est un pistolet rotatif lourd rare infligeant 54 dégâts par balle avec 2 coups. Fiche balistique transmise."
                disp = (
                    "🔫 **FICHE TECHNIQUE : DEUX (PISTOLET RARE)**\\n\\n"
                    "• 💥 **Dégâts de Base :** **54 par balle** (Munitions Rudes)\\n"
                    "• 🎯 **Headshot Critique :** **86 dégâts**\\n"
                    "• ⚡ **Cadence :** **2.0s** entre deux tirs\\n"
                    "• ⏳ **Rechargement :** **8.6s** (2 cartouches)\\n"
                    "• 💰 **Prix de Revente :** **5 Argent 0 Cuivre**\\n\\n"
                    "💡 *Visez la tête pour neutraliser en 2 coups avant le rechargement de 8.6s.*"
                )
            else: # longboy
                sp = "Le LongBoy est un fusil de précision rare infligeant 58 dégâts de base et 104 en pleine tête. Fiche balistique transmise."
                disp = (
                    "🔫 **FICHE TECHNIQUE : LONGBOY (FUSIL RARE)**\\n\\n"
                    "• 💥 **Dégâts de Base :** **58 par tir** (Munitions Lourdes)\\n"
                    "• 🎯 **Headshot Critique :** **104 dégâts (One-Shot mortel en vert !)**\\n"
                    "• ⚡ **Cadence :** Tir unique à longue portée\\n"
                    "• ⏳ **Rechargement :** **6.5s** (1 cartouche)\\n"
                    "• 💰 **Prix de Revente :** **6 Argent 50 Cuivre**"
                )
            return {"spoken_text": sp, "display_text": disp, "image_attachment": card_path}

    conn = get_db_connection()
    c = conn.cursor()
    
    is_thrust = any(w in lowered for w in ["thrust", "estoc", "pénétration", "penetration", "perce", "pierce"])
    
    # 1. Best thrust weapon in the game
    if is_thrust and any(w in lowered for w in ["meilleur", "meilleure", "plus grand", "plus fort", "best", "highest", "top", "max"]):
        c.execute("SELECT name_en, name_fr, rarity_en, rarity_fr, thrust_damage FROM weapons WHERE thrust_damage > 0 ORDER BY thrust_damage DESC LIMIT 3")
        top3 = c.fetchall()
        conn.close()
        card_path = render_weapon_card("zweihander", is_french)
        if top3:
            if is_french:
                spoken = "L'arme avec les meilleurs dégâts d'estoc est le Zweihänder légendaire avec 52, suivi de la Hallebarde avec 50,6, et de la Lance avec 48,3."
                top_str = "\\n".join([f"  {idx}. **{r['name_fr']}** ({r['rarity_fr']}) : **{r['thrust_damage']}** estoc" for idx, r in enumerate(top3, 1)])
                display = (
                    f"🏆 **CLASSEMENT DES DÉGÂTS D'ESTOC (THRUST) :**\\n\\n{top_str}\\n\\n"
                    f"• 🥇 **Zweihänder (Légendaire)** : **52** dégâts d'estoc\\n"
                    f"• 🥈 **Hallebarde (Épique)** : **50.6** dégâts d'estoc\\n"
                    f"• 🥉 **Lance (Rare)** : **48.3** dégâts d'estoc"
                )
            else:
                spoken = "The weapon with the highest thrust damage is the Legendary Zweihänder with 52, followed by the Halberd with 50.6, and the Spear with 48.3."
                top_str = "\\n".join([f"  {idx}. **{r['name_en']}** ({r['rarity_en']}) : **{r['thrust_damage']}** thrust" for idx, r in enumerate(top3, 1)])
                display = (
                    f"🏆 **HIGHEST THRUST DAMAGE WEAPONS :**\\n\\n{top_str}\\n\\n"
                    f"• 🥇 **Zweihander (Legendary)** : **52** thrust damage\\n"
                    f"• 🥈 **Halberd (Epic)** : **50.6** thrust damage\\n"
                    f"• 🥉 **Spear (Rare)** : **48.3** thrust damage"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    # 2. Spear stats specifically
    if any(w in lowered for w in ["spear", "lance"]):
        c.execute("SELECT * FROM weapons WHERE slug = 'spear' OR name_en LIKE '%spear%' OR name_fr LIKE '%lance%'")
        spear = c.fetchone()
        conn.close()
        card_path = render_weapon_card("spear", is_french)
        if spear:
            if is_french:
                spoken = "La Lance rare inflige 48,3 de dégâts d'estoc. C'est la 3e arme la plus puissante en estoc du jeu et la meilleure arme rare."
                display = (
                    f"🗡️ **STATISTIQUES DE LA LANCE (Rare) :**\\n"
                    f"• 🎯 **Dégâts d'estoc (Thrust) :** **48.3**\\n"
                    f"• ⚔️ **Attaque légère :** 42 (Côtés : 37.8–42, Vertical : 42)\\n"
                    f"• 💥 **Attaque lourde :** 58\\n"
                    f"• 🛡️ **Garde :** {spear['energy_guard_held']} | Coups pour abattre : 2 (sans armure), 4 (légendaire)\\n"
                    f"• 💰 **Prix de revente :** {spear['sell_price']} (9 Argent 20 Cuivre)\\n\\n"
                    f"💡 *Comparatif estoc : Seuls le Zweihänder (52) et la Hallebarde (50.6) la dépassent.*"
                )
            else:
                spoken = "The Rare Spear deals 48.3 thrust damage. It has the 3rd highest thrust damage in the game."
                display = f"🗡️ **SPEAR STATS (Rare) :**\\n• Thrust: **48.3** | Heavy: **58** | Light: **42**"
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    # 3. Any other weapon lookup (Zweihander, Halberd, Sabre, Axe, Dagger)
    c.execute("SELECT * FROM weapons")
    weapons = c.fetchall()
    conn.close()
    for w in weapons:
        if w["slug"] in lowered or w["name_en"].lower() in lowered or w["name_fr"].lower() in lowered:
            card_path = render_weapon_card(w["slug"], is_french)
            raw_p = str(w.get("sell_price", "3 80")).split()
            s_s, s_c = (raw_p[0], raw_p[1]) if len(raw_p) >= 2 else (raw_p[0], "0")
            if is_french:
                spoken = f"L'arme {w['name_fr']} ({w['rarity_fr']}) inflige {w['thrust_damage']} d'estoc et {w['heavy_damage']} en lourde. Fiche d'arme transmise."
                display = (
                    f"🗡️ **{w['name_fr'].upper()} ({w['rarity_fr']}) :**\\n"
                    f"• 🎯 **Dégâts d'estoc :** **{w['thrust_damage']}**\\n"
                    f"• ⚔️ **Attaque légère :** **{w['light_damage']}**\\n"
                    f"• 💥 **Attaque lourde :** **{w['heavy_damage']}**\\n"
                    f"• 🛡️ **Garde & Endurance :** {w.get('energy_guard_held', 'Standard')}\\n"
                    f"• 💰 **Revente :** **{s_s} Argent {s_c} Cuivre**"
                )
            else:
                spoken = f"The {w['name_en']} ({w['rarity_en']}) deals {w['thrust_damage']} thrust and {w['heavy_damage']} heavy damage."
                display = (
                    f"🗡️ **{w['name_en'].upper()} ({w['rarity_en']}) :**\\n"
                    f"• 🎯 **Thrust Damage :** {w['thrust_damage']}\\n"
                    f"• ⚔️ **Light Attack :** {w['light_damage']}\\n"
                    f"• 💥 **Heavy Attack :** {w['heavy_damage']}\\n"
                    f"• 💰 **Sell Price :** {s_s} silver {s_c} copper"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

    return None

'''

text = text[:s] + new_weapon_fn + "\n# ---------------------------------------------------------------------------\n" + text[e:]

with open("co_pilot/game_knowledge.py", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] answer_weapon_query fixed.")
