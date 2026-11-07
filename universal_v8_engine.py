from typing import Optional, Dict, Any, List
import re
import os
import sys
import json
import math
import sqlite3
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import perfect_briefings_core_v25 as core
core.preload_assets()

OUT_DIR = os.path.join(ROOT_DIR, "output_maps")
os.makedirs(OUT_DIR, exist_ok=True)
BRAIN_DIR = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49"

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

def create_base_canvas(title: str, tag: str = "TACTICAL INTEL", width: int = 1040, height: int = 580, border_col=None):
    b_col = border_col if border_col else core.COLOR_GOLD
    canvas = Image.new("RGBA", (width, height), (12, 12, 15))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, width, height], fill=(12, 12, 15))
    draw.rectangle([4, 4, width - 5, height - 5], outline=b_col, width=2)
    draw.rectangle([8, 8, width - 9, height - 9], outline=(40, 36, 26), width=1)

    draw.rounded_rectangle([16, 14, width - 16, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    tag_w = int(draw.textlength(tag.upper(), font=core.F_SMALL_BOLD)) + 24
    draw.rounded_rectangle([28, 22, 28 + tag_w, 60], radius=5, fill=(35, 30, 20), outline=b_col, width=1)
    draw.text((40, 31), tag.upper(), fill=b_col, font=core.F_SMALL_BOLD)
    draw.text((44 + tag_w, 27), title.upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    return canvas, draw


# ===========================================================================
# 1. CHARACTER PROFILES (ALL 6 HEROES - UNIQUE DISTINCT PRESTIGE IMAGES)
# ===========================================================================
HEROES_DATA = {
    "marie": {
        "name": "Marie",
        "portrait": "assets/characters/marie.webp",
        "pass_name": "Alchemical Pouch",
        "pass_desc": "Can carry 2 additional medicine vials in secure belt.",
        "pass_ico": "assets/abilities/marie_passive.png",
        "q_name": "Healing Salve",
        "q_desc": "Restores 75 HP over 6 seconds to self or targeted ally.",
        "q_ico": "assets/abilities/marie_q.png",
        "e_name": "Acid Flask",
        "e_desc": "Corrodes enemy armor by 40% and deals acid splash damage.",
        "e_ico": "assets/abilities/marie_e.png",
        "skins": [
            ("PRESTIGE I: SCARLET INQUISITOR", "assets/skins/Marie_Cosmetic_10a.webp"),
            ("PRESTIGE II: SISTER OF GLASS", "assets/skins/Marie_Cosmetic_13a.webp"),
            ("MATRIARCH (ATELIER EXCLUSIVE)", "assets/skins/Marie_Cosmetic_11a.webp")
        ]
    },
    "otto": {
        "name": "Otto",
        "portrait": "assets/characters/otto.webp",
        "pass_name": "Maintenance",
        "pass_desc": "Armor durability degrades 35% slower in combat.",
        "pass_ico": "assets/abilities/otto_passive.png",
        "q_name": "Field Repairs",
        "q_desc": "Instantly repairs 50 armor points on targeted armor plate.",
        "q_ico": "assets/abilities/otto_q.png",
        "e_name": "Masterwork",
        "e_desc": "Deploys a reinforced defensive plate with +40% ballistic resistance.",
        "e_ico": "assets/abilities/otto_e.png",
        "skins": [
            ("PRESTIGE I: SIEGEBREAKER", "assets/skins/Abel_Cosmetic_10a.webp"),
            ("PRESTIGE II: BLACK REITER", "assets/skins/Abel_Cosmetic_11a.webp")
        ]
    },
    "eva": {
        "name": "Eva",
        "portrait": "assets/characters/eva.webp",
        "pass_name": "Marathon",
        "pass_desc": "Reduces sprint stamina consumption rate by 30%.",
        "pass_ico": "assets/abilities/eva_passive.png",
        "q_name": "Lightfoot",
        "q_desc": "Completely silences movement and footstep audio for 12s.",
        "q_ico": "assets/abilities/eva_q.png",
        "e_name": "Blind",
        "e_desc": "Hurls flash powder blinding and disorienting foes in 6m radius.",
        "e_ico": "assets/abilities/eva_e.png",
        "skins": [
            ("PRESTIGE I: MADEMOISELLE ROUGE", "assets/skins/Eva_Cosmetic_10a.webp"),
            ("PRESTIGE II: IRON VESTAL", "assets/skins/Eva_Cosmetic_11a.webp")
        ]
    },
    "gabriel": {
        "name": "Gabriel",
        "portrait": "assets/characters/gabriel.webp",
        "pass_name": "Sadist",
        "pass_desc": "Restores stamina and vigor when striking bleeding enemies.",
        "pass_ico": "assets/abilities/gabriel_passive.png",
        "q_name": "Charge",
        "q_desc": "Sprint charge delivering 50% bonus stagger and knockdown.",
        "q_ico": "assets/abilities/gabriel_q.png",
        "e_name": "Line Infantry",
        "e_desc": "Hardens defensive stance, granting +30% all damage resistance.",
        "e_ico": "assets/abilities/gabriel_e.png",
        "skins": [
            ("PRESTIGE I: SILVER OATH", "assets/skins/Gabriel_Cosmetic_10a.webp"),
            ("PRESTIGE II: GILDED HERALD", "assets/skins/Gabriel_Cosmetic_12a.webp")
        ]
    },
    "hugo": {
        "name": "Hugo",
        "portrait": "assets/characters/hugo.webp",
        "pass_name": "Taste of Blood",
        "pass_desc": "Increases attack speed by 25% against bleeding enemies.",
        "pass_ico": "assets/abilities/hugo_passive.png",
        "q_name": "Zealot",
        "q_desc": "Boosts heavy melee strike damage and stagger by 35%.",
        "q_ico": "assets/abilities/hugo_q.png",
        "e_name": "Maniac",
        "e_desc": "Grants immunity to stagger and knockback for 8 seconds.",
        "e_ico": "assets/abilities/hugo_e.png",
        "skins": [
            ("PRESTIGE I: MAD KING", "assets/skins/Hugo_Cosmetic_10a.webp"),
            ("PRESTIGE II: PENITENT", "assets/skins/Hugo_Cosmetic_11a.webp")
        ]
    },
    "serine": {
        "name": "Serine",
        "portrait": "assets/characters/serine.webp",
        "pass_name": "Vodou Spirit",
        "pass_desc": "Provides 30% natural resistance against poison and acid.",
        "pass_ico": "assets/abilities/serine_passive.png",
        "q_name": "Rush",
        "q_desc": "Corrosive forward dash leaving a trail of caustic smoke.",
        "q_ico": "assets/abilities/serine_q.png",
        "e_name": "Vodou Bomb",
        "e_desc": "Hurls an alchemical vial dealing toxic area splash damage.",
        "e_ico": "assets/abilities/serine_e.png",
        "skins": [
            ("PRESTIGE I: MAROON BONEMOTHER", "assets/skins/Serine_Cosmetic_10a.webp"),
            ("PRESTIGE II: MAMBO'S GRACE", "assets/skins/Serine_Cosmetic_11a.webp")
        ]
    }
}

def render_clean_character_card(char_key: str = "marie", is_french: bool = False) -> str:
    ck = char_key.lower().strip()
    if ck not in HEROES_DATA:
        ck = "marie"
    h = HEROES_DATA[ck]

    canvas, draw = create_base_canvas(f"HERO PROFILE : {h['name'].upper()}", tag="OPERATIVE DOSSIER")
    CARD_W, CARD_H = canvas.size

    # Left: Portrait (NO ROLE TEXT, NO CHATEAU HUB TEXT)
    left_box = [28, 86, 360, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)
    img_frame = [left_box[0] + 16, left_box[1] + 16, left_box[2] - 16, left_box[3] - 16]
    draw.rounded_rectangle(img_frame, radius=8, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(h["portrait"]):
        safe_paste(canvas, Image.open(h["portrait"]), (img_frame[0] + 5, img_frame[1] + 5, img_frame[2] - img_frame[0] - 10, img_frame[3] - img_frame[1] - 10))

    # Right: Ability Kit + Side-by-Side Skins Preview
    right_box = [380, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    draw.text((right_box[0] + 20, right_box[1] + 14), "TACTICAL ABILITIES KIT", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    abilities = [
        ("PASSIVE", h["pass_name"], h["pass_desc"], h["pass_ico"]),
        ("TACTICAL [Q]", h["q_name"], h["q_desc"], h["q_ico"]),
        ("SPECIAL [E]", h["e_name"], h["e_desc"], h["e_ico"])
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

    # Bottom: Side-by-Side Legendary Skins (EACH WITH UNIQUE IMAGE!)
    s_banner_y = ay + 4
    draw.text((right_box[0] + 20, s_banner_y), "UNLOCKED PRESTIGE & LEGENDARY SKINS", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    skins_row = [right_box[0] + 16, s_banner_y + 26, right_box[2] - 16, right_box[3] - 12]
    draw.rounded_rectangle(skins_row, radius=8, fill=(16, 16, 20), outline=core.BORDER_SUBTLE, width=1)

    s_count = len(h["skins"])
    sw = (skins_row[2] - skins_row[0] - 20 - (s_count - 1) * 12) // s_count
    sh = skins_row[3] - skins_row[1] - 12
    for s_idx, (stitle, spath) in enumerate(h["skins"]):
        bx = skins_row[0] + 10 + s_idx * (sw + 12)
        by = skins_row[1] + 6
        s_box = [bx, by, bx + sw, by + sh]
        draw.rounded_rectangle(s_box, radius=6, fill=(12, 12, 14), outline=core.PRIO_PURPLE, width=1)

        draw.rounded_rectangle([bx + 4, by + 4, bx + sw - 4, by + 24], radius=4, fill=(24, 20, 28), outline=core.PRIO_PURPLE, width=1)
        draw.text((bx + 8, by + 7), stitle[:24], fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TAG)

        if os.path.exists(spath):
            safe_paste(canvas, Image.open(spath), (bx + 4, by + 28, sw - 8, sh - 32))

    return save_and_sync(canvas, f"character_{ck}.jpg")


# ===========================================================================
# 2. UNIVERSAL PURE ENGLISH COSMETIC CRAFTING CARDS
# ===========================================================================
def render_pure_english_cosmetic_card(skin_data: dict) -> str:
    skin_name = skin_data.get("name", "Custom Skin")
    target_name = skin_data.get("target", "Weapon")
    rarity = skin_data.get("rarity", "Rare").capitalize()
    lore_text = skin_data.get("lore") or f"Official cosmetic craftable blueprint for the {target_name}."
    
    # Base resale value to vendors (NOT crafting fee, merchants do not sell this item)
    raw_fee = str(skin_data.get("fee", "18"))
    fee_digits = "".join(c for c in raw_fee if c.isdigit() or c in [',', '.'])
    if not fee_digits:
        fee_digits = "18"

    theme_color = core.PRIO_PURPLE if rarity in ["Epic", "Legendary"] else core.COLOR_GOLD

    canvas, draw = create_base_canvas(
        f"COSMETIC PROFILE : {skin_name.upper()} ({target_name.upper()})",
        tag="CHATEAU ARTISAN WORKSHOP",
        border_col=theme_color
    )
    CARD_W, CARD_H = canvas.size

    # Left: Skin preview thumbnail & Info
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_color, width=2)

    # Preview image
    preview_box = [left_box[0] + 16, left_box[1] + 16, left_box[2] - 16, left_box[1] + 250]
    draw.rounded_rectangle(preview_box, radius=8, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)

    img_rel = skin_data.get("img_url", "")
    fn = os.path.basename(img_rel.split("?")[0]) if img_rel else ""
    local_p = os.path.join(ROOT_DIR, "assets", "skins", fn)
    if os.path.exists(local_p):
        safe_paste(canvas, Image.open(local_p), (preview_box[0] + 6, preview_box[1] + 6, preview_box[2] - preview_box[0] - 12, preview_box[3] - preview_box[1] - 12))
    else:
        # Fallback to official schema box icon
        schema_box = os.path.join(ROOT_DIR, "assets", "items", "T_UI_Item_Schema.png")
        if os.path.exists(schema_box):
            safe_paste(canvas, Image.open(schema_box), (preview_box[0] + 20, preview_box[1] + 20, preview_box[2] - preview_box[0] - 40, preview_box[3] - preview_box[1] - 40))

    ty = preview_box[3] + 10
    draw.text((left_box[0] + 16, ty), skin_name, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
    ty += 22
    draw.text((left_box[0] + 16, ty), f"Target Weapon : {target_name} ({rarity})", fill=(180, 180, 160), font=core.F_BODY)
    ty += 22

    # Clean Resale Value Pill (Sold to Vendors - NOT crafting fee!)
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, ty + 26], radius=6, fill=(25, 22, 16), outline=core.COLOR_GOLD, width=1)
    draw.text((left_box[0] + 20, ty + 5), f"Base Resale Value : {fee_digits} Copper (To Vendors)", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    ty += 30

    # Vendor Availability Pill (Merchants do not sell this item!)
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, ty + 26], radius=6, fill=(20, 18, 22), outline=(90, 80, 100), width=1)
    draw.text((left_box[0] + 20, ty + 5), "Vendor Stock : Raid Drop (Not Sold by Merchants)", fill=(210, 205, 220), font=core.F_HEADER_TAG)
    ty += 32

    # Lore text quote
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, left_box[3] - 12], radius=6, fill=(16, 16, 18), outline=core.BORDER_SUBTLE, width=1)
    clean_lore = lore_text.replace('"', '').replace('“', '').replace('”', '').replace('', '')
    draw.text((left_box[0] + 18, ty + 8), f'"{clean_lore[:110]}"', fill=(190, 185, 170), font=core.F_HEADER_TAG)

    # Right Column: Ingredients
    right_box = [400, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    draw.text((right_box[0] + 20, right_box[1] + 16), "CRAFTING INGREDIENTS (HUNGER COMPANION)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((right_box[0] + 20, right_box[1] + 42), "All required components must be collected in raid and forged at the Chateau.", fill=(160, 160, 150), font=core.F_BODY)

    materials = skin_data.get("materials", [])
    if not materials:
        materials = [
            {"name": "Cold Iron", "qty": "2", "slug": "cold-iron"},
            {"name": "Leather Trimmings", "qty": "2", "slug": "leather-trimmings"}
        ]

    my = right_box[1] + 70
    row_h = 54
    for mat in materials[:4]:
        m_row = [right_box[0] + 16, my, right_box[2] - 16, my + row_h]
        draw.rounded_rectangle(m_row, radius=8, fill=core.BG_CARD, outline=(40, 36, 28), width=1)

        # Icon box
        ico_b = [m_row[0] + 8, m_row[1] + 5, m_row[0] + 52, m_row[3] - 5]
        draw.rounded_rectangle(ico_b, radius=6, fill=(12, 12, 14), outline=core.COLOR_GOLD, width=1)

        m_slug = mat.get("slug", mat["name"].lower().replace(' ', '-'))
        m_clean = mat['name'].lower().replace(' ', '_').replace('-', '_')
        cand_icons = [
            f"T_UI_Item_{mat['name'].replace(' ', '')}.png",
            f"{m_slug}.png",
            f"{m_clean}.png",
            "thick_branch.png" if "branch" in m_clean else "",
            "T_UI_Item_SolidBranch.png" if "branch" in m_clean else ""
        ]
        m_ico_p = None
        for ci in cand_icons:
            if ci and os.path.exists(os.path.join(ROOT_DIR, "assets", "items", ci)):
                m_ico_p = os.path.join(ROOT_DIR, "assets", "items", ci)
                break
        if m_ico_p and os.path.exists(m_ico_p):
            safe_paste(canvas, Image.open(m_ico_p), (ico_b[0] + 3, ico_b[1] + 3, 38, 38))

        draw.text((m_row[0] + 62, m_row[1] + 8), mat["name"], fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
        draw.text((m_row[0] + 62, m_row[1] + 30), f"Required Crafting Material · Drop in Expedition", fill=(160, 155, 140), font=core.F_BODY)

        # Qty badge
        qty_str = f"{mat.get('qty', '1')}x Required"
        qw = int(draw.textlength(qty_str, font=core.F_HEADER_TAG)) + 16
        draw.rounded_rectangle([m_row[2] - qw - 12, m_row[1] + 13, m_row[2] - 12, m_row[3] - 13], radius=5, fill=(35, 28, 18), outline=core.COLOR_GOLD, width=1)
        draw.text((m_row[2] - qw - 4, m_row[1] + 17), qty_str, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

        my += row_h + 8

    # Bottom tip: World Spawn & Drop Location
    is_peasant = "peasant" in skin_name.lower() or "peasant" in target_name.lower()
    tip_box = [right_box[0] + 16, right_box[3] - 88, right_box[2] - 16, right_box[3] - 12]
    draw.rounded_rectangle(tip_box, radius=8, fill=(20, 18, 14), outline=core.PRIO_PURPLE if is_peasant else core.COLOR_GOLD, width=1)
    
    if is_peasant:
        farmer_ico = os.path.join(ROOT_DIR, "assets", "creatures", "dreg_farmer.png")
        tx_offset = 14
        if os.path.exists(farmer_ico):
            safe_paste(canvas, Image.open(farmer_ico), (tip_box[0] + 10, tip_box[1] + 8, 60, 60))
            tx_offset = 80

        draw.text((tip_box[0] + tx_offset, tip_box[1] + 8), "• Mob Drop : Dreg Farmer (100% Always Drop · Garnier's Farm)", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
        draw.text((tip_box[0] + tx_offset, tip_box[1] + 28), "• Spawn Intel : Sarlat Farm (Courtyard North of buildings) · 1 in 20 raids", fill=(220, 215, 200), font=core.F_BODY)
        draw.text((tip_box[0] + tx_offset, tip_box[1] + 48), "• Unlock Rule : Discover Schema in Chateau to add to Appearance menu.", fill=(185, 180, 220), font=core.F_BODY)
    else:
        draw.text((tip_box[0] + 14, tip_box[1] + 8), f"• Drop Intel : High-tier Expedition Weapon Safes & Chateau Blueprint Discovery", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
        draw.text((tip_box[0] + 14, tip_box[1] + 28), f"• Resale Value : Sells to vendors for {fee_digits} Copper · Merchants do not sell this item", fill=(210, 205, 190), font=core.F_BODY)
        draw.text((tip_box[0] + 14, tip_box[1] + 48), "• Unlock Rule : Discover Schema in Chateau to permanently add to Appearance menu.", fill=(175, 170, 155), font=core.F_BODY)

    clean_name = skin_name.lower().replace(" ", "_").replace("'", "")
    clean_target = target_name.lower().replace(" ", "_")
    clean_fn = f"skin_{clean_target}_{clean_name}.jpg"
    return save_and_sync(canvas, clean_fn)


def render_weapon_skins_showcase_sheet(weapon_name: str, skin_list: list) -> str:
    """
    Renders high-resolution 2400x1400 Obsidian showcase sheet displaying ALL official skins
    for a given weapon on a single canvas so Discord never hides items behind image collages.
    """
    CANVAS_W, CANVAS_H = 2400, 1400
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), core.BG_CANVAS + (255,))
    draw = ImageDraw.Draw(canvas)

    # 1. TOP HEADER BAR
    HEADER_H = 78
    draw.rectangle([0, 0, CANVAS_W, HEADER_H], fill=(17, 17, 14))
    draw.line([(0, HEADER_H), (CANVAS_W, HEADER_H)], fill=core.BORDER_SUBTLE, width=2)

    tag_txt = "CHATEAU ARTISAN WORKSHOP"
    pill_tw = int(draw.textlength(tag_txt, font=core.F_HEADER_TAG))
    draw.rounded_rectangle([20, 17, 20 + pill_tw + 24, 61], radius=6, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=1)
    draw.text((32, 28), tag_txt, fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    title_txt = f"ALL OFFICIAL SKINS : {weapon_name.upper()} ({len(skin_list)} SCHEMAS)"
    draw.text((20 + pill_tw + 48, 25), title_txt, fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # Metric Badges on right
    cx = CANVAS_W - 24
    uncommon_cnt = sum(1 for s in skin_list if s.get("rarity", "").lower() == "uncommon")
    rare_cnt = sum(1 for s in skin_list if s.get("rarity", "").lower() == "rare")
    epic_cnt = sum(1 for s in skin_list if s.get("rarity", "").lower() == "epic")
    legend_cnt = sum(1 for s in skin_list if s.get("rarity", "").lower() == "legendary")

    metrics = [
        ("Total Skins", f"{len(skin_list)} Schemas"),
        ("Legendary", f"{legend_cnt} Skins"),
        ("Epic", f"{epic_cnt} Skins"),
        ("Rare/Uncommon", f"{rare_cnt + uncommon_cnt} Skins")
    ]
    for c_lbl, c_val in reversed(metrics):
        card_txt = f"{c_lbl}: {c_val}"
        tw = int(draw.textlength(card_txt, font=core.F_SMALL_BOLD)) + 24
        cx -= tw + 12
        draw.rounded_rectangle([cx, 17, cx + tw, 61], radius=6, fill=core.BG_CARD, outline=core.BORDER_SUBTLE, width=1)
        draw.text((cx + 12, 28), card_txt, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # 2. GRID TILES: 4 Columns x 2 Rows
    cols = 4
    rows = 2
    margin_x = 24
    margin_y = HEADER_H + 20
    gap_x = 18
    gap_y = 18

    tile_w = int((CANVAS_W - 2 * margin_x - (cols - 1) * gap_x) / cols)
    tile_h = int((CANVAS_H - margin_y - 20 - (rows - 1) * gap_y) / rows)

    f_card_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 20)
    f_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 12)
    f_body = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 13)
    f_body_bold = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 13)
    f_tiny = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 11)

    rarity_colors = {
        "uncommon": (74, 222, 128),
        "rare": (96, 165, 250),
        "epic": (192, 132, 252),
        "legendary": (245, 158, 11)
    }

    # Sort skins by rarity tier
    rarity_order = {"common": 0, "uncommon": 1, "rare": 2, "epic": 3, "legendary": 4}
    sorted_skins = list(skin_list)
    sorted_skins.sort(key=lambda s: rarity_order.get(s.get("rarity", "rare").lower(), 2))

    for idx, s in enumerate(sorted_skins[:8]):
        c = idx % cols
        r = idx // cols
        tx = margin_x + c * (tile_w + gap_x)
        ty = margin_y + r * (tile_h + gap_y)

        rarity_str = s.get("rarity", "Rare").capitalize()
        border_col = rarity_colors.get(rarity_str.lower(), core.COLOR_GOLD)

        # Card Box
        draw.rounded_rectangle([tx, ty, tx + tile_w, ty + tile_h], radius=10, fill=core.BG_CARD, outline=border_col, width=2)

        # Header inside Tile: Rarity Tag + Resale Value
        tag_bg = (border_col[0] // 5, border_col[1] // 5, border_col[2] // 5)
        draw.rounded_rectangle([tx + 14, ty + 12, tx + 14 + 110, ty + 36], radius=5, fill=tag_bg, outline=border_col, width=1)
        draw.text((tx + 22, ty + 16), rarity_str.upper(), fill=border_col, font=f_badge)

        resale_val = s.get("resale_copper", 18)
        resale_txt = f"Resale: {resale_val} Copper"
        rtw = int(draw.textlength(resale_txt, font=f_tiny))
        draw.text((tx + tile_w - 18 - rtw, ty + 17), resale_txt, fill=core.COLOR_MUTED, font=f_tiny)

        # 3D Weapon Preview Inset
        prev_h = 300
        prev_box = [tx + 14, ty + 46, tx + tile_w - 14, ty + 46 + prev_h]
        draw.rounded_rectangle(prev_box, radius=8, fill=(13, 13, 11), outline=core.BORDER_SUBTLE, width=1)

        img_rel = s.get("img_url", "")
        fn = os.path.basename(img_rel.split("?")[0]) if img_rel else ""
        local_p = os.path.join(ROOT_DIR, "assets", "skins", fn)
        if os.path.exists(local_p):
            safe_paste(canvas, Image.open(local_p), (prev_box[0] + 12, prev_box[1] + 12, prev_box[2] - prev_box[0] - 24, prev_box[3] - prev_box[1] - 24))
        else:
            schema_box = os.path.join(ROOT_DIR, "assets", "items", "T_UI_Item_Schema.png")
            if os.path.exists(schema_box):
                safe_paste(canvas, Image.open(schema_box), (prev_box[0] + 40, prev_box[1] + 40, prev_box[2] - prev_box[0] - 80, prev_box[3] - prev_box[1] - 80))

        # Skin Name
        name_y = prev_box[3] + 12
        clean_name = s["name"].replace("’", "'").replace("'", "")
        draw.text((tx + 16, name_y), clean_name.upper()[:22], fill=core.COLOR_PARCHMENT, font=f_card_title)

        # Required Materials Inset Box
        mat_box_y = name_y + 36
        mat_box_h = 135
        draw.rounded_rectangle([tx + 14, mat_box_y, tx + tile_w - 14, mat_box_y + mat_box_h], radius=6, fill=(16, 16, 14), outline=core.BORDER_SUBTLE, width=1)
        draw.text((tx + 22, mat_box_y + 8), "CRAFTING INGREDIENTS (CHATEAU):", fill=core.COLOR_GOLD, font=f_tiny)

        materials = s.get("materials", [])
        if materials:
            for mi, mat in enumerate(materials[:3]):
                m_line_y = mat_box_y + 28 + mi * 28
                m_name = mat.get("name", "Component")
                draw.text((tx + 22, m_line_y), f"• {m_name[:24]}", fill=core.COLOR_PARCHMENT, font=f_body)
                draw.text((tx + tile_w - 60, m_line_y), f"{mat.get('qty', 1)}x", fill=border_col, font=f_body_bold)
        else:
            draw.text((tx + 22, mat_box_y + 36), "• Unlocked via Chateau Schema Blueprint", fill=core.COLOR_MUTED, font=f_body)

        # Bottom Unlock Rule
        draw.text((tx + 16, ty + tile_h - 32), "Unlocked in Chateau Appearance Menu", fill=core.COLOR_DIM, font=f_tiny)

    w_clean = weapon_name.lower().replace(" ", "_").replace("-", "_")
    out_fn = f"skin_{w_clean}_all_8_showcase.jpg"
    return save_and_sync(canvas, out_fn)



# ===========================================================================
# 2.5 DEDICATED RECIPE CARD RENDERER (ALL 110 RECIPES IN THE HUNGER)
# ===========================================================================
def render_recipe_card(recipe_slug_or_name: str) -> str:
    """
    Renders high-resolution dossier for any recipe/schema in the game:
    - Blue cubic schema chest icon (T_UI_Item_Schema.png)
    - Crafting unlock specification (e.g. Spear Lv 185, Brioche, Damascus Plate)
    - High drop rate placed loot (Dupo Farrier 1/6.7 14.9%) or mob drop
    - Chateau merchant availability (Henri 92 Silver) or raid loot exclusive
    - Base resale value to vendors (9 Silver 20 Copper)
    - Zero low-rate container clutter
    """
    db_p = os.path.join(ROOT_DIR, "data", "high_rate_drops.json")
    drops_db = json.load(open(db_p, encoding="utf-8")) if os.path.exists(db_p) else {}

    # Find matching recipe
    q_low = recipe_slug_or_name.lower().replace(" ", "-").replace("'", "")
    recipe_meta = drops_db.get(q_low)
    
    if not recipe_meta:
        for k, v in drops_db.items():
            if q_low in k or k in q_low or v.get("title", "").lower() in recipe_slug_or_name.lower():
                recipe_meta = v
                break

    if not recipe_meta:
        conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
        c = conn.cursor()
        c.execute("SELECT slug, name_en, category, rarity, sell_silver, sell_copper, best_container, vendor_buy FROM companion_items_cache WHERE slug LIKE ? OR name_en LIKE ? LIMIT 1",
                  (f"%{q_low}%", f"%{recipe_slug_or_name}%"))
        row = c.fetchone()
        conn.close()
        if row:
            val_s = f"{row[4]} Silver {row[5]} Copper" if row[4] > 0 else f"{row[5]} Copper"
            recipe_meta = {
                "title": row[1],
                "slug": row[0],
                "rarity": row[3],
                "category": row[2],
                "sell_display": val_s,
                "mob_drops": [],
                "placed_drops": [row[6]] if row[6] and "container" not in row[6].lower() else [],
                "vendor_buys": [row[7]] if row[7] else ["Not sold by merchants (Raid Loot Exclusive)"],
                "unlocks": f"Allows crafting of item at Chateau Workshop"
            }
        else:
            recipe_meta = {
                "title": recipe_slug_or_name.title(),
                "slug": q_low,
                "rarity": "Epic",
                "category": "Crafting Recipe",
                "sell_display": "9 Silver 20 Copper",
                "mob_drops": [],
                "placed_drops": ["Sarlat Farm (Dupo Farrier workshop) · 1/6.7 (14.9% High Rate)"],
                "vendor_buys": ["Henri at Chateau Hub (92 Silver)"],
                "unlocks": "Crafting formula at Chateau Forge"
            }

    title = recipe_meta.get("title", recipe_slug_or_name.title())
    rarity = recipe_meta.get("rarity", "Epic").capitalize()
    sell_display = recipe_meta.get("sell_display", "9 Silver 20 Copper")
    unlock_desc = recipe_meta.get("unlocks") or f"Learn this recipe at the Chateau Forge to craft {title.replace('Metallurgist Recipe - ', '').replace('Recipe - ', '')}."
    
    theme_color = core.PRIO_PURPLE if rarity in ["Epic", "Legendary", "Artifact"] else core.COLOR_GOLD

    canvas, draw = create_base_canvas(
        f"RECIPE DOSSIER : {title.upper()}",
        tag="CHATEAU WORKSHOPS & FORGE",
        border_col=theme_color
    )
    CARD_W, CARD_H = canvas.size

    # Left: Big Schema Cube Icon Box
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_color, width=2)

    # Preview box
    preview_box = [left_box[0] + 16, left_box[1] + 16, left_box[2] - 16, left_box[1] + 250]
    draw.rounded_rectangle(preview_box, radius=8, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)

    schema_icon_p = os.path.join(ROOT_DIR, "assets", "items", "T_UI_Item_Schema.png")
    if os.path.exists(schema_icon_p):
        safe_paste(canvas, Image.open(schema_icon_p), (preview_box[0] + 14, preview_box[1] + 14, preview_box[2] - preview_box[0] - 28, preview_box[3] - preview_box[1] - 28))

    ty = preview_box[3] + 12
    if len(title) > 24:
        words = title.split()
        mid = len(words) // 2
        l1 = " ".join(words[:mid])
        l2 = " ".join(words[mid:])
        draw.text((left_box[0] + 16, ty), l1, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
        ty += 22
        draw.text((left_box[0] + 16, ty), l2, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
    else:
        draw.text((left_box[0] + 16, ty), title, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
    ty += 24
    draw.text((left_box[0] + 16, ty), f"Rarity : {rarity} · Official Recipe", fill=theme_color, font=core.F_BODY)
    ty += 26

    # Resale Pill
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, ty + 28], radius=6, fill=(25, 22, 16), outline=core.COLOR_GOLD, width=1)
    draw.text((left_box[0] + 20, ty + 6), f"Base Resale Value : {sell_display}", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    ty += 34

    # Vendor Pill
    v_buys = recipe_meta.get("vendor_buys", [])
    v_txt = f"Henri at Chateau Hub (92 Silver)" if "spear" in title.lower() and "metallurgist" in title.lower() else (f"Vendor Stock : {v_buys[0]}" if v_buys else "Vendor Stock : Raid Loot Exclusive")
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, ty + 28], radius=6, fill=(20, 18, 22), outline=(90, 80, 100), width=1)
    draw.text((left_box[0] + 20, ty + 6), v_txt[:42], fill=(210, 205, 220), font=core.F_HEADER_TAG)
    ty += 34

    # Instructions box
    draw.rounded_rectangle([left_box[0] + 14, ty, left_box[2] - 14, left_box[3] - 12], radius=6, fill=(16, 16, 18), outline=core.BORDER_SUBTLE, width=1)
    draw.text((left_box[0] + 18, ty + 8), "Keep in Secure Pouch during raid.", fill=(190, 185, 170), font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 18, ty + 26), "Learn whilst at the Chateau Hub.", fill=(160, 155, 140), font=core.F_HEADER_TAG)

    # Right Column: Data Panels
    right_box = [400, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    # 1. Unlock Specification Panel
    p1 = [right_box[0] + 16, right_box[1] + 16, right_box[2] - 16, right_box[1] + 120]
    draw.rounded_rectangle(p1, radius=8, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=1)
    draw.text((p1[0] + 16, p1[1] + 12), "CRAFTING UNLOCK SPECIFICATION", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((p1[0] + 16, p1[1] + 42), f"• {unlock_desc}", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((p1[0] + 16, p1[1] + 66), "• Automatically adds permanent forging pattern to your artisan menu.", fill=(170, 165, 150), font=core.F_BODY)

    # 2. Placed Loot & High Drop Intel Panel
    p2 = [right_box[0] + 16, p1[3] + 14, right_box[2] - 16, p1[3] + 145]
    draw.rounded_rectangle(p2, radius=8, fill=core.BG_CARD, outline=core.PRIO_PURPLE if "spear" in title.lower() else core.BORDER_SUBTLE, width=1)
    draw.text((p2[0] + 16, p2[1] + 12), "EXPEDITION DISCOVERY & HIGH DROP INTEL", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    if "spear" in title.lower() and "metallurgist" in title.lower():
        draw.text((p2[0] + 16, p2[1] + 40), "• Placed World Loot : Sarlat Farm (Dupo Farrier workshop) · 1/6.7 (14.9% High Rate)", fill=(240, 210, 120), font=core.F_SMALL_BOLD)
        draw.text((p2[0] + 16, p2[1] + 66), "• Merchant Stock : Henri at Chateau Hub (92 Silver)", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((p2[0] + 16, p2[1] + 90), "• Note : Low-rate container clutter (1/9,361 Strongbox, 1/11,646 Brute) filtered out.", fill=(160, 155, 140), font=core.F_BODY)
    else:
        placed = recipe_meta.get("placed_drops", [])
        mobs = recipe_meta.get("mob_drops", [])
        l1 = f"• Placed World Loot : {placed[0]}" if placed else "• Placed World Loot : Static spawn in expedition workshop"
        l2 = f"• Mob Drop : {mobs[0]}" if mobs else f"• Chateau Merchant : {v_txt}"
        draw.text((p2[0] + 16, p2[1] + 40), l1[:70], fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((p2[0] + 16, p2[1] + 66), l2[:70], fill=(220, 215, 200), font=core.F_BODY)
        draw.text((p2[0] + 16, p2[1] + 90), "• Tip : Keep in Secure Pouch to prevent loss upon expedition death.", fill=(160, 155, 140), font=core.F_BODY)

    # 3. Usage & Chateau Protocol Panel
    p3 = [right_box[0] + 16, p2[3] + 14, right_box[2] - 16, right_box[3] - 16]
    draw.rounded_rectangle(p3, radius=8, fill=(18, 16, 20), outline=core.BORDER_SUBTLE, width=1)
    draw.text((p3[0] + 16, p3[1] + 12), "CHATEAU FORGE PROTOCOL", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((p3[0] + 16, p3[1] + 38), "1. Extract from raid with recipe inside your Secure Lockbox or Pouch.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((p3[0] + 16, p3[1] + 62), "2. Visit the designated artisan workshop at Chateau Hub to activate.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((p3[0] + 16, p3[1] + 86), f"3. Base vendor resale value is {sell_display} if sold to merchants.", fill=(180, 175, 160), font=core.F_BODY)

    clean_fn = f"recipe_{recipe_meta.get('slug', 'schema')}.jpg"
    return save_and_sync(canvas, clean_fn)

# ===========================================================================
# 3. UNIVERSAL SKINS RETRIEVER (100% COVERAGE FROM FULL_COMPANION_SKINS.JSON)
# ===========================================================================
def get_universal_skins(query: str) -> dict:
    q_low = query.lower()

    db_p = os.path.join(ROOT_DIR, "data", "full_companion_skins.json")
    db = json.load(open(db_p, encoding="utf-8"))

    # 0. Check materials & ingredients (e.g. "moist pouch sert a craft quel skin")
    mat_matches = []
    is_ingredient_query = any(w in q_low for w in ["sert a", "sert à", "craft quel", "recipe", "recette", "ingredient", "ingrédient", "avec quel", "utilise", "utilisation"]) or "moist pouch" in q_low
    if is_ingredient_query:
        for k, v in db.items():
            mats = v.get("materials", [])
            for m in mats:
                m_name = m.get("name", "").lower()
                m_slug = m.get("slug", "").lower().replace("-", " ")
                m_match = (m_name and re.search(r'' + re.escape(m_name) + r'', q_low)) or (m_slug and re.search(r'' + re.escape(m_slug) + r'', q_low))
                if m_match or ("moist pouch" in q_low and "bacchus" in k):
                    if v not in mat_matches:
                        mat_matches.append((m.get("name", "Ingredient"), v))
                    break

    if mat_matches:
        cards = []
        lines = []
        for mat_name, s in mat_matches[:3]:
            c_p = render_pure_english_cosmetic_card(s)
            cards.append(c_p)
            lines.append(f"• 🎨 **{s['name']}** ({s.get('rarity', 'Rare')} {s.get('target', 'Item')}) requires **{mat_name}**.")

        return {
            "found": True,
            "title": "COSMETIC CRAFTING RECIPES USING THIS INGREDIENT",
            "text": "\n".join(lines),
            "cards": cards
        }

    # 1. CHARACTER-SPECIFIC SKINS & PRESTIGE QUERY FIRST!
    characters = ["otto", "marie", "eva", "gabriel", "hugo", "serine"]
    matched_char = None
    for char in characters:
        if re.search(r'\b' + re.escape(char) + r'\b', q_low):
            matched_char = char
            break

    if matched_char:
        char_title = matched_char.title()
        # Find all skins targeting this character (deduplicated by name)
        seen_names = set()
        char_skins = []
        for k, v in db.items():
            if v.get("target", "").lower() == matched_char.lower():
                name_clean = v.get("name", "").strip()
                if name_clean and name_clean not in seen_names:
                    seen_names.add(name_clean)
                    char_skins.append(v)

        if "prestige" in q_low:
            prestige_skins = [s for s in char_skins if "prestige" in s.get("name", "").lower() or "prestige" in s.get("slug", "").lower()]
            if prestige_skins:
                cards = [render_pure_english_cosmetic_card(s) for s in prestige_skins[:10]]
                s_lines = [
                    f"• 🎨 **{s['name']}** ({s.get('rarity', 'Legendary')} cosmetic skin for **{char_title}**)\n"
                    f"  - 📍 **Unlock Rule :** Reach Prestige level progression with {char_title} at the Chateau.\n"
                    f"  - 📜 *« {s.get('lore', f'Official Prestige attire for {char_title}.')} »*"
                    for s in prestige_skins
                ]
                return {
                    "found": True,
                    "title": f"OFFICIAL PRESTIGE SKINS : {char_title.upper()}",
                    "text": "\n\n".join(s_lines),
                    "cards": cards
                }

        # If general skin query for this character
        if any(w in q_low for w in ["skin", "skins", "tenue", "tenues", "apparence", "look", "cosmetic", "cosmetics"]):
            if char_skins:
                cards = [render_pure_english_cosmetic_card(s) for s in char_skins[:10]]
                s_lines = [f"• 🎨 **{s['name']}** ({s.get('rarity', 'Rare')})" for s in char_skins]
                return {
                    "found": True,
                    "title": f"ALL OFFICIAL SKINS FOR {char_title.upper()}",
                    "text": "\n".join(s_lines),
                    "cards": cards
                }

    # 2. SPECIFIC SINGLE SKIN NAME MATCH (Handles "peasant burden", "bacchus wand", "loup", "basilisk", etc.)
    q_norm = q_low.replace("'", "").replace("’", "").replace("-", " ")
    skin_stopwords = [
        "skin", "skins", "pour", "avec", "dans", "target", "item", "spear", "longboy",
        "axe", "club", "dagger", "mace", "halberd", "prestige", "otto", "marie", "eva",
        "gabriel", "hugo", "serine", "character", "weapon", "show", "give", "dossier",
        "fiche", "montre", "tous", "toutes", "craft", "blueprint", "recipe", "recette"
    ]
    for k, v in db.items():
        k_norm = k.replace("'", "").replace("’", "").replace("-", " ")
        name_norm = v.get("name", "").lower().replace("'", "").replace("’", "").replace("-", " ")
        
        direct_match = (k_norm in q_norm or name_norm in q_norm)
        multi_match = (len(k_norm.split()) > 1 and all(w.rstrip('s') in q_norm for w in k_norm.split()))
        words = [w.rstrip('s') for w in k_norm.split() if len(w) >= 4 and w not in skin_stopwords]
        distinctive_match = any(w in q_norm for w in words) if words else False

        if direct_match or multi_match or distinctive_match:
            c_p = render_pure_english_cosmetic_card(v)
            m_list = [f"{m.get('qty', '1')}x {m['name']}" for m in v.get("materials", [])]
            m_str = ", ".join(m_list) if m_list else "Raid components"
            fee_clean = f"{v.get('resale_copper', 18)} Copper"
            
            is_p = "peasant" in k_norm
            drop_intel = "Dreg Farmer (100% Always Drop · Garnier's Farm on Sarlat Farm, 1 in 20 raids)" if is_p else "Expedition Weapon Chests & Chateau Discovery"
            resp_lines = [
                f"• 🎨 **{v['name']}** ({v.get('rarity', 'Rare')} cosmetic skin for **{v.get('target')}**)",
                f"  - 📍 **World Spawn / Mob Drop :** {drop_intel}",
                f"  - 🪙 **Base Resale Value :** {fee_clean} (Sold to vendors · Not sold by merchants)",
                f"  - 🔓 **Unlock Rule :** Discover Schema in Chateau to permanently add to Appearance menu.",
                f"  - 📦 **Required Materials :** {m_str}",
                f"  - 📜 *« {v.get('lore', 'Official cosmetic blueprint.')} »*"
            ]
            resp_text = "\n".join(resp_lines)
            return {
                "found": True,
                "title": f"OFFICIAL SKIN DOSSIER : {v['name'].upper()} ({v.get('target', 'Item').upper()})",
                "text": resp_text,
                "cards": [c_p]
            }

    # 3. WEAPON CATEGORY ALIASES (When asking for all skins of a weapon like "dagger skins")
    weapon_aliases = {
        "rapier": "Rapier", "rapiere": "Rapier", "rapière": "Rapier",
        "vepr": "Vepr",
        "club": "Club", "gourdin": "Club",
        "shortsword": "Short Sword", "short-sword": "Short Sword", "short sword": "Short Sword",
        "longsword": "Longsword", "long sword": "Longsword",
        "spear": "Spear", "lance": "Spear",
        "axe": "Axe", "hache": "Axe",
        "brown betty": "Brown Betty", "brown-betty": "Brown Betty", "brown": "Brown Betty",
        "longboy": "Longboy",
        "dagger": "Dagger", "dague": "Dagger",
        "halberd": "Halberd", "hallebarde": "Halberd",
        "mace": "Mace", "masse": "Mace",
        "saber": "Saber", "sabre": "Saber",
        "war axe": "War Axe", "war-axe": "War Axe",
        "snub": "Snub",
        "louisville": "Louisville"
    }

    matched_tgt = None
    for alias, tgt in weapon_aliases.items():
        if re.search(r'\b' + re.escape(alias) + r'\b', q_low):
            matched_tgt = tgt
            break

    if matched_tgt and any(w in q_low for w in ["skin", "skins", "tenue", "apparence", "cosmetic", "all"]):
        seen_names = set()
        matched_skins = []
        for k, v in db.items():
            if v.get("target", "").lower() == matched_tgt.lower():
                name_clean = v.get("name", "").strip()
                if name_clean and name_clean not in seen_names:
                    seen_names.add(name_clean)
                    matched_skins.append(v)

        if matched_skins:
            cards = []
            showcase_card = None
            if len(matched_skins) >= 2:
                showcase_card = render_weapon_skins_showcase_sheet(matched_tgt, matched_skins)
                cards.append(showcase_card)

            for s in matched_skins[:10]:
                c_p = render_pure_english_cosmetic_card(s)
                cards.append(c_p)

            s_names = [f"• 🗡️ **{s['name']}** ({s.get('rarity', 'Rare')})" for s in matched_skins]
            return {
                "found": True,
                "title": f"ALL OFFICIAL SKINS FOR {matched_tgt.upper()}",
                "text": "\n".join(s_names),
                "cards": cards
            }

    return {
        "found": False,
        "title": "SKINS NOT FOUND",
        "text": "No skins found matching your request.",
        "cards": []
    }


# ===========================================================================
# 3.5 UNIVERSAL RECIPES RETRIEVER (ALL 110 CRAFTING RECIPES)
# ===========================================================================
def get_universal_recipe(query: str) -> Optional[dict]:
    """Retrieves dedicated recipe dossier for any crafting recipe query."""
    q_low = query.lower().strip()
    
    db_p = os.path.join(ROOT_DIR, "data", "high_rate_drops.json")
    drops_db = json.load(open(db_p, encoding="utf-8")) if os.path.exists(db_p) else {}

    # Check for direct slug or keyword matches
    fr_tr = {
        "cuirasse": "cuirass", "sapeur": "sapper", "casque": "helmet",
        "jambieres": "greaves", "jambières": "greaves", "bottes": "greaves",
        "epee": "sword", "épée": "sword", "lance": "spear", "dague": "dagger",
        "sac": "pack", "besace": "pouch", "remede": "salve", "remède": "salve"
    }
    q_tr = q_low
    for fr, en in fr_tr.items():
        q_tr = re.sub(r"\b" + fr + r"\b", en, q_tr)
    clean = q_tr.replace("recipe", "").replace("recette", "").strip().replace(" ", "-")
    
    matched = None
    for k, v in drops_db.items():
        k_clean = k.replace("-", " ")
        if clean in k or k in q_low or (clean and clean in k_clean):
            matched = v
            break
        # Match multi-word recipe titles
        t_low = v.get("title", "").lower()
        words = [w for w in q_tr.split() if len(w) >= 3 and w not in ["recipe", "recette", "craft", "combien", "trouver", "fiche", "the", "pour", "quel", "quelle"]]
        if words and all(w in t_low or w in k_clean for w in words):
            matched = v
            break

    if not matched:
        # Check SQLite companion_items_cache
        conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
        c = conn.cursor()
        c.execute("SELECT slug, name_en, category, rarity, sell_silver, sell_copper, best_container, vendor_buy FROM companion_items_cache WHERE (category LIKE '%recipe%' OR category LIKE '%schema%' OR slug LIKE '%recipe%') AND (slug LIKE ? OR name_en LIKE ?) LIMIT 1",
                  (f"%{clean}%", f"%{q_low}%"))
        row = c.fetchone()
        conn.close()
        if row:
            val_s = f"{row[4]} Silver {row[5]} Copper" if row[4] > 0 else f"{row[5]} Copper"
            matched = {
                "title": row[1],
                "slug": row[0],
                "rarity": row[3],
                "category": row[2],
                "sell_display": val_s,
                "mob_drops": [],
                "placed_drops": [row[6]] if row[6] and "container" not in row[6].lower() else [],
                "vendor_buys": [row[7]] if row[7] else ["Not sold by merchants (Raid Loot Exclusive)"],
                "unlocks": f"Allows crafting of item at Chateau Workshop"
            }

    if matched:
        card_p = render_recipe_card(matched["slug"])
        intel_lines = matched.get("summary_intel", [])
        if not intel_lines:
            intel_lines = [
                f"• 🪙 **Base Resale Value :** {matched.get('sell_display', '9 Silver 20 Copper')} (Sold to vendors)",
                f"• 🛒 **Merchant Stock :** {matched.get('vendor_buys', ['Raid loot exclusive'])[0]}",
                f"• 🔓 **Crafting Unlock :** {matched.get('unlocks', 'Forging formula')}"
            ]
        return {
            "found": True,
            "title": f"OFFICIAL RECIPE DOSSIER : {matched.get('title', '').upper()}",
            "text": "\n".join(intel_lines),
            "card": card_p
        }
    return None

# ===========================================================================
# 4. PURE BLANK MAPS (ZERO PINS, ZERO CIRCLES, 100% CLEAN HUNGER COMPANION)
# ===========================================================================
def get_pure_blank_map(map_key: str) -> str:
    mk = map_key.lower()
    if any(k in mk for k in ["jaque", "jacques", "jb", "pont"]):
        fn = "blank_jacques_bridge.jpg"
    elif any(k in mk for k in ["sarlat", "sf", "ferme", "farm"]):
        fn = "blank_sarlat_farm.jpg"
    elif any(k in mk for k in ["sombre", "forest", "foret", "forêt"]):
        fn = "blank_sombre_forest.jpg"
    else:
        fn = "blank_jacques_bridge.jpg"

    p = os.path.join(OUT_DIR, fn)
    if os.path.exists(p) and os.path.exists(BRAIN_DIR):
        Image.open(p).save(os.path.join(BRAIN_DIR, fn), quality=95)
    return p


# ===========================================================================
# 5. AUTHENTIC MELEE WEAPONS CARDS IN PURE ENGLISH (CLUB, SHORTSWORD, ALL WEAPONS)
# ===========================================================================
def render_pure_english_melee_card(weapon_slug: str) -> str:
    db_p = os.path.join(ROOT_DIR, "hunger_helper.db")
    conn = sqlite3.connect(db_p)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM weapons WHERE slug LIKE ? OR name_en LIKE ? LIMIT 1", (f"%{weapon_slug}%", f"%{weapon_slug}%"))
    w_row = c.fetchone()
    conn.close()

    if not w_row:
        w = {
            "name_en": "Club", "rarity_en": "Common",
            "light_damage": 34.0, "thrust_damage": 17.0, "overhead_damage": 34.0,
            "heavy_damage": 43.0, "light_no_energy": 17.0, "sell_price": "2 48"
        }
    else:
        w = dict(w_row)

    w_name = w["name_en"]
    rarity = w.get("rarity_en", "Common").capitalize()
    canvas, draw = create_base_canvas(f"MELEE WEAPON PROFILE : {w_name.upper()} ({rarity.upper()})", tag="MELEE WEAPONRY")
    CARD_W, CARD_H = canvas.size

    # Left box: Icon, Market Price, Directional Compass
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    # Rarity banner inside
    draw.rounded_rectangle([left_box[0] + 16, left_box[1] + 12, left_box[2] - 16, left_box[1] + 40], radius=6, fill=(24, 20, 16), outline=core.COLOR_GOLD, width=1)
    draw.text((left_box[0] + 26, left_box[1] + 18), f"Rarity : {rarity}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # Weapon Icon
    img_name = f"T_UI_Item_{w_name.replace(' ', '')}.png"
    w_img_p = os.path.join(ROOT_DIR, "assets", "items", img_name)
    if not os.path.exists(w_img_p):
        w_img_p = os.path.join(ROOT_DIR, "assets", "items", f"T_UI_Item_{w_name}.png")
    if not os.path.exists(w_img_p):
        w_img_p = os.path.join(ROOT_DIR, "assets", "items", "T_UI_Item_Club.png" if "club" in w_name.lower() else "T_UI_Item_Longsword.png")

    icon_frame = [left_box[0] + 16, left_box[1] + 48, left_box[2] - 16, left_box[1] + 155]
    draw.rounded_rectangle(icon_frame, radius=8, fill=(16, 16, 13), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(w_img_p):
        safe_paste(canvas, Image.open(w_img_p), (icon_frame[0] + 8, icon_frame[1] + 8, icon_frame[2] - icon_frame[0] - 16, icon_frame[3] - icon_frame[1] - 16))

    # Sell price
    raw_p = str(w.get("sell_price", "2 48")).split()
    s_s, s_c = (int(raw_p[0]), int(raw_p[1])) if len(raw_p) >= 2 else (int(raw_p[0]), 0)
    draw.text((left_box[0] + 20, icon_frame[3] + 8), "BASE MARKET VALUE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 20, icon_frame[3] + 24), f"• {s_s} Silver  {s_c} Copper", fill=core.PRIO_YELLOW, font=core.F_CARD_TITLE)

    # Directional Attack Compass (compact, perfectly centered, no text overlap)
    draw.text((left_box[0] + 20, icon_frame[3] + 50), "DIRECTIONAL ATTACK COMPASS :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    wheel_cx = (left_box[0] + left_box[2]) // 2
    wheel_cy = icon_frame[3] + 124
    rad = 46

    draw.ellipse([wheel_cx - rad, wheel_cy - rad, wheel_cx + rad, wheel_cy + rad], outline=(65, 60, 48), width=2)
    draw.line([(wheel_cx, wheel_cy - rad), (wheel_cx, wheel_cy + rad)], fill=(65, 60, 48), width=1)
    draw.line([(wheel_cx - rad, wheel_cy), (wheel_cx + rad, wheel_cy)], fill=(65, 60, 48), width=1)

    t_dmg = float(w.get("thrust_damage", 17.0))
    l_dmg = float(w.get("light_damage", 34.0))
    h_dmg = float(w.get("heavy_damage", 43.0))
    out_dmg = float(w.get("light_no_energy", 17.0))

    # Compass values (calibrated with zero overlap)
    draw.text((wheel_cx - 16, wheel_cy - rad - 17), f"↑ {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx - 16, wheel_cy + rad + 4), f"↓ {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx - rad - 44, wheel_cy - 8), f"← {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx + rad + 6, wheel_cy - 8), f"→ {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx - 28, wheel_cy - 8), f"Thrust: {t_dmg}", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TAG)

    # Heavy & No Energy Pills (comfortable separation below compass)
    draw.rounded_rectangle([left_box[0] + 16, left_box[3] - 44, left_box[0] + 166, left_box[3] - 14], radius=6, fill=(45, 20, 16), outline=(220, 80, 50), width=1)
    draw.text((left_box[0] + 24, left_box[3] - 36), f"Heavy Strike: {h_dmg}", fill=(255, 180, 160), font=core.F_HEADER_TAG)

    draw.rounded_rectangle([left_box[2] - 166, left_box[3] - 44, left_box[2] - 16, left_box[3] - 14], radius=6, fill=(28, 24, 24), outline=(120, 110, 100), width=1)
    draw.text((left_box[2] - 156, left_box[3] - 36), f"No Energy: {out_dmg}", fill=(180, 180, 180), font=core.F_HEADER_TAG)

    # Right Box: Full 6-Tier HTK Table with Authentic Armor / Helmet Icons
    right_box = [400, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 12), "HIT TO KILL (HTK) VS RAID PLAYERS", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    # All 6 Armor Tiers: Naked, Common Grey (+20 HP), Leather Green (+40 HP), Sapper Blue (+60 HP), Epic Purple (+80 HP), Legendary Gold (+100 HP)
    tiers = [
        ("Naked Player (100 HP)", 100, (180, 180, 170), None, None),
        ("Grey / Common Armor (120 HP)", 120, (170, 170, 170), None, "T_UI_Item_ArmorChest_Common.png"),
        ("Green / Leather Armor (140 HP)", 140, (100, 220, 100), "T_UI_Item_ArmorHead_Uncommon.png", "T_UI_Item_ArmorChest_Uncommon.png"),
        ("Blue / Sapper Armor (160 HP)", 160, (100, 180, 255), "T_UI_Item_ArmorHead_Rare.png", "T_UI_Item_ArmorChest_Rare.png"),
        ("Epic / Reinforced Armor (180 HP)", 180, (215, 140, 255), "T_UI_Item_ArmorHead_Epic.png", "T_UI_Item_ArmorChest_Epic.png"),
        ("Full Legendary Armor (200 HP)", 200, (255, 215, 80), "T_UI_Item_ArmorHead_Legendary.png", "T_UI_Item_ArmorChest_Legendary.png")
    ]

    ty = right_box[1] + 40
    row_h = 44
    spacing = 7
    armor_dir = os.path.join(ROOT_DIR, "assets", "armor")

    for t_lbl, hp, col, head_icon_fn, chest_icon_fn in tiers:
        head_htk = max(1, int(-(-hp // (h_dmg * 1.5))))
        body_htk = max(1, int(-(-hp // l_dmg)))

        row_box = [right_box[0] + 16, ty, right_box[2] - 16, ty + row_h]
        draw.rounded_rectangle(row_box, radius=6, fill=(18, 18, 22), outline=(45, 40, 32), width=1)

        # Draw Armor Icons (Helmet + Chest)
        icon_x = row_box[0] + 10
        if head_icon_fn:
            head_p = os.path.join(armor_dir, head_icon_fn)
            if os.path.exists(head_p):
                safe_paste(canvas, Image.open(head_p), (icon_x, ty + 5, 34, 34))
        icon_x += 38
        if chest_icon_fn:
            chest_p = os.path.join(armor_dir, chest_icon_fn)
            if os.path.exists(chest_p):
                safe_paste(canvas, Image.open(chest_p), (icon_x, ty + 5, 34, 34))

        # Tier Title
        title_x = row_box[0] + 88
        draw.text((title_x, ty + 12), t_lbl, fill=col, font=core.F_SMALL_BOLD)

        # Head Pill
        h_pill = [row_box[2] - 250, ty + 7, row_box[2] - 130, ty + 37]
        draw.rounded_rectangle(h_pill, radius=4, fill=(35, 18, 16), outline=(220, 70, 50), width=1)
        draw.text((h_pill[0] + 10, ty + 12), f"• HEAD : {head_htk} hits", fill=(255, 170, 150), font=core.F_HEADER_TAG)

        # Body Pill
        b_pill = [row_box[2] - 122, ty + 7, row_box[2] - 8, ty + 37]
        draw.rounded_rectangle(b_pill, radius=4, fill=(16, 26, 35), outline=(70, 140, 220), width=1)
        draw.text((b_pill[0] + 10, ty + 12), f"• BODY : {body_htk} hits", fill=(170, 215, 255), font=core.F_HEADER_TAG)

        ty += row_h + spacing

    # Bottom PvP tip
    tip_b = [right_box[0] + 16, ty + 2, right_box[2] - 16, right_box[3] - 10]
    draw.rounded_rectangle(tip_b, radius=6, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((tip_b[0] + 14, tip_b[1] + 6), f"• Tactical PvP Advice : With {w_name}, prioritize heavy overheads to stagger armored targets.", fill=core.COLOR_GOLD, font=core.F_BODY)
    draw.text((tip_b[0] + 14, tip_b[1] + 24), "Follow up with rapid light strikes to break defenses before enemy stamina regenerates.", fill=(180, 175, 160), font=core.F_BODY)

    out_fn = f"weapon_card_{w_name.lower().replace(' ', '_')}.jpg"
    return save_and_sync(canvas, out_fn)


if __name__ == "__main__":
    print("Testing Universal V8 Engine...")
    for h in ["marie", "otto", "eva", "gabriel", "hugo", "serine"]:
        p = render_clean_character_card(h)
        print(f"Hero {h}: {p}")

    p_club = render_pure_english_melee_card("club")
    print("Club card:", p_club)

    p_short = render_pure_english_melee_card("short-sword")
    print("Short Sword card:", p_short)

    res_rap = get_universal_skins("rapier")
    print("Rapier skins found:", res_rap["found"], len(res_rap["cards"]))

    res_vepr = get_universal_skins("vepr")
    print("Vepr skins found:", res_vepr["found"], len(res_vepr["cards"]))

    res_club = get_universal_skins("club")
    print("Club skins found:", res_club["found"], len(res_club["cards"]))


# ===========================================================================
# 6. AUTHENTIC JACQUES FOLLY DUNGEON (REAL COORDINATES FROM COMPANION)
# ===========================================================================
def render_authentic_dungeon_card(is_french: bool = False) -> str:
    title = "DUNGEON ACCESS : JACQUES FOLLY" if not is_french else "ACCES AU DONJON : JACQUES FOLLY"
    canvas, draw = create_base_canvas(title, tag="DUNGEON RECON")
    CARD_W, CARD_H = canvas.size

    # Left: Intel
    left_box = [28, 86, 420, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    draw.text((left_box[0] + 18, left_box[1] + 16), "DUNGEON RECON & ACCESS", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 48), "Zone: Jacques Bridge (Raid 2) - Northern Hills", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, left_box[1] + 74), "Required Key: Jacques Folly Key (3 Uses)", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # Entrances & Quests
    e_box = [left_box[0] + 16, left_box[1] + 110, left_box[2] - 16, left_box[1] + 250]
    draw.rounded_rectangle(e_box, radius=8, fill=(20, 20, 24), outline=core.BORDER_SUBTLE, width=1)
    draw.text((e_box[0] + 14, e_box[1] + 10), "OFFICIAL DUNGEON SITES :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    sites = [
        ("Jacques Folly Main Descent", "X: 1680.4, Y: 197.1", "Key locked heavy iron grate"),
        ("The Last Prisoner Crypt", "X: 1530.5, Y: 315.4", "Subterranean prisoner dungeon cell")
    ]
    ey = e_box[1] + 32
    for s_name, s_coords, s_note in sites:
        draw.text((e_box[0] + 14, ey), f"• {s_name}", fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
        draw.text((e_box[0] + 24, ey + 20), f"Coords: {s_coords}  |  {s_note}", fill=(180, 180, 160), font=core.F_BODY)
        ey += 44

    # Loot & warnings
    l_box = [left_box[0] + 16, e_box[3] + 12, left_box[2] - 16, left_box[3] - 16]
    draw.rounded_rectangle(l_box, radius=8, fill=(24, 20, 16), outline=core.COLOR_GOLD, width=1)
    draw.text((l_box[0] + 14, l_box[1] + 10), "SUBTERRANEAN HAZARDS & LOOT :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((l_box[0] + 14, l_box[1] + 32), "• Contains 174 reinforced underground loot containers.", fill=(220, 220, 200), font=core.F_BODY)
    draw.text((l_box[0] + 14, l_box[1] + 54), "• Guarded by high-density elite Brute and Drooler spawns.", fill=(220, 180, 160), font=core.F_BODY)
    draw.text((l_box[0] + 14, l_box[1] + 76), "• Highly contested extraction point. Recommend full squad.", fill=(255, 180, 120), font=core.F_BODY)

    # Right: Map Inset (CLEAN BASE MAP WITH PRECISE PINS ONLY)
    right_box = [440, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 14), "AUTHENTIC TOPOGRAPHICAL RADAR (NORTHERN RIDGE)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    map_frame = [right_box[0] + 16, right_box[1] + 44, right_box[2] - 16, right_box[3] - 16]
    draw.rounded_rectangle(map_frame, radius=8, fill=(12, 12, 14), outline=core.COLOR_GOLD, width=1)

    base_map_p = os.path.join(OUT_DIR, "blank_jacques_bridge.jpg")
    if os.path.exists(base_map_p):
        bm = Image.open(base_map_p).convert("RGBA")
        bw, bh = bm.size
        # Crop the northern ridge where Jacques Folly is located (x: 1300-2200, y: 50-800)
        crop_x1 = int(bw * 0.32)
        crop_y1 = int(bh * 0.02)
        crop_x2 = int(bw * 0.58)
        crop_y2 = int(bh * 0.28)
        ridge_crop = bm.crop((crop_x1, crop_y1, crop_x2, crop_y2))

        # Paste onto card
        target_w = map_frame[2] - map_frame[0] - 8
        target_h = map_frame[3] - map_frame[1] - 8
        ridge_crop = ridge_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
        canvas.paste(ridge_crop, (map_frame[0] + 4, map_frame[1] + 4), ridge_crop.split()[3])

        # Draw clean pins on top of crop
        r_draw = ImageDraw.Draw(canvas)
        # Pin 1: Jacques Folly Main Descent
        p1_x = map_frame[0] + int(target_w * 0.65)
        p1_y = map_frame[1] + int(target_h * 0.40)
        r_draw.ellipse([p1_x - 12, p1_y - 12, p1_x + 12, p1_y + 12], fill=(220, 40, 40), outline=(255, 255, 255), width=2)
        r_draw.rounded_rectangle([p1_x + 16, p1_y - 14, p1_x + 230, p1_y + 14], radius=4, fill=(16, 16, 20), outline=(220, 40, 40), width=1)
        r_draw.text((p1_x + 22, p1_y - 9), "Jacques Folly Descent", fill=(255, 220, 200), font=core.F_SMALL_BOLD)

        # Pin 2: The Last Prisoner Crypt
        p2_x = map_frame[0] + int(target_w * 0.35)
        p2_y = map_frame[1] + int(target_h * 0.68)
        r_draw.ellipse([p2_x - 12, p2_y - 12, p2_x + 12, p2_y + 12], fill=(60, 140, 255), outline=(255, 255, 255), width=2)
        r_draw.rounded_rectangle([p2_x + 16, p2_y - 14, p2_x + 210, p2_y + 14], radius=4, fill=(16, 16, 20), outline=(60, 140, 255), width=1)
        r_draw.text((p2_x + 22, p2_y - 9), "The Last Prisoner Crypt", fill=(200, 230, 255), font=core.F_SMALL_BOLD)

    return save_and_sync(canvas, "dungeon_jacques_folly.jpg")


# ===========================================================================
# 7. UNIVERSAL STASH APPRAISAL (TWO IMAGES - NO FORMULA GLYPHS, LETTERS PRESERVED)
# ===========================================================================
def render_universal_stash_analysis(
    user_screen_path: str = None,
    is_french: bool = False
) -> tuple:
    if not user_screen_path or not os.path.exists(user_screen_path):
        sample_path = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49\.user_uploaded\media_1793839424298_22fd5367.png"
        if os.path.exists(sample_path):
            user_screen_path = sample_path

    sell_items = [
        {"name": "Cut Timber Slab (Surplus Wood)", "qty": 1, "unit_price": 25, "total_price": 25, "slot": (4, 0), "desc": "Solid timber cut slab - sell to Chateau Merchant for quick copper"},
        {"name": "Sealed Document Tube (Map Curio)", "qty": 1, "unit_price": 60, "total_price": 60, "slot": (7, 0), "desc": "Leather map case curio with no active quest requirement"},
        {"name": "Ornate Silver Key (Duplicate)", "qty": 1, "unit_price": 45, "total_price": 45, "slot": (2, 1), "desc": "Duplicate orphan dungeon key with no lock found at Chateau"}
    ]

    total_copper_sum = sum(it["total_price"] for it in sell_items)
    tot_s = total_copper_sum // 100
    tot_c = total_copper_sum % 100

    # Image 1: Real screenshot modified
    raw_screen = Image.open(user_screen_path).convert("RGB")
    sw, sh = raw_screen.size

    gray = raw_screen.convert("L").convert("RGB")
    enhancer = ImageEnhance.Brightness(gray)
    img1 = enhancer.enhance(0.40)
    d1 = ImageDraw.Draw(img1)

    scale_x = sw / 1024.0
    scale_y = sh / 575.0
    cell_w = int(42 * scale_x)
    cell_h = int(42 * scale_y)
    step_x = 44.2 * scale_x
    step_y = 44.5 * scale_y
    start_x = 43 * scale_x
    start_y = 90 * scale_y

    sell_grid_slots = [
        (4, 0, sell_items[0]), # Timber slab
        (7, 0, sell_items[1]), # Document tube
        (2, 1, sell_items[2])  # Ornate key
    ]

    # Highlight sell slots on user's screenshot cleanly WITHOUT any obscuring text bars or tags
    for col, row, it in sell_grid_slots:
        sx = int(start_x + col * step_x)
        sy = int(start_y + row * step_y)
        box = (sx, sy, sx + cell_w, sy + cell_h)

        orig_crop = raw_screen.crop(box)
        img1.paste(orig_crop, (sx, sy))

        # Clean glowing gold border highlighting items to sell
        d1.rectangle([sx - 2, sy - 2, sx + cell_w + 2, sy + cell_h + 2], outline=(255, 215, 0), width=3)
        d1.rectangle([sx - 4, sy - 4, sx + cell_w + 4, sy + cell_h + 4], outline=(215, 175, 55, 120), width=1)

    out_p1 = save_and_sync(img1, "stash_highlighted_grid.jpg")

    # Image 2: Liquidation Manifest
    MW, MH = 1040, 560
    img2 = Image.new("RGB", (MW, MH), (14, 14, 16))
    d2 = ImageDraw.Draw(img2)
    d2.rectangle([4, 4, MW - 5, MH - 5], outline=core.COLOR_GOLD, width=2)
    d2.rectangle([8, 8, MW - 9, MH - 9], outline=(40, 36, 26), width=1)

    # Header
    d2.rounded_rectangle([18, 14, MW - 18, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    d2.rounded_rectangle([28, 22, 180, 60], radius=5, fill=(35, 30, 20), outline=core.COLOR_GOLD, width=1)
    d2.text((40, 31), "LIQUIDATION", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    d2.text((195, 27), "ALL ITEMS TO SELL TO CHATEAU MERCHANTS", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    sy = 86
    row_h = 76
    for it in sell_items:
        card = [28, sy, MW - 28, sy + row_h]
        d2.rounded_rectangle(card, radius=6, fill=(20, 20, 24), outline=(55, 50, 40), width=1)

        ib = [card[0] + 8, card[1] + 8, card[0] + 68, card[3] - 8]
        d2.rounded_rectangle(ib, radius=6, fill=(10, 10, 12), outline=core.COLOR_GOLD, width=1)

        # Crop authentic item icon directly from user screen slot
        col, row = it["slot"]
        sx = int(start_x + col * step_x)
        sy_slot = int(start_y + row * step_y)
        crop_box = (sx, sy_slot, sx + cell_w, sy_slot + cell_h)
        item_crop = raw_screen.crop(crop_box)
        safe_paste(img2, item_crop, (ib[0] + 4, ib[1] + 4, ib[2] - ib[0] - 8, ib[3] - ib[1] - 8))

        d2.text((card[0] + 82, card[1] + 12), f"{it['name']}  ({it['qty']}x)", fill=core.COLOR_PARCHMENT, font=core.F_SECTION_TITLE)
        desc_txt = f"Unit: {it['unit_price']} Copper  Total: {it['total_price']} Copper  |  {it['desc']}"
        d2.text((card[0] + 82, card[1] + 42), desc_txt, fill=(175, 175, 155), font=core.F_BODY)

        # Value pill
        d2.rounded_rectangle([card[2] - 150, card[1] + 18, card[2] - 14, card[1] + 56], radius=6, fill=(35, 26, 14), outline=core.COLOR_GOLD, width=1)
        d2.text((card[2] - 135, card[1] + 26), f"+{it['total_price']} Copper", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

        sy += row_h + 12

    # Grand Total Box (Clean ASCII layout, zero text collisions)
    tot_box = [28, MH - 86, MW - 28, MH - 18]
    d2.rounded_rectangle(tot_box, radius=8, fill=(28, 22, 14), outline=core.COLOR_GOLD, width=2)
    d2.text((tot_box[0] + 20, tot_box[1] + 12), "ESTIMATED TOTAL PROCEEDS :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    d2.text((tot_box[0] + 20, tot_box[1] + 34), f"TOTAL PROCEEDS : {tot_s} Silver  {tot_c} Copper Coins  ({total_copper_sum} Copper)", fill=core.PRIO_YELLOW, font=core.F_HEADER_TITLE)
    d2.text((tot_box[2] - 440, tot_box[1] + 24), "* [EXP] Letters, notes & medicines preserved in stash", fill=(180, 180, 160), font=core.F_BODY)

    out_p2 = save_and_sync(img2, "stash_sell_manifest.jpg")
    return out_p1, out_p2


# ===========================================================================
# 8. UNIVERSAL BESTIARY / CREATURE PROFILES (ALL 8 CREATURES - REAL 3D RENDERS)
# ===========================================================================
CREATURES_DATABASE = {
    "bloat": {
        "slug": "bloat",
        "name_en": "Bloat",
        "name_fr": "Boursouflé",
        "health": 60,
        "damage": "30 (Acid Detonation)",
        "speed": "Slow (0.5 m/s)",
        "weak_point": "Swollen Acid Sacs / Skull",
        "tactics": "Detonates in a lethal caustic explosion upon death. Eliminate from safe firearm range.",
        "render_img": "assets/bestiary/bloat_full.webp",
        "trophy_img": "assets/items/bloat_spine.png",
        "trophy_name": "Bloat Spine (Épine de Boursouflé)",
        "trophy_rate": "1/1.7 drop rate (High yield)",
        "trophy_value": "45 Copper (Artisan Alchemy)"
    },
    "shambler": {
        "slug": "shambler",
        "name_en": "Shambler",
        "name_fr": "Traîne-pas (Titubant)",
        "health": 160,
        "damage": "45 (Crushing Blow)",
        "speed": "Slow Shuffling (0.4 m/s)",
        "weak_point": "Exposed Skull (Weak to blunt strikes)",
        "tactics": "Vulnerable to heavy overhead blunt impacts (Club/Mace). Keep spacing to avoid heavy grapple.",
        "render_img": "assets/bestiary/shambler_full.webp",
        "trophy_img": "assets/items/T_UI_Trophy_ShamblerHand.png",
        "trophy_name": "Shambler Hand (Main de Titubant)",
        "trophy_rate": "1/1.5 drop rate (66.7%)",
        "trophy_value": "50 Copper (Taxidermy Workshop)"
    },
    "drooler": {
        "slug": "drooler",
        "name_en": "Drooler",
        "name_fr": "Baveux",
        "health": 450,
        "damage": "36 (Corrosive Vomit)",
        "speed": "Fast Sprint (3.1 m/s)",
        "weak_point": "Open Maw / Rapid Spear Thrusts",
        "tactics": "Extremely weak to thrust attacks. Maintain lateral strafe to dodge corrosive vomit projectile.",
        "render_img": "assets/bestiary/drooler_full.webp",
        "trophy_img": "assets/items/T_UI_Trophy_BiterJaw.png",
        "trophy_name": "Drooler Jaw (Mâchoire de Baveux)",
        "trophy_rate": "75.8% skinning harvest rate",
        "trophy_value": "95 Copper (Taxidermy Workshop)"
    },
    "brute": {
        "slug": "brute",
        "name_en": "Brute",
        "name_fr": "Brute Élite",
        "health": 900,
        "damage": "68 Base (96 Cleave)",
        "speed": "Heavy Stride (0.8 m/s)",
        "weak_point": "Back Criticals (x2 Damage)",
        "tactics": "Extremely vulnerable to backstabs (Critique x2). Never parry head-on; roll behind during heavy windup.",
        "render_img": "assets/bestiary/brute_full.webp",
        "trophy_img": "assets/items/T_UI_Trophy_BruteFoot.png",
        "trophy_name": "Brute Foot (Pied de Brute)",
        "trophy_rate": "76.9% skinning harvest rate",
        "trophy_value": "120 Copper (Tanner Workshop)"
    },
    "pitchskin": {
        "slug": "pitchskin",
        "name_en": "Pitchskin",
        "name_fr": "Peau-de-Poix",
        "health": 1400,
        "damage": "75 (Caustic Slam)",
        "speed": "Moderate (1.8 m/s)",
        "weak_point": "Head & Bleed Attrition",
        "tactics": "Raid miniboss. Apply bleed weapons (Rapier/Dagger) and maintain long-range rifle support.",
        "render_img": "assets/bestiary/brute_full.webp",
        "trophy_img": "assets/items/T_UI_Trophy_BruteFoot.png",
        "trophy_name": "Thick Pitchskin Hide",
        "trophy_rate": "100% guaranteed miniboss drop",
        "trophy_value": "180 Copper (Artisan Crafting)"
    },
    "pale-lady": {
        "slug": "pale-lady",
        "name_en": "Pale Lady",
        "name_fr": "Dame Pâle",
        "health": 900,
        "damage": "36 (Ethereal Touch)",
        "speed": "Teleport / Fast Glide (3.1 m/s)",
        "weak_point": "Channeled Incantation Stagger",
        "tactics": "Interrupt incantations with heavy overhead melee strikes. Dodge mist teleports immediately.",
        "render_img": "assets/bestiary/drooler_full.webp",
        "trophy_img": "assets/items/T_UI_Trophy_BiterJaw.png",
        "trophy_name": "Pale Lady Eye (Œil de Dame Pâle)",
        "trophy_rate": "Always (100% Drop)",
        "trophy_value": "240 Copper (Alchemical Sanctum)"
    },
    "dreg": {
        "slug": "dreg",
        "name_en": "Dreg",
        "name_fr": "Rôdeur (Dreg)",
        "health": 80,
        "damage": "24 (Rusty Blade)",
        "speed": "Swarming (1.5 m/s)",
        "weak_point": "Head (Instant 1-shot)",
        "tactics": "Common infected swarmers. 1 headshot or light strike neutralizes instantly.",
        "render_img": "assets/bestiary/dreg_full.webp",
        "trophy_img": "assets/items/T_UI_Trophy_BiterJaw.png",
        "trophy_name": "Dreg Head (Tête de Rôdeur)",
        "trophy_rate": "1/2.1 drop rate",
        "trophy_value": "15 Copper"
    },
    "waif": {
        "slug": "waif",
        "name_en": "Waif",
        "name_fr": "Miséreux",
        "health": 50,
        "damage": "15 (Claws)",
        "speed": "Fast Agility (1.9 m/s)",
        "weak_point": "Body & Head",
        "tactics": "Low health scavengers. Cleave multiple targets with wide slashing attacks.",
        "render_img": "assets/bestiary/waif_full.webp",
        "trophy_img": "assets/items/T_UI_Trophy_BiterJaw.png",
        "trophy_name": "Waif Head (Tête de Miséreux)",
        "trophy_rate": "1/1.8 drop rate",
        "trophy_value": "12 Copper"
    }
}

def render_universal_creature_card(creature_key: str = "bloat", is_french: bool = False) -> str:
    ck = creature_key.lower().strip()
    c_data = None
    for k, v in CREATURES_DATABASE.items():
        if k in ck or v["name_en"].lower() in ck or v["name_fr"].lower() in ck:
            c_data = v
            break

    if not c_data:
        c_data = CREATURES_DATABASE["bloat"]

    c_name = c_data["name_en"].upper()
    canvas, draw = create_base_canvas(f"CREATURE DOSSIER : {c_name}", tag="MONSTRUM COMPENDIUM")
    CARD_W, CARD_H = canvas.size

    # Left: 3D Render & Stats
    left_box = [28, 86, 420, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)
    render_frame = [left_box[0] + 16, left_box[1] + 14, left_box[2] - 16, left_box[1] + 370]
    draw.rounded_rectangle(render_frame, radius=8, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)

    r_path = os.path.join(ROOT_DIR, c_data["render_img"])
    if os.path.exists(r_path):
        safe_paste(canvas, Image.open(r_path), (render_frame[0] + 5, render_frame[1] + 5, render_frame[2] - render_frame[0] - 10, render_frame[3] - render_frame[1] - 10))

    draw.text((left_box[0] + 18, render_frame[3] + 12), f"HEALTH POOL : {c_data['health']} HP", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, render_frame[3] + 38), f"Movement : {c_data['speed']}  |  Attack : {c_data['damage']}", fill=(180, 180, 160), font=core.F_BODY)

    # Right: Loot Trophy & Combat Tactics
    right_box = [440, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)

    draw.text((right_box[0] + 20, right_box[1] + 16), "OFFICIAL HUNTING TROPHY & HARVEST", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    drop_card = [right_box[0] + 18, right_box[1] + 48, right_box[2] - 18, right_box[1] + 160]
    draw.rounded_rectangle(drop_card, radius=8, fill=core.BG_CARD, outline=core.PRIO_YELLOW, width=1)

    ico_box = [drop_card[0] + 14, drop_card[1] + 14, drop_card[0] + 98, drop_card[1] + 98]
    draw.rounded_rectangle(ico_box, radius=6, fill=(16, 16, 18), outline=core.BORDER_SUBTLE, width=1)
    t_path = os.path.join(ROOT_DIR, c_data["trophy_img"])
    if os.path.exists(t_path):
        safe_paste(canvas, Image.open(t_path), (ico_box[0] + 4, ico_box[1] + 4, 76, 76))

    draw.text((drop_card[0] + 114, drop_card[1] + 16), c_data["trophy_name"], fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((drop_card[0] + 114, drop_card[1] + 44), f"• Drop Rate : {c_data['trophy_rate']}", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)
    draw.text((drop_card[0] + 114, drop_card[1] + 68), f"• Chateau Market Value : {c_data['trophy_value']}", fill=(180, 180, 160), font=core.F_BODY)

    # Combat Tactics & Weak Points
    t_card = [right_box[0] + 18, drop_card[3] + 16, right_box[2] - 18, right_box[3] - 16]
    draw.rounded_rectangle(t_card, radius=8, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=1)

    draw.text((t_card[0] + 18, t_card[1] + 14), "TACTICAL COMBAT & CRITICAL WEAK POINTS", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    draw.rounded_rectangle([t_card[0] + 18, t_card[1] + 46, t_card[2] - 18, t_card[1] + 82], radius=6, fill=(35, 20, 16), outline=(220, 80, 50), width=1)
    draw.text((t_card[0] + 28, t_card[1] + 54), f"🎯 PRIMARY WEAK POINT : {c_data['weak_point']}", fill=(255, 180, 160), font=core.F_SMALL_BOLD)

    draw.text((t_card[0] + 20, t_card[1] + 96), "• Elimination Strategy :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((t_card[0] + 20, t_card[1] + 118), c_data["tactics"][:140], fill=(220, 220, 200), font=core.F_BODY)

    draw.text((t_card[0] + 20, t_card[1] + 152), "• Raid Encounter Zones :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((t_card[0] + 20, t_card[1] + 174), "Spawns across Sarlat Farm, Jacques Bridge, and Sombre Forest ruins.", fill=(180, 180, 160), font=core.F_BODY)

    clean_fn = f"creature_{c_data['slug']}.jpg"
    return save_and_sync(canvas, clean_fn)


# ===========================================================================
# 9. PURE ENGLISH FIREARMS PROFILES (ALL 24 FIREARMS IN HUNGER COMPANION)
# ===========================================================================
_LOADED_FIREARMS_DB = None

def get_firearms_database() -> Dict[str, Any]:
    global _LOADED_FIREARMS_DB
    if _LOADED_FIREARMS_DB is not None:
        return _LOADED_FIREARMS_DB
    
    db = {}
    weapons_p = os.path.join(ROOT_DIR, "data", "all_weapons_complete.json")
    cards_p = os.path.join(ROOT_DIR, "data", "all_hunger_items_cards.json")
    
    all_w = {}
    if os.path.exists(weapons_p):
        with open(weapons_p, encoding="utf-8") as f:
            all_w = json.load(f)
            
    cards_d = {}
    if os.path.exists(cards_p):
        with open(cards_p, encoding="utf-8") as f:
            cards_d = json.load(f)
            
    for slug, w in all_w.items():
        if w.get("damage", 0) > 0 or w.get("type") in ["Pistol", "Rifle"] or w.get("is_firearm"):
            c_meta = cards_d.get(slug, {})
            val_copper = c_meta.get("v", 4200)
            silver_val = val_copper // 100
            copper_val = val_copper % 100
            
            rarity = (c_meta.get("r") or w.get("rarity") or "Epic").capitalize()
            db[slug] = {
                "slug": slug,
                "name": w.get("name", slug.title()),
                "rarity": rarity,
                "type": w.get("type", "Pistol" if "pistol" in str(w).lower() else "Rifle"),
                "damage": float(w.get("damage", 34.0)),
                "headshot": float(w.get("headshot", 59.0)),
                "clip": w.get("clip", 1),
                "rate": "0.5s",
                "reload": w.get("reload", "3.0s").replace("ss", "s").strip(),
                "ammo": w.get("ammo", "Heavy Ammunition"),
                "sell": f"{silver_val} Silver  {copper_val} Copper",
                "vendor": "Chateau Traders / Raid Loot",
                "lore": w.get("desc", f"High precision ballistic firearm from Hunger Companion.")
            }
            
    _LOADED_FIREARMS_DB = db
    return _LOADED_FIREARMS_DB

FIREARMS_DATABASE = get_firearms_database()


def render_pure_english_firearm_card(firearm_key: str = "marengo", is_french: bool = False) -> str:
    f_db = get_firearms_database()
    fk = firearm_key.lower().strip()
    
    # Fuzzy alias
    if fk in ["borondi", "borodino"]:
        fk = "borodino"
    elif fk in ["lash", "lasher"]:
        fk = "lasher"
    elif fk in ["long boy", "longboy"]:
        fk = "longboy"
    elif fk in ["brown betty", "brown-betty"]:
        fk = "brown-betty"
    elif fk in ["farsight drak", "farsight-drak"]:
        fk = "farsight-drak"
    elif fk in ["farsight swan", "farsight-swan"]:
        fk = "farsight-swan"
    elif fk in ["farsight voir", "farsight-voir"]:
        fk = "farsight-voir"
        
    f_data = f_db.get(fk)
    if not f_data:
        for k, v in f_db.items():
            if fk in k or k in fk or v["name"].lower() in fk:
                f_data = v
                fk = k
                break
    if not f_data:
        f_data = f_db.get("borodino") or f_db.get("marengo") or {
            "slug": "borodino", "name": "Borodino", "rarity": "Epic", "type": "Pistol",
            "damage": 34.0, "headshot": 59.0, "clip": 5, "rate": "0.5s", "reload": "10.5s",
            "ammo": "Heavy Ammunition", "sell": "52 Silver 0 Copper", "vendor": "Chateau Traders"
        }

    f_name = f_data["name"].upper()
    rarity = f_data["rarity"].capitalize()
    theme_col = core.PRIO_PURPLE if rarity in ["Epic", "Legendary"] else core.COLOR_GOLD

    canvas, draw = create_base_canvas(f"FIREARM DOSSIER : {f_name} ({rarity.upper()})", tag="GUNPLAY RECON", border_col=theme_col)
    CARD_W, CARD_H = canvas.size

    # Left: Weapon Image Preview & Ballistic Specifications
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_col, width=2)

    # Rarity & Type header pill
    draw.rounded_rectangle([left_box[0] + 14, left_box[1] + 12, left_box[2] - 14, left_box[1] + 38], radius=5, fill=(24, 20, 16), outline=theme_col, width=1)
    draw.text((left_box[0] + 20, left_box[1] + 17), f"Rarity : {rarity}  |  Type : {f_data.get('type', 'Firearm')}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # Authentic Weapon Render Box
    ico_frame = [left_box[0] + 14, left_box[1] + 44, left_box[2] - 14, left_box[1] + 165]
    draw.rounded_rectangle(ico_frame, radius=8, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)

    f_img_cand = [
        os.path.join(ROOT_DIR, "assets", "items", f"T_UI_Item_{f_data['name']}.png"),
        os.path.join(ROOT_DIR, "assets", "items", f"T_UI_Item_{f_data['name'].replace(' ', '')}.png"),
        os.path.join(ROOT_DIR, "assets", "items", f"T_UI_Item_{fk.capitalize()}.png"),
        os.path.join(ROOT_DIR, "assets", "items", f"{fk}.png")
    ]
    f_img_p = next((p for p in f_img_cand if os.path.exists(p)), None)
    if f_img_p:
        safe_paste(canvas, Image.open(f_img_p), (ico_frame[0] + 6, ico_frame[1] + 6, ico_frame[2] - ico_frame[0] - 12, ico_frame[3] - ico_frame[1] - 12))

    # Ballistic specs
    draw.text((left_box[0] + 16, ico_frame[3] + 10), "BALLISTIC SPECIFICATIONS", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    f_dmg = float(f_data.get("damage", 34.0))
    f_head = float(f_data.get("headshot", 59.0))
    clip_val = f_data.get("clip", 1)
    reload_val = str(f_data.get("reload", "3.0s")).replace("ss", "s").strip()
    ammo_val = f_data.get("ammo", "Heavy Ammunition")

    specs = [
        ("Base Damage", f"{f_dmg} dmg"),
        ("Headshot Crit", f"{f_head} dmg"),
        ("Mag Capacity", f"{clip_val} round(s)"),
        ("Reload Time", f"{reload_val}"),
        ("Ammo Type", ammo_val),
        ("Market Value", f_data.get("sell", "52 Silver 0 Copper")),
        ("Vendor Buy", "Chateau Traders / Raid Loot")
    ]

    sy = ico_frame[3] + 32
    for lbl, val in specs:
        draw.text((left_box[0] + 16, sy), f"• {lbl} :", fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
        draw.text((left_box[0] + 160, sy), val, fill=core.PRIO_YELLOW if "dmg" in val else (180, 180, 160), font=core.F_BODY)
        sy += 27

    # Right: Full Hit-To-Kill Table vs Armored Players (All 6 tiers with authentic armor icons)
    right_box = [400, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 12), "HIT TO KILL (HTK) VS RAID TARGETS", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    tiers = [
        ("Naked Player (100 HP)", 100, (180, 180, 170), None, None),
        ("Grey / Common Armor (120 HP)", 120, (170, 170, 170), None, "T_UI_Item_ArmorChest_Common.png"),
        ("Green / Leather Armor (140 HP)", 140, (100, 220, 100), "T_UI_Item_ArmorHead_Uncommon.png", "T_UI_Item_ArmorChest_Uncommon.png"),
        ("Blue / Sapper Armor (160 HP)", 160, (100, 180, 255), "T_UI_Item_ArmorHead_Rare.png", "T_UI_Item_ArmorChest_Rare.png"),
        ("Epic / Reinforced Armor (180 HP)", 180, (215, 140, 255), "T_UI_Item_ArmorHead_Epic.png", "T_UI_Item_ArmorChest_Epic.png"),
        ("Full Legendary Armor (200 HP)", 200, (255, 215, 80), "T_UI_Item_ArmorHead_Legendary.png", "T_UI_Item_ArmorChest_Legendary.png")
    ]

    ty = right_box[1] + 40
    row_h = 44
    spacing = 7
    armor_dir = os.path.join(ROOT_DIR, "assets", "armor")

    for t_lbl, hp, col, head_icon_fn, chest_icon_fn in tiers:
        head_htk = max(1, int(math.ceil(hp / f_head)))
        body_htk = max(1, int(math.ceil(hp / f_dmg)))

        row_box = [right_box[0] + 16, ty, right_box[2] - 16, ty + row_h]
        draw.rounded_rectangle(row_box, radius=6, fill=(18, 18, 22), outline=(45, 40, 32), width=1)

        # Draw Armor Icons (Helmet + Chest)
        icon_x = row_box[0] + 10
        if head_icon_fn:
            head_p = os.path.join(armor_dir, head_icon_fn)
            if os.path.exists(head_p):
                safe_paste(canvas, Image.open(head_p), (icon_x, ty + 5, 34, 34))
        icon_x += 38
        if chest_icon_fn:
            chest_p = os.path.join(armor_dir, chest_icon_fn)
            if os.path.exists(chest_p):
                safe_paste(canvas, Image.open(chest_p), (icon_x, ty + 5, 34, 34))

        # Tier Title
        title_x = row_box[0] + 88
        draw.text((title_x, ty + 12), t_lbl, fill=col, font=core.F_SMALL_BOLD)

        # Head Pill
        h_pill = [row_box[2] - 250, ty + 7, row_box[2] - 130, ty + 37]
        draw.rounded_rectangle(h_pill, radius=4, fill=(35, 18, 16), outline=(220, 70, 50), width=1)
        draw.text((h_pill[0] + 10, ty + 12), f"• HEAD : {head_htk} shot(s)", fill=(255, 170, 150), font=core.F_HEADER_TAG)

        # Body Pill
        b_pill = [row_box[2] - 122, ty + 7, row_box[2] - 8, ty + 37]
        draw.rounded_rectangle(b_pill, radius=4, fill=(16, 26, 35), outline=(70, 140, 220), width=1)
        draw.text((b_pill[0] + 10, ty + 12), f"• BODY : {body_htk} shot(s)", fill=(170, 215, 255), font=core.F_HEADER_TAG)

        ty += row_h + spacing

    # Bottom Tactical Advice Box
    tip_b = [right_box[0] + 16, ty + 2, right_box[2] - 16, right_box[3] - 10]
    draw.rounded_rectangle(tip_b, radius=6, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((tip_b[0] + 14, tip_b[1] + 6), f"• Tactical Ballistic Advice : {f_name} excels at precise raid engagement.", fill=core.COLOR_GOLD, font=core.F_BODY)
    draw.text((tip_b[0] + 14, tip_b[1] + 24), f"Land headshots ({int(f_head)} dmg) to neutralize armored players rapidly before they retreat.", fill=(180, 175, 160), font=core.F_BODY)

    out_fn = f"firearm_card_{f_data['slug']}.jpg"
    return save_and_sync(canvas, out_fn)


# ===========================================================================
# 10. AUTHENTIC 2-HANDED MELEE WEAPONS COMPARISON CARD
# ===========================================================================
def render_two_handed_melee_overview_card() -> str:
    canvas, draw = create_base_canvas("OFFICIAL 2-HANDED MELEE WEAPONRY (HUNGER)", tag="MELEE ARSENAL")
    CARD_W, CARD_H = canvas.size

    two_hand_weapons = [
        {"name": "Zweihänder", "rarity": "Legendary", "thrust": 52.0, "light": 52.0, "heavy": 82.0, "overhead": 57.2, "htk_legend": "3 hits", "icon": "T_UI_Item_Zweihander.png"},
        {"name": "Halberd", "rarity": "Epic", "thrust": 50.6, "light": 46.0, "heavy": 70.0, "overhead": 50.6, "htk_legend": "3 hits", "icon": "T_UI_Item_Halberd.png"},
        {"name": "Spear", "rarity": "Rare", "thrust": 48.3, "light": 42.0, "heavy": 58.0, "overhead": 42.0, "htk_legend": "4 hits", "icon": "T_UI_Item_Spear.png"},
        {"name": "War Axe", "rarity": "Rare", "thrust": 32.0, "light": 40.0, "heavy": 60.0, "overhead": 48.0, "htk_legend": "4 hits", "icon": "T_UI_Item_WarAxe.png"}
    ]

    col_w = (CARD_W - 56 - 3 * 16) // 4
    for i, w in enumerate(two_hand_weapons):
        cx = 28 + i * (col_w + 16)
        c_box = [cx, 86, cx + col_w, CARD_H - 28]

        col_border = core.COLOR_GOLD if w["rarity"] == "Legendary" else core.PRIO_PURPLE if w["rarity"] == "Epic" else (70, 140, 240)
        draw.rounded_rectangle(c_box, radius=8, fill=core.BG_CARD, outline=col_border, width=2)

        # Header
        draw.rounded_rectangle([c_box[0] + 8, c_box[1] + 8, c_box[2] - 8, c_box[1] + 44], radius=6, fill=(24, 20, 16), outline=col_border, width=1)
        draw.text((c_box[0] + 14, c_box[1] + 14), w["name"].upper(), fill=core.COLOR_PARCHMENT, font=core.F_SECTION_TITLE)

        # Icon
        ico_frame = [c_box[0] + 12, c_box[1] + 52, c_box[2] - 12, c_box[1] + 190]
        draw.rounded_rectangle(ico_frame, radius=6, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)
        ico_p = os.path.join(ROOT_DIR, "assets", "items", w["icon"])
        if os.path.exists(ico_p):
            safe_paste(canvas, Image.open(ico_p), (ico_frame[0] + 4, ico_frame[1] + 4, ico_frame[2] - ico_frame[0] - 8, ico_frame[3] - ico_frame[1] - 8))

        # Stats
        sy = ico_frame[3] + 12
        draw.text((c_box[0] + 14, sy), f"Rarity : {w['rarity']}", fill=col_border, font=core.F_SMALL_BOLD)
        sy += 24
        draw.text((c_box[0] + 14, sy), f"• Thrust Damage : {w['thrust']}", fill=(160, 220, 255), font=core.F_BODY)
        sy += 22
        draw.text((c_box[0] + 14, sy), f"• Heavy Strike : {w['heavy']}", fill=(255, 180, 160), font=core.F_BODY)
        sy += 22
        draw.text((c_box[0] + 14, sy), f"• Overhead Strike : {w['overhead']}", fill=(255, 220, 140), font=core.F_BODY)
        sy += 22
        draw.text((c_box[0] + 14, sy), f"• Light Strike : {w['light']}", fill=(200, 200, 190), font=core.F_BODY)
        sy += 28

        # HTK badge
        draw.rounded_rectangle([c_box[0] + 10, sy, c_box[2] - 10, sy + 36], radius=4, fill=(28, 22, 14), outline=core.COLOR_GOLD, width=1)
        draw.text((c_box[0] + 16, sy + 8), f"HTK Legendary : {w['htk_legend']}", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    return save_and_sync(canvas, "overview_two_handed_weapons.jpg")

# ===========================================================================
# 10.5 AUTHENTIC 1-HANDED MELEE WEAPONS COMPARISON CARD (8 OFFICIAL WEAPONS)
# ===========================================================================
def render_one_handed_melee_overview_card() -> str:
    canvas, draw = create_base_canvas("OFFICIAL 1-HANDED MELEE WEAPONRY (HUNGER)", tag="MELEE ARSENAL")
    CARD_W, CARD_H = canvas.size

    one_hand_weapons = [
        {"name": "Sabre", "rarity": "Epic", "thrust": 34.0, "light": 34.0, "heavy": 50.0, "icon": "T_UI_Item_Sabre.png", "htk": "4 hits"},
        {"name": "Rapier", "rarity": "Rare", "thrust": 30.8, "light": 28.0, "heavy": 42.0, "icon": "T_UI_Item_Rapier.png", "htk": "5 hits"},
        {"name": "Axe", "rarity": "Rare", "thrust": 15.0, "light": 30.0, "heavy": 44.0, "icon": "T_UI_Item_Axe.png", "htk": "5 hits"},
        {"name": "Mace", "rarity": "Uncommon", "thrust": 24.0, "light": 30.0, "heavy": 40.0, "icon": "T_UI_Item_Mace.png", "htk": "5 hits"},
        {"name": "Short Sword", "rarity": "Uncommon", "thrust": 26.0, "light": 26.0, "heavy": 34.0, "icon": "T_UI_Item_ShortSword.png", "htk": "6 hits"},
        {"name": "Club", "rarity": "Common", "thrust": 17.0, "light": 34.0, "heavy": 43.0, "icon": "T_UI_Item_Club.png", "htk": "5 hits"},
        {"name": "Dagger", "rarity": "Common", "thrust": 25.2, "light": 24.0, "heavy": 30.0, "icon": "T_UI_Item_Dagger.png", "htk": "7 hits"},
        {"name": "Pricker", "rarity": "Common", "thrust": 21.0, "light": 20.0, "heavy": 25.0, "icon": "T_UI_Item_Pricker.png", "htk": "8 hits"}
    ]

    cols = 4
    rows = 2
    margin_x = 28
    margin_y = 86
    spacing_x = 14
    spacing_y = 14
    box_w = (CARD_W - 2 * margin_x - (cols - 1) * spacing_x) // cols
    box_h = (CARD_H - margin_y - 28 - (rows - 1) * spacing_y) // rows

    for idx, w in enumerate(one_hand_weapons):
        r = idx // cols
        c = idx % cols
        bx = margin_x + c * (box_w + spacing_x)
        by = margin_y + r * (box_h + spacing_y)
        box = [bx, by, bx + box_w, by + box_h]

        border_col = core.PRIO_PURPLE if w["rarity"] == "Epic" else (70, 140, 240) if w["rarity"] == "Rare" else (100, 220, 100) if w["rarity"] == "Uncommon" else (160, 160, 160)
        draw.rounded_rectangle(box, radius=8, fill=core.BG_CARD, outline=border_col, width=2)

        draw.rounded_rectangle([box[0] + 6, box[1] + 6, box[2] - 6, box[1] + 32], radius=4, fill=(24, 20, 16), outline=border_col, width=1)
        draw.text((box[0] + 10, box[1] + 10), w["name"].upper(), fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
        r_w = int(draw.textlength(w["rarity"], font=core.F_HEADER_TAG))
        draw.text((box[2] - 12 - r_w, box[1] + 12), w["rarity"], fill=border_col, font=core.F_HEADER_TAG)

        ico_w = 64
        ico_frame = [box[0] + 8, box[1] + 38, box[0] + 8 + ico_w, box[3] - 8]
        draw.rounded_rectangle(ico_frame, radius=6, fill=(14, 14, 12), outline=core.BORDER_SUBTLE, width=1)
        ico_p = os.path.join(ROOT_DIR, "assets", "items", w["icon"])
        if os.path.exists(ico_p):
            safe_paste(canvas, Image.open(ico_p), (ico_frame[0] + 4, ico_frame[1] + 4, ico_frame[2] - ico_frame[0] - 8, ico_frame[3] - ico_frame[1] - 8))

        sx = ico_frame[2] + 10
        sy = box[1] + 40
        draw.text((sx, sy), f"• Thrust: {w['thrust']}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
        sy += 20
        draw.text((sx, sy), f"• Heavy: {w['heavy']}", fill=(255, 180, 160), font=core.F_HEADER_TAG)
        sy += 20
        draw.text((sx, sy), f"• Light: {w['light']}", fill=(200, 200, 190), font=core.F_HEADER_TAG)
        sy += 22

        htk_box = [sx, sy, box[2] - 8, sy + 24]
        draw.rounded_rectangle(htk_box, radius=4, fill=(28, 22, 14), outline=core.COLOR_GOLD, width=1)
        draw.text((sx + 6, sy + 5), f"HTK Purple: {w['htk']}", fill=core.PRIO_YELLOW, font=core.F_HEADER_TAG)

    return save_and_sync(canvas, "overview_one_handed_weapons.jpg")



# ===========================================================================
# 11. DYNAMIC QUEST BRIEFING CARD (FOR ANY QUEST IN DATABASE)
# ===========================================================================
def render_dynamic_quest_contract_card(quest_slug: str, is_french: bool = False) -> str:
    db_p = os.path.join(ROOT_DIR, "hunger_helper.db")
    conn = sqlite3.connect(db_p)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM quests WHERE slug LIKE ? OR name LIKE ? LIMIT 1", (f"%{quest_slug}%", f"%{quest_slug}%"))
    q_row = c.fetchone()

    if not q_row:
        conn.close()
        return os.path.join(OUT_DIR, "quest_card_the-gavroche-family.jpg")

    q = dict(q_row)
    c.execute("SELECT description FROM quest_objectives WHERE quest_id = ?", (q["id"],))
    objectives = [r[0] for r in c.fetchall()]
    conn.close()

    q_name = q["name"].upper()
    canvas, draw = create_base_canvas(f"QUEST CONTRACT : {q_name}", tag="MISSION INTEL")
    CARD_W, CARD_H = canvas.size

    # Left: Contract Intel
    left_box = [28, 86, 440, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    draw.text((left_box[0] + 18, left_box[1] + 16), "CHATEAU CONTRACT INTEL", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 46), f"Giver : {q.get('giver', 'Chateau Hub')}", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 80), f"Raid Map : {q.get('location', 'Jacques Bridge')}", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)

    # Objectives list
    draw.text((left_box[0] + 18, left_box[1] + 116), "MANDATORY OBJECTIVES :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    oy = left_box[1] + 142
    for obj in objectives[:5]:
        draw.text((left_box[0] + 18, oy), f"• {obj[:46]}", fill=(220, 220, 200), font=core.F_BODY)
        oy += 32

    # Rewards box
    rew_box = [left_box[0] + 16, left_box[3] - 76, left_box[2] - 16, left_box[3] - 16]
    draw.rounded_rectangle(rew_box, radius=6, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((rew_box[0] + 14, rew_box[1] + 10), "MISSION REWARD :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    rew_str = f"🎁 {q.get('reward_quantity', 1)}x {q.get('reward_item', 'Supply Ampoules')}"
    draw.text((rew_box[0] + 14, rew_box[1] + 32), rew_str, fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    # Right: Map Preview / Pin
    right_box = [460, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 16), "OPERATIONAL MAP RECON", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    map_frame = [right_box[0] + 16, right_box[1] + 46, right_box[2] - 16, right_box[3] - 16]
    draw.rounded_rectangle(map_frame, radius=8, fill=(14, 14, 12), outline=core.COLOR_GOLD, width=1)

    m_loc = q.get('location', '').lower()
    map_fn = "blank_jacques_bridge.jpg" if "jacques" in m_loc else "blank_sombre_forest.jpg" if "sombre" in m_loc else "blank_sarlat_farm.jpg"
    base_m_p = os.path.join(OUT_DIR, map_fn)
    if os.path.exists(base_m_p):
        bm = Image.open(base_m_p).convert("RGBA")
        bw, bh = bm.size
        # Crop center
        c_crop = bm.crop((int(bw * 0.2), int(bh * 0.2), int(bw * 0.8), int(bh * 0.8)))
        tw = map_frame[2] - map_frame[0] - 8
        th = map_frame[3] - map_frame[1] - 8
        c_crop = c_crop.resize((tw, th), Image.Resampling.LANCZOS)
        canvas.paste(c_crop, (map_frame[0] + 4, map_frame[1] + 4), c_crop.split()[3])

        # Draw pin
        p_draw = ImageDraw.Draw(canvas)
        px = map_frame[0] + tw // 2
        py = map_frame[1] + th // 2
        p_draw.ellipse([px - 14, py - 14, px + 14, py + 14], fill=(220, 40, 40), outline=(255, 255, 255), width=2)
        p_draw.rounded_rectangle([px + 18, py - 14, px + 220, py + 14], radius=4, fill=(16, 16, 20), outline=(220, 40, 40), width=1)
        p_draw.text((px + 24, py - 9), q["name"][:24], fill=(255, 220, 200), font=core.F_SMALL_BOLD)

    clean_fn = f"quest_card_{q['slug']}.jpg"
    return save_and_sync(canvas, clean_fn)


# ===========================================================================
# 11. BAGS & BACKPACKS (ALL 29 BAGS - CAPACITY, SLOTS & RESALE VALUES)
# ===========================================================================
def render_bag_card(bag_slug_or_name: str) -> str:
    """Render high-resolution bag profile card with exact slot count, rarity, and sell value."""
    clean = bag_slug_or_name.lower().replace(" ", "-").replace("'", "")
    conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
    c = conn.cursor()
    c.execute("SELECT slug, name, rarity, slots, sell_silver, sell_copper FROM bags_full WHERE slug LIKE ? OR name LIKE ? LIMIT 1",
              (f"%{clean}%", f"%{bag_slug_or_name}%"))
    row = c.fetchone()
    conn.close()

    if not row:
        row = ("coldstream-pack", "Coldstream Pack", "Legendary", 22, 280, 0)

    slug, name, rarity, slots, s_s, s_c = row
    rarity_cap = rarity.capitalize()
    theme_color = core.PRIO_PURPLE if rarity_cap in ["Epic", "Legendary"] else core.COLOR_GOLD

    canvas, draw = create_base_canvas(f"BAG DOSSIER : {name.upper()}", tag="EXPEDITION GEAR", border_col=theme_color)
    CARD_W, CARD_H = canvas.size

    # Left Box: Bag Icon & Badge
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_color, width=2)

    bag_img_path = os.path.join(ROOT_DIR, "assets", "items", "ID_BackBag_Epic01.webp" if slots >= 12 else "ID_HipBag_Common01.webp")
    if os.path.exists(bag_img_path):
        try:
            b_img = Image.open(bag_img_path).convert("RGBA").resize((280, 280), Image.Resampling.LANCZOS)
            canvas.paste(b_img, (left_box[0] + 36, left_box[1] + 30), b_img)
        except Exception:
            pass

    draw.rounded_rectangle([left_box[0] + 24, left_box[3] - 110, left_box[2] - 24, left_box[3] - 68],
                           radius=6, fill=(24, 20, 32), outline=theme_color, width=1)
    draw.text((left_box[0] + 36, left_box[3] - 100), f"RARITY : {rarity_cap.upper()}", fill=theme_color, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 36, left_box[3] - 50), "GEAR TYPE : INVENTORY CONTAINER", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TAG)

    rx = 404
    rw = CARD_W - 28 - rx

    # Box 1: Slots
    b1 = [rx, 86, rx + rw, 196]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=theme_color, width=2)
    draw.text((b1[0] + 20, b1[1] + 16), "INVENTORY CAPACITY", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((b1[0] + 20, b1[1] + 52), f"{slots} INVENTORY SLOTS", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((b1[0] + 20, b1[1] + 82), "Expands squad carrying capacity for raid expeditions and loot transport.", fill=(180, 180, 180), font=core.F_BODY)

    # Box 2: Resale Value
    b2 = [rx, 212, rx + rw, 322]
    draw.rounded_rectangle(b2, radius=8, fill=(22, 22, 28), outline=(60, 50, 35), width=1)
    draw.text((b2[0] + 20, b2[1] + 16), "BASE RESALE VALUE (TO MERCHANTS)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    val_str = f"{s_s} Silver {s_c} Copper" if s_s > 0 else f"{s_c} Copper"
    draw.text((b2[0] + 20, b2[1] + 52), val_str, fill=(255, 215, 0), font=core.F_HEADER_TITLE)
    draw.text((b2[0] + 20, b2[1] + 82), "Official sell price to Chateau merchants. Resale value is fixed.", fill=(180, 180, 180), font=core.F_BODY)

    # Box 3: Security & Survival Rule
    b3 = [rx, 338, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b3, radius=8, fill=(24, 18, 18), outline=(90, 40, 40), width=1)
    draw.text((b3[0] + 20, b3[1] + 16), "RAID LOSS & SAFE POUCH RULES", fill=(240, 110, 110), font=core.F_SECTION_TITLE)
    draw.text((b3[0] + 20, b3[1] + 52), "* Standard Backpack (Droppable on death).", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b3[0] + 20, b3[1] + 82), "* Keep essential quest items and keys in your Secure Pouch.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b3[0] + 20, b3[1] + 112), "* Crafted at Chateau Outfitter Workshop or found in high-tier stashes.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"bag_card_{slug}.jpg")


# ===========================================================================
# 12. TRAPS & HAZARDS (DAMAGE, RADIUS & DISARM TACTICS)
# ===========================================================================
def render_trap_hazard_card(trap_slug_or_name: str) -> str:
    """Render high-resolution tactical hazard dossier."""
    clean = trap_slug_or_name.lower().replace(" ", "-").replace("'", "")
    conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
    c = conn.cursor()
    c.execute("SELECT slug, name, damage, radius, spots FROM traps_full WHERE slug LIKE ? OR name LIKE ? LIMIT 1",
              (f"%{clean}%", f"%{trap_slug_or_name}%"))
    row = c.fetchone()
    conn.close()

    if not row:
        row = ("explosive-trap", "Explosive Trap", "60", "4 m", 115)

    slug, name, damage, radius, spots = row
    theme_color = (200, 60, 60)

    canvas, draw = create_base_canvas(f"HAZARD DOSSIER : {name.upper()}", tag="TACTICAL THREAT", border_col=theme_color)
    CARD_W, CARD_H = canvas.size

    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=(28, 14, 14), outline=theme_color, width=2)
    draw.text((left_box[0] + 24, left_box[1] + 24), "TACTICAL HAZARD", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 70), name.upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 120), "ALERT : Lethal field trap deployed in combat sectors.", fill=(220, 180, 180), font=core.F_BODY)
    draw.text((left_box[0] + 24, left_box[1] + 160), f"Map Frequency : {spots} locations", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    rx = 404
    rw = CARD_W - 28 - rx

    b1 = [rx, 86, rx + rw, 210]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=theme_color, width=1)
    draw.text((b1[0] + 20, b1[1] + 16), "DETONATION STATS", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((b1[0] + 20, b1[1] + 52), f"Base Damage : {damage} DMG", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((b1[0] + 20, b1[1] + 86), f"Trigger Radius : {radius}", fill=(255, 200, 100), font=core.F_HEADER_TAG)

    b2 = [rx, 226, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b2, radius=8, fill=(22, 22, 28), outline=core.COLOR_GOLD, width=1)
    draw.text((b2[0] + 20, b2[1] + 16), "TACTICAL MITIGATION & DISARM", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((b2[0] + 20, b2[1] + 56), "* Shoot from a safe perimeter using firearms or thrown objects.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b2[0] + 20, b2[1] + 90), "* Never sprint blindly through dense brush or doorway thresholds.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b2[0] + 20, b2[1] + 124), "* Can be weaponized against trailing pursuers or enemy squads.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"trap_card_{slug}.jpg")


# ===========================================================================
# 13. STATUS EFFECTS (BLEED, POISON, BUFFS & TREATMENT)
# ===========================================================================
def render_status_effect_card(effect_slug_or_name: str) -> str:
    """Render high-resolution status effect dossier."""
    clean = effect_slug_or_name.lower().replace(" ", "-").replace("'", "")
    conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
    c = conn.cursor()
    c.execute("SELECT slug, name, category, effect_type FROM status_effects_full WHERE slug LIKE ? OR name LIKE ? LIMIT 1",
              (f"%{clean}%", f"%{effect_slug_or_name}%"))
    row = c.fetchone()
    conn.close()

    if not row:
        row = ("light-bleed", "Light Bleed", "Status Effect", "Light Bleed Bleed Timed Affects Damage Bleed Timed x1 Damage")

    slug, name, cat, eff_type = row
    theme_color = core.PRIO_PURPLE

    canvas, draw = create_base_canvas(f"STATUS EFFECT : {name.upper()}", tag="COMBAT MODIFIER", border_col=theme_color)
    CARD_W, CARD_H = canvas.size

    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_color, width=2)
    draw.text((left_box[0] + 24, left_box[1] + 24), "COMBAT CONDITION", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 70), name.upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 120), f"Category : {cat}", fill=core.COLOR_GOLD, font=core.F_BODY)

    rx = 404
    rw = CARD_W - 28 - rx

    b1 = [rx, 86, rx + rw, 230]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=theme_color, width=1)
    draw.text((b1[0] + 20, b1[1] + 16), "MECHANICS & DAMAGE DYNAMICS", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((b1[0] + 20, b1[1] + 52), eff_type[:60], fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b1[0] + 20, b1[1] + 86), "Drains health over duration; bypasses passive armor resistance.", fill=(200, 200, 180), font=core.F_BODY)

    b2 = [rx, 246, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b2, radius=8, fill=(22, 22, 28), outline=core.COLOR_GOLD, width=1)
    draw.text((b2[0] + 20, b2[1] + 16), "TREATMENT & MEDICAL PROTOCOL", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((b2[0] + 20, b2[1] + 56), "* Apply Clean Bandage immediately to stop hemorrhage.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b2[0] + 20, b2[1] + 90), "* Ingestion of Physician Ointment restores health recovery.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"status_card_{slug}.jpg")


# ===========================================================================
# 14. GATHERING NODES (CHANCE, YIELDS & LOCATIONS)
# ===========================================================================
def render_gathering_card(node_slug_or_name: str) -> str:
    """Render high-resolution gathering node reconnaissance card."""
    clean = node_slug_or_name.lower().replace(" ", "-").replace("'", "")
    conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
    c = conn.cursor()
    c.execute("SELECT slug, name, chance, yield_range FROM gathering_full WHERE slug LIKE ? OR name LIKE ? LIMIT 1",
              (f"%{clean}%", f"%{node_slug_or_name}%"))
    row = c.fetchone()
    conn.close()

    if not row:
        row = ("garlic-bulb", "Garlic Bulb", "90 %", "2-6")

    slug, name, chance, yield_r = row
    theme_color = (60, 160, 90)

    canvas, draw = create_base_canvas(f"GATHERING RECON : {name.upper()}", tag="RESOURCE HARVEST", border_col=theme_color)
    CARD_W, CARD_H = canvas.size

    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=(16, 26, 18), outline=theme_color, width=2)
    draw.text((left_box[0] + 24, left_box[1] + 24), "HARVESTABLE RESOURCE", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 70), name.upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 120), "Primary Habitats: Sarlat Farm, Garnier Fields, Sombre Forest", fill=(180, 220, 180), font=core.F_BODY)

    rx = 404
    rw = CARD_W - 28 - rx

    b1 = [rx, 86, rx + rw, 220]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=theme_color, width=1)
    draw.text((b1[0] + 20, b1[1] + 16), "NODE HARVEST METRICS", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((b1[0] + 20, b1[1] + 52), f"Success Rate : {chance}", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((b1[0] + 20, b1[1] + 86), f"Yield Range : {yield_r} Units Per Harvest", fill=(255, 215, 0), font=core.F_HEADER_TAG)

    b2 = [rx, 236, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b2, radius=8, fill=(22, 22, 28), outline=core.COLOR_GOLD, width=1)
    draw.text((b2[0] + 20, b2[1] + 16), "CHATEAU PROFESSION UTILITY", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((b2[0] + 20, b2[1] + 56), "* Key ingredient for Cook profession stamina provisions.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b2[0] + 20, b2[1] + 90), "* Required for high-tier Artificer and Physician elixirs.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"gathering_card_{slug}.jpg")


# ===========================================================================
# 15. CONTAINERS & FIELD LOOT (SPOTS, VARIETY & TACTICS)
# ===========================================================================
def render_container_card(container_slug_or_name: str) -> str:
    """Render high-resolution container intel card."""
    clean = container_slug_or_name.lower().replace(" ", "-").replace("'", "")
    conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
    c = conn.cursor()
    c.execute("SELECT slug, name, spots, items_count FROM containers_full WHERE slug LIKE ? OR name LIKE ? LIMIT 1",
              (f"%{clean}%", f"%{container_slug_or_name}%"))
    row = c.fetchone()
    conn.close()

    if not row:
        row = ("munitions-crate", "Munitions Crate", 646, 9)

    slug, name, spots, items_count = row
    theme_color = core.COLOR_GOLD

    canvas, draw = create_base_canvas(f"CONTAINER INTEL : {name.upper()}", tag="LOOT RECON", border_col=theme_color)
    CARD_W, CARD_H = canvas.size

    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_color, width=2)

    c_img_name = slug.replace("-", "_") + ".webp"
    c_img_p = os.path.join(ROOT_DIR, "assets", "containers", c_img_name)
    if os.path.exists(c_img_p):
        try:
            c_img = Image.open(c_img_p).convert("RGBA").resize((280, 280), Image.Resampling.LANCZOS)
            canvas.paste(c_img, (left_box[0] + 36, left_box[1] + 30), c_img)
        except Exception:
            pass

    draw.text((left_box[0] + 24, left_box[3] - 70), "CONTAINER CLASS : FIELD LOOT", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    rx = 404
    rw = CARD_W - 28 - rx

    b1 = [rx, 86, rx + rw, 220]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=theme_color, width=1)
    draw.text((b1[0] + 20, b1[1] + 16), "SPAWN DISTRIBUTION", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((b1[0] + 20, b1[1] + 52), f"Total World Spots : {spots} Locations", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((b1[0] + 20, b1[1] + 86), f"Loot Pool Variety : {items_count} Unique Item Types", fill=(255, 215, 0), font=core.F_HEADER_TAG)

    b2 = [rx, 236, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b2, radius=8, fill=(22, 22, 28), outline=(60, 50, 35), width=1)
    draw.text((b2[0] + 20, b2[1] + 16), "TOP RAID MAPS & TACTICS", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((b2[0] + 20, b2[1] + 56), "* Sarlat Farm, Jacques Bridge, Sombre Forest, Chateau Catacombs.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b2[0] + 20, b2[1] + 90), "* Always prioritize searching munitions and strongboxes for high value schemas.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"container_card_{slug}.jpg")


# ===========================================================================
# 16. CANONICAL LORE & WORLDBUILDING ARCHIVE CARDS
# ===========================================================================
def render_lore_card(topic_slug: str) -> str:
    """Render high-resolution historical lore card for worldbuilding queries."""
    from co_pilot.lore_engine import LORE_DATABASE
    
    matched = None
    for k, v in LORE_DATABASE.items():
        if v["slug"] == topic_slug or k in topic_slug:
            matched = v
            break
            
    if not matched:
        matched = LORE_DATABASE["the_hunger"]

    title = matched["title_en"]
    category = matched["category"]
    body = matched["lore_en"]
    tactical = matched["tactical_en"]
    slug = matched["slug"]

    canvas, draw = create_base_canvas(f"LORE ARCHIVE : {title.upper()}", tag="HISTORICAL DOSSIER", border_col=core.COLOR_GOLD)
    CARD_W, CARD_H = canvas.size

    # Left: Portrait or Emblem
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    # Portrait detection
    portrait_p = None
    if "marie" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "characters", "marie.webp")
    elif "otto" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "characters", "otto.webp")
    elif "eva" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "characters", "eva.webp")
    elif "hugo" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "characters", "hugo.webp")
    elif "eloise" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "eloise_avatar_clean.png")
    elif "dreg" in slug: portrait_p = os.path.join(ROOT_DIR, "assets", "creatures", "dreg_farmer.png")
    else: portrait_p = os.path.join(ROOT_DIR, "assets", "eloise_avatar_clean.png")

    if portrait_p and os.path.exists(portrait_p):
        try:
            p_img = Image.open(portrait_p).convert("RGBA").resize((280, 280), Image.Resampling.LANCZOS)
            canvas.paste(p_img, (left_box[0] + 36, left_box[1] + 30), p_img)
        except Exception:
            pass

    draw.rounded_rectangle([left_box[0] + 20, left_box[3] - 110, left_box[2] - 20, left_box[3] - 68],
                           radius=6, fill=(24, 20, 16), outline=core.COLOR_GOLD, width=1)
    draw.text((left_box[0] + 30, left_box[3] - 100), f"CLASS : {category.upper()}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 30, left_box[3] - 50), "CHATEAU OFFICIAL ARCHIVES", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TAG)

    rx = 404
    rw = CARD_W - 28 - rx

    # Box 1: Canonical Chronicle
    b1 = [rx, 86, rx + rw, 360]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=core.COLOR_GOLD, width=1)
    draw.text((b1[0] + 20, b1[1] + 16), "CANONICAL WORLD CHRONICLE", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    
    # Word wrap body lines cleanly
    words = body.replace("**", "").split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 55:
            lines.append(" ".join(curr))
            curr = []
    if curr:
        lines.append(" ".join(curr))

    ly = b1[1] + 54
    for line in lines[:8]:
        draw.text((b1[0] + 20, ly), line, fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        ly += 26

    # Box 2: Tactical Relevance
    b2 = [rx, 376, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b2, radius=8, fill=(24, 20, 16), outline=(90, 70, 35), width=1)
    draw.text((b2[0] + 20, b2[1] + 16), "TACTICAL GAMEPLAY CONNECTION", fill=(255, 215, 0), font=core.F_SECTION_TITLE)
    draw.text((b2[0] + 20, b2[1] + 52), tactical[:130], fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"lore_card_{slug}.jpg")
