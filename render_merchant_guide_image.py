import os, sys
from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 2560
CANVAS_H = 1440

# Authentic Hunger Companion Theme Colors
BG_CANVAS     = (11, 11, 9)        # Deep Obsidian #0b0b09
BG_PANEL      = (18, 18, 15)       # Dark Card Panel #12120f
BG_CARD       = (25, 25, 21)       # Card Surface #191915
BG_CARD_LIGHT = (32, 32, 27)       # Inner Accent Surface #20201b
BORDER_SUBTLE = (45, 41, 33)       # Antique Bronze #2d2921
BORDER_FOCUS  = (75, 68, 52)       # Highlight Bronze #4b4434

COLOR_GOLD      = (229, 192, 123)  # Title Gold #e5c07b
COLOR_PARCHMENT = (240, 235, 224)  # Parchment White #f0ebe0
COLOR_MUTED     = (168, 160, 145)  # Muted Beige #a8a091
COLOR_DIM       = (125, 118, 105)  # Dim Bronze #7d7669

# Status Accents
COLOR_BUYABLE_GREEN = (74, 222, 128)  # #4ade80 Emerald
COLOR_BUYABLE_BG    = (20, 45, 30)
COLOR_LOOT_RED      = (248, 113, 113) # #f87171 Coral/Red
COLOR_LOOT_BG       = (48, 20, 22)
COLOR_YELLOW        = (250, 204, 21)  # #facc15 Gold Yellow
COLOR_CYAN          = (56, 189, 248)  # #38bdf8 Cauldron Cyan
COLOR_PURPLE        = (192, 132, 252) # #c084fc Trophy Purple

def load_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

SERIF_BOLD = ["C:\\Windows\\Fonts\\georgiab.ttf", "C:\\Windows\\Fonts\\cambriab.ttf"]
SERIF_REG  = ["C:\\Windows\\Fonts\\georgia.ttf", "C:\\Windows\\Fonts\\cambria.ttc"]
SANS_BOLD  = ["C:\\Windows\\Fonts\\segoeuib.ttf", "C:\\Windows\\Fonts\\arialbd.ttf"]
SANS_REG   = ["C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\arial.ttf"]

F_TITLE       = load_font(SERIF_BOLD, 25)
F_SUBTITLE    = load_font(SANS_BOLD, 13)
F_BADGE       = load_font(SANS_BOLD, 13)
F_SECTION     = load_font(SERIF_BOLD, 18)
F_SUB_SECTION = load_font(SANS_BOLD, 14)
F_ITEM_NAME   = load_font(SERIF_BOLD, 16)
F_QTY         = load_font(SANS_BOLD, 13)
F_DETAIL_BOLD = load_font(SANS_BOLD, 12)
F_DETAIL_REG  = load_font(SANS_REG, 12)
F_SMALL       = load_font(SANS_REG, 11)

DOC_DIR = r"C:\Users\PC\Documents\HungerHelper"
ITEM_DIR = os.path.join(DOC_DIR, "assets", "items")
CONT_DIR = os.path.join(DOC_DIR, "assets", "containers")

def get_item_icon(name):
    p = os.path.join(ITEM_DIR, f"{name}.png")
    if os.path.exists(p):
        try:
            return Image.open(p).convert("RGBA")
        except:
            pass
    return None

def get_cont_icon(name):
    p = os.path.join(CONT_DIR, f"{name}.webp")
    if os.path.exists(p):
        try:
            return Image.open(p).convert("RGBA")
        except:
            pass
    return None

def draw_card(img, draw, box, item_name, qty_str, quest_str, vendor_or_source, price_or_zone, tip_str, icon_name, cont_icon_name=None, is_buyable=True, hub_color=COLOR_YELLOW):
    x, y, w, h = box
    draw.rounded_rectangle([x, y, x+w, y+h], radius=6, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
    
    stripe_color = COLOR_BUYABLE_GREEN if is_buyable else COLOR_LOOT_RED
    draw.rounded_rectangle([x, y, x+4, y+h], radius=2, fill=stripe_color)
    
    icon_box_size = 50
    icon_x = x + 10
    icon_y = y + (h - icon_box_size) // 2
    draw.rounded_rectangle([icon_x, icon_y, icon_x+icon_box_size, icon_y+icon_box_size], radius=5, fill=BG_CARD_LIGHT, outline=BORDER_FOCUS, width=1)
    
    ico = get_item_icon(icon_name)
    if ico:
        ico_res = ico.resize((icon_box_size-8, icon_box_size-8), Image.Resampling.LANCZOS)
        img.paste(ico_res, (icon_x+4, icon_y+4), ico_res)
        
    c_offset_x = 0
    if cont_icon_name:
        c_ico = get_cont_icon(cont_icon_name)
        if c_ico:
            c_box_size = 36
            cx = icon_x + icon_box_size + 6
            cy = y + (h - c_box_size) // 2
            draw.rounded_rectangle([cx, cy, cx+c_box_size, cy+c_box_size], radius=4, fill=BG_CARD_LIGHT, outline=BORDER_SUBTLE, width=1)
            c_ico_res = c_ico.resize((c_box_size-6, c_box_size-6), Image.Resampling.LANCZOS)
            img.paste(c_ico_res, (cx+3, cy+3), c_ico_res)
            c_offset_x = c_box_size + 6
            
    tx = icon_x + icon_box_size + 10 + c_offset_x
    
    # Line 1: Item Name + Qty Badge + Status Pill
    draw.text((tx, y + 6), item_name, font=F_ITEM_NAME, fill=COLOR_PARCHMENT)
    name_w = int(draw.textlength(item_name, font=F_ITEM_NAME))
    badge_x = tx + name_w + 8
    
    qty_bg = COLOR_BUYABLE_BG if is_buyable else COLOR_LOOT_BG
    qty_border = COLOR_BUYABLE_GREEN if is_buyable else COLOR_LOOT_RED
    qty_text_w = int(draw.textlength(qty_str, font=F_QTY))
    draw.rounded_rectangle([badge_x, y+5, badge_x + qty_text_w + 10, y + 23], radius=4, fill=qty_bg, outline=qty_border, width=1)
    draw.text((badge_x + 5, y + 6), qty_str, font=F_QTY, fill=COLOR_PARCHMENT)
    
    status_tag = "BUYABLE" if is_buyable else "LOOT ONLY"
    tag_w = int(draw.textlength(status_tag, font=F_BADGE))
    tag_x = x + w - tag_w - 14
    draw.rounded_rectangle([tag_x - 5, y+5, tag_x + tag_w + 5, y + 23], radius=4, fill=(15, 15, 12), outline=stripe_color, width=1)
    draw.text((tag_x, y + 6), status_tag, font=F_BADGE, fill=stripe_color)
    
    # Line 2: Quest
    draw.text((tx, y + 28), "Quest: ", font=F_DETAIL_BOLD, fill=COLOR_MUTED)
    draw.text((tx + 40, y + 28), quest_str, font=F_DETAIL_REG, fill=COLOR_GOLD)
    
    # Line 3: Source / Vendor
    if is_buyable:
        draw.text((tx, y + 46), "Vendor: ", font=F_DETAIL_BOLD, fill=COLOR_MUTED)
        draw.text((tx + 48, y + 46), vendor_or_source, font=F_DETAIL_BOLD, fill=hub_color)
        if price_or_zone:
            draw.text((tx + 48 + int(draw.textlength(vendor_or_source, font=F_DETAIL_BOLD)) + 6, y + 46), f"({price_or_zone})", font=F_DETAIL_REG, fill=COLOR_DIM)
    else:
        draw.text((tx, y + 46), "Source: ", font=F_DETAIL_BOLD, fill=COLOR_MUTED)
        draw.text((tx + 48, y + 46), vendor_or_source, font=F_DETAIL_BOLD, fill=COLOR_PARCHMENT)
        if price_or_zone:
            draw.text((tx + 48 + int(draw.textlength(vendor_or_source, font=F_DETAIL_BOLD)) + 6, y + 46), f"• {price_or_zone}", font=F_DETAIL_REG, fill=COLOR_DIM)
            
    # Line 4: Tactical Intel
    draw.text((tx, y + 64), "Intel: ", font=F_DETAIL_BOLD, fill=stripe_color)
    draw.text((tx + 36, y + 64), tip_str, font=F_SMALL, fill=COLOR_MUTED)


def render():
    print("Initializing canvas 2560x1440...")
    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG_CANVAS)
    draw = ImageDraw.Draw(img)
    
    # ================= TOP HEADER BAR =================
    draw.rectangle([0, 0, CANVAS_W, 76], fill=(16, 16, 13))
    draw.line([0, 76, CANVAS_W, 76], fill=COLOR_GOLD, width=2)
    
    # Header Titles
    draw.text((24, 12), "HUNGER COMPANION // MAIN QUEST ITEM LOGISTICS & PROCUREMENT GUIDE", font=F_TITLE, fill=COLOR_GOLD)
    draw.text((26, 46), "SPEEDRUN RECON & VENDOR PROCUREMENT DIRECTORY • 48 STANDARD MAIN QUESTS • EXCLUDES UNIQUE COLLECTIBLES", font=F_SUBTITLE, fill=COLOR_MUTED)
    
    # Header Badges on Right
    badge_x = CANVAS_W - 470
    # Buyable badge
    draw.rounded_rectangle([badge_x, 20, badge_x + 210, 54], radius=5, fill=COLOR_BUYABLE_BG, outline=COLOR_BUYABLE_GREEN, width=1)
    draw.text((badge_x + 16, 27), "✔ 12 ITEMS BUYABLE", font=F_BADGE, fill=COLOR_BUYABLE_GREEN)
    
    # Loot-only badge
    draw.rounded_rectangle([badge_x + 225, 20, badge_x + 445, 54], radius=5, fill=COLOR_LOOT_BG, outline=COLOR_LOOT_RED, width=1)
    draw.text((badge_x + 241, 27), "✖ 15 LOOT ONLY (RAID)", font=F_BADGE, fill=COLOR_LOOT_RED)
    
    # ================= COLUMN LAYOUT =================
    PAD_X = 20
    PAD_Y = 90
    COL_GAP = 18
    COL_W = (CANVAS_W - (PAD_X * 2) - (COL_GAP * 2)) // 3 # ~824px
    
    COL1_X = PAD_X
    COL2_X = PAD_X + COL_W + COL_GAP
    COL3_X = PAD_X + (COL_W + COL_GAP) * 2
    
    COL_H = CANVAS_H - PAD_Y - 20 # 1330px
    
    CARD_H = 83
    CARD_GAP = 6
    
    # ------------------ COLUMN 1: BUYABLE ITEMS (ALL 12) ------------------
    # Background panel
    draw.rounded_rectangle([COL1_X, PAD_Y, COL1_X + COL_W, PAD_Y + COL_H], radius=8, fill=BG_PANEL, outline=BORDER_SUBTLE, width=1)
    
    # Col 1 Header
    draw.rectangle([COL1_X, PAD_Y, COL1_X + COL_W, PAD_Y + 54], fill=(22, 28, 22))
    draw.line([COL1_X, PAD_Y + 54, COL1_X + COL_W, PAD_Y + 54], fill=COLOR_BUYABLE_GREEN, width=2)
    draw.text((COL1_X + 16, PAD_Y + 12), "1. BUYABLE AT MERCHANTS (SAVE RAID TIME)", font=F_SECTION, fill=COLOR_BUYABLE_GREEN)
    draw.text((COL1_X + 16, PAD_Y + 35), "12 ITEMS SOLD IN HUB OR CAULDRON • SKIP HOURS OF EXTRACTION GRIND", font=F_SMALL, fill=COLOR_MUTED)
    
    c1_y = PAD_Y + 64
    
    # Group A: Outer Ramparts (Starting Hub)
    draw.text((COL1_X + 16, c1_y), "OUTER RAMPARTS ENCAMPMENT MERCHANTS (STARTING HUB)", font=F_SUB_SECTION, fill=COLOR_YELLOW)
    c1_y += 24
    
    buyable_outer = [
        ("Heavy Ammunition", "10x", "Bearing Arms (Reynauld)", "Reynauld / Piro", "~2c each", "Reynauld gives this quest and sells the ammo right at his stall.", "heavy_ammunition", COLOR_YELLOW),
        ("Longboy Weapon", "1x", "A Long Boy (Mr Sweet)", "Piro / Reynauld", "~1s 31c", "Buying directly bypasses tedious weapon crate searches.", "longboy", COLOR_YELLOW),
        ("Seamstress Needle", "5x", "Under the Skin (Piro)", "Octave de Villiers", "~15c each", "Octave's tailoring stall in the Outer Ramparts stocks these reliably.", "seamstress_needle", COLOR_YELLOW),
        ("Sealed Bloodbag", "1x", "Under the Skin (Piro)", "Piro / Dr. Moreau", "~5s 31c", "Piro sells blood supplies right beside his smoke fire.", "sealed_bloodbag", COLOR_YELLOW),
        ("Thick Branch", "2x", "Child's Play (Louis)", "Reynauld", "~18c each", "Raw timber sold by Reynauld; instant hand-in for Louis.", "thick_branch", COLOR_YELLOW),
        ("Tavern Wine", "3x", "Sweet Lubrication (Mr Sweet)", "Mr Sweet", "~18c each", "Stocked in Mr Sweet's own tavern supply rotation.", "tavern_wine", COLOR_YELLOW),
        ("Thin Mead", "3x", "Sweet Lubrication (Mr Sweet)", "Mr Sweet", "~11c each", "Cheap fermented beverage sold directly at the hub bar.", "thin_mead", COLOR_YELLOW)
    ]
    
    for item in buyable_outer:
        draw_card(img, draw, (COL1_X + 12, c1_y, COL_W - 24, CARD_H), item[0], item[1], item[2], item[3], item[4], item[5], item[6], is_buyable=True, hub_color=item[7])
        c1_y += CARD_H + CARD_GAP
        
    c1_y += 8
    # Group B: Cauldron (Deep Hub)
    draw.text((COL1_X + 16, c1_y), "THE CAULDRON PROGRESSION MERCHANTS (DEEP HUB)", font=F_SUB_SECTION, fill=COLOR_CYAN)
    c1_y += 24
    
    buyable_cauldron = [
        ("Saltpetre", "20x", "Bare Necessities (Eloise)", "Doctor Lucien Moreau", "~3c each", "HIGH PRIORITY! 20x takes forever to loot; Dr. Moreau clears this instantly.", "saltpetre", COLOR_CYAN),
        ("Tallow Balm", "10x", "Bare Necessities (Eloise)", "Doctor Lucien Moreau", "~6c each", "HIGH PRIORITY! Physician stock clears Eloise's main requirement.", "tallow_balm", COLOR_CYAN),
        ("Bezoar", "3x", "Of Blight and Bezoars (Piro)", "Doctor Lucien Moreau", "~15c each", "Rare alchemical drop in raids; buy from Dr. Moreau's clinic.", "bezoar", COLOR_CYAN),
        ("Hartshorn", "2x", "Of Blight and Bezoars (Piro)", "Doctor Lucien Moreau", "~1s 10c", "Medical reagent exclusively stocked at Moreau's apothecary.", "hartshorn", COLOR_CYAN),
        ("Fresh Egg", "5x", "Gardon's Gambit (Louis)", "Grillard", "~16c each", "Sold by Cauldron cook Grillard; saves looting farm pantries.", "fresh_egg", COLOR_CYAN)
    ]
    
    for item in buyable_cauldron:
        draw_card(img, draw, (COL1_X + 12, c1_y, COL_W - 24, CARD_H), item[0], item[1], item[2], item[3], item[4], item[5], item[6], is_buyable=True, hub_color=item[7])
        c1_y += CARD_H + CARD_GAP
        
        
    # ------------------ COLUMN 2: LOOT-ONLY CONTAINERS (9 ITEMS) ------------------
    draw.rounded_rectangle([COL2_X, PAD_Y, COL2_X + COL_W, PAD_Y + COL_H], radius=8, fill=BG_PANEL, outline=BORDER_SUBTLE, width=1)
    
    # Col 2 Header
    draw.rectangle([COL2_X, PAD_Y, COL2_X + COL_W, PAD_Y + 54], fill=(28, 20, 20))
    draw.line([COL2_X, PAD_Y + 54, COL2_X + COL_W, PAD_Y + 54], fill=COLOR_LOOT_RED, width=2)
    draw.text((COL2_X + 16, PAD_Y + 12), "2. LOOT ONLY: CONTAINER SCAVENGING", font=F_SECTION, fill=COLOR_LOOT_RED)
    draw.text((COL2_X + 16, PAD_Y + 35), "9 ITEMS NEVER SOLD BY MERCHANTS • MUST TARGET CONTAINER NODES IN RAIDS", font=F_SMALL, fill=COLOR_MUTED)
    
    c2_y = PAD_Y + 64
    draw.text((COL2_X + 16, c2_y), "CONTAINER TARGET DIRECTORY & HIGH-YIELD SPAWNS", font=F_SUB_SECTION, fill=COLOR_GOLD)
    c2_y += 24
    
    loot_containers = [
        ("Flour", "20x", "Making Dough (Eloise)", "Flour Sacks", "Château & Sarlat", "Target 40 Flour Sacks in Central Village & Granaries East of Château.", "flour", "flour_sack", "47.6% drop rate in granaries. Collect over 2-3 speedrun rotations."),
        ("Charcoal", "15x", "Last Embers (Eloise)", "Piles of Ash", "Manor Hearths", "14 Hearth spots in burnt Manor kitchens North of Village.", "charcoal", "pile_of_ash", "52.6% drop rate. Search hearth grates and burnt stoves."),
        ("Damp Rag", "5x", "Bare Necessities (Eloise)", "Tooling Bins / Desks", "Workshops & Ruins", "Check Tooling Bins near Windmill workshops and ledger desks.", "damp_rag", "tooling_bin", "High spawn rate inside mechanical maintenance bins."),
        ("China Bowl", "1x", "A Touch of Bribery (Mr Sweet)", "Wall Cabinets", "Château Interior", "Residential dining cabinets and sideboard furniture.", "china_bowl", "wall_cabinet", "Search dining rooms on 2nd floor of intact villas."),
        ("Opium", "1x", "A Touch of Bribery (Mr Sweet)", "Physician Bags", "Jacques Medicinals", "Apothecary bags and field hospital ruins.", "opium", "physician_bag", "Spawns in medical caches near infirmary tents."),
        ("Opium Pipe", "1x", "A Touch of Bribery (Mr Sweet)", "Wall Cabinets / Desks", "Château Manors", "Private quarters inside wealthy residential ruins.", "opium_pipe", "wall_cabinet", "Often paired near China Bowl spots in manor bedrooms."),
        ("Arsenic", "1x", "Of Blight and Bezoars (Piro)", "Jacques Medicinals", "Infirmary Ruins", "Toxic reagent jars in field hospital drug kits.", "arsenic", "jacques_medicinals", "Check shelf kits in field medical tents and labs."),
        ("Glass Vial", "1x", "Under the Skin (Piro)", "Physician Bags", "Medical Caches", "Common alchemical container found in doctor satchels.", "glass_vial", "physician_bag", "Guaranteed from physician kit nodes across all maps."),
        ("Silver Dish", "1x", "Under the Skin (Piro)", "Strongboxes / Desks", "Officers' Quarters", "High-tier bullion crates and officer quarters desks.", "silver_dish", "strongbox", "Requires Silver Key to access locked strongroom cases.")
    ]
    
    for item in loot_containers:
        draw_card(img, draw, (COL2_X + 12, c2_y, COL_W - 24, CARD_H), item[0], item[1], item[2], item[3], item[4], item[8], item[6], cont_icon_name=item[7], is_buyable=False)
        c2_y += CARD_H + CARD_GAP
        
        
    # ------------------ COLUMN 3: CREATURE TROPHIES + PROCUREMENT INTEL ------------------
    draw.rounded_rectangle([COL3_X, PAD_Y, COL3_X + COL_W, PAD_Y + COL_H], radius=8, fill=BG_PANEL, outline=BORDER_SUBTLE, width=1)
    
    # Col 3 Header
    draw.rectangle([COL3_X, PAD_Y, COL3_X + COL_W, PAD_Y + 54], fill=(28, 20, 24))
    draw.line([COL3_X, PAD_Y + 54, COL3_X + COL_W, PAD_Y + 54], fill=COLOR_PURPLE, width=2)
    draw.text((COL3_X + 16, PAD_Y + 12), "3. LOOT ONLY: CREATURE TROPHY HARVESTS", font=F_SECTION, fill=COLOR_PURPLE)
    draw.text((COL3_X + 16, PAD_Y + 35), "6 HARVEST OBJECTIVES FOR 'TISSUE & BLOOD' (PIRO) • HARVEST FROM ELITES", font=F_SMALL, fill=COLOR_MUTED)
    
    c3_y = PAD_Y + 64
    draw.text((COL3_X + 16, c3_y), "BESTIARY HARVEST OBJECTIVES (LOOT-ONLY)", font=F_SUB_SECTION, fill=COLOR_PURPLE)
    c3_y += 24
    
    trophies = [
        ("Dreg Head", "10x", "Tissue and Blood (Piro)", "Common Dregs", "All Maps / Trenches", "Standard infested roamers. Easy to farm in outer trenches.", "dreg_head", "Kill standard dregs with headshots; 100% head harvest rate."),
        ("Waif Head", "10x", "Tissue and Blood (Piro)", "Lurking Waifs", "Ruins & Rubble", "Agile ambushers creeping along ruined roofs and alleyways.", "waif_head", "Listen for clicking footsteps; harvest heads upon kill."),
        ("Shambler Hand", "5x", "Tissue and Blood (Piro)", "Heavy Shamblers", "Patrol Corridors", "Bulky armored infected. Slow-moving but heavy health pool.", "shambler_hand", "Aim for exposed arm joints; harvest severed hand."),
        ("Bloat Spine", "5x", "Tissue and Blood (Piro)", "Volatile Bloats", "Toxic Marshes", "Explosive bile carriers. Kill from range before detonation!", "bloat_spine", "Snipe from distance to prevent explosion destroying the spine."),
        ("Brute Foot", "1x", "Tissue and Blood (Piro)", "Armored Brutes", "Fortress Gates", "Massive apex elite. Bring high-caliber ammo or ambush with team.", "brute_foot", "Stagger with heavy explosives, then finish off legs."),
        ("Drooler Jaw", "1x", "Tissue and Blood (Piro)", "Acidic Droolers", "Canals & Cellars", "Spits corrosive acid from submerged positions.", "drooler_jaw", "Bait out of water before eliminating to loot jaw safely.")
    ]
    
    for item in trophies:
        draw_card(img, draw, (COL3_X + 12, c3_y, COL_W - 24, CARD_H), item[0], item[1], item[2], item[3], item[4], item[7], item[6], cont_icon_name=None, is_buyable=False)
        c3_y += CARD_H + CARD_GAP
        
    c3_y += 12
    # Speedrun Procurement Briefing Box
    draw.rounded_rectangle([COL3_X + 12, c3_y, COL3_X + COL_W - 12, PAD_Y + COL_H - 14], radius=6, fill=(22, 22, 18), outline=BORDER_FOCUS, width=1)
    
    # Briefing title
    draw.text((COL3_X + 24, c3_y + 12), "⚡ SPEEDRUN LOGISTICS & VENDOR TACTICS", font=F_SUB_SECTION, fill=COLOR_GOLD)
    
    tips = [
        ("1. CHECK LOUIS ON EVERY HUB RESET:", "Louis regularly stocks Silver Key (12s 60c) and Gold Key (25s 60c). Always buy them out to access high-tier Strongboxes in Château."),
        ("2. PRE-BUY SALTPETRE & TALLOW BALM:", "Do NOT waste raid slots searching Tooling Bins for 20x Saltpetre and 10x Balm. Head straight to Doctor Lucien Moreau in the Cauldron to instantly complete Eloise's 'Bare Necessities'."),
        ("3. SKIP WEAPON CRATE HUNTING:", "Mr Sweet's 'A Long Boy' quest requires delivering a Longboy weapon. Buy it directly from Piro or Reynauld in the Outer Ramparts hub for ~1s 31c."),
        ("4. HARVEST TISSUE & BLOOD PASSIVELY:", "Accept 'Tissue and Blood' from Piro immediately so monster kills during Flour/Charcoal runs count toward your 10x Dreg and 10x Waif head counts."),
        ("5. BARE NECESSITIES ROUTE:", "Buy Saltpetre & Balm from Moreau -> Only Damp Rags (5x) require raid extraction (Tooling Bins).")
    ]
    
    ty = c3_y + 36
    for title, desc in tips:
        draw.text((COL3_X + 24, ty), title, font=F_DETAIL_BOLD, fill=COLOR_YELLOW)
        # wrap desc if needed
        draw.text((COL3_X + 24, ty + 16), desc, font=F_SMALL, fill=COLOR_MUTED)
        ty += 38
        
    # Bottom watermark / status line
    draw.line([20, CANVAS_H - 24, CANVAS_W - 20, CANVAS_H - 24], fill=BORDER_SUBTLE, width=1)
    draw.text((24, CANVAS_H - 20), "HUNGER COMPANION TACTICAL RECON SYSTEM • GOOD DOG STUDIOS • SPEEDRUN PROGRESSION OPTIMIZER", font=F_SMALL, fill=COLOR_DIM)
    
    # Save Image to multiple destinations
    out_paths = [
        os.path.join(DOC_DIR, "merchant_quest_items_guide.png"),
        os.path.join(r"C:\Users\PC\Desktop\Hunger_Raid_Maps", "merchant_quest_items_guide.png"),
        os.path.join(r"C:\Users\PC\.gemini\antigravity\brain\31f232ba-f37d-4331-8fda-d6f94602b088", "merchant_quest_items_guide.png")
    ]
    
    for op in out_paths:
        try:
            os.makedirs(os.path.dirname(op), exist_ok=True)
            img.save(op, "PNG", optimize=True)
            print(f"Saved: {op}")
        except Exception as e:
            print(f"Error saving {op}: {e}")

if __name__ == "__main__":
    render()
