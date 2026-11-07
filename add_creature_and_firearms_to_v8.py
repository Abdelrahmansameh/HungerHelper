# -*- coding: utf-8 -*-
import os

code_to_add = r'''

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
# 9. PURE ENGLISH FIREARMS PROFILES (MARENGO, DRAK, LASHER, AUSTER, DEUX, LONGBOY)
# ===========================================================================
FIREARMS_DATABASE = {
    "marengo": {
        "slug": "marengo",
        "name": "Marengo",
        "rarity": "Epic",
        "type": "Pistol",
        "damage": 39,
        "headshot": 68,
        "clip": 6,
        "rate": "0.5s",
        "reload": "3.0s",
        "ammo": "Heavy Ammunition",
        "sell": "0 Silver 42 Copper",
        "vendor": "Voyant the Rifleman (42s 38c)",
        "lore": "An early lever-action prototype revolver offering rapid sustained fire."
    },
    "drak": {
        "slug": "drak",
        "name": "Drak",
        "rarity": "Legendary",
        "type": "Rifle",
        "damage": 107,
        "headshot": 192,
        "clip": 1,
        "rate": "0.5s",
        "reload": "3.2s",
        "ammo": "Exotic Ammunition",
        "sell": "4 Silver 25 Copper",
        "vendor": "Ambrose's Tithe (Loot exclusive)",
        "lore": "An immense large-bore rifle hurling a monstrous steel slug with terrifying stopping power."
    },
    "lasher": {
        "slug": "lasher",
        "name": "Lasher",
        "rarity": "Epic",
        "type": "Rifle",
        "damage": 30,
        "headshot": 52,
        "clip": 14,
        "rate": "0.2s",
        "reload": "3.9s",
        "ammo": "Heavy Ammunition",
        "sell": "0 Silver 86 Copper",
        "vendor": "Voyant the Rifleman (86s 36c)",
        "lore": "A vicious chain-fed repeater that rattles and spits smoke with every rapid shot fired."
    },
    "auster": {
        "slug": "auster",
        "name": "Auster",
        "rarity": "Uncommon",
        "type": "Pistol",
        "damage": 48,
        "headshot": 78,
        "clip": 2,
        "rate": "0.25s (Double-tap)",
        "reload": "12.6s",
        "ammo": "Rough Ammunition",
        "sell": "3 Silver 50 Copper",
        "vendor": "Octave de Villiers (3s 50c)",
        "lore": "Fast twin-barrel self-defense firearm delivering an instant double-tap punch."
    },
    "deux": {
        "slug": "deux",
        "name": "Deux",
        "rarity": "Rare",
        "type": "Pistol",
        "damage": 54,
        "headshot": 86,
        "clip": 2,
        "rate": "2.0s",
        "reload": "8.6s",
        "ammo": "Rough Ammunition",
        "sell": "5 Silver 0 Copper",
        "vendor": "Voyant the Rifleman (5s 0c)",
        "lore": "Heavy twin-barrel rotary pistol built to punch through reinforced raid armor."
    },
    "longboy": {
        "slug": "longboy",
        "name": "LongBoy",
        "rarity": "Rare",
        "type": "Rifle",
        "damage": 58,
        "headshot": 104,
        "clip": 1,
        "rate": "Single Precision Shot",
        "reload": "6.5s",
        "ammo": "Heavy Ammunition",
        "sell": "6 Silver 50 Copper",
        "vendor": "Voyant the Rifleman (6s 50c)",
        "lore": "Long-range marksman rifle capable of delivering lethal long-range headshots."
    }
}

def render_pure_english_firearm_card(firearm_key: str = "marengo", is_french: bool = False) -> str:
    fk = firearm_key.lower().strip()
    f_data = None
    for k, v in FIREARMS_DATABASE.items():
        if k in fk or v["name"].lower() in fk:
            f_data = v
            break
    if not f_data:
        f_data = FIREARMS_DATABASE["marengo"]

    f_name = f_data["name"].upper()
    rarity = f_data["rarity"].upper()
    theme_col = core.PRIO_PURPLE if rarity in ["EPIC", "LEGENDARY"] else core.COLOR_GOLD

    canvas, draw = create_base_canvas(f"FIREARM DOSSIER : {f_name} ({rarity})", tag="GUNPLAY RECON", border_col=theme_col)
    CARD_W, CARD_H = canvas.size

    # Left: Stats & Value
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_col, width=2)

    # Ballistic specs
    draw.text((left_box[0] + 18, left_box[1] + 16), "BALLISTIC SPECIFICATIONS", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    specs = [
        ("Base Damage (≤40m)", f"{f_data['damage']} dmg per round"),
        ("Headshot Critical", f"{f_data['headshot']} critical dmg"),
        ("Magazine Capacity", f"{f_data['clip']} round(s) chambered"),
        ("Fire Rate Interval", f_data["rate"]),
        ("Tactical Reload", f"{f_data['reload']} full cycle"),
        ("Ammunition Type", f_data["ammo"]),
        ("Chateau Market Value", f_data["sell"]),
        ("Merchant Acquisition", f_data["vendor"][:28])
    ]

    sy = left_box[1] + 48
    for lbl, val in specs:
        draw.text((left_box[0] + 18, sy), f"• {lbl} :", fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
        draw.text((left_box[0] + 28, sy + 20), val, fill=core.PRIO_YELLOW if "dmg" in val else (180, 180, 160), font=core.F_BODY)
        sy += 42

    # Right: Full Hit-To-Kill Table vs Armored Players
    right_box = [400, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 14), "HIT TO KILL (HTK) VS RAID TARGETS", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    tiers = [
        ("Naked Player (100 HP)", 100, (180, 180, 170)),
        ("Green / Leather Armor (140 HP)", 140, (100, 220, 100)),
        ("Blue / Sapper Armor (160 HP)", 160, (100, 180, 255)),
        ("Epic / Reinforced Armor (180 HP)", 180, (215, 140, 255)),
        ("Full Legendary Armor (200 HP)", 200, (255, 215, 80))
    ]

    f_dmg = f_data["damage"]
    f_head = f_data["headshot"]

    ty = right_box[1] + 46
    row_h = 56
    for t_lbl, hp, col in tiers:
        head_htk = max(1, int(-(-hp // f_head)))
        body_htk = max(1, int(-(-hp // f_dmg)))

        row_box = [right_box[0] + 16, ty, right_box[2] - 16, ty + row_h]
        draw.rounded_rectangle(row_box, radius=6, fill=(18, 18, 22), outline=(45, 40, 32), width=1)

        draw.text((row_box[0] + 14, row_box[1] + 8), t_lbl, fill=col, font=core.F_SMALL_BOLD)

        # Head pill
        h_pill = [row_box[0] + 14, row_box[1] + 28, row_box[0] + 150, row_box[3] - 6]
        draw.rounded_rectangle(h_pill, radius=4, fill=(35, 18, 16), outline=(220, 70, 50), width=1)
        draw.text((h_pill[0] + 10, h_pill[1] + 3), f"🎯 Head: {head_htk} shot(s)", fill=(255, 170, 150), font=core.F_HEADER_TAG)

        # Body pill
        b_pill = [row_box[0] + 160, row_box[1] + 28, row_box[0] + 300, row_box[3] - 6]
        draw.rounded_rectangle(b_pill, radius=4, fill=(16, 26, 35), outline=(70, 140, 220), width=1)
        draw.text((b_pill[0] + 10, b_pill[1] + 3), f"🛡️ Body: {body_htk} shot(s)", fill=(170, 215, 255), font=core.F_HEADER_TAG)

        ty += row_h + 8

    # Bottom Gunplay Tip
    tip_b = [right_box[0] + 16, right_box[3] - 56, right_box[2] - 16, right_box[3] - 12]
    draw.rounded_rectangle(tip_b, radius=6, fill=(24, 20, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((tip_b[0] + 14, tip_b[1] + 6), f"🎯 Ballistic Combat Advice : With {f_data['name']}, always aim for the head to maximize critical multiplier.", fill=core.COLOR_GOLD, font=core.F_BODY)
    draw.text((tip_b[0] + 14, tip_b[1] + 24), f"Chambering: {f_data['ammo']}. Ensure full reload cover before engaging armored targets.", fill=(180, 175, 160), font=core.F_BODY)

    clean_fn = f"firearm_{f_data['slug']}.jpg"
    return save_and_sync(canvas, clean_fn)


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
'''

with open("universal_v8_engine.py", "a", encoding="utf-8") as f:
    f.write(code_to_add)

print("Successfully added Creatures, Firearms, 2H Melee, and Dynamic Quests to universal_v8_engine.py!")
