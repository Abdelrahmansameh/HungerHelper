# -*- coding: utf-8 -*-
import os
import re

# 1. UPDATE co_pilot/card_renderer.py
with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    cr_text = f.read()

# Let's insert find_item_icon and FIREARMS_DATA before render_item_card
find_item_icon_code = '''
def find_item_icon(name_or_slug: str):
    """Finds exact item / weapon / container icon without falling back to a canister."""
    q = name_or_slug.lower().strip()
    alias_map = {
        "family ring": "T_UI_Item_LouisFathersRing.png",
        "family": "T_UI_Item_LouisFathersRing.png",
        "bague": "T_UI_Item_LouisFathersRing.png",
        "anneau": "T_UI_Item_LouisFathersRing.png",
        "deux": "ID_Weap_Pistol_Rare01.webp",
        "auster": "ID_Weap_Pistol_Rare01.webp",
        "cavalier": "ID_Weap_Pistol_Rare01.webp",
        "pistolet": "ID_Weap_Pistol_Rare01.webp",
        "zweihander": "ID_Weap_2HMelee_Legendary02.webp",
        "zweihänder": "ID_Weap_2HMelee_Legendary02.webp",
        "deux mains": "ID_Weap_2HMelee_Legendary02.webp",
        "longboy": "longboy.png",
        "fusil": "longboy.png",
        "farine": "flour.png",
        "flour": "flour.png",
        "coarse flour": "T_UI_Item_CoarseFlour.png",
        "sang": "sealed_bloodbag.png",
        "pompe": "sealed_bloodbag.png",
        "pince": "sealed_bloodbag.png",
        "blood": "sealed_bloodbag.png",
        "baume": "tallow_balm.png",
        "balm": "tallow_balm.png",
        "potion": "tallow_balm.png",
        "munition": "heavy_ammunition.png",
        "ammunition": "heavy_ammunition.png",
        "cle": "gold_key.png",
        "clé": "gold_key.png",
        "key": "gold_key.png",
        "silver key": "silver_key.png",
        "gold key": "gold_key.png",
        "lance": "thick_branch.png",
        "spear": "thick_branch.png",
        "salpetre": "saltpetre.png",
        "salpêtre": "saltpetre.png",
        "charbon": "charcoal.png",
        "oeuf": "fresh_egg.png",
        "dague": "seamstress_needle.png",
        "bezoard": "bezoar.png",
        "bezoar": "bezoar.png"
    }
    for k, v in alias_map.items():
        if k in q:
            img = core.ITEM_IMGS.get(v)
            if img:
                return img
            p = os.path.join(ROOT_DIR, "assets", "items", v)
            if os.path.exists(p):
                return Image.open(p).convert("RGBA")
    clean = q.replace(" ", "_") + ".png"
    if clean in core.ITEM_IMGS:
        return core.ITEM_IMGS[clean]
    return core.CONTAINER_IMGS.get("strongbox.webp")


FIREARMS_DATA = {
    "auster": {
        "slug": "auster", "name_en": "Auster", "name_fr": "Auster",
        "category": "Pistolet à double canon", "rarity_en": "Uncommon", "rarity_fr": "Peu Commun",
        "bullet_dmg": 48.0, "head_dmg": 78.0, "fire_rate": 0.25, "reload": 12.6,
        "clip": "2 cartouches", "ammo": "Munitions Rudes", "sell_price": "3 50",
        "hits_green": "2 tirs tête (1 tête + 1 corps = K.O. en 0.25s)",
        "hits_naked": "1 tête (mortel) ou 2 corps",
        "hits_sapper": "2 tête ou 4 corps",
        "hits_legend": "5 tête ou 5 corps",
        "hits_brute": "10 tête ou 19 corps",
        "tip": "Cadence ultra-rapide de 0.25s entre tirs : un enchaînement tête puis corps abat un joueur en armure verte en 0.25s chrono !"
    },
    "deux": {
        "slug": "deux", "name_en": "Deux", "name_fr": "Deux",
        "category": "Pistolet rotatif lourd", "rarity_en": "Rare", "rarity_fr": "Rare",
        "bullet_dmg": 54.0, "head_dmg": 86.0, "fire_rate": 2.0, "reload": 8.6,
        "clip": "2 cartouches", "ammo": "Munitions Rudes", "sell_price": "5 00",
        "hits_green": "2 tirs tête (1 tête + 1 corps = K.O. en 2.0s)",
        "hits_naked": "1 tir tête (108 dmg) = ONE-SHOT !",
        "hits_sapper": "2 tête ou 3 corps",
        "hits_legend": "4 tête ou 4 corps",
        "hits_brute": "9 tête ou 17 corps",
        "tip": "Le Deux dispose de 2 canons rotatifs. Visez la tête puis le buste pour abattre la cible avant le rechargement !"
    },
    "longboy": {
        "slug": "longboy", "name_en": "LongBoy", "name_fr": "LongBoy",
        "category": "Fusil de tireur d'élite", "rarity_en": "Rare", "rarity_fr": "Rare",
        "bullet_dmg": 58.0, "head_dmg": 104.0, "fire_rate": 3.5, "reload": 6.5,
        "clip": "1 cartouche", "ammo": "Munitions Lourdes", "sell_price": "6 50",
        "hits_green": "1 tir tête (104 dmg) = ONE-SHOT MORTEL !",
        "hits_naked": "1 tir tête (116 dmg) = ONE-SHOT !",
        "hits_sapper": "2 tête ou 2 corps",
        "hits_legend": "3 tête ou 4 corps",
        "hits_brute": "8 tête ou 16 corps",
        "tip": "Portée maximale et puissance d'arrêt redoutable. One-shot garanti en pleine tête sur armures légères et moyennes !"
    },
    "cavalier": {
        "slug": "cavalier", "name_en": "Cavalier", "name_fr": "Cavalier",
        "category": "Pistolet d'officier", "rarity_en": "Epic", "rarity_fr": "Épique",
        "bullet_dmg": 52.0, "head_dmg": 84.0, "fire_rate": 1.2, "reload": 7.8,
        "clip": "2 cartouches", "ammo": "Munitions Rudes", "sell_price": "7 20",
        "hits_green": "2 tirs tête ou 3 buste",
        "hits_naked": "1 tête ou 2 buste",
        "hits_sapper": "2 tête ou 3 buste",
        "hits_legend": "4 tête ou 4 buste",
        "hits_brute": "9 tête ou 18 corps",
        "tip": "Maniement véloce et rechargement plus court que l'Auster. Idéal en arme secondaire pour les duels rapprochés."
    }
}
'''

# Replace icon search in render_item_card
old_icon_block = """    # Try finding item icon
    ico_img = None
    if icon_name:
        exact_disk_path = os.path.join(ROOT_DIR, "assets", "items", icon_name)
        if os.path.exists(exact_disk_path):
            try:
                ico_img = Image.open(exact_disk_path).convert("RGBA")
            except Exception:
                pass
    clean_key = item_name.lower().replace(" ", "_") + ".png"
    if not ico_img and icon_name and icon_name in core.ITEM_IMGS:
        ico_img = core.ITEM_IMGS[icon_name]
    elif clean_key in core.ITEM_IMGS:
        ico_img = core.ITEM_IMGS.get(clean_key)
    elif any(w in item_name.lower() for w in ["deux", "gun", "fusil", "pistolet", "longboy"]):
        ico_img = core.ITEM_IMGS.get("longboy.png")
    elif any(w in item_name.lower() for w in ["clef", "clé", "key"]):
        ico_img = core.ITEM_IMGS.get("gold_key.png") or core.ITEM_IMGS.get("silver_key.png")
    else:
        ico_img = core.CONTAINER_IMGS.get("strongbox.webp")"""

new_icon_block = """    # Try finding exact item icon
    ico_img = find_item_icon(icon_name or item_name)"""

# Update render_weapon_card completely to support both Firearms & Melee with icons and bars
weapon_fn_start = "def render_weapon_card(weapon_slug_or_name: str, is_french: bool = True) -> str:"
quest_fn_start = "def render_quest_card(quest_query: str, is_french: bool = True) -> str:"

w_start_idx = cr_text.find(weapon_fn_start)
q_start_idx = cr_text.find(quest_fn_start)
assert w_start_idx != -1 and q_start_idx != -1, "Indices for render_weapon_card not found"

new_render_weapon_card = '''def render_weapon_card(weapon_slug_or_name: str, is_french: bool = True) -> str:
    """
    Renders high-resolution weapon combat card faithful to Hunger Companion:
    - Official Rarity, Category, Damage Type, In-Game Weapon Icon
    - Visual Damage Bars for Melee or Gunplay Bars for Firearms
    - Guard stamina drain / Fire rate & Reload speed
    - Hits to Down (TTK) across player armor types
    - Market value and combat TTK advice
    """
    import sqlite3
    w_lowered = weapon_slug_or_name.lower().strip()

    # 1. FIREARMS (Auster, Deux, LongBoy, Cavalier, etc.)
    firearm_key = None
    for k in FIREARMS_DATA.keys():
        if k in w_lowered:
            firearm_key = k
            break
    if not firearm_key and ("pistolet" in w_lowered or "pistol" in w_lowered):
        firearm_key = "deux"
    elif not firearm_key and ("fusil" in w_lowered or "rifle" in w_lowered):
        firearm_key = "longboy"

    if firearm_key:
        f_data = FIREARMS_DATA[firearm_key]
        w_name = f_data["name_fr"] if is_french else f_data["name_en"]
        rarity = f_data["rarity_fr"] if is_french else f_data["rarity_en"]

        canvas, draw = create_base_canvas(f"FICHE ARME : {w_name.upper()} ({rarity.upper()})", tag="ARME À FEU")

        # Left Column
        left_box = [28, 86, 320, CARD_H - 28]
        draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

        # Weapon Icon Frame
        icon_frame = [left_box[0] + 16, left_box[1] + 16, left_box[2] - 16, left_box[1] + 180]
        draw.rounded_rectangle(icon_frame, radius=8, fill=(16, 16, 13), outline=core.BORDER_SUBTLE, width=1)
        w_ico = find_item_icon(firearm_key)
        if w_ico:
            core.paste_icon_safe(canvas, w_ico, (icon_frame[0] + 10, icon_frame[1] + 10, 160, 140), bg_color=(16, 16, 13))

        # Rarity badge
        rarity_box = [left_box[0] + 16, icon_frame[3] + 10, left_box[2] - 16, icon_frame[3] + 46]
        r_lower = rarity.lower()
        rarity_col = (
            core.COLOR_GOLD if "legend" in r_lower or "légend" in r_lower else
            core.PRIO_PURPLE if "epic" in r_lower or "épique" in r_lower else
            (70, 140, 240) if "rare" in r_lower else
            core.PRIO_YELLOW
        )
        draw.rounded_rectangle(rarity_box, radius=6, fill=(26, 22, 14), outline=rarity_col, width=1)
        rw = int(draw.textlength(rarity.upper(), font=core.F_CARD_TITLE))
        draw.text((int(rarity_box[0] + (rarity_box[2] - rarity_box[0] - rw) / 2), rarity_box[1] + 6), rarity.upper(), fill=rarity_col, font=core.F_CARD_TITLE)

        # Category
        draw.text((left_box[0] + 18, rarity_box[3] + 12), "CATÉGORIE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
        draw.text((left_box[0] + 18, rarity_box[3] + 34), f_data["category"], fill=core.COLOR_PARCHMENT, font=core.F_BODY)

        # Market Value
        raw_p = f_data["sell_price"].split()
        s_s, s_c = int(raw_p[0]), int(raw_p[1])
        draw.text((left_box[0] + 18, rarity_box[3] + 68), "VALEUR MARCHANDE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
        # S coin
        draw.ellipse([left_box[0] + 18, rarity_box[3] + 94, left_box[0] + 38, rarity_box[3] + 114], fill=(210, 215, 225), outline=(255, 255, 255), width=2)
        draw.text((left_box[0] + 24, rarity_box[3] + 95), "S", fill=(30, 30, 40), font=core.F_SMALL_BOLD)
        draw.text((left_box[0] + 46, rarity_box[3] + 90), f"{s_s} Argent", fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
        # C coin
        draw.ellipse([left_box[0] + 144, rarity_box[3] + 94, left_box[0] + 164, rarity_box[3] + 114], fill=(195, 115, 60), outline=(235, 145, 80), width=2)
        draw.text((left_box[0] + 150, rarity_box[3] + 95), "C", fill=(40, 20, 10), font=core.F_SMALL_BOLD)
        draw.text((left_box[0] + 172, rarity_box[3] + 90), f"{s_c} Cuivre", fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)

        # Ammo & Reload
        draw.text((left_box[0] + 18, rarity_box[3] + 128), "MUNITION & CHARGEUR :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
        draw.text((left_box[0] + 18, rarity_box[3] + 150), f"{f_data['clip']} · {f_data['ammo']}", fill=(190, 190, 170), font=core.F_BODY)

        # Right Column: Gunplay Stats Bars
        right_box = [340, 86, CARD_W - 28, CARD_H - 28]
        draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

        draw.text((right_box[0] + 20, right_box[1] + 16), "PROFIL BALISTIQUE & DÉGÂTS (HUNGER COMPANION)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

        gun_stats = [
            ("DÉGÂTS PAR BALLE (CORPS)", f_data["bullet_dmg"], 100.0, core.COLOR_GOLD),
            ("CRITIQUE PLEINE TÊTE (HEADSHOT)", f_data["head_dmg"], 120.0, (230, 80, 50)),
            ("CADENCE ENTRE TIRS (SECONDES)", 100.0 - min(100.0, f_data["fire_rate"] * 30), 100.0, core.PRIO_PURPLE),
            ("VITESSE DE RECHARGEMENT", 100.0 - min(100.0, f_data["reload"] * 7), 100.0, core.PRIO_YELLOW),
        ]

        by = right_box[1] + 56
        bar_max_w = right_box[2] - right_box[0] - 220

        for s_label, s_val, s_max, s_col in gun_stats:
            draw.text((right_box[0] + 20, by), s_label, fill=(200, 200, 180), font=core.F_SMALL_BOLD)
            bar_x = right_box[0] + 20
            bar_y = by + 24
            draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_max_w, bar_y + 16], radius=4, fill=(24, 24, 20), outline=core.BORDER_SUBTLE, width=1)
            fill_w = int(bar_max_w * max(0.1, min(1.0, s_val / s_max)))
            draw.rounded_rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + 16], radius=4, fill=s_col)
            draw.text((bar_x + bar_max_w + 16, bar_y - 4), f"{s_val:.1f}", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
            by += 54

        # TTK Advice Box
        adv_box = [right_box[0] + 18, by + 10, right_box[2] - 18, right_box[3] - 16]
        draw.rounded_rectangle(adv_box, radius=8, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=1)
        draw.text((adv_box[0] + 16, adv_box[1] + 12), "[TACTIQUE & TTK COMBAT] GUIDE D'ÉLIMINATION", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
        draw.text((adv_box[0] + 16, adv_box[1] + 40), f"• Joueur Armure Verte : {f_data['hits_green']}", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((adv_box[0] + 16, adv_box[1] + 66), f"• Conseil Pro : {f_data['tip'][:120]}", fill=(180, 180, 160), font=core.F_BODY)

        out_p = os.path.join(OUT_DIR, f"firearm_card_{firearm_key}.jpg")
        canvas.convert("RGB").save(out_p, quality=95)
        return out_p

    # 2. MELEE WEAPONS (Spear, Zweihander, Halberd, Sabre, Axe, Dagger)
    db_p = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hunger_helper.db"))
    conn = sqlite3.connect(db_p)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM weapons WHERE slug = ? OR name_en LIKE ? OR name_fr LIKE ? LIMIT 1",
              (w_lowered.replace(" ", "-"), f"%{weapon_slug_or_name}%", f"%{weapon_slug_or_name}%"))
    w_row = c.fetchone()
    conn.close()

    if not w_row:
        # Fallback to zweihander or spear
        w_data = {
            "name_en": "Spear", "name_fr": "Lance", "category": "melee", "rarity_en": "Rare", "rarity_fr": "Rare",
            "thrust_damage": 48.3, "heavy_damage": 58.0, "overhead_damage": 42.0, "light_damage": 42.0, "light_no_energy": 21.0,
            "energy_guard_held": "6 / 12 guard 5 held 25/s", "hits_to_down": "2 sans armure · 4 légendaire", "sell_price": "9 20"
        }
    else:
        w_data = dict(w_row)

    w_name = w_data["name_fr"] if is_french else w_data["name_en"]
    rarity = w_data["rarity_fr"] if is_french else w_data["rarity_en"]

    canvas, draw = create_base_canvas(f"FICHE ARME : {w_name.upper()} ({rarity.upper()})", tag="ARME DE COMBAT")

    # Left Column
    left_box = [28, 86, 320, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    # Icon frame
    icon_frame = [left_box[0] + 16, left_box[1] + 16, left_box[2] - 16, left_box[1] + 180]
    draw.rounded_rectangle(icon_frame, radius=8, fill=(16, 16, 13), outline=core.BORDER_SUBTLE, width=1)
    w_ico = find_item_icon(w_name)
    if w_ico:
        core.paste_icon_safe(canvas, w_ico, (icon_frame[0] + 10, icon_frame[1] + 10, 160, 140), bg_color=(16, 16, 13))

    # Rarity badge
    rarity_box = [left_box[0] + 16, icon_frame[3] + 10, left_box[2] - 16, icon_frame[3] + 46]
    r_lower = rarity.lower()
    rarity_col = (
        core.COLOR_GOLD if "legend" in r_lower or "légend" in r_lower else
        core.PRIO_PURPLE if "epic" in r_lower or "épique" in r_lower else
        (70, 140, 240) if "rare" in r_lower else
        core.PRIO_YELLOW
    )
    draw.rounded_rectangle(rarity_box, radius=6, fill=(26, 22, 14), outline=rarity_col, width=1)
    rw = int(draw.textlength(rarity.upper(), font=core.F_CARD_TITLE))
    draw.text((int(rarity_box[0] + (rarity_box[2] - rarity_box[0] - rw) / 2), rarity_box[1] + 6), rarity.upper(), fill=rarity_col, font=core.F_CARD_TITLE)

    # Category
    draw.text((left_box[0] + 18, rarity_box[3] + 12), "CATÉGORIE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, rarity_box[3] + 34), f"Arme de Mêlée ({w_data.get('category', 'Melee').title()})", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    # Sell price
    raw_p = w_data.get("sell_price", "3 80").strip().split()
    s_s, s_c = (int(raw_p[0]), int(raw_p[1])) if len(raw_p) >= 2 else (int(raw_p[0]) if raw_p and raw_p[0].isdigit() else 3, 0)

    draw.text((left_box[0] + 18, rarity_box[3] + 68), "VALEUR MARCHANDE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    # Coin disc S
    draw.ellipse([left_box[0] + 18, rarity_box[3] + 94, left_box[0] + 38, rarity_box[3] + 114], fill=(210, 215, 225), outline=(255, 255, 255), width=2)
    draw.text((left_box[0] + 24, rarity_box[3] + 95), "S", fill=(30, 30, 40), font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 46, rarity_box[3] + 90), f"{s_s} Argent", fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
    # Coin disc C
    draw.ellipse([left_box[0] + 144, rarity_box[3] + 94, left_box[0] + 164, rarity_box[3] + 114], fill=(195, 115, 60), outline=(235, 145, 80), width=2)
    draw.text((left_box[0] + 150, rarity_box[3] + 95), "C", fill=(40, 20, 10), font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 172, rarity_box[3] + 90), f"{s_c} Cuivre", fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)

    # Guard and hits to down
    draw.text((left_box[0] + 18, rarity_box[3] + 128), "PARADE & ENDURANCE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, rarity_box[3] + 150), w_data.get("energy_guard_held", "6 / 12 guard 5 held"), fill=(190, 190, 170), font=core.F_BODY)

    # Right Column: Visual Damage Bars like Hunger Companion!
    right_box = [340, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    draw.text((right_box[0] + 20, right_box[1] + 16), "PROFIL DE DÉGÂTS (HUNGER COMPANION)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    damage_stats = [
        ("DÉGÂTS D'ESTOC (THRUST)", float(w_data.get("thrust_damage", 40.0)), 100.0, core.COLOR_GOLD),
        ("ATTAQUE LOURDE (HEAVY)", float(w_data.get("heavy_damage", 60.0)), 100.0, (230, 80, 50)),
        ("ATTAQUE VERTICALE (OVERHEAD)", float(w_data.get("overhead_damage", 45.0)), 100.0, core.PRIO_PURPLE),
        ("ATTAQUE LÉGÈRE (LIGHT)", float(w_data.get("light_damage", 40.0)), 100.0, core.PRIO_YELLOW),
        ("SANS ÉNERGIE (NO STAMINA)", float(w_data.get("light_no_energy", 20.0)), 100.0, (140, 140, 140)),
    ]

    by = right_box[1] + 56
    bar_max_w = right_box[2] - right_box[0] - 220

    for s_label, s_val, s_max, s_col in damage_stats:
        draw.text((right_box[0] + 20, by), s_label, fill=(200, 200, 180), font=core.F_SMALL_BOLD)
        bar_x = right_box[0] + 20
        bar_y = by + 24
        draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_max_w, bar_y + 16], radius=4, fill=(24, 24, 20), outline=core.BORDER_SUBTLE, width=1)
        fill_w = int(bar_max_w * min(1.0, s_val / s_max))
        draw.rounded_rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + 16], radius=4, fill=s_col)
        draw.text((bar_x + bar_max_w + 16, bar_y - 4), f"{s_val:.1f}", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
        by += 54

    # TTK Advice Box
    adv_box = [right_box[0] + 18, by + 10, right_box[2] - 18, right_box[3] - 16]
    draw.rounded_rectangle(adv_box, radius=8, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=1)
    draw.text((adv_box[0] + 16, adv_box[1] + 12), "[TACTIQUE & TTK] ANALYSE DE COMBAT", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    h_dmg = float(w_data.get("heavy_damage", 60.0))
    t_dmg = float(w_data.get("thrust_damage", 40.0))
    b_hits_h = int(900 / h_dmg) + (1 if 900 % h_dmg else 0)
    b_hits_crit = int(900 / (t_dmg * 2.0)) + (1 if 900 % (t_dmg * 2.0) else 0)
    draw.text((adv_box[0] + 16, adv_box[1] + 40), f"• Brute Élite (900 PV) : {b_hits_h} frappes lourdes ou {b_hits_crit} coups d'estoc dans le dos !", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((adv_box[0] + 16, adv_box[1] + 66), f"• Recommandé avec : Marie (Soins) ou Jean (Tank lourd). Vitesse de frappe élevée.", fill=(180, 180, 160), font=core.F_BODY)

    out_p = os.path.join(OUT_DIR, f"weapon_card_{w_name.lower().replace(' ', '_')}.jpg")
    canvas.convert("RGB").save(out_p, quality=95)
    return out_p
'''

# Replace weapon card function
cr_text = cr_text[:w_start_idx] + new_render_weapon_card + "\n\n" + cr_text[q_start_idx:]

# Replace old icon block in render_item_card
if old_icon_block in cr_text:
    cr_text = cr_text.replace(old_icon_block, new_icon_block, 1)

# Add find_item_icon before render_item_card
item_card_start = "def render_item_card(item_name: str,"
cr_text = cr_text.replace(item_card_start, find_item_icon_code + "\n\n" + item_card_start, 1)

# Add render_stash_report_card at the end of card_renderer.py
stash_report_card_code = '''

# ---------------------------------------------------------------------------
# 1.9 STASH & INVENTORY APPRAISAL CARD
# ---------------------------------------------------------------------------

def render_stash_report_card(
    username: str = "Player",
    character_name: str = "Marie",
    profession_name: str = "Apothicaire",
    total_silver: int = 18,
    total_copper: int = 45,
    keep_items: Optional[List[str]] = None,
    sell_items: Optional[List[str]] = None,
    merchant_tip: Optional[str] = None
) -> str:
    """
    Renders high-resolution stash appraisal card:
    - User Profile (Character & Profession context)
    - Total Estimated Liquidity in Silver & Copper coins
    - Stash Rules: All consumables, armor plates, bags, food, armors, weapons, blood tools KEPT (even duplicates)
    - Conditional keep: Active quest items & character/profession craft components
    - Items to sell with estimated profit
    - Merchant price fluctuation reminder (±15% vendor rotations)
    """
    canvas, draw = create_base_canvas(f"ANALYSE DE STASH & INVENTAIRE : {username.upper()}", tag="ÉCONOMIE DU CHÂTEAU")

    # Left Column: Profile & Appraisal
    left_box = [28, 86, 340, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    draw.text((left_box[0] + 18, left_box[1] + 18), "PROFIL DE L'EXPÉDITIONNAIRE", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 52), f"Joueur : {username}", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 92), f"Personnage : {character_name}", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, left_box[1] + 120), f"Profession : {profession_name}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # Coins Box
    draw.text((left_box[0] + 18, left_box[1] + 165), "VALEUR TOTALE À VENDRE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    
    # S coin
    draw.ellipse([left_box[0] + 18, left_box[1] + 195, left_box[0] + 44, left_box[1] + 221], fill=(210, 215, 225), outline=(255, 255, 255), width=2)
    draw.text((left_box[0] + 26, left_box[1] + 197), "S", fill=(30, 30, 40), font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 54, left_box[1] + 193), f"{total_silver} Argent", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # C coin
    draw.ellipse([left_box[0] + 170, left_box[1] + 195, left_box[0] + 196, left_box[1] + 221], fill=(195, 115, 60), outline=(235, 145, 80), width=2)
    draw.text((left_box[0] + 178, left_box[1] + 197), "C", fill=(40, 20, 10), font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 206, left_box[1] + 193), f"{total_copper} Cuivre", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # Merchant rotation note
    rot_box = [left_box[0] + 16, left_box[1] + 245, left_box[2] - 16, left_box[1] + 440]
    draw.rounded_rectangle(rot_box, radius=8, fill=(20, 18, 14), outline=core.BORDER_SUBTLE, width=1)
    draw.text((rot_box[0] + 12, rot_box[1] + 12), "⚖️ MARCHÉ & ROTATIONS :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    m_text = merchant_tip or (
        "Les marchands du Château appliquent des fluctuations de prix (+-15%) selon le cycle de rotation de leur stock quotidien. "
        "Ne vendez que vos surplus non vitaux pour maximiser vos gains en argent !"
    )
    # Wrap text simply
    words = m_text.split()
    l_cur = ""
    my = rot_box[1] + 40
    for w in words:
        if len(l_cur + " " + w) > 34:
            draw.text((rot_box[0] + 12, my), l_cur, fill=(180, 180, 160), font=core.F_SMALL_BOLD)
            l_cur = w
            my += 22
        else:
            l_cur += (" " if l_cur else "") + w
    if l_cur:
        draw.text((rot_box[0] + 12, my), l_cur, fill=(180, 180, 160), font=core.F_SMALL_BOLD)

    # Right Column: Keep vs Sell Breakdown
    right_box = [360, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    # Top Half: KEEP IN STASH (Green/Gold theme)
    k_box = [right_box[0] + 16, right_box[1] + 16, right_box[2] - 16, right_box[1] + 225]
    draw.rounded_rectangle(k_box, radius=8, fill=(18, 26, 18), outline=(60, 150, 60), width=1)
    draw.text((k_box[0] + 16, k_box[1] + 12), "🔒 À GARDER EN STASH (AUCUNE VENTE - DOUBLONS CONSERVÉS) :", fill=(100, 220, 100), font=core.F_SECTION_TITLE)

    default_keep = [
        "• Consommables : Potions de vie, baumes, plaques d'armure & vivres (Pain/Soupe).",
        "• Équipement de Raid : Toutes armures, sacs, armes et munitions (même en doublon).",
        "• Outils de Sang : Pinces et pompes de prélèvement d'échantillons sanguins scellées.",
        f"• Quêtes & Craft : Objets pour quêtes actives et composants dédiés à {character_name} & {profession_name}."
    ]
    lines_k = keep_items if keep_items else default_keep
    ky = k_box[1] + 44
    for kl in lines_k[:4]:
        draw.text((k_box[0] + 16, ky), kl[:75], fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        ky += 38

    # Bottom Half: SELL TO MERCHANTS (Gold/Red theme)
    s_box = [right_box[0] + 16, k_box[3] + 14, right_box[2] - 16, right_box[3] - 16]
    draw.rounded_rectangle(s_box, radius=8, fill=(28, 20, 16), outline=(200, 140, 50), width=1)
    draw.text((s_box[0] + 16, s_box[1] + 12), "🛒 À VENDRE AUX MARCHANDS DU CHÂTEAU (LIQUIDATION OPTIMALE) :", fill=core.PRIO_YELLOW, font=core.F_SECTION_TITLE)

    default_sell = [
        "• Bric-à-brac sans utilité : Bibelots, assiettes ternies, chiffons sans recette.",
        "• Trophées inutilisés : Parties de monstres non demandées par vos quêtes actuelles.",
        f"• Surplus d'artisanat : Composants hors-profession ({profession_name}) à convertir en espèces.",
        f"• Bénéfice Net Estimé : {total_silver} Pièces d'Argent et {total_copper} Pièces de Cuivre !"
    ]
    lines_s = sell_items if sell_items else default_sell
    sy = s_box[1] + 44
    for sl in lines_s[:4]:
        draw.text((s_box[0] + 16, sy), sl[:75], fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        sy += 38

    out_p = os.path.join(OUT_DIR, f"stash_report_{username.lower().replace(' ', '_')}.jpg")
    canvas.convert("RGB").save(out_p, quality=95)
    return out_p
'''

cr_text += stash_report_card_code

with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(cr_text)

print("[OK] card_renderer.py patched successfully.")
