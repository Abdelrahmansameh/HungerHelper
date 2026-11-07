from co_pilot.card_store import stored_card
import os
import sys
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

    # Header bar (NO WATERMARK)
    draw.rounded_rectangle([16, 14, CARD_W - 16, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    tag_w = int(draw.textlength(tag.upper(), font=core.F_SMALL_BOLD)) + 24
    draw.rounded_rectangle([28, 22, 28 + tag_w, 60], radius=5, fill=(35, 30, 20), outline=core.COLOR_GOLD, width=1)
    draw.text((40, 31), tag.upper(), fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((44 + tag_w, 27), title.upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    return canvas, draw

# ===========================================================================
# 1. CHARACTER CARD (KIT + SKINS SIDE-BY-SIDE - NO ROLE / CHATEAU HUB FLUFF)
# ===========================================================================
def render_clean_character_card(char_key: str = "marie", is_french: bool = False) -> str:
    c_low = char_key.lower().strip()
    if "eva" in c_low:
        hero_name = "Eva"
        portrait = "assets/characters/eva.webp"
        q_ico = "assets/abilities/eva_q.png"
        e_ico = "assets/abilities/eva_e.png"
        pass_ico = "assets/abilities/eva_passive.png"
        q_name = "Caltrops" if not is_french else "Chausse-trappes"
        q_desc = "Throws metal spikes slowing enemy movement by 60%." if not is_french else "Répand des pointes ralentissant les ennemis de 60%."
        e_name = "Flashbang" if not is_french else "Grenade Aveuglante"
        e_desc = "Blinds and disorients all targets within 8 meters." if not is_french else "Aveugle les cibles dans un rayon de 8 mètres."
        pass_name = "Lightfoot" if not is_french else "Pied Léger"
        pass_desc = "Footstep noise reduced by 35%, crouch speed increased." if not is_french else "Bruit de pas réduit de 35%, accroupi plus rapide."
        skin_imgs = ["assets/skins/Eva_Cosmetic_10a.webp"]
    elif "hugo" in c_low:
        hero_name = "Hugo"
        portrait = "assets/characters/hugo.webp"
        q_ico = "assets/abilities/hugo_q.png"
        e_ico = "assets/abilities/hugo_e.png"
        pass_ico = "assets/abilities/hugo_passive.png"
        q_name = "Fortify" if not is_french else "Fortification"
        q_desc = "Deploys a temporary personal shield absorbing 120 damage." if not is_french else "Bouclier temporaire absorbant 120 dégâts."
        e_name = "War Cry" if not is_french else "Cri de Guerre"
        e_desc = "Increases squad melee attack speed by 20% for 8 seconds." if not is_french else "Augmente la vitesse de frappe de 20% pendant 8s."
        pass_name = "Thick Skin" if not is_french else "Cuir Épais"
        pass_desc = "Passively absorbs 15% physical impact damage." if not is_french else "Ignore 15% des dégâts physiques d'impact."
        skin_imgs = ["assets/skins/Hugo_Cosmetic_10a.webp"]
    elif "otto" in c_low:
        hero_name = "Otto"
        portrait = "assets/characters/otto.webp"
        q_ico = "assets/abilities/otto_q.png"
        e_ico = "assets/abilities/otto_e.png"
        pass_ico = "assets/abilities/otto_passive.png"
        q_name = "Siegebreaker" if not is_french else "Brise-Siège"
        q_desc = "Heavy shoulder charge knocking down foes and breaking doors." if not is_french else "Charge lourde renversant les ennemis et brisant les portes."
        e_name = "Iron Will" if not is_french else "Volonté de Fer"
        e_desc = "Grants immunity to stagger and bleed for 10 seconds." if not is_french else "Immunité aux déséquilibres et saignements pendant 10s."
        pass_name = "Armor Smith" if not is_french else "Maître Armurier"
        pass_desc = "Armor durability depletes 30% slower during raids." if not is_french else "Durabilité d'armure s'use 30% moins vite en raid."
        skin_imgs = ["assets/skins/Otto_Cosmetic_10a.webp"]
    else: # Marie default
        hero_name = "Marie"
        portrait = "assets/characters/marie.webp"
        q_ico = "assets/abilities/marie_q.png"
        e_ico = "assets/abilities/marie_e.png"
        pass_ico = "assets/abilities/marie_passive.png"
        q_name = "Healing Salve" if not is_french else "Baume Curatif"
        q_desc = "Restores 75 HP over 6 seconds to self or targeted ally." if not is_french else "Restaure 75 PV sur 6 secondes à soi ou un allié."
        e_name = "Acid Flask" if not is_french else "Fiole d'Acide"
        e_desc = "Corrodes enemy armor by 40% and deals acid splash damage." if not is_french else "Brise l'armure de 40% et inflige des dégâts d'acide."
        pass_name = "Alchemical Pouch" if not is_french else "Besace d'Alchimiste"
        pass_desc = "Can carry 2 additional medicine vials in secure belt." if not is_french else "Peut transporter 2 fioles de soin supplémentaires."
        skin_imgs = [
            "assets/skins/Marie_Cosmetic_09a.webp",
            "assets/skins/Marie_Cosmetic_11a.webp",
            "assets/skins/Marie_Cosmetic_12a.webp"
        ]

    title = f"HERO : {hero_name.upper()}" if not is_french else f"HÉROS : {hero_name.upper()}"
    canvas, draw = create_base_canvas(title, tag="TACTICAL OPERATIVE")

    # Left: Portrait Box
    left_box = [28, 86, 360, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)
    img_frame = [left_box[0] + 16, left_box[1] + 16, left_box[2] - 16, left_box[3] - 16]
    draw.rounded_rectangle(img_frame, radius=8, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(portrait):
        safe_paste(canvas, Image.open(portrait), (img_frame[0] + 5, img_frame[1] + 5, img_frame[2] - img_frame[0] - 10, img_frame[3] - img_frame[1] - 10))

    # Right: Ability Kit + Side-by-Side Skins Preview
    right_box = [380, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    hdr_kit = "TACTICAL ABILITIES" if not is_french else "COMPÉTENCES TACTIQUES"
    draw.text((right_box[0] + 20, right_box[1] + 14), hdr_kit, fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    abilities = [
        ("PASSIVE", pass_name, pass_desc, pass_ico),
        ("TACTICAL [Q]", q_name, q_desc, q_ico),
        ("SPECIAL [E]", e_name, e_desc, e_ico)
    ]

    ay = right_box[1] + 44
    for key_lbl, ab_n, ab_d, ab_ico in abilities:
        row = [right_box[0] + 16, ay, right_box[2] - 16, ay + 66]
        draw.rounded_rectangle(row, radius=8, fill=core.BG_CARD, outline=(45, 42, 35), width=1)

        ico_b = [row[0] + 10, row[1] + 8, row[0] + 60, row[3] - 8]
        draw.rounded_rectangle(ico_b, radius=6, fill=(14, 14, 16), outline=core.COLOR_GOLD, width=1)
        if os.path.exists(ab_ico):
            safe_paste(canvas, Image.open(ab_ico), (ico_b[0] + 4, ico_b[1] + 4, 42, 42))

        draw.rounded_rectangle([row[0] + 70, row[1] + 10, row[0] + 185, row[1] + 32], radius=4, fill=(35, 28, 16), outline=core.COLOR_GOLD, width=1)
        draw.text((row[0] + 76, row[1] + 12), key_lbl, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
        draw.text((row[0] + 195, row[1] + 10), ab_n, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
        draw.text((row[0] + 70, row[1] + 38), ab_d, fill=(180, 180, 160), font=core.F_BODY)

        ay += 74

    # Bottom: Side-by-side skin images WITHOUT extra text
    s_banner_y = ay + 4
    hdr_skins = "COSMETIC SKINS PREVIEW" if not is_french else "APERÇU DES SKINS DÉBLOCABLES"
    draw.text((right_box[0] + 20, s_banner_y), hdr_skins, fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    skins_row = [right_box[0] + 16, s_banner_y + 26, right_box[2] - 16, right_box[3] - 12]
    draw.rounded_rectangle(skins_row, radius=8, fill=(16, 16, 20), outline=core.BORDER_SUBTLE, width=1)

    # Place multiple skins side-by-side
    valid_skins = [p for p in skin_imgs if os.path.exists(p)]
    if valid_skins:
        sw = (skins_row[2] - skins_row[0] - 20 - (len(valid_skins) - 1) * 12) // len(valid_skins)
        sh = skins_row[3] - skins_row[1] - 12
        for s_idx, sp in enumerate(valid_skins):
            bx = skins_row[0] + 10 + s_idx * (sw + 12)
            by = skins_row[1] + 6
            s_box = [bx, by, bx + sw, by + sh]
            draw.rounded_rectangle(s_box, radius=6, fill=(12, 12, 14), outline=core.PRIO_PURPLE, width=1)
            safe_paste(canvas, Image.open(sp), (bx + 4, by + 4, sw - 8, sh - 8))

    out_name = f"character_{hero_name.lower()}.jpg"
    return save_and_sync(canvas, out_name)


# ===========================================================================
# 2. DUNGEON CARD (ALL 3 ENTRANCES ON JACQUES BRIDGE - NO SIDEBAR)
# ===========================================================================
@stored_card('is_french')
def render_clean_dungeon_card(is_french: bool = False) -> str:
    title = "DUNGEON : JACQUES FOLLY (SUBTERRANEAN BASTION)" if not is_french else "DONJON : JACQUES FOLLY (LA FOLIE DE JACQUES)"
    canvas, draw = create_base_canvas(title, tag="DUNGEON ACCESS")

    # Left: Intel Panel
    left_box = [28, 86, 420, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    hdr_intel = "DUNGEON RECON & ACCESS" if not is_french else "RENSEIGNEMENTS DU DONJON"
    draw.text((left_box[0] + 18, left_box[1] + 16), hdr_intel, fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    loc_t = "Location: Jacques Bridge Subterranean" if not is_french else "Lieu : Sous-sol de Jacques Bridge"
    key_t = "Required Key: Jacques Folly Key (3 Uses)" if not is_french else "Clé requise : Clé de Jacques Folly (3 usages)"
    draw.text((left_box[0] + 18, left_box[1] + 48), loc_t, fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, left_box[1] + 74), key_t, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # 3 Entrances listed
    e_box = [left_box[0] + 16, left_box[1] + 110, left_box[2] - 16, left_box[1] + 245]
    draw.rounded_rectangle(e_box, radius=8, fill=(20, 20, 24), outline=core.BORDER_SUBTLE, width=1)
    e_hdr = "3 SUBTERRANEAN ENTRANCES :" if not is_french else "3 PORTES D'ENTRÉE DU DONJON :"
    draw.text((e_box[0] + 14, e_box[1] + 10), e_hdr, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((e_box[0] + 14, e_box[1] + 34), "[1] North Iron Gate (Bridge North Bastion)", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((e_box[0] + 14, e_box[1] + 60), "[2] Courtyard Crypt Door (Fort Courtyard)", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((e_box[0] + 14, e_box[1] + 86), "[3] Undercroft Iron Door (Arch Sub-Level)", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    # Loot & Spawns
    l_box = [left_box[0] + 16, e_box[3] + 12, left_box[2] - 16, left_box[3] - 14]
    draw.rounded_rectangle(l_box, radius=8, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    l_hdr = "LOOT & SPATIAL INTEL :" if not is_french else "BUTIN & CONTENEURS :"
    draw.text((l_box[0] + 14, l_box[1] + 10), l_hdr, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((l_box[0] + 14, l_box[1] + 34), "• 174 Subterranean Containers & High-Tier Weapon Chests.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((l_box[0] + 14, l_box[1] + 58), "• Key Spawns: 5 desks & bastion crates across bridge roadway.", fill=(180, 180, 160), font=core.F_BODY)

    # Right: Map showing ALL THREE ENTRANCES on Jacques Bridge
    right_box = [440, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    m_hdr = "ALL 3 ENTRANCE DOORS PLOTTED (JACQUES BRIDGE BASTION)" if not is_french else "LES 3 PORTES D'ENTRÉE SUR LE PONT JACQUES"
    draw.text((right_box[0] + 20, right_box[1] + 14), m_hdr, fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    raw_map_p = os.path.join(ROOT_DIR, "jacques-bridge.webp")
    if os.path.exists(raw_map_p):
        base_map = Image.open(raw_map_p).convert("RGBA")
        mw, mh = base_map.size

        # Bastion area center on 4096 scale
        cx, cy = int(1680.0 / 2048.0 * mw), int(450.0 / 2048.0 * mh)
        rad_w, rad_h = 750, 520
        crop = base_map.crop((max(0, cx - rad_w), max(0, cy - rad_h), min(mw, cx + rad_w), min(mh, cy + rad_h)))

        c_draw = ImageDraw.Draw(crop)
        # Entrances relative coordinates on cropped area:
        # Entrances in 2048 scale:
        # 1. North Iron Gate: (1835.9, 505.5) -> (1835.9 - (cx * 2048 / mw) + rad_w * 2048 / mw)
        entrances = [
            (1835.90, 505.49, "[1] North Iron Gate"),
            (1605.21, 512.75, "[2] Courtyard Crypt Door"),
            (1418.37, 337.55, "[3] Undercroft Iron Door")
        ]

        for ex, ey, elbl in entrances:
            # Map ex, ey to crop coordinates
            px = int((ex / 2048.0 * mw) - (cx - rad_w))
            py = int((ey / 2048.0 * mh) - (cy - rad_h))

            # Draw Pin
            c_draw.ellipse([px - 28, py - 28, px + 28, py + 28], fill=(235, 60, 60, 90), outline=(235, 60, 60), width=4)
            c_draw.ellipse([px - 14, py - 14, px + 14, py + 14], fill=(235, 60, 60), outline=(255, 255, 255), width=2)
            c_draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(20, 20, 20))

            # Label
            lw = int(c_draw.textlength(elbl, font=core.F_CARD_TITLE)) + 24
            c_draw.rounded_rectangle([px - lw // 2, py + 20, px + lw // 2, py + 52], radius=5, fill=(16, 16, 20, 240), outline=(235, 60, 60), width=2)
            c_draw.text((px - lw // 2 + 12, py + 25), elbl, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)

        target_w = right_box[2] - right_box[0] - 32
        target_h = right_box[3] - right_box[1] - 56
        safe_paste(canvas, crop, (right_box[0] + 16, right_box[1] + 44, target_w, target_h))

    return save_and_sync(canvas, "dungeon_jacques-folly.jpg")


# ===========================================================================
# 3. CREATURE CARD (DROOLER 3D RENDER + BRUTE - NO WATERMARK - ENGLISH DEFAULT)
# ===========================================================================
def render_clean_creature_card(creature_key: str = "drooler", is_french: bool = False) -> str:
    c_low = creature_key.lower().strip()
    is_brute = "brute" in c_low

    if is_brute:
        c_name = "BRUTE"
        hp, speed, dmg = 900, "Slow (0.8 m/s)" if not is_french else "Lente (0.8 m/s)", "68 Base (96 Area)"
        render_img = os.path.join(ROOT_DIR, "assets", "bestiary", "BP_Brute_Parent__full.webp")
        trophy_img = os.path.join(ROOT_DIR, "assets", "items", "T_UI_Trophy_BruteFoot.png")
        trophy_name = "Brute Foot" if not is_french else "Patte de Brute"
        trophy_rate = "76.9% skinning drop rate" if not is_french else "76.9% au dépeçage"
        trophy_val = "120 Copper (Tanner Workshop)" if not is_french else "120 Cuivres (Atelier du Tanneur)"
        tactics = [
            ("Backstab Criticals (x2 Dmg)", "Extremely vulnerable to heavy thrust attacks in the back.") if not is_french else ("Critiques dans le dos (x2)", "Vulnérable aux attaques d'estoc lourdes dans le dos."),
            ("Sweeping Cleave Dodge", "Telegraphs a wide 360-degree sweep. Roll backward before impact.") if not is_french else ("Esquive du balayage", "Roulez en arrière avant le balayage lourd.")
        ]
    else:
        c_name = "DROOLER"
        hp, speed, dmg = 450, "Fast (3.1 m/s)" if not is_french else "Rapide (3.1 m/s)", "36 (Acid Spit)"
        render_img = os.path.join(ROOT_DIR, "assets", "bestiary", "BP_Biter_Parent__full.webp")
        if not os.path.exists(render_img):
            render_img = os.path.join(ROOT_DIR, "assets", "bestiary", "BP_Biter_Parent__face.webp")
        trophy_img = os.path.join(ROOT_DIR, "assets", "items", "T_UI_Trophy_BiterJaw.png")
        trophy_name = "Drooler Jaw" if not is_french else "Mâchoire de Baveux"
        trophy_rate = "75.8% skinning drop rate" if not is_french else "75.8% au dépeçage"
        trophy_val = "95 Copper (Taxidermy Workshop)" if not is_french else "95 Cuivres (Atelier de Taxidermie)"
        tactics = [
            ("Rapid Thrust Piercing", "Extremely weak to spear thrusts. Eliminated in under 4 seconds.") if not is_french else ("Perforation d'estoc rapide", "Sensible aux frappes d'estoc de lance. Éliminé en 4s."),
            ("Corrosive Acid Evasion", "Maintain lateral strafe movement to evade ranged acid projectiles.") if not is_french else ("Esquive du jet acide", "Gardez une trajectoire latérale pour esquiver le crachat.")
        ]

    canvas, draw = create_base_canvas(f"CREATURE : {c_name}", tag="MONSTRUM COMPENDIUM")

    # Left: 3D Render
    left_box = [28, 86, 420, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)
    render_frame = [left_box[0] + 16, left_box[1] + 14, left_box[2] - 16, left_box[1] + 370]
    draw.rounded_rectangle(render_frame, radius=8, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(render_img):
        safe_paste(canvas, Image.open(render_img), (render_frame[0] + 5, render_frame[1] + 5, render_frame[2] - render_frame[0] - 10, render_frame[3] - render_frame[1] - 10))

    draw.text((left_box[0] + 18, render_frame[3] + 12), f"HEALTH POOL : {hp} HP", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, render_frame[3] + 38), f"Movement : {speed}  |  Attack : {dmg}", fill=(180, 180, 160), font=core.F_BODY)

    # Right: Loot & Combat Tactics
    right_box = [440, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    hdr_loot = "OFFICIAL HUNTING TROPHY & HARVEST" if not is_french else "BUTIN & TROPHÉE OFFICIEL DE CHASSE"
    draw.text((right_box[0] + 20, right_box[1] + 16), hdr_loot, fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    drop_card = [right_box[0] + 18, right_box[1] + 48, right_box[2] - 18, right_box[1] + 155]
    draw.rounded_rectangle(drop_card, radius=8, fill=core.BG_CARD, outline=core.PRIO_YELLOW, width=1)

    ico_box = [drop_card[0] + 14, drop_card[1] + 14, drop_card[0] + 94, drop_card[1] + 94]
    draw.rounded_rectangle(ico_box, radius=6, fill=(16, 16, 18), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(trophy_img):
        safe_paste(canvas, Image.open(trophy_img), (ico_box[0] + 4, ico_box[1] + 4, 72, 72))

    draw.text((drop_card[0] + 110, drop_card[1] + 16), trophy_name, fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((drop_card[0] + 110, drop_card[1] + 48), f"• Drop Rate : {trophy_rate}", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)
    draw.text((drop_card[0] + 110, drop_card[1] + 74), f"• Market Value : {trophy_val}", fill=(180, 180, 160), font=core.F_BODY)

    ty = drop_card[3] + 18
    hdr_tact = "OFFICIAL COMBAT TACTICS" if not is_french else "TACTIQUES OFFICIELLES DE COMBAT"
    draw.text((right_box[0] + 20, ty), hdr_tact, fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    ty += 34

    for title_t, desc_t in tactics:
        t_box = [right_box[0] + 18, ty, right_box[2] - 18, ty + 72]
        draw.rounded_rectangle(t_box, radius=6, fill=core.BG_CARD, outline=(45, 42, 35), width=1)
        draw.text((t_box[0] + 14, t_box[1] + 10), f"⚔️ {title_t}", fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
        draw.text((t_box[0] + 14, t_box[1] + 36), desc_t, fill=(180, 180, 160), font=core.F_BODY)
        ty += 82

    out_name = f"creature_{c_name.lower()}.jpg"
    return save_and_sync(canvas, out_name)


# ===========================================================================
# 4. GAVROCHE QUEST CARD (CLEAN MAP CROP - NO SIDEBAR - NO JAQUES FOLLY)
# ===========================================================================
def render_clean_gavroche_quest_card(is_french: bool = False) -> str:
    title = "QUEST : THE GAVROCHE FAMILY (RUINS CAMP)" if not is_french else "QUÊTE : LA FAMILLE GAVROCHE (CAMP DES RUINES)"
    canvas, draw = create_base_canvas(title, tag="RECONNAISSANCE")

    # Left: Contract details
    left_box = [28, 86, 430, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    hdr_contract = "CONTRACT INTEL" if not is_french else "DÉTAILS DU CONTRAT"
    draw.text((left_box[0] + 18, left_box[1] + 16), hdr_contract, fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 48), "The Gavroche Family", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 82), "Giver: Eloise (Chateau Hub)" if not is_french else "Commanditaire : Éloïse (Château Hub)", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, left_box[1] + 108), "Map: Jacques Bridge (East Riverbank)" if not is_french else "Carte : Jacques Bridge (Berges Est)", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    hdr_obj = "RECON OBJECTIVES :" if not is_french else "OBJECTIFS DE RECONNAISSANCE :"
    draw.text((left_box[0] + 18, left_box[1] + 148), hdr_obj, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, left_box[1] + 174), "1. Cross Jacques Bridge toward East riverbank.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 202), "2. Locate isolated Gavroche family camp ruins.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 230), "3. Discover site and safely extract back to Chateau.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    hdr_req = "ITEM REQUIREMENTS :" if not is_french else "ITEMS REQUIS :"
    draw.text((left_box[0] + 18, left_box[1] + 272), hdr_req, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, left_box[1] + 296), "• Pure reconnaissance mission (No loot turn-in required).", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 322), "• Note: 'The Last Prisoner' quest takes place inside", fill=(175, 175, 155), font=core.F_BODY)
    draw.text((left_box[0] + 18, left_box[1] + 344), "  Jacques Folly subterranean dungeon, not here.", fill=(175, 175, 155), font=core.F_BODY)

    rew_box = [left_box[0] + 16, left_box[1] + 385, left_box[2] - 16, left_box[3] - 14]
    draw.rounded_rectangle(rew_box, radius=8, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    hdr_rew = "MISSION REWARDS :" if not is_french else "RÉCOMPENSES DE MISSION :"
    draw.text((rew_box[0] + 14, rew_box[1] + 8), hdr_rew, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((rew_box[0] + 14, rew_box[1] + 30), "• 3x Stewed Apples (Healing Provisions)", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((rew_box[0] + 14, rew_box[1] + 52), "• +250 Reputation XP at Chateau Hub", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    # Right: Clean Tactical Map without sidebar
    right_box = [450, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    hdr_map = "GAVROCHE CAMP SPOT (ISOLATED PIN - NO SIDEBAR)" if not is_french else "EMPLACEMENT DU CAMPEMENT (AUCUN AUTRE POINT DISPERSÉ)"
    draw.text((right_box[0] + 20, right_box[1] + 16), hdr_map, fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    raw_map_p = os.path.join(ROOT_DIR, "jacques-bridge.webp")
    if os.path.exists(raw_map_p):
        base_map = Image.open(raw_map_p).convert("RGBA")
        mw, mh = base_map.size
        cx, cy = 2950, 626
        rad = 650
        crop = base_map.crop((max(0, cx - rad), max(0, cy - rad), min(mw, cx + rad), min(mh, cy + rad)))

        c_draw = ImageDraw.Draw(crop)
        pin_x, pin_y = rad, rad
        c_draw.ellipse([pin_x - 32, pin_y - 32, pin_x + 32, pin_y + 32], fill=(245, 200, 60, 70), outline=(245, 200, 60), width=4)
        c_draw.ellipse([pin_x - 16, pin_y - 16, pin_x + 16, pin_y + 16], fill=(245, 200, 60), outline=(255, 255, 255), width=2)
        c_draw.ellipse([pin_x - 5, pin_y - 5, pin_x + 5, pin_y + 5], fill=(20, 20, 20))

        lbl = "GAVROCHE CAMP (EAST RUINS)" if not is_french else "CAMPEMENT GAVROCHE (RUINES)"
        lw = int(c_draw.textlength(lbl, font=core.F_CARD_TITLE)) + 30
        c_draw.rounded_rectangle([pin_x - lw // 2, pin_y + 24, pin_x + lw // 2, pin_y + 60], radius=6, fill=(16, 16, 18, 240), outline=core.COLOR_GOLD, width=2)
        c_draw.text((pin_x - lw // 2 + 15, pin_y + 30), lbl, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)

        target_w = right_box[2] - right_box[0] - 32
        target_h = right_box[3] - right_box[1] - 60
        safe_paste(canvas, crop, (right_box[0] + 16, right_box[1] + 48, target_w, target_h))

    return save_and_sync(canvas, "quest_card_the-gavroche-family.jpg")


if __name__ == "__main__":
    print("Testing clean_cards_v5...")
    p_char = render_clean_character_card("marie")
    p_dun = render_clean_dungeon_card()
    p_cr = render_clean_creature_card("drooler")
    p_br = render_clean_creature_card("brute")
    p_gav = render_clean_gavroche_quest_card()
    print("All clean_cards_v5 rendered successfully!")
