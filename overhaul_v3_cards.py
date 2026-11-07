import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)
import perfect_briefings_core_v25 as core
core.preload_assets()

OUT_DIR = os.path.join(ROOT_DIR, "output_maps")
os.makedirs(OUT_DIR, exist_ok=True)
BRAIN_DIR = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49"

CARD_W = 1040
CARD_H = 580

def save_and_sync(canvas: Image.Image, filename: str) -> str:
    out_p = os.path.join(OUT_DIR, filename)
    canvas.convert("RGB").save(out_p, quality=95)
    if os.path.exists(BRAIN_DIR):
        brain_p = os.path.join(BRAIN_DIR, filename)
        canvas.convert("RGB").save(brain_p, quality=95)
    return out_p

def safe_paste(canvas, img, box):
    if img is None:
        return
    x, y, w, h = box
    im = img.convert("RGBA")
    im.thumbnail((w, h), Image.Resampling.LANCZOS)
    px = x + (w - im.width) // 2
    py = y + (h - im.height) // 2
    canvas.paste(im, (px, py), im.split()[3])

def create_base_canvas(title: str, tag: str = "TACTICAL INTEL"):
    canvas = Image.new("RGBA", (CARD_W, CARD_H), (12, 12, 15))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, CARD_W, CARD_H], fill=(12, 12, 15))
    draw.rectangle([4, 4, CARD_W - 5, CARD_H - 5], outline=core.COLOR_GOLD, width=2)
    draw.rectangle([8, 8, CARD_W - 9, CARD_H - 9], outline=(40, 36, 26), width=1)

    # Header
    draw.rounded_rectangle([16, 14, CARD_W - 16, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    tag_w = int(draw.textlength(tag.upper(), font=core.F_SMALL_BOLD)) + 24
    draw.rounded_rectangle([28, 22, 28 + tag_w, 60], radius=5, fill=(35, 30, 20), outline=core.COLOR_GOLD, width=1)
    draw.text((40, 31), tag.upper(), fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((44 + tag_w, 27), title.upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    wm = "HUNGER COMPANION x ELOISE"
    draw.text((CARD_W - int(draw.textlength(wm, font=core.F_SMALL_BOLD)) - 28, 31), wm, fill=(120, 110, 80), font=core.F_SMALL_BOLD)
    return canvas, draw

# ---------------------------------------------------------------------------
# 1. CLEAN GAVROCHE QUEST CARD (NO SIDEBAR, NO JAQUES FOLLY, PURE RECON)
# ---------------------------------------------------------------------------
def render_clean_gavroche_quest_card(is_french: bool = True) -> str:
    canvas, draw = create_base_canvas("QUEST : THE GAVROCHE FAMILY (FAMILLE GAVROCHE)", tag="RECONNAISSANCE")

    # Left: Contract details
    left_box = [28, 86, 430, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    draw.text((left_box[0] + 18, left_box[1] + 16), "DÉTAILS DU CONTRAT", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 48), "The Gavroche Family", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 82), "Commanditaire : Éloïse (Château Hub)", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, left_box[1] + 108), "Carte : Jacques Bridge (Berges Est)", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    draw.text((left_box[0] + 18, left_box[1] + 148), "OBJECTIFS DE RECONNAISSANCE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, left_box[1] + 174), "1. Traverser le Pont Jacques vers les berges Est.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 202), "2. Localiser le campement isolé de la famille Gavroche.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 230), "3. Valider la découverte et extraire sain et sauf.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    draw.text((left_box[0] + 18, left_box[1] + 272), "ITEMS REQUIS :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, left_box[1] + 296), "• Aucun item à ramener (Mission de pur repérage).", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 322), "• Note : La quête 'The Last Prisoner' est indépendante", fill=(175, 175, 155), font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 344), "  et se déroule dans les geôles du donjon Jacques Folly.", fill=(175, 175, 155), font=core.F_BODY)

    rew_box = [left_box[0] + 16, left_box[1] + 385, left_box[2] - 16, left_box[3] - 14]
    draw.rounded_rectangle(rew_box, radius=8, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((rew_box[0] + 14, rew_box[1] + 8), "RÉCOMPENSES DE MISSION :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((rew_box[0] + 14, rew_box[1] + 30), "• 3x Pommes Cuites (Stewed Apples - Vivres de soin)", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((rew_box[0] + 14, rew_box[1] + 52), "• +250 Points d'Expérience de Réputation Hub", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    # Right: Clean Tactical Map without sidebar and without Jaques Folly!
    right_box = [450, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 16), "EMPLACEMENT DU CAMPEMENT (AUCUN AUTRE POINT DISPERSÉ)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    raw_map_p = os.path.join(ROOT_DIR, "jacques-bridge.webp")
    if os.path.exists(raw_map_p):
        base_map = Image.open(raw_map_p).convert("RGBA")
        mw, mh = base_map.size
        # Gavroche camp on riverbank: x approx 1479*2, y approx 313*2 in 4096 scale
        cx, cy = 2950, 626
        rad = 650
        crop = base_map.crop((max(0, cx - rad), max(0, cy - rad), min(mw, cx + rad), min(mh, cy + rad)))

        # Draw pin directly
        c_draw = ImageDraw.Draw(crop)
        pin_x, pin_y = rad, rad
        c_draw.ellipse([pin_x - 32, pin_y - 32, pin_x + 32, pin_y + 32], fill=(245, 200, 60, 70), outline=(245, 200, 60), width=4)
        c_draw.ellipse([pin_x - 16, pin_y - 16, pin_x + 16, pin_y + 16], fill=(245, 200, 60), outline=(255, 255, 255), width=2)
        c_draw.ellipse([pin_x - 5, pin_y - 5, pin_x + 5, pin_y + 5], fill=(20, 20, 20))

        # Label pill
        lbl = "CAMPEMENT GAVROCHE (RUINES)"
        lw = int(c_draw.textlength(lbl, font=core.F_CARD_TITLE)) + 30
        c_draw.rounded_rectangle([pin_x - lw // 2, pin_y + 24, pin_x + lw // 2, pin_y + 60], radius=6, fill=(16, 16, 18, 240), outline=core.COLOR_GOLD, width=2)
        c_draw.text((pin_x - lw // 2 + 15, pin_y + 30), lbl, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)

        target_w = right_box[2] - right_box[0] - 32
        target_h = right_box[3] - right_box[1] - 60
        safe_paste(canvas, crop, (right_box[0] + 16, right_box[1] + 48, target_w, target_h))

    return save_and_sync(canvas, "quest_card_the-gavroche-family.jpg")


# ---------------------------------------------------------------------------
# 2. CLEAN CREATURE CARD (DROOLER 3D RENDER + TROPHY JAW DROP)
# ---------------------------------------------------------------------------
def render_clean_creature_card(creature_key: str = "drooler", is_french: bool = True) -> str:
    c_low = creature_key.lower().strip()
    is_brute = "brute" in c_low

    if is_brute:
        c_name_fr, c_name_en = "Brute", "Brute"
        hp, speed, dmg = 900, "Lente (0.8 m/s)", "68 (Zone 96)"
        render_img = os.path.join(ROOT_DIR, "assets", "bestiary", "BP_Brute_Parent__full.webp")
        trophy_img = os.path.join(ROOT_DIR, "assets", "items", "T_UI_Trophy_BruteFoot.png")
        trophy_name = "Patte de Brute (Brute Foot)"
        trophy_rate = "76.9% de chances au dépeçage"
        trophy_val = "120 Cuivres (Atelier du Tanneur)"
        tactics = [
            ("Frappe d'Estoc dans le dos (Critique x2)", "Vulnérable aux frappes lourdes et d'estoc dans le dos."),
            ("Esquive de Balayage", "Prépare un large balayage circulaire. Roulez en arrière avant l'impact.")
        ]
    else:
        c_name_fr, c_name_en = "Baveux", "Drooler"
        hp, speed, dmg = 450, "Rapide (3.1 m/s)", "36 (Jet Acide)"
        # Official 3D monster model render:
        render_img = os.path.join(ROOT_DIR, "assets", "bestiary", "BP_Biter_Parent__full.webp")
        if not os.path.exists(render_img):
            render_img = os.path.join(ROOT_DIR, "assets", "bestiary", "BP_Biter_Parent__face.webp")
        # Official trophy item:
        trophy_img = os.path.join(ROOT_DIR, "assets", "items", "T_UI_Trophy_BiterJaw.png")
        trophy_name = "Mâchoire de Baveux (Drooler Jaw)"
        trophy_rate = "75.8% de chances au dépeçage"
        trophy_val = "95 Cuivres (Atelier de Taxidermie)"
        tactics = [
            ("Perforation Rapide (Lance / Rapière)", "Sensible aux attaques d'estoc rapides. Éliminé en 4 secondes chrono."),
            ("Esquive du Crachat Corrosif", "Garder une trajectoire latérale pour esquiver le jet acide à distance.")
        ]

    canvas, draw = create_base_canvas(f"CREATURE : {c_name_en.upper()} ({c_name_fr.upper()})", tag="MONSTRUM COMPENDIUM")

    # Left: 3D Monster Render
    left_box = [28, 86, 420, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    render_frame = [left_box[0] + 16, left_box[1] + 14, left_box[2] - 16, left_box[1] + 370]
    draw.rounded_rectangle(render_frame, radius=8, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(render_img):
        safe_paste(canvas, Image.open(render_img), (render_frame[0] + 5, render_frame[1] + 5, render_frame[2] - render_frame[0] - 10, render_frame[3] - render_frame[1] - 10))

    draw.text((left_box[0] + 18, render_frame[3] + 12), f"POINTS DE VIE : {hp} PV", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, render_frame[3] + 38), f"Vitesse : {speed}  |  Dégâts : {dmg}", fill=(180, 180, 160), font=core.F_BODY)

    # Right: Loot Drop & Official Tactics
    right_box = [440, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    # 1. BUTIN OFFICIEL DE CHASSE (WITH REAL TROPHY ICON)
    draw.text((right_box[0] + 20, right_box[1] + 16), "BUTIN & TROPHÉE PRINCIPAL DE CHASSE", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    drop_card = [right_box[0] + 18, right_box[1] + 48, right_box[2] - 18, right_box[1] + 155]
    draw.rounded_rectangle(drop_card, radius=8, fill=core.BG_CARD, outline=core.PRIO_YELLOW, width=1)

    ico_box = [drop_card[0] + 14, drop_card[1] + 14, drop_card[0] + 94, drop_card[1] + 94]
    draw.rounded_rectangle(ico_box, radius=6, fill=(16, 16, 18), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(trophy_img):
        safe_paste(canvas, Image.open(trophy_img), (ico_box[0] + 4, ico_box[1] + 4, 72, 72))

    draw.text((drop_card[0] + 110, drop_card[1] + 16), trophy_name, fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((drop_card[0] + 110, drop_card[1] + 48), f"• Taux de drop officiel : {trophy_rate}", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)
    draw.text((drop_card[0] + 110, drop_card[1] + 74), f"• Valeur marchande au Château : {trophy_val}", fill=(180, 180, 160), font=core.F_BODY)

    # 2. TACTIQUES OFFICIELLES HUNGER COMPANION
    ty = drop_card[3] + 18
    draw.text((right_box[0] + 20, ty), "TACTIQUES OFFICIELLES (HUNGER COMPANION)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    ty += 34

    for title_t, desc_t in tactics:
        t_box = [right_box[0] + 18, ty, right_box[2] - 18, ty + 72]
        draw.rounded_rectangle(t_box, radius=6, fill=core.BG_CARD, outline=(45, 42, 35), width=1)
        draw.text((t_box[0] + 14, t_box[1] + 10), f"⚔️ {title_t}", fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
        draw.text((t_box[0] + 14, t_box[1] + 36), desc_t, fill=(180, 180, 160), font=core.F_BODY)
        ty += 82

    out_name = f"creature_{c_name_en.lower()}.jpg"
    return save_and_sync(canvas, out_name)


# ---------------------------------------------------------------------------
# 3. CHARACTER CARD (HERO KIT + PRESTIGE SKINS MINI PREVIEW - NO CLASS LABEL)
# ---------------------------------------------------------------------------
def render_clean_character_card(char_key: str = "marie", is_french: bool = True) -> str:
    c_low = char_key.lower().strip()
    if "eva" in c_low:
        hero_name = "Eva"
        portrait = "assets/characters/eva.webp"
        q_ico = "assets/abilities/eva_q.png"
        e_ico = "assets/abilities/eva_e.png"
        pass_ico = "assets/abilities/eva_passive.png"
        q_name, q_desc = "Caltrops (Chausse-trappes)", "Répand des pointes métalliques ralentissant les ennemis de 60%."
        e_name, e_desc = "Flashbang (Grenade)", "Aveugle et désoriente les cibles dans un rayon de 8 mètres."
        pass_name, pass_desc = "Lightfoot (Pied Léger)", "Bruit de pas réduit de 35% et vitesse d'accroupissement augmentée."
        prestige_img = "assets/skins/Eva_Cosmetic_10a.webp"
        prestige_title = "Prestige I: Mademoiselle Rouge"
    elif "hugo" in c_low:
        hero_name = "Hugo"
        portrait = "assets/characters/hugo.webp"
        q_ico = "assets/abilities/hugo_q.png"
        e_ico = "assets/abilities/hugo_e.png"
        pass_ico = "assets/abilities/hugo_passive.png"
        q_name, q_desc = "Fortify (Fortification)", "Pose un bouclier temporaire absorbant 120 points de dégâts."
        e_name, e_desc = "War Cry (Cri de Guerre)", "Augmente la vitesse de frappe de toute l'escouade de 20% pendant 8s."
        pass_name, pass_desc = "Thick Skin (Cuir Épais)", "Ignore 15% des dégâts physiques d'impact perforants."
        prestige_img = "assets/skins/Hugo_Cosmetic_10a.webp"
        prestige_title = "Prestige I: Iron Vanguard"
    else:
        hero_name = "Marie"
        portrait = "assets/characters/marie.webp"
        q_ico = "assets/abilities/marie_q.png"
        e_ico = "assets/abilities/marie_e.png"
        pass_ico = "assets/abilities/marie_passive.png"
        q_name, q_desc = "Healing Salve (Baume)", "Restaure 75 PV sur 6 secondes à soi-même ou un allié."
        e_name, e_desc = "Acid Flask (Fiole d'Acide)", "Brise l'armure ennemie de 40% et inflige des dégâts d'acide."
        pass_name, pass_desc = "Alchemical Pouch", "Peut transporter 2 fioles supplémentaires dans sa besace."
        prestige_img = "assets/skins/Marie_Cosmetic_09a.webp"
        prestige_title = "Prestige I: Scarlet Inquisitor"

    canvas, draw = create_base_canvas(f"HERO PROFILE : {hero_name.upper()} (EXPÉDITIONNAIRE)", tag="SURVIVANT OFFICIEL")

    # Left: Official Hero Portrait
    left_box = [28, 86, 360, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    img_frame = [left_box[0] + 16, left_box[1] + 14, left_box[2] - 16, left_box[1] + 370]
    draw.rounded_rectangle(img_frame, radius=8, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(portrait):
        safe_paste(canvas, Image.open(portrait), (img_frame[0] + 5, img_frame[1] + 5, img_frame[2] - img_frame[0] - 10, img_frame[3] - img_frame[1] - 10))

    draw.text((left_box[0] + 18, img_frame[3] + 14), hero_name, fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 18, img_frame[3] + 46), "Rôle : Expéditionnaire & Survivant de Raid", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, img_frame[3] + 70), "Château Hub · Compétences Officielles", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    # Right: Abilities Kit + Prestige Skin Preview
    right_box = [380, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    draw.text((right_box[0] + 20, right_box[1] + 14), "KIT DE COMPÉTENCES ACTIVES & PASSIVES", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    abilities = [
        ("PASSIVE", pass_name, pass_desc, pass_ico),
        ("TACTIQUE (Q)", q_name, q_desc, q_ico),
        ("SPÉCIALE (E)", e_name, e_desc, e_ico)
    ]

    ay = right_box[1] + 44
    for key_lbl, ab_n, ab_d, ab_ico in abilities:
        row = [right_box[0] + 16, ay, right_box[2] - 16, ay + 68]
        draw.rounded_rectangle(row, radius=8, fill=core.BG_CARD, outline=(45, 42, 35), width=1)

        ico_b = [row[0] + 10, row[1] + 8, row[0] + 62, row[3] - 8]
        draw.rounded_rectangle(ico_b, radius=6, fill=(14, 14, 16), outline=core.COLOR_GOLD, width=1)
        if os.path.exists(ab_ico):
            safe_paste(canvas, Image.open(ab_ico), (ico_b[0] + 4, ico_b[1] + 4, 44, 44))

        draw.rounded_rectangle([row[0] + 72, row[1] + 10, row[0] + 185, row[1] + 32], radius=4, fill=(35, 28, 16), outline=core.COLOR_GOLD, width=1)
        draw.text((row[0] + 78, row[1] + 12), key_lbl, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
        draw.text((row[0] + 195, row[1] + 10), ab_n, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
        draw.text((row[0] + 72, row[1] + 38), ab_d[:75], fill=(180, 180, 160), font=core.F_BODY)

        ay += 76

    # Bottom: Prestige Skins Showcase (Small Visual Preview!)
    p_box = [right_box[0] + 16, ay + 6, right_box[2] - 16, right_box[3] - 14]
    draw.rounded_rectangle(p_box, radius=8, fill=(24, 20, 26), outline=core.PRIO_PURPLE, width=1)

    p_ico_box = [p_box[0] + 10, p_box[1] + 8, p_box[0] + 90, p_box[3] - 8]
    draw.rounded_rectangle(p_ico_box, radius=6, fill=(14, 14, 16), outline=core.PRIO_PURPLE, width=1)
    if os.path.exists(prestige_img):
        safe_paste(canvas, Image.open(prestige_img), (p_ico_box[0] + 4, p_ico_box[1] + 4, 72, p_ico_box[3] - p_ico_box[1] - 8))

    draw.text((p_box[0] + 104, p_box[1] + 12), f"APPARITION DE PRESTIGE : {prestige_title}", fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
    draw.text((p_box[0] + 104, p_box[1] + 38), "Déblocable à l'Atelier du Tailleur après accomplissement des paliers de raid de haut niveau.", fill=(180, 175, 160), font=core.F_BODY)

    out_name = f"character_{hero_name.lower()}.jpg"
    return save_and_sync(canvas, out_name)


# ---------------------------------------------------------------------------
# 4. CLEAN JACQUES FOLLY DUNGEON CARD (LARGE MAP ON RIGHT - NO UNREADABLE SIDEBAR!)
# ---------------------------------------------------------------------------
def render_clean_dungeon_card(is_french: bool = True) -> str:
    canvas, draw = create_base_canvas("DUNGEON : JACQUES FOLLY (LA FOLIE DE JACQUES)", tag="DONJON VERROUILLÉ")

    # Left Column: Dungeon Intel
    left_box = [28, 86, 440, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    draw.text((left_box[0] + 18, left_box[1] + 16), "RENSEIGNEMENTS SUR LE DONJON", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 48), "Jacques Folly (La Folie)", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 82), "Localisation : Sous-sol de Jacques Bridge", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, left_box[1] + 108), "Clé requise : Clé de la folie de Jacques (Rare)", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # Key spawn & container stats
    c_box = [left_box[0] + 16, left_box[1] + 145, left_box[2] - 16, left_box[1] + 250]
    draw.rounded_rectangle(c_box, radius=8, fill=(20, 20, 24), outline=core.BORDER_SUBTLE, width=1)
    draw.text((c_box[0] + 14, c_box[1] + 10), "CONTENEURS & BUTIN :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((c_box[0] + 14, c_box[1] + 34), "• 174 conteneurs au total dans les salles souterraines.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((c_box[0] + 14, c_box[1] + 58), "• Spawns de la clé : Tables d'officiers et tiroirs de Jacques Bridge.", fill=(180, 180, 160), font=core.F_BODY)

    # Mobs
    m_box = [left_box[0] + 16, c_box[3] + 12, left_box[2] - 16, left_box[3] - 14]
    draw.rounded_rectangle(m_box, radius=8, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((m_box[0] + 14, m_box[1] + 10), "MENACES INTÉRIEURES :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((m_box[0] + 14, m_box[1] + 34), "• Brutes Élite et Baveux embusqués dans les corridors étroits.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((m_box[0] + 14, m_box[1] + 58), "• Risque élevé d'encerclement : Gardez une torche et des soins.", fill=(180, 180, 160), font=core.F_BODY)

    # Right Column: Large Clean Entrance Map with NO SIDEBAR!
    right_box = [460, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 16), "ENTRÉE DU DONJON (SANS BARRE LATÉRALE ILLISIBLE)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    raw_map_p = os.path.join(ROOT_DIR, "jacques-bridge.webp")
    if os.path.exists(raw_map_p):
        base_map = Image.open(raw_map_p).convert("RGBA")
        mw, mh = base_map.size
        # Jacques Folly entrance pin in 4096 scale
        cx, cy = 1850 * 2, 1520 * 2
        rad = 600
        crop = base_map.crop((max(0, cx - rad), max(0, cy - rad), min(mw, cx + rad), min(mh, cy + rad)))

        c_draw = ImageDraw.Draw(crop)
        pin_x, pin_y = rad, rad
        c_draw.ellipse([pin_x - 34, pin_y - 34, pin_x + 34, pin_y + 34], fill=(235, 60, 60, 80), outline=(235, 60, 60), width=4)
        c_draw.ellipse([pin_x - 16, pin_y - 16, pin_x + 16, pin_y + 16], fill=(235, 60, 60), outline=(255, 255, 255), width=2)
        c_draw.ellipse([pin_x - 5, pin_y - 5, pin_x + 5, pin_y + 5], fill=(20, 20, 20))

        lbl = "ENTRÉE DU DONJON (JACQUES FOLLY)"
        lw = int(c_draw.textlength(lbl, font=core.F_CARD_TITLE)) + 30
        c_draw.rounded_rectangle([pin_x - lw // 2, pin_y + 24, pin_x + lw // 2, pin_y + 60], radius=6, fill=(16, 16, 18, 240), outline=(235, 60, 60), width=2)
        c_draw.text((pin_x - lw // 2 + 15, pin_y + 30), lbl, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)

        target_w = right_box[2] - right_box[0] - 32
        target_h = right_box[3] - right_box[1] - 60
        safe_paste(canvas, crop, (right_box[0] + 16, right_box[1] + 48, target_w, target_h))

    return save_and_sync(canvas, "dungeon_jacques-folly.jpg")

if __name__ == "__main__":
    print("Testing overhaul_v3_cards...")
    p_gav = render_clean_gavroche_quest_card()
    p_drool = render_clean_creature_card("drooler")
    p_brute = render_clean_creature_card("brute")
    p_char = render_clean_character_card("marie")
    p_dungeon = render_clean_dungeon_card()
    print("All overhaul_v3_cards rendered successfully!")
