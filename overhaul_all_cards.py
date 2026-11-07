import os
import math
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import perfect_briefings_core_v25 as core

CARD_W = 1200
CARD_H = 750

ROOT_DIR = r"C:\Users\PC\Documents\HungerHelper"
OUT_DIR = os.path.join(ROOT_DIR, "output_maps")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
ARTIFACT_DIR = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49"
DESKTOP_DIR = r"C:\Users\PC\Desktop\Hunger_Helper"

os.makedirs(OUT_DIR, exist_ok=True)

RARITY_COLORS = {
    "common": ((160, 160, 160), "COMMON", (30, 30, 30)),
    "uncommon": ((80, 200, 120), "UNCOMMON", (20, 45, 25)),
    "rare": ((70, 150, 240), "RARE", (20, 35, 55)),
    "epic": ((180, 100, 230), "EPIC", (45, 25, 60)),
    "legendary": ((245, 200, 60), "LEGENDARY", (55, 45, 15)),
}

def create_base_canvas(title: str, tag: str = "COMPAGNON TACTIQUE", border_col=None):
    canvas = Image.new("RGBA", (CARD_W, CARD_H), (15, 14, 12, 255))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, CARD_W, CARD_H], fill=(15, 14, 12))
    b_col = border_col or core.COLOR_GOLD
    draw.rounded_rectangle([10, 10, CARD_W - 10, CARD_H - 10], radius=12, outline=b_col, width=2)

    draw.rounded_rectangle([28, 22, 185, 54], radius=6, fill=(28, 22, 14), outline=b_col, width=1)
    draw.text((38, 30), tag, fill=b_col, font=core.F_HEADER_TAG)
    draw.text((200, 24), title, fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.line([(28, 68), (CARD_W - 28, 68)], fill=core.BORDER_SUBTLE, width=1)
    return canvas, draw

def safe_paste(canvas, img, box):
    im = img.convert("RGBA")
    w = max(10, box[2] - box[0])
    h = max(10, box[3] - box[1])
    im.thumbnail((w, h), Image.Resampling.LANCZOS)
    x = box[0] + (w - im.size[0]) // 2
    y = box[1] + (h - im.size[1]) // 2
    alpha = im.split()[3]
    canvas.paste(im, (x, y), alpha)

def save_and_copy(canvas, filename):
    out_p = os.path.join(OUT_DIR, filename)
    canvas.convert("RGB").save(out_p, quality=95)
    art_p = os.path.join(ARTIFACT_DIR, filename)
    try:
        canvas.convert("RGB").save(art_p, quality=95)
    except Exception:
        pass
    print(f"Generated & Saved: {filename}")
    return out_p

# ===========================================================================
# 1. MELEE WEAPONS WITH DIRECTIONAL ATTACK WHEEL & PLAYER HTK (NO BRUTE!)
# ===========================================================================
def render_clean_melee_card(weapon_slug: str, is_french: bool = True) -> str:
    db_p = os.path.join(ROOT_DIR, "hunger_helper.db")
    conn = sqlite3.connect(db_p)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM weapons WHERE slug LIKE ? OR name_en LIKE ? LIMIT 1", (f"%{weapon_slug}%", f"%{weapon_slug}%"))
    w_row = c.fetchone()
    conn.close()

    if not w_row:
        w = {
            "name_en": "Longsword", "name_fr": "Longsword", "rarity_en": "Uncommon",
            "light_damage": 38.0, "thrust_damage": 38.0, "overhead_damage": 38.0,
            "heavy_damage": 49.0, "light_no_energy": 19.0, "sell_price": "5 25"
        }
    else:
        w = dict(w_row)

    rarity_k = w.get("rarity_en", "Uncommon").lower()
    text_col, tag_lbl, bg_tint = RARITY_COLORS.get(rarity_k, RARITY_COLORS["uncommon"])
    w_name = w["name_en"] if not is_french else (w["name_fr"] if w.get("name_fr") else w["name_en"])

    canvas, draw = create_base_canvas(f"FICHE D'ARME : {w_name.upper()} ({tag_lbl})", tag="ARME DE MÊLÉE", border_col=text_col)

    # Left Column: Image, Price, Directional Wheel
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=text_col, width=2)

    # Rarity banner inside
    draw.rounded_rectangle([left_box[0] + 16, left_box[1] + 12, left_box[2] - 16, left_box[1] + 40], radius=6, fill=bg_tint, outline=text_col, width=1)
    draw.text((left_box[0] + 26, left_box[1] + 18), f"Rareté : {tag_lbl}", fill=text_col, font=core.F_SMALL_BOLD)

    # Weapon Icon
    img_name = f"T_UI_Item_{w['name_en'].replace(' ', '')}.png"
    w_img_p = os.path.join(ASSETS_DIR, "items", img_name)
    if not os.path.exists(w_img_p):
        w_img_p = os.path.join(ASSETS_DIR, "items", f"T_UI_Item_{w['name_en']}.png")
    if not os.path.exists(w_img_p):
        w_img_p = os.path.join(ASSETS_DIR, "items", "T_UI_Item_Longsword.png")

    icon_frame = [left_box[0] + 16, left_box[1] + 48, left_box[2] - 16, left_box[1] + 180]
    draw.rounded_rectangle(icon_frame, radius=8, fill=(16, 16, 13), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(w_img_p):
        safe_paste(canvas, Image.open(w_img_p), icon_frame)

    # Sell price
    raw_p = str(w.get("sell_price", "5 25")).split()
    s_s, s_c = (int(raw_p[0]), int(raw_p[1])) if len(raw_p) >= 2 else (int(raw_p[0]), 0)
    draw.text((left_box[0] + 20, icon_frame[3] + 10), "PRIX DE BASE AU MARCHÉ :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.ellipse([left_box[0] + 20, icon_frame[3] + 30, left_box[0] + 38, icon_frame[3] + 48], fill=(210, 215, 225), outline=(255, 255, 255), width=2)
    draw.text((left_box[0] + 25, icon_frame[3] + 31), "S", fill=(30, 30, 40), font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 44, icon_frame[3] + 28), f"{s_s} Argent", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    draw.ellipse([left_box[0] + 160, icon_frame[3] + 30, left_box[0] + 178, icon_frame[3] + 48], fill=(195, 115, 60), outline=(235, 145, 80), width=2)
    draw.text((left_box[0] + 165, icon_frame[3] + 31), "C", fill=(40, 20, 10), font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 184, icon_frame[3] + 28), f"{s_c} Cuivre", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # Directional Attack Compass Wheel (HUNGER COMPANION EXACT REPLICA!)
    draw.text((left_box[0] + 20, icon_frame[3] + 64), "CADRAN D'ATTAQUES DIRECTIONNELLES :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    
    wheel_cx = (left_box[0] + left_box[2]) // 2
    wheel_cy = icon_frame[3] + 195
    rad = 85

    draw.ellipse([wheel_cx - rad, wheel_cy - rad, wheel_cx + rad, wheel_cy + rad], outline=(60, 55, 45), width=2)
    draw.line([(wheel_cx, wheel_cy - rad), (wheel_cx, wheel_cy + rad)], fill=(60, 55, 45), width=1)
    draw.line([(wheel_cx - rad, wheel_cy), (wheel_cx + rad, wheel_cy)], fill=(60, 55, 45), width=1)
    draw.line([(wheel_cx - rad * 0.7, wheel_cy - rad * 0.7), (wheel_cx + rad * 0.7, wheel_cy + rad * 0.7)], fill=(45, 40, 35), width=1)
    draw.line([(wheel_cx - rad * 0.7, wheel_cy + rad * 0.7), (wheel_cx + rad * 0.7, wheel_cy - rad * 0.7)], fill=(45, 40, 35), width=1)

    t_dmg = float(w.get("thrust_damage", 38.0))
    l_dmg = float(w.get("light_damage", 38.0))
    o_dmg = float(w.get("overhead_damage", 38.0))
    h_dmg = float(w.get("heavy_damage", 49.0))
    side_dmg = 43.7 if "longsword" in w["name_en"].lower() else l_dmg
    out_dmg = float(w.get("light_no_energy", 19.0))

    # Overhead
    draw.text((wheel_cx - 15, wheel_cy - rad - 22), f"↑ {o_dmg:.1f}", fill=text_col, font=core.F_SMALL_BOLD)
    # Thrust
    draw.rounded_rectangle([wheel_cx - 28, wheel_cy - 14, wheel_cx + 28, wheel_cy + 14], radius=4, fill=(24, 20, 14), outline=text_col, width=1)
    draw.text((wheel_cx - 20, wheel_cy - 9), f"Estoc {t_dmg:.0f}", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    # Sides
    draw.text((wheel_cx + rad + 6, wheel_cy - 8), f"{side_dmg:.1f}", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)
    draw.text((wheel_cx - rad - 38, wheel_cy - 8), f"{side_dmg:.1f}", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)
    # Diagonals
    draw.text((wheel_cx + rad*0.6, wheel_cy - rad*0.6 - 10), f"{side_dmg:.1f}", fill=(180, 180, 160), font=core.F_BODY)
    draw.text((wheel_cx - rad*0.6 - 28, wheel_cy - rad*0.6 - 10), f"{side_dmg:.1f}", fill=(180, 180, 160), font=core.F_BODY)
    draw.text((wheel_cx + rad*0.6, wheel_cy + rad*0.6 - 2), f"{side_dmg:.1f}", fill=(180, 180, 160), font=core.F_BODY)
    draw.text((wheel_cx - rad*0.6 - 28, wheel_cy + rad*0.6 - 2), f"{side_dmg:.1f}", fill=(180, 180, 160), font=core.F_BODY)

    # Badges Heavy & Out of energy
    draw.rounded_rectangle([left_box[0] + 20, left_box[3] - 48, left_box[0] + 165, left_box[3] - 14], radius=6, fill=(45, 20, 16), outline=(220, 70, 50), width=1)
    draw.text((left_box[0] + 28, left_box[3] - 42), f"Attaque Lourde : {h_dmg:.0f}", fill=(255, 140, 120), font=core.F_SMALL_BOLD)

    draw.rounded_rectangle([left_box[0] + 180, left_box[3] - 48, left_box[2] - 20, left_box[3] - 14], radius=6, fill=(24, 24, 24), outline=(80, 80, 80), width=1)
    draw.text((left_box[0] + 192, left_box[3] - 42), f"Sans Énergie : {out_dmg:.0f}", fill=(160, 160, 160), font=core.F_SMALL_BOLD)

    # -------------------------------------------------------------
    # Right Column: PvP HTK Table by Armor Tier (NO BRUTE!)
    # -------------------------------------------------------------
    right_box = [400, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 16), "TABLEAU HIT TO KILL (HTK) VS JOUEURS EN RAID", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    armor_tiers = [
        ("Naked", "Joueur Nu / Sans Armure (100 PV)", (160, 160, 160), 100, None, None, 2, 3),
        ("Uncommon", "Armure Verte / Uncommon (140 PV)", (80, 200, 120), 140, "T_UI_Item_ArmorHead_Uncommon.png", "T_UI_Item_ArmorChest_Uncommon.png", 2, 3),
        ("Rare", "Armure Bleue / Sapeur (160 PV)", (70, 150, 240), 160, "T_UI_Item_ArmorHead_Rare.png", "T_UI_Item_ArmorChest_Rare.png", 2, 4),
        ("Epic", "Armure Épique / Renforcée (180 PV)", (180, 100, 230), 180, "T_UI_Item_ArmorHead_Epic.png", "T_UI_Item_ArmorChest_Epic.png", 3, 4),
        ("Legendary", "Armure Légendaire Complète (200 PV)", (245, 200, 60), 200, "T_UI_Item_ArmorHead_Legendary.png", "T_UI_Item_ArmorChest_Legendary.png", 3, 5),
    ]

    ay = right_box[1] + 54
    for key, title, col, hp, helm_ico, chest_ico, h_hits, b_hits in armor_tiers:
        box = [right_box[0] + 18, ay, right_box[2] - 18, ay + 82]
        draw.rounded_rectangle(box, radius=8, fill=core.BG_CARD, outline=col, width=1)

        draw.text((box[0] + 16, box[1] + 10), title, fill=col, font=core.F_SMALL_BOLD)

        hx = box[0] + 16
        if helm_ico:
            hp_p = os.path.join(ASSETS_DIR, "armor", helm_ico)
            if os.path.exists(hp_p):
                safe_paste(canvas, Image.open(hp_p), [hx, box[1] + 34, hx + 40, box[1] + 74])
                hx += 46

        if chest_ico:
            cp_p = os.path.join(ASSETS_DIR, "armor", chest_ico)
            if os.path.exists(cp_p):
                safe_paste(canvas, Image.open(cp_p), [hx, box[1] + 34, hx + 40, box[1] + 74])
                hx += 52

        draw.rounded_rectangle([hx + 10, box[1] + 36, hx + 195, box[1] + 70], radius=6, fill=(35, 20, 18), outline=(230, 80, 60), width=1)
        draw.text((hx + 20, box[1] + 43), f"🎯 Tête : {h_hits} coups", fill=(255, 140, 120), font=core.F_SMALL_BOLD)

        draw.rounded_rectangle([hx + 210, box[1] + 36, hx + 395, box[1] + 70], radius=6, fill=(20, 28, 35), outline=(80, 160, 240), width=1)
        draw.text((hx + 220, box[1] + 43), f"🛡️ Corps : {b_hits} coups", fill=(140, 200, 255), font=core.F_SMALL_BOLD)

        ay += 94

    tip_box = [right_box[0] + 18, ay + 6, right_box[2] - 18, right_box[3] - 14]
    draw.rounded_rectangle(tip_box, radius=6, fill=(28, 24, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((tip_box[0] + 14, tip_box[1] + 8), "💡 CONSEIL TACTIQUE DE DUEL PVP (HUNGER COMPANION) :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((tip_box[0] + 14, tip_box[1] + 30), f"Avec la {w_name}, visez impérativement la tête : 2 frappes (dont 1 lourde) abattent n'importe quel joueur jusqu'à l'armure bleue !", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    out_file = f"weapon_card_{w['name_en'].lower().replace(' ', '_')}.jpg"
    return save_and_copy(canvas, out_file)


# ===========================================================================
# 2. BESTIARY: OFFICIAL 3D RENDERS & PROBABLE DROPS
# ===========================================================================
def render_clean_creature_card(creature_key: str = "drooler", is_french: bool = True) -> str:
    c_low = creature_key.lower().strip()
    is_brute = "brute" in c_low

    if is_brute:
        c_name_fr = "Brute"
        c_name_en = "Brute"
        hp = 900
        threat = "Menace Élite au Corps-à-Corps · Lente & Dévastatrice"
        render_img = os.path.join(ASSETS_DIR, "bestiary", "brute_full.webp")
        trophy_img = os.path.join(ASSETS_DIR, "items", "brute_foot.png")
        trophy_name = "Patte de Brute (Trophy)"
        rate_trophy = "76.9%"
        desc = "Créature massive blindée aux membres déformés. Inflige 96 points de dégâts par frappe de zone."
        tips = [
            ("⚔️ Stratégie : Attaque dans le dos (Critique x2)", "Vulnérable aux frappes d'estoc et attaques lourdes dans le dos."),
            ("🏃 Esquive de Charge :", "Prépare un grand balayage avant de frapper. Roulez ou reculez avant l'impact.")
        ]
    else:
        c_name_fr = "Baveux"
        c_name_en = "Drooler"
        hp = 450
        threat = "Menace Rapide & Acide · Crachat Corrosif à Distance"
        render_img = os.path.join(ASSETS_DIR, "bestiary", "drooler_full.webp")
        trophy_img = os.path.join(ASSETS_DIR, "items", "drooler_jaw.png")
        trophy_name = "Mâchoire de Baveux (Trophy)"
        rate_trophy = "76.9%"
        desc = "Chasseur agile se déplaçant à 3.1 m/s. Crache un venin acide infligeant des dégâts continus."
        tips = [
            ("🎯 Point Faible : Frappes d'Estoc Rapides", "Faible résistance à la perforation. Une rapière ou lance l'élimine en 4 secondes."),
            ("🏃 Vitesse & Meute :", "Éliminez-le en priorité avant qu'il n'empoisonne toute votre escouade.")
        ]

    canvas, draw = create_base_canvas(f"BESTIAIRE OFFICIEL : {c_name_fr.upper()} ({c_name_en.upper()})", tag="MONSTRUM COMPENDIUM")

    # Left: Official 3D Full Monster Render
    left_box = [28, 86, 420, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    render_frame = [left_box[0] + 16, left_box[1] + 14, left_box[2] - 16, left_box[1] + 380]
    draw.rounded_rectangle(render_frame, radius=8, fill=(12, 12, 10), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(render_img):
        safe_paste(canvas, Image.open(render_img), render_frame)

    draw.text((left_box[0] + 18, render_frame[3] + 14), f"POINTS DE VIE : {hp} PV", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, render_frame[3] + 46), threat, fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    # Right: Stats, Official Lore & Probable Drops
    right_box = [440, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 16), "DÉTAILS TACTIQUES & BUTINS (HUNGER COMPANION)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    draw.text((right_box[0] + 20, right_box[1] + 48), desc, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((right_box[0] + 20, right_box[1] + 86), "BUTIN PROBABLE & TROPHÉES D'ÉQUARRISSAGE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    drop_card = [right_box[0] + 18, right_box[1] + 114, right_box[2] - 18, right_box[1] + 205]
    draw.rounded_rectangle(drop_card, radius=8, fill=core.BG_CARD, outline=(45, 42, 35), width=1)

    if os.path.exists(trophy_img):
        safe_paste(canvas, Image.open(trophy_img), [drop_card[0] + 16, drop_card[1] + 12, drop_card[0] + 81, drop_card[1] + 77])

    draw.text((drop_card[0] + 95, drop_card[1] + 14), trophy_name, fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
    draw.text((drop_card[0] + 95, drop_card[1] + 38), f"Taux d'apparition : {rate_trophy} · Nécessaire pour artisanat et contrats", fill=core.PRIO_YELLOW, font=core.F_BODY)
    draw.text((drop_card[0] + 95, drop_card[1] + 58), "Butin bonus rare : Clé de la folie de Jacques (1/226)", fill=(180, 180, 160), font=core.F_BODY)

    draw.text((right_box[0] + 20, right_box[1] + 225), "STRATÉGIES DE COMBAT HOMOLOGUÉES :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    ty = right_box[1] + 255
    for t_head, t_body in tips:
        t_box = [right_box[0] + 18, ty, right_box[2] - 18, ty + 74]
        draw.rounded_rectangle(t_box, radius=6, fill=core.BG_CARD, outline=(45, 42, 30), width=1)
        draw.text((t_box[0] + 14, t_box[1] + 10), t_head, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
        draw.text((t_box[0] + 14, t_box[1] + 36), t_body, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        ty += 88

    out_file = f"creature_{c_name_en.lower()}.jpg"
    return save_and_copy(canvas, out_file)


# ===========================================================================
# 3. CHARACTER CARD: HERO PORTRAIT + 3 ABILITY ICONS (PASSIVE, Q, E) + SKINS
# ===========================================================================
OFFICIAL_HEROES = {
    "eva": {
        "name": "Eva", "title": "Vagabond Huntress", "role": "Dirty Scum · Rôdeuse & Éclaireuse",
        "p_name": "Steel Legs (Passif)", "p_desc": "Vitesse de sprint prolongée et coût d'endurance de course réduit.", "p_ico": "eva_passive.png",
        "q_name": "Lightfoot (Touche Q)", "q_desc": "Déplacement silencieux éliminant les bruits de pas pendant 8 secondes.", "q_ico": "eva_q.png",
        "e_name": "Blind (Touche E)", "e_desc": "Projette une poudre aveuglante désorientant les cibles proches.", "e_ico": "eva_e.png",
        "portrait": "eva.webp", "skins": "Dirty Scum, Fleeing Whelp, Deft Apprentice, Adept Survivor, Revered Legend"
    },
    "gabriel": {
        "name": "Gabriel", "title": "Soldier of Fortune", "role": "Dirty Scum · Fantassin & Ligne de Front",
        "p_name": "Charge (Passif)", "p_desc": "Bonus d'impact et de dégâts majeurs sur la frappe portée en sprint.", "p_ico": "gabriel_passive.png",
        "q_name": "Brace (Touche Q)", "q_desc": "Posture fortifiée réduisant les dégâts subis de 35% de face.", "q_ico": "gabriel_q.png",
        "e_name": "Sadist (Touche E)", "e_desc": "Régénère un montant de vigueur et d'endurance sur coup critique.", "e_ico": "gabriel_e.png",
        "portrait": "gabriel.webp", "skins": "Dirty Scum, Athos (Légendaire), Fleeing Whelp, Deft Apprentice"
    },
    "hugo": {
        "name": "Hugo", "title": "The Maniac", "role": "Dirty Scum · Berserker & Dégâts Bruts",
        "p_name": "Taste of Blood (Passif)", "p_desc": "Vitesse d'attaque accrue contre les ennemis souffrant de saignement.", "p_ico": "hugo_passive.png",
        "q_name": "Zealot (Touche Q)", "q_desc": "Cri de ferveur augmentant temporairement les dégâts des frappes lourdes.", "q_ico": "hugo_q.png",
        "e_name": "Maniac (Touche E)", "e_desc": "Frénésie sanguinaire procurant une immunité aux étourdissements.", "e_ico": "hugo_e.png",
        "portrait": "hugo.webp", "skins": "Dirty Scum, Fleeing Whelp, Deft Apprentice, Plucky Journeyman"
    },
    "marie": {
        "name": "Marie", "title": "Warrior Nun", "role": "Dirty Scum · Médecin de Terrain & Soutien",
        "p_name": "Gentle Touch (Passif)", "p_desc": "Vitesse d'application des bandages et soins accrue de 50%.", "p_ico": "marie_passive.png",
        "q_name": "Vespers (Touche Q)", "q_desc": "Aura apaisante dissipant immédiatement les poisons et saignements.", "q_ico": "marie_q.png",
        "e_name": "Mending Prayer (Touche E)", "e_desc": "Restaure instantanément 45 PV au lanceur ou à l'allié visé.", "e_ico": "marie_e.png",
        "portrait": "marie.webp", "skins": "Dirty Scum, Matriarch (Légendaire), Black Habit (Rare), Revered Legend"
    },
    "otto": {
        "name": "Otto", "title": "Sergeant-at-Arms", "role": "Dirty Scum · Sapeur & Blindage",
        "p_name": "Maintenance (Passif)", "p_desc": "Ralentit la perte de durabilité des armures équipées de 20%.", "p_ico": "otto_passive.png",
        "q_name": "Field Repairs (Touche Q)", "q_desc": "Répare sur le terrain une partie de la plaque d'armure fissurée.", "q_ico": "otto_q.png",
        "e_name": "Masterwork (Touche E)", "e_desc": "Améliore temporairement la défense face aux tirs à distance.", "e_ico": "otto_e.png",
        "portrait": "otto.webp", "skins": "Dirty Scum, Masterwork Sapper, Fleeing Whelp, Plucky Journeyman"
    },
    "serine": {
        "name": "Serine", "title": "Vodou Poisoner", "role": "Dirty Scum · Contrôle & Toxines",
        "p_name": "Voudou Spirit (Passif)", "p_desc": "Résistance passive de 30% aux venins et dégâts de poison.", "p_ico": "serine_passive.png",
        "q_name": "Rush (Touche Q)", "q_desc": "Ruée tactique rapide laissant une traînée de brume corrosive.", "q_ico": "serine_q.png",
        "e_name": "Voudou Bomb (Touche E)", "e_desc": "Bombe incendiaire toxique infligeant des dégâts de zone continus.", "e_ico": "serine_e.png",
        "portrait": "serine.webp", "skins": "Dirty Scum, Vodou Priestess, Fleeing Whelp, Deft Apprentice"
    }
}

def render_clean_character_card(hero_key: str = "marie", is_french: bool = True) -> str:
    k = hero_key.lower().strip()
    if k in ["serene", "vodou"]: k = "serine"
    data = OFFICIAL_HEROES.get(k, OFFICIAL_HEROES["marie"])

    canvas, draw = create_base_canvas(f"PROFIL OFFICIEL DU HÉROS : {data['name'].upper()}", tag="PERSONNAGE JOUABLE")

    # Left Box: Official Portrait & Skins
    left_box = [28, 86, 360, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    port_p = os.path.join(ASSETS_DIR, "characters", data["portrait"])
    port_frame = [left_box[0] + 16, left_box[1] + 14, left_box[2] - 16, left_box[1] + 320]
    draw.rounded_rectangle(port_frame, radius=8, fill=(12, 12, 10), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(port_p):
        safe_paste(canvas, Image.open(port_p), port_frame)

    draw.text((left_box[0] + 18, port_frame[3] + 14), data["name"].upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 18, port_frame[3] + 44), data["title"], fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, port_frame[3] + 70), f"Classe : {data['role']}", fill=core.PRIO_PURPLE, font=core.F_BODY)

    draw.text((left_box[0] + 18, port_frame[3] + 104), "SKINS DÉBLOCABLES :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, port_frame[3] + 128), data["skins"][:100], fill=(180, 180, 160), font=core.F_BODY)

    # Right Box: THE 3 ABILITY CARDS WITH REAL ICONS!
    right_box = [380, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 16), "KIT DE COMPÉTENCES ACTIVES & PASSIF", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    abilities = [
        (data["p_name"], data["p_desc"], data["p_ico"], core.PRIO_YELLOW),
        (data["q_name"], data["q_desc"], data["q_ico"], (80, 200, 120)),
        (data["e_name"], data["e_desc"], data["e_ico"], (220, 90, 80))
    ]

    ay = right_box[1] + 55
    for a_title, a_desc, a_icon_file, b_col in abilities:
        a_card = [right_box[0] + 18, ay, right_box[2] - 18, ay + 140]
        draw.rounded_rectangle(a_card, radius=8, fill=core.BG_CARD, outline=b_col, width=2)

        ico_p = os.path.join(ASSETS_DIR, "abilities", a_icon_file)
        if os.path.exists(ico_p):
            safe_paste(canvas, Image.open(ico_p), [a_card[0] + 16, a_card[1] + 18, a_card[0] + 116, a_card[1] + 118])

        draw.text((a_card[0] + 130, a_card[1] + 18), a_title, fill=b_col, font=core.F_SECTION_TITLE)
        draw.text((a_card[0] + 130, a_card[1] + 55), a_desc, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        ay += 155

    squad_box = [right_box[0] + 18, ay + 10, right_box[2] - 18, right_box[3] - 14]
    draw.rounded_rectangle(squad_box, radius=6, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((squad_box[0] + 14, squad_box[1] + 8), "💡 SYNERGIE D'ESCOUADE TACTIQUE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((squad_box[0] + 14, squad_box[1] + 30), f"Le kit de {data['name']} apporte un avantage décisif en raid d'extraction lors des combats serrés.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    out_file = f"character_{data['name'].lower()}.jpg"
    return save_and_copy(canvas, out_file)


# ===========================================================================
# 4. QUEST CARD & CLEAN MINIATURE MAP (NO JAQUES FOLLY ON GAVROCHE MAP!)
# ===========================================================================
def render_clean_gavroche_quest_card(is_french: bool = True) -> str:
    canvas, draw = create_base_canvas("FICHE DE QUÊTE : THE GAVROCHE FAMILY", tag="MISSION PRINCIPALE")

    left_box = [28, 86, 430, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    draw.text((left_box[0] + 18, left_box[1] + 16), "DÉTAILS DU CONTRAT", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 48), "The Gavroche Family", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 82), "Commanditaire : Éloïse (Château Hub)", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, left_box[1] + 108), "Carte Déployée : Pont Jacques (Jacques Bridge)", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    draw.text((left_box[0] + 18, left_box[1] + 148), "OBJECTIFS DE MISSION :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, left_box[1] + 174), "1. Traverser le Pont Jacques vers les berges Est.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 202), "2. Localiser le campement de fortune des Gavroche.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 230), "3. Inspecter les tentes et valider la reconnaissance.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    draw.text((left_box[0] + 18, left_box[1] + 275), "ITEMS REQUIS :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, left_box[1] + 302), "• Aucun item à ramener (Quête de reconnaissance pure).", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 328), "• Note : La quête 'The Last Prisoner' est indépendante", fill=(180, 180, 160), font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 350), "  et se déroule dans les cellules du donjon Jacques Folly.", fill=(180, 180, 160), font=core.F_BODY)

    rew_box = [left_box[0] + 16, left_box[1] + 395, left_box[2] - 16, left_box[3] - 16]
    draw.rounded_rectangle(rew_box, radius=8, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((rew_box[0] + 14, rew_box[1] + 10), "RÉCOMPENSES :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((rew_box[0] + 14, rew_box[1] + 34), "• 3x Pommes Cuites (Stewed Apples - Vivres de soin)", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((rew_box[0] + 14, rew_box[1] + 58), "• +250 Points d'Expérience d'Artisanat", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    # Right Column: CLEAN TACTICAL MAP (WITHOUT SIDEBAR & WITHOUT JAQUES FOLLY!)
    right_box = [450, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 16), "EMPLACEMENT DU CAMPEMENT (BERGES EST DU FLEUVE)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    jacques_base_p = os.path.join(ROOT_DIR, "data", "maps", "jacques_bridge_hq.jpg")
    if not os.path.exists(jacques_base_p):
        jacques_base_p = os.path.join(ROOT_DIR, "assets", "jacques_bridge.png")

    if os.path.exists(jacques_base_p):
        j_img = Image.open(jacques_base_p).convert("RGBA")
        mw, mh = j_img.size
        cx = int(mw * 0.58)
        cy = int(mh * 0.28)
        rad_w, rad_h = int(mw * 0.25), int(mh * 0.25)
        crop_rect = (max(0, cx - rad_w), max(0, cy - rad_h), min(mw, cx + rad_w), min(mh, cy + rad_h))
        m_crop = j_img.crop(crop_rect)

        m_draw = ImageDraw.Draw(m_crop)
        pin_x = m_crop.size[0] // 2
        pin_y = m_crop.size[1] // 2
        m_draw.ellipse([pin_x - 14, pin_y - 14, pin_x + 14, pin_y + 14], fill=(245, 200, 60), outline=(255, 255, 255), width=3)
        m_draw.rounded_rectangle([pin_x - 110, pin_y + 18, pin_x + 110, pin_y + 48], radius=6, fill=(20, 20, 16, 220), outline=core.COLOR_GOLD, width=2)
        m_draw.text((pin_x - 95, pin_y + 24), "CAMPEMENT GAVROCHE", fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)

        safe_paste(canvas, m_crop, [right_box[0] + 16, right_box[1] + 50, right_box[2] - 16, right_box[3] - 16])

    return save_and_copy(canvas, "quest_card_the-gavroche-family.jpg")


# ===========================================================================
# 5. DUNGEON CARD (JACQUES FOLLY - CLEAN MAP WITHOUT SIDEBAR!)
# ===========================================================================
def render_clean_dungeon_card(is_french: bool = True) -> str:
    canvas, draw = create_base_canvas("DONJON & SECRET : LA FOLIE DE JACQUES", tag="SALLE VERROUILLÉE")

    left_box = [28, 86, 440, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    draw.text((left_box[0] + 18, left_box[1] + 16), "DÉTAILS DU DONJON", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 48), "La Folie de Jacques (Jacques Folly)", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 80), "Carte : Pont Jacques · Niveau sous-terrain", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)

    draw.text((left_box[0] + 18, left_box[1] + 120), "CLÉ REQUISE & EMPLACEMENT DE SPAWN :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, left_box[1] + 146), "• Clé Requise : Clé de la folie de Jacques (3 usages)", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 172), "• Spawns en conteneurs : Meubles de cuisine, Coffres de raid", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 198), "• Spawns au sol / Hors conteneurs : Posée sur la table de la chapelle", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, left_box[1] + 224), "  ou sur l'étagère de l'apothicaire abandonné.", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    draw.text((left_box[0] + 18, left_box[1] + 265), "MENACES ET CONTENEURS RARES DU DONJON :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, left_box[1] + 292), "• Monstres : 2x Baveux en patrouille et 1x Brute dans la crypte.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 318), "• Conteneurs : 174 conteneurs (Grands coffres renforcés, armoires).", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 344), "• Butin légendaire : Armes rares, lingots et équipement de sapeur.", fill=core.PRIO_YELLOW, font=core.F_BODY)

    right_box = [460, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 16), "ACCÈS AU DONJON SOUS LE PONT JACQUES", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    jacques_base_p = os.path.join(ROOT_DIR, "data", "maps", "jacques_bridge_hq.jpg")
    if not os.path.exists(jacques_base_p):
        jacques_base_p = os.path.join(ROOT_DIR, "assets", "jacques_bridge.png")

    if os.path.exists(jacques_base_p):
        j_img = Image.open(jacques_base_p).convert("RGBA")
        mw, mh = j_img.size
        cx = int(mw * 0.65)
        cy = int(mh * 0.55)
        rad_w, rad_h = int(mw * 0.22), int(mh * 0.22)
        crop_rect = (max(0, cx - rad_w), max(0, cy - rad_h), min(mw, cx + rad_w), min(mh, cy + rad_h))
        m_crop = j_img.crop(crop_rect)

        m_draw = ImageDraw.Draw(m_crop)
        pin_x = m_crop.size[0] // 2
        pin_y = m_crop.size[1] // 2
        m_draw.ellipse([pin_x - 14, pin_y - 14, pin_x + 14, pin_y + 14], fill=(180, 100, 230), outline=(255, 255, 255), width=3)
        m_draw.rounded_rectangle([pin_x - 110, pin_y + 18, pin_x + 110, pin_y + 48], radius=6, fill=(20, 20, 16, 220), outline=core.PRIO_PURPLE, width=2)
        m_draw.text((pin_x - 90, pin_y + 24), "ENTRÉE JACQUES FOLLY", fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)

        safe_paste(canvas, m_crop, [right_box[0] + 16, right_box[1] + 50, right_box[2] - 16, right_box[3] - 16])

    return save_and_copy(canvas, "dungeon_jacques-folly.jpg")


# ===========================================================================
# 6. STASH & INVENTORY: TWO IMAGES (HIGHLIGHTED GRID & SELL MANIFEST)
# ===========================================================================
def render_stash_two_images():
    img1 = Image.new("RGBA", (CARD_W, CARD_H), (15, 14, 12, 255))
    d1 = ImageDraw.Draw(img1)
    d1.rectangle([0, 0, CARD_W, CARD_H], fill=(15, 14, 12))
    d1.rounded_rectangle([10, 10, CARD_W - 10, CARD_H - 10], radius=12, outline=core.COLOR_GOLD, width=2)
    d1.text((38, 28), "ANALYSE DE STASH : OBJETS À VENDRE EN SURBRILLANCE", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    d1.line([(28, 68), (CARD_W - 28, 68)], fill=core.BORDER_SUBTLE, width=1)

    sample_items = [
        ("Plaque de Cuirasse", False, 2, 0, "T_UI_Item_ArmorChest_Uncommon.png"),
        ("Casque de Cuir", False, 1, 0, "T_UI_Item_ArmorHead_Uncommon.png"),
        ("Potions de Soin", False, 4, 0, "sealed_bloodbag.png"),
        ("Vivres de Sarlat", False, 6, 0, "flour.png"),
        ("Cagoule Déchirée", True, 3, 30, "ID_HipBag_Common01.webp"),
        ("Tunique Usée", True, 2, 45, "ID_BackBag_Epic01.webp"),
        ("Bourse de Cuivre", True, 1, 120, "china_bowl.png"),
        ("Munitions Lourdes", False, 20, 0, "heavy_ammunition.png"),
        ("Clé de Jacques", False, 1, 0, "gold_key.png"),
        ("Zweihänder", False, 1, 0, "T_UI_Item_Zweihaender.png"),
        ("Cuiller en Étain", True, 4, 15, "silver_dish.png"),
        ("Chiffon Mouillé", True, 5, 8, "damp_rag.png")
    ]

    gx, gy = 38, 90
    col_w, row_h = 175, 185
    for idx, (iname, is_sell, qty, pr, ico) in enumerate(sample_items):
        r = idx // 6
        c_i = idx % 6
        bx = gx + c_i * col_w
        by = gy + r * row_h
        cell = [bx, by, bx + col_w - 12, by + row_h - 12]

        border_c = (245, 200, 60) if is_sell else (45, 45, 45)
        fill_c = (35, 28, 14) if is_sell else (18, 18, 18)
        d1.rounded_rectangle(cell, radius=8, fill=fill_c, outline=border_c, width=3 if is_sell else 1)

        ico_p = os.path.join(ASSETS_DIR, "items", ico)
        if not os.path.exists(ico_p):
            ico_p = os.path.join(ASSETS_DIR, "armor", ico)
        if os.path.exists(ico_p):
            im = Image.open(ico_p).convert("RGBA")
            if not is_sell:
                # Desaturate keep items to grayscale!
                lum = im.convert("L").convert("RGBA")
                safe_paste(img1, lum, [cell[0] + 25, cell[1] + 12, cell[2] - 25, cell[1] + 105])
            else:
                safe_paste(img1, im, [cell[0] + 25, cell[1] + 12, cell[2] - 25, cell[1] + 105])

        status_txt = "À VENDRE" if is_sell else "À GARDER"
        status_col = core.PRIO_YELLOW if is_sell else (100, 100, 100)
        d1.rounded_rectangle([cell[0] + 10, cell[3] - 46, cell[2] - 10, cell[3] - 26], radius=4, fill=(10, 10, 10), outline=status_col, width=1)
        d1.text((cell[0] + 18, cell[3] - 44), f"{status_txt} (x{qty})", fill=status_col, font=core.F_SMALL_BOLD)
        d1.text((cell[0] + 12, cell[3] - 22), iname[:18], fill=core.COLOR_PARCHMENT if is_sell else (120, 120, 120), font=core.F_BODY)

    d1.rounded_rectangle([38, CARD_H - 75, CARD_W - 38, CARD_H - 25], radius=6, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    d1.text((50, CARD_H - 65), "📊 ROTATION DU MARCHÉ : Prix actuels +12% supérieurs au prix de base. Moment très favorable pour vendre !", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    out_p1 = save_and_copy(img1, "stash_highlighted_grid.jpg")

    # Image 2: Clean Sell Manifest
    img2 = Image.new("RGBA", (CARD_W, CARD_H), (15, 14, 12, 255))
    d2 = ImageDraw.Draw(img2)
    d2.rectangle([0, 0, CARD_W, CARD_H], fill=(15, 14, 12))
    d2.rounded_rectangle([10, 10, CARD_W - 10, CARD_H - 10], radius=12, outline=core.COLOR_GOLD, width=2)
    d2.text((38, 28), "BORDEREAU DE VENTE : ARTICLES SÉLECTIONNÉS (MARCHANDS)", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    d2.line([(28, 68), (CARD_W - 28, 68)], fill=core.BORDER_SUBTLE, width=1)

    sell_only = [
        ("Cagoule Déchirée (Doublon armure basse)", 3, 30, 90, "ID_HipBag_Common01.webp"),
        ("Tunique Usée (Doublon moyen)", 2, 45, 90, "ID_BackBag_Epic01.webp"),
        ("Bourse de Cuivre (Bijou marchand)", 1, 120, 120, "china_bowl.png"),
        ("Cuiller en Étain (Rebut de table)", 4, 15, 60, "silver_dish.png"),
        ("Chiffon Mouillé (Surplus non utilisé)", 5, 8, 40, "damp_rag.png")
    ]

    total_copper = sum(item[3] for item in sell_only)
    tot_s = total_copper // 100
    tot_c = total_copper % 100

    sy = 90
    for s_name, s_qty, u_price, t_price, s_ico in sell_only:
        card = [38, sy, CARD_W - 38, sy + 74]
        d2.rounded_rectangle(card, radius=8, fill=core.BG_CARD, outline=(45, 42, 35), width=1)

        ico_p = os.path.join(ASSETS_DIR, "items", s_ico)
        if os.path.exists(ico_p):
            safe_paste(img2, Image.open(ico_p), [card[0] + 16, card[1] + 10, card[0] + 70, card[1] + 64])

        d2.text((card[0] + 85, card[1] + 14), f"{s_name} (x{s_qty})", fill=core.COLOR_PARCHMENT, font=core.F_SECTION_TITLE)
        d2.text((card[0] + 85, card[1] + 42), f"Prix unitaire : {u_price} Cuivre · Rapport total : {t_price} Cuivre", fill=(180, 180, 160), font=core.F_BODY)

        d2.rounded_rectangle([card[2] - 180, card[1] + 18, card[2] - 18, card[1] + 56], radius=6, fill=(35, 28, 14), outline=core.COLOR_GOLD, width=1)
        d2.text((card[2] - 165, card[1] + 26), f"+{t_price} Cuivres", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)
        sy += 86

    tot_box = [38, CARD_H - 120, CARD_W - 38, CARD_H - 30]
    d2.rounded_rectangle(tot_box, radius=8, fill=(28, 22, 14), outline=core.COLOR_GOLD, width=2)
    d2.text((54, tot_box[1] + 18), "TOTAL ESTIMÉ DE LA VENTE AUX MARCHANDS :", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    d2.text((54, tot_box[1] + 50), f"💰 {tot_s} Pièces d'Argent  {tot_c} Pièces de Cuivre (Soit {total_copper} Cuivres au total)", fill=core.PRIO_YELLOW, font=core.F_HEADER_TITLE)

    out_p2 = save_and_copy(img2, "stash_sell_manifest.jpg")
    return out_p1, out_p2


# ===========================================================================
# 7. TALENT TREES: IMAGE 2 (ONLY SELECTED TALENTS SUMMARY)
# ===========================================================================
def render_clean_talent_summary_card():
    canvas, draw = create_base_canvas("RÉSUMÉ DU BUILD ACTUEL : TALENTS SÉLECTIONNÉS (91 PTS)", tag="COMPÉTENCES DU JOUEUR")

    draw.rounded_rectangle([28, 86, CARD_W - 28, 125], radius=6, fill=(22, 20, 18), outline=core.BORDER_SUBTLE, width=1)
    draw.text((45, 96), "◆ ARMS : 37/71 (Tier VIII Débloqué)    |    ◆ SURVIVAL : 36/78 (Tier VIII Débloqué)    |    ◆ PHYSIOLOGY : 18/83 (Tier IV)", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    selected = [
        ("ARMS · DEFT STRIKES (5/5)", "-25% de coût d'endurance sur attaques légères à 2 mains.", "Synergie Zweihänder absolue : enchaînements continus sans fatigue.", (48, 209, 204)),
        ("ARMS · MAÎTRISE TIER VIII (1/1)", "Palier ultime débloqué pour amplifier les dégâts de mêlée.", "Confère un bonus dévastateur lors des duels rapprochés.", (48, 209, 204)),
        ("SURVIVAL · SURGEON (5/5)", "Relève un coéquipier au sol 25% plus vite en plein raid.", "Sauvetage d'escouade décisif sous le feu ennemi.", (155, 114, 207)),
        ("SURVIVAL · MAÎTRISE TIER VIII (1/1)", "Protection du vivant débloquée pour une résilience maximale.", "Résistance passive élevée contre monstres et saignements.", (155, 114, 207)),
        ("PHYSIOLOGY · ENDURANCE & MOBILITÉ (18 PTS)", "Sprint prolongé 5/5, Vitalité max 5/5, Agilité au saut 5/5, Coagulation 3/5.", "Compense intégralement le poids des armes lourdes.", (224, 122, 158)),
    ]

    ty = 140
    for name, desc, note, col in selected:
        card = [28, ty, CARD_W - 28, ty + 95]
        draw.rounded_rectangle(card, radius=8, fill=core.BG_CARD, outline=col, width=2)
        draw.text((card[0] + 18, card[1] + 12), name, fill=col, font=core.F_SECTION_TITLE)
        draw.text((card[0] + 18, card[1] + 42), desc, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((card[0] + 18, card[1] + 66), note, fill=(180, 180, 160), font=core.F_BODY)
        ty += 105

    b_box = [28, CARD_H - 72, CARD_W - 28, CARD_H - 18]
    draw.rounded_rectangle(b_box, radius=6, fill=(28, 24, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((45, b_box[1] + 15), "💡 SYNTHÈSE TACTIQUE : Build 100% orienté assaut lourd et secours d'escouade. Aucun point gaspillé.", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    return save_and_copy(canvas, "build_selected_talents_summary.jpg")


if __name__ == "__main__":
    print("Generating all redesigned cards...")
    f1 = render_clean_melee_card("longsword", is_french=True)
    f2 = render_clean_melee_card("zweihander", is_french=True)
    f3 = render_clean_melee_card("spear", is_french=True)
    f4 = render_clean_creature_card("drooler", is_french=True)
    f5 = render_clean_creature_card("brute", is_french=True)
    f6 = render_clean_character_card("marie", is_french=True)
    f7 = render_clean_character_card("gabriel", is_french=True)
    f8 = render_clean_character_card("eva", is_french=True)
    f9 = render_clean_gavroche_quest_card(is_french=True)
    f10 = render_clean_dungeon_card(is_french=True)
    f11, f12 = render_stash_two_images()
    f13 = render_clean_talent_summary_card()
    print("ALL CARDS SUCCESSFULLY GENERATED AND OVERHAULED!")
