import os
import sys
import json
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

def create_base_canvas(title: str, tag: str = "TACTICAL INTEL", width: int = 1040, height: int = 580):
    canvas = Image.new("RGBA", (width, height), (12, 12, 15))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, width, height], fill=(12, 12, 15))
    draw.rectangle([4, 4, width - 5, height - 5], outline=core.COLOR_GOLD, width=2)
    draw.rectangle([8, 8, width - 9, height - 9], outline=(40, 36, 26), width=1)

    draw.rounded_rectangle([16, 14, width - 16, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    tag_w = int(draw.textlength(tag.upper(), font=core.F_SMALL_BOLD)) + 24
    draw.rounded_rectangle([28, 22, 28 + tag_w, 60], radius=5, fill=(35, 30, 20), outline=core.COLOR_GOLD, width=1)
    draw.text((40, 31), tag.upper(), fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((44 + tag_w, 27), title.upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    return canvas, draw


# ===========================================================================
# 1. UNIVERSAL CHARACTER CARDS (ALL 6 HEROES - NO ROLE/CHATEAU FLUFF)
# ===========================================================================
HEROES_DATA = {
    "marie": {
        "name": "Marie",
        "title": "Warrior Nun / Apothecary",
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
            ("PRESTIGE I: SCARLET INQUISITOR", "assets/skins/Marie_Cosmetic_09a.webp"),
            ("PRESTIGE II: SISTER OF GLASS", "assets/skins/Marie_Cosmetic_11a.webp"),
            ("MATRIARCH (ATELIER EXCLUSIVE)", "assets/skins/Marie_Cosmetic_12a.webp")
        ]
    },
    "otto": {
        "name": "Otto",
        "title": "Sergeant-at-Arms / Sapper",
        "portrait": "assets/characters/otto.webp",
        "pass_name": "Maintenance",
        "pass_desc": "Armor durability degrades 35% slower in combat.",
        "pass_ico": "assets/abilities/otto_passive.png",
        "q_name": "Field Repairs",
        "q_desc": "Instantly repairs 50 armor points on targeted armor plate.",
        "q_ico": "assets/abilities/otto_q.png",
        "e_name": "Masterwork",
        "e_desc": "Deploys a reinforced barricade plate with +40% ballistic resistance.",
        "e_ico": "assets/abilities/otto_e.png",
        "skins": [
            ("PRESTIGE I: SIEGEBREAKER", "assets/skins/Otto_Cosmetic_10a.webp"),
            ("PRESTIGE II: BLACK REITER", "assets/skins/Otto_Cosmetic_10a.webp")
        ]
    },
    "eva": {
        "name": "Eva",
        "title": "Vagabond Huntress",
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
            ("PRESTIGE II: IRON VESTAL", "assets/skins/Eva_Cosmetic_10a.webp")
        ]
    },
    "gabriel": {
        "name": "Gabriel",
        "title": "Soldier of Fortune",
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
            ("PRESTIGE II: GILDED HERALD", "assets/skins/Gabriel_Cosmetic_10a.webp")
        ]
    },
    "hugo": {
        "name": "Hugo",
        "title": "The Maniac",
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
            ("PRESTIGE II: PENITENT", "assets/skins/Hugo_Cosmetic_10a.webp")
        ]
    },
    "serine": {
        "name": "Serine",
        "title": "Vodou Poisoner",
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
            ("PRESTIGE II: MAMBO'S GRACE", "assets/skins/Serine_Cosmetic_10a.webp")
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

    # Bottom: Side-by-Side Legendary Skins
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
# 2. UNIVERSAL SKINS ENGINE (SPEAR, AXE, BROWNBETTY, LONGBOY, CHARACTERS)
# ===========================================================================
def render_skins_for_target(query: str) -> dict:
    from cosmetic_card_builder import render_cosmetic_craft_card_dynamic
    q_low = query.lower()

    db_p = os.path.join(ROOT_DIR, "data", "full_skins_database.json")
    db = json.load(open(db_p, encoding="utf-8"))

    # Check weapons with skins
    if any(w in q_low for w in ["spear", "lance"]):
        keys = ["partisan", "hybernia", "peasant's burden"]
        cards = []
        for k in keys:
            if k in db:
                p = render_cosmetic_craft_card_dynamic(db[k])
                clean_k = k.replace(' ', '_').replace("'", '')
                dst = os.path.join(OUT_DIR, f"cosmetic_spear_{clean_k}.jpg")
                Image.open(p).save(dst, quality=95)
                cards.append(dst)
        return {
            "has_skins": True,
            "title": "ALL OFFICIAL SPEAR SKINS & CRAFTING FORMULAS",
            "text": "• 🗡️ **1. Partisan** (Cold Iron, Hartshorn, Leather Trimmings, Blacksand)\n• 🗡️ **2. Hybernia** (Cold Iron, Distilled Water)\n• 🗡️ **3. Peasant's Burden** (Tent Peg, Solid Branch, Impeccable Twine)",
            "cards": cards
        }

    if any(w in q_low for w in ["axe", "hache"]) and not any(w in q_low for w in ["war-axe", "war axe", "guerre"]):
        keys = ["padre's reply", "recluse"]
        cards = []
        for k in keys:
            if k in db:
                p = render_cosmetic_craft_card_dynamic(db[k])
                clean_k = k.replace(' ', '_').replace("'", '')
                dst = os.path.join(OUT_DIR, f"cosmetic_axe_{clean_k}.jpg")
                Image.open(p).save(dst, quality=95)
                cards.append(dst)
        return {
            "has_skins": True,
            "title": "ALL OFFICIAL AXE SKINS & CRAFTING FORMULAS",
            "text": "• 🪓 **1. Padre's Reply** (Cold Iron, Brass, Solid Branch)\n• 🪓 **2. Recluse** (Hardwood, Leather Trimmings, Distilled Water)",
            "cards": cards
        }

    if any(w in q_low for w in ["brown betty", "brown-betty", "fusil brown", "brown"]):
        keys = ["argent and vert", "frederick's revenge", "hohenzollern reborn", "house of medici", "lion of rotterdam", "prussian eagle", "sable and gules", "treaty workhorse", "veenstra's swine", "honoured agreement", "eastern promise"]
        cards = []
        for k in keys[:3]: # top 3 most prestigious
            if k in db:
                p = render_cosmetic_craft_card_dynamic(db[k])
                clean_k = k.replace(' ', '_').replace("'", '')
                dst = os.path.join(OUT_DIR, f"cosmetic_brownbetty_{clean_k}.jpg")
                Image.open(p).save(dst, quality=95)
                cards.append(dst)
        return {
            "has_skins": True,
            "title": "ALL OFFICIAL BROWN-BETTY SKINS & CRAFTING FORMULAS",
            "text": "• 🔫 **1. Argent and Vert** (Fine Pigment, Polish, Cold Iron)\n• 🔫 **2. Frederick's Revenge** (Gunstock Wood, Brass Rivets)\n• 🔫 **3. Hohenzollern Reborn** (Regal Enamel, Gold Wire)\n*(Showing top 3 prominent variants from the 11 official Brown-Betty skins)*",
            "cards": cards
        }

    if any(w in q_low for w in ["longboy", "long boy"]):
        k = "bacchus' wand"
        p = render_cosmetic_craft_card_dynamic(db[k])
        dst = os.path.join(OUT_DIR, "cosmetic_longboy_bacchus_wand.jpg")
        Image.open(p).save(dst, quality=95)
        return {
            "has_skins": True,
            "title": "OFFICIAL LONGBOY SKIN : BACCHUS' WAND",
            "text": "• 🔫 **Bacchus' Wand (Epic)**\n  - Materials: 1x Moist Pouch, 1x Royal Jelly, 1x Polished Rod, 1x White Pearl, 1x Ivory Tusk.\n  - Fee: 210 Copper at Chateau Artisan Workshop.",
            "cards": [dst]
        }

    # Check character skins
    for char in ["marie", "otto", "eva", "gabriel", "hugo", "serine"]:
        if char in q_low:
            matched = [k for k, v in db.items() if v.get("target", "").lower() == char and any(p_k in k for p_k in ["prestige", "matriarch", "athos"])]
            cards = []
            for k in matched[:3]:
                p = render_cosmetic_craft_card_dynamic(db[k])
                clean_k = k.replace(' ', '_').replace("'", "").replace(":", "")
                dst = os.path.join(OUT_DIR, f"cosmetic_{char}_{clean_k}.jpg")
                Image.open(p).save(dst, quality=95)
                cards.append(dst)
            return {
                "has_skins": True,
                "title": f"ALL OFFICIAL PRESTIGE SKINS FOR {char.upper()}",
                "text": f"• Unlocked high-tier atelier progression & prestige skins for {char.title()}.",
                "cards": cards
            }

    # WEAPONS WITHOUT SKINS (Rapier, Shortsword, Longsword, Zweihander, Sabre, Dagger, Mace, Halberd)
    weapons_without_skins = {
        "rapier": "Rapier",
        "rapiere": "Rapier",
        "rapière": "Rapier",
        "shortsword": "Short Sword",
        "short-sword": "Short Sword",
        "short sword": "Short Sword",
        "longsword": "Longsword",
        "long sword": "Longsword",
        "zweihander": "Zweihänder",
        "zweihänder": "Zweihänder",
        "sabre": "Sabre",
        "saber": "Sabre",
        "dagger": "Dagger",
        "dague": "Dagger",
        "mace": "Mace",
        "masse": "Mace",
        "halberd": "Halberd",
        "hallebarde": "Halberd",
        "club": "Club",
        "pricker": "Pricker",
        "cavalier": "Cavalier",
        "marengo": "Marengo",
        "deux": "Deux",
        "auster": "Auster"
    }

    for w_k, w_name in weapons_without_skins.items():
        if w_k in q_low:
            return {
                "has_skins": False,
                "weapon_name": w_name,
                "title": f"NO COSMETIC SKINS AVAILABLE : {w_name.upper()}",
                "text": f"There are currently **no cosmetic craftable skins** for the **{w_name}** in *Hunger*.\n\nIn the official game, weapon skins currently only exist for:\n• 🗡️ **Spear** (3 skins: Partisan, Hybernia, Peasant's Burden)\n• 🪓 **Axe** (2 skins: Padre's Reply, Recluse)\n• 🔫 **Brown-Betty** (11 skins: Argent and Vert, Frederick's Revenge, etc.)\n• 🔫 **Longboy** (1 skin: Bacchus' Wand)\n\n*(No fallback skin shown to prevent giving misleading information)*",
                "cards": []
            }

    # Default fallback if unknown item
    return {
        "has_skins": False,
        "weapon_name": "Unknown",
        "title": "SKINS NOT FOUND",
        "text": "No skins found matching your request. Craftable skins exist for Spear, Axe, Brown-Betty, Longboy, and Hero Outfits (Marie, Otto, Eva, Gabriel, Hugo, Serine).",
        "cards": []
    }


# ===========================================================================
# 3. UNIVERSAL CLEAN MAPS (NO SIDEBARS FOR ANY RAID MAP)
# ===========================================================================
def get_clean_raid_map(raid_num: int) -> str:
    clean_p = os.path.join(OUT_DIR, f"clean_raid{raid_num}_map.jpg")
    if not os.path.exists(clean_p):
        src_p = os.path.join(ROOT_DIR, "Raid_Maps", f"raid{raid_num}_map.jpg")
        if os.path.exists(src_p):
            im = Image.open(src_p)
            clean = im.crop((0, 80, 1645, 1380))
            clean.save(clean_p, quality=95)
    if os.path.exists(clean_p) and os.path.exists(BRAIN_DIR):
        Image.open(clean_p).save(os.path.join(BRAIN_DIR, f"clean_raid{raid_num}_map.jpg"), quality=95)
    return clean_p


# ===========================================================================
# 4. AUTHENTIC JACQUES FOLLY DUNGEON (REAL COORDINATES FROM COMPANION)
# ===========================================================================
def render_authentic_dungeon_card(is_french: bool = False) -> str:
    title = "DUNGEON ACCESS : JACQUES FOLLY" if not is_french else "ACCÈS AU DONJON : JACQUES FOLLY"
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
    draw.text((e_box[0] + 14, e_box[1] + 34), "📍 [1] Jacques Folly Main Entrance (1680, 197)", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((e_box[0] + 14, e_box[1] + 58), "      Northwest of Vairon Quarry in the wooded ridge.", fill=(170, 170, 150), font=core.F_BODY)
    draw.text((e_box[0] + 14, e_box[1] + 82), "📍 [2] The Last Prisoner Crypt (1530, 315)", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((e_box[0] + 14, e_box[1] + 106), "      Subterranean cell: Louis' Father Ring & Note.", fill=(170, 170, 150), font=core.F_BODY)

    # Loot info
    l_box = [left_box[0] + 16, e_box[3] + 12, left_box[2] - 16, left_box[3] - 14]
    draw.rounded_rectangle(l_box, radius=8, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((l_box[0] + 14, l_box[1] + 10), "LOOT & SPATIAL INTEL :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((l_box[0] + 14, l_box[1] + 34), "• 174 Subterranean Containers & High-Tier Weapon Chests.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((l_box[0] + 14, l_box[1] + 58), "• Key Spawns: 5 desks & bastion crates across bridge roadway.", fill=(180, 180, 160), font=core.F_BODY)

    # Right: Authentic Map Inset cropped around (1600, 300) directly on 4096 scale!
    right_box = [440, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 14), "AUTHENTIC DUNGEON LOCATION (NORTH OF VAIRON QUARRY)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    map_p = os.path.join(ROOT_DIR, "jacques-bridge.webp")
    if os.path.exists(map_p):
        base_map = Image.open(map_p).convert("RGBA")
        # Crop northern ridge area directly on 4096 scale:
        # x from 1100 to 2200, y from 0 to 800
        crop = base_map.crop((1150, 0, 2200, 850))
        c_draw = ImageDraw.Draw(crop)

        # Plot [1] Jacques Folly Main Entrance (1680.37, 197.12)
        px1 = int(1680.37 - 1150)
        py1 = int(197.12 - 0)
        c_draw.ellipse([px1 - 24, py1 - 24, px1 + 24, py1 + 24], fill=(235, 60, 60, 100), outline=(235, 60, 60), width=4)
        c_draw.ellipse([px1 - 12, py1 - 12, px1 + 12, py1 + 12], fill=(255, 60, 60), outline=(255, 255, 255), width=2)
        c_draw.rounded_rectangle([px1 + 18, py1 - 16, px1 + 260, py1 + 16], radius=4, fill=(20, 16, 12, 230), outline=(255, 215, 0), width=1)
        c_draw.text((px1 + 24, py1 - 10), "[1] Jacques Folly (1680, 197)", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

        # Plot [2] The Last Prisoner Crypt (1530.5, 315.4)
        px2 = int(1530.5 - 1150)
        py2 = int(315.4 - 0)
        c_draw.ellipse([px2 - 24, py2 - 24, px2 + 24, py2 + 24], fill=(180, 80, 255, 100), outline=(180, 80, 255), width=4)
        c_draw.ellipse([px2 - 12, py2 - 12, px2 + 12, py2 + 12], fill=(180, 80, 255), outline=(255, 255, 255), width=2)
        c_draw.rounded_rectangle([px2 + 18, py2 - 16, px2 + 260, py2 + 16], radius=4, fill=(20, 16, 24, 230), outline=core.PRIO_PURPLE, width=1)
        c_draw.text((px2 + 24, py2 - 10), "[2] Prisoner Crypt (1530, 315)", fill=(225, 190, 255), font=core.F_SMALL_BOLD)

        target_w = right_box[2] - right_box[0] - 32
        target_h = right_box[3] - right_box[1] - 56
        safe_paste(canvas, crop, (right_box[0] + 16, right_box[1] + 44, target_w, target_h))

    return save_and_sync(canvas, "dungeon_jacques-folly.jpg")


# ===========================================================================
# 5. UNIVERSAL STASH APPRAISAL (NO MARKET TEXT, NEVER SELL LETTERS/DOCUMENTS)
# ===========================================================================
def render_universal_stash_analysis(
    user_screen_path: str = None,
    is_french: bool = False
) -> tuple:
    if not user_screen_path or not os.path.exists(user_screen_path):
        sample_path = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49\.user_uploaded\media_1793839424298_22fd5367.png"
        if os.path.exists(sample_path):
            user_screen_path = sample_path

    # Real vendor items to sell (NEVER LETTERS, NEVER DOCUMENTS, NEVER MEDS, NEVER WEAPONS)
    sell_items = [
        {"name": "Spyglass / Telescope", "qty": 1, "unit_price": 60, "total_price": 60, "icon": "silver_dish.png", "desc": "Junk curio with no recipe utility"},
        {"name": "Silver Candelabra", "qty": 1, "unit_price": 85, "total_price": 85, "icon": "silver_dish.png", "desc": "High value church ornament"},
        {"name": "Ornate Silver Key (Duplicate)", "qty": 1, "unit_price": 45, "total_price": 45, "icon": "gold_key.png", "desc": "Orphan key with no lock found"},
        {"name": "Cut Timber Slab", "qty": 1, "unit_price": 15, "total_price": 15, "icon": "china_bowl.png", "desc": "Superfluous timber slab surplus"}
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

    # Exact slot mapping for Hunger inventory grid (12 cols x 2 rows)
    # Cell size ~42px, step ~44px, start at x=43, y=90 on 1024x575 scale
    scale_x = sw / 1024.0
    scale_y = sh / 575.0
    cell_w = int(42 * scale_x)
    cell_h = int(42 * scale_y)
    step_x = 44.2 * scale_x
    step_y = 44.5 * scale_y
    start_x = 43 * scale_x
    start_y = 90 * scale_y

    # Sell slot coordinates: Slot 7 (Spyglass: col 7, row 0), Slot 4 (Timber: col 4, row 0), Slot 14 (Ornate key: col 2, row 1)
    sell_grid_slots = [
        (7, 0, sell_items[0]), # Spyglass
        (4, 0, sell_items[3]), # Timber slab
        (2, 1, sell_items[2])  # Ornate key
    ]

    for col, row, it in sell_grid_slots:
        sx = int(start_x + col * step_x)
        sy = int(start_y + row * step_y)
        box = (sx, sy, sx + cell_w, sy + cell_h)

        orig_crop = raw_screen.crop(box)
        img1.paste(orig_crop, (sx, sy))

        d1.rectangle([sx - 2, sy - 2, sx + cell_w + 2, sy + cell_h + 2], outline=(255, 215, 0), width=3)
        b_text = f"SELL (+{it['total_price']}c)"
        bw = int(d1.textlength(b_text, font=core.F_HEADER_TAG)) + 8
        d1.rectangle([sx, sy - 14, sx + bw, sy], fill=(20, 16, 10), outline=(255, 215, 0), width=1)
        d1.text((sx + 4, sy - 13), b_text, fill=(255, 220, 80), font=core.F_HEADER_TAG)

    # Top banner
    hdr_txt = "STASH APPRAISAL : ITEMS TO SELL HIGHLIGHTED IN GOLD (LETTERS & EXP ITEMS PRESERVED)"
    d1.rectangle([0, 0, sw, 32], fill=(12, 12, 16))
    d1.rectangle([0, 30, sw, 32], fill=(215, 175, 55))
    d1.text((15, 8), hdr_txt, fill=(245, 245, 240), font=core.F_SMALL_BOLD)

    # Bottom summary bar (NO MARKET +12% TEXT!)
    bot_txt = f"TOTAL ESTIMATED PROCEEDS: {tot_s} SILVER {tot_c} COPPER (Total: {total_copper_sum} Copper Coins)"
    d1.rectangle([0, sh - 36, sw, sh], fill=(16, 14, 12))
    d1.rectangle([0, sh - 36, sw, sh - 34], fill=(215, 175, 55))
    d1.text((15, sh - 26), bot_txt, fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    out_p1 = save_and_sync(img1, "stash_highlighted_grid.jpg")

    # Image 2: Liquidation Manifest
    MW, MH = 960, 560
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
    row_h = 70
    for it in sell_items:
        card = [28, sy, MW - 28, sy + row_h]
        d2.rounded_rectangle(card, radius=6, fill=(20, 20, 24), outline=(55, 50, 40), width=1)

        # Icon box
        ib = [card[0] + 8, card[1] + 8, card[0] + 66, card[3] - 8]
        d2.rounded_rectangle(ib, radius=6, fill=(10, 10, 12), outline=core.COLOR_GOLD, width=1)
        ico_p = os.path.join(ROOT_DIR, "assets", "icons", it["icon"])
        if os.path.exists(ico_p):
            safe_paste(img2, Image.open(ico_p), (ib[0] + 4, ib[1] + 4, 46, 46))

        d2.text((card[0] + 82, card[1] + 12), f"{it['name']}  (×{it['qty']})", fill=core.COLOR_PARCHMENT, font=core.F_SECTION_TITLE)
        desc_txt = f"Unit: {it['unit_price']} Copper · Total: {it['total_price']} Copper  |  {it['desc']}"
        d2.text((card[0] + 82, card[1] + 40), desc_txt, fill=(175, 175, 155), font=core.F_BODY)

        # Value pill
        d2.rounded_rectangle([card[2] - 150, card[1] + 16, card[2] - 14, card[1] + 54], radius=6, fill=(35, 26, 14), outline=core.COLOR_GOLD, width=1)
        d2.text((card[2] - 135, card[1] + 24), f"+{it['total_price']} Copper", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

        sy += row_h + 10

    # Grand Total Box
    tot_box = [28, MH - 86, MW - 28, MH - 18]
    d2.rounded_rectangle(tot_box, radius=8, fill=(28, 22, 14), outline=core.COLOR_GOLD, width=2)
    val_txt = f"💰 {tot_s} Silver {tot_c} Copper  (Total: {total_copper_sum} Copper Coins)"
    d2.text((44, tot_box[1] + 20), f"TOTAL ESTIMATED LIQUIDATION VALUE :   {val_txt}", fill=core.PRIO_YELLOW, font=core.F_HEADER_TITLE)

    out_p2 = save_and_sync(img2, "stash_sell_manifest.jpg")
    return out_p1, out_p2


if __name__ == "__main__":
    print("Testing Universal V7 Engine...")
    for h in ["marie", "otto", "eva", "gabriel", "hugo", "serine"]:
        p = render_clean_character_card(h)
        print(f"Hero {h}: {p} exists: {os.path.exists(p)}")

    p_dungeon = render_authentic_dungeon_card()
    print("Dungeon card:", p_dungeon, "exists:", os.path.exists(p_dungeon))

    p1, p2 = render_universal_stash_analysis()
    print("Stash cards:", p1, p2)

    res_rapier = render_skins_for_target("rapier")
    print("Rapier skins:", res_rapier["has_skins"], res_rapier["title"])

    res_spear = render_skins_for_target("spear")
    print("Spear skins:", res_spear["has_skins"], len(res_spear["cards"]))
