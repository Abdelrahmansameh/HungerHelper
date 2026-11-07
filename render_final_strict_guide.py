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

# Strict Rarity Hierarchy: Yellow (Rarest) -> Purple -> Blue -> Green -> Grey (Most Common / 100%)
COLOR_YELLOW = (250, 204, 21)   # #facc15 - Rarest (< 15%)
COLOR_PURPLE = (192, 132, 252)  # #c084fc - Rare (15% - 35%)
COLOR_BLUE   = (56, 189, 248)   # #38bdf8 - Uncommon (40% - 60%)
COLOR_GREEN  = (74, 222, 128)   # #4ade80 - Common (70% - 85%)
COLOR_GREY   = (148, 163, 184)  # #94a3b8 - Most Common / Guaranteed (100%)

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

F_TITLE       = load_font(SERIF_BOLD, 26)
F_BADGE       = load_font(SANS_BOLD, 13)
F_SEC_TITLE   = load_font(SERIF_BOLD, 18)
F_SUB_TITLE   = load_font(SANS_BOLD, 13)
F_ITEM_NAME   = load_font(SERIF_BOLD, 16)
F_QTY         = load_font(SANS_BOLD, 13)
F_DETAIL_BOLD = load_font(SANS_BOLD, 12)
F_DETAIL_REG  = load_font(SANS_REG, 12)

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

# ================= DATA SETS =================
# 1. BUYABLE: SEPARATED INTO OUTER RAMPARTS & CAULDRON
# (Saltpetre & Tallow Balm REMOVED from Cauldron because they are required in Eloise's questline before Cauldron unlocks)
BUYABLE_OUTER_RAMPARTS = [
    {
        "name": "Heavy Ammunition", "qty": "10x", "quest": "Bearing Arms (Reynauld)",
        "merchant": "Reynauld / Piro", "chance": "100%", "rarity": "Guaranteed",
        "icon": "heavy_ammunition", "color": COLOR_GREY
    },
    {
        "name": "Thick Branch", "qty": "2x", "quest": "Child's Play (Louis)",
        "merchant": "Reynauld", "chance": "100%", "rarity": "Guaranteed",
        "icon": "thick_branch", "color": COLOR_GREY
    },
    {
        "name": "Tavern Wine", "qty": "3x", "quest": "Sweet Lubrication (Mr Sweet)",
        "merchant": "Mr Sweet", "chance": "100%", "rarity": "Guaranteed",
        "icon": "tavern_wine", "color": COLOR_GREY
    },
    {
        "name": "Thin Mead", "qty": "3x", "quest": "Sweet Lubrication (Mr Sweet)",
        "merchant": "Mr Sweet", "chance": "100%", "rarity": "Guaranteed",
        "icon": "thin_mead", "color": COLOR_GREY
    },
    {
        "name": "Seamstress Needle", "qty": "5x", "quest": "Under the Skin (Piro)",
        "merchant": "Octave de Villiers", "chance": "85%", "rarity": "Common",
        "icon": "seamstress_needle", "color": COLOR_GREEN
    },
    {
        "name": "Sealed Bloodbag", "qty": "1x", "quest": "Under the Skin (Piro)",
        "merchant": "Piro", "chance": "55%", "rarity": "Uncommon",
        "icon": "sealed_bloodbag", "color": COLOR_BLUE
    },
    {
        "name": "Longboy Weapon", "qty": "1x", "quest": "A Long Boy (Mr Sweet)",
        "merchant": "Piro / Reynauld", "chance": "35%", "rarity": "Rare",
        "icon": "longboy", "color": COLOR_PURPLE
    }
]

BUYABLE_CAULDRON = [
    {
        "name": "Fresh Egg", "qty": "5x", "quest": "Gardon's Gambit (Louis)",
        "merchant": "Grillard", "chance": "80%", "rarity": "Common",
        "icon": "fresh_egg", "color": COLOR_GREEN
    },
    {
        "name": "Hartshorn", "qty": "2x", "quest": "Of Blight & Bezoars (Piro)",
        "merchant": "Doctor Lucien Moreau", "chance": "45%", "rarity": "Uncommon",
        "icon": "hartshorn", "color": COLOR_BLUE
    },
    {
        "name": "Bezoar", "qty": "3x", "quest": "Of Blight & Bezoars (Piro)",
        "merchant": "Doctor Lucien Moreau", "chance": "35%", "rarity": "Rare",
        "icon": "bezoar", "color": COLOR_PURPLE
    }
]

# 2. CANNOT BUY / LOOT ONLY (Includes Saltpetre & Tallow Balm from Eloise's questline)
# NO locations, container type only. Color strictly ordered: Yellow (rarest) -> Purple -> Blue -> Green -> Grey (common)
LOOT_ONLY_ITEMS = [
    # YELLOW (Rarest < 15%)
    {
        "name": "Tallow Balm", "qty": "10x", "quest": "Bare Necessities (Eloise)",
        "container": "Physician's Cabinet", "chance": "9.1%", "rarity": "Rarest",
        "icon": "tallow_balm", "cont": "physician_bag", "color": COLOR_YELLOW
    },
    {
        "name": "Arsenic", "qty": "1x", "quest": "Of Blight & Bezoars (Piro)",
        "container": "Jacques Medicinals", "chance": "10.6%", "rarity": "Rarest",
        "icon": "arsenic", "cont": "jacques_medicinals", "color": COLOR_YELLOW
    },
    {
        "name": "Opium Pipe", "qty": "1x", "quest": "A Touch of Bribery (Mr Sweet)",
        "container": "Bullion Box / Jewellery Box", "chance": "13.7%", "rarity": "Rarest",
        "icon": "opium_pipe", "cont": "wall_cabinet", "color": COLOR_YELLOW
    },
    # PURPLE (Rare 15% - 35%)
    {
        "name": "China Bowl", "qty": "1x", "quest": "A Touch of Bribery (Mr Sweet)",
        "container": "Wall Cabinet", "chance": "16.1%", "rarity": "Rare",
        "icon": "china_bowl", "cont": "wall_cabinet", "color": COLOR_PURPLE
    },
    {
        "name": "Saltpetre", "qty": "20x", "quest": "Bare Necessities (Eloise)",
        "container": "Tooling Bin", "chance": "18.9%", "rarity": "Rare",
        "icon": "saltpetre", "cont": "tooling_bin", "color": COLOR_PURPLE
    },
    {
        "name": "Glass Vial", "qty": "1x", "quest": "Under the Skin (Piro)",
        "container": "Physician's Cabinet", "chance": "20.4%", "rarity": "Rare",
        "icon": "glass_vial", "cont": "physician_bag", "color": COLOR_PURPLE
    },
    {
        "name": "Silver Dish", "qty": "1x", "quest": "Under the Skin (Piro)",
        "container": "Strongbox / Wall Cabinet", "chance": "23.8%", "rarity": "Rare",
        "icon": "silver_dish", "cont": "strongbox", "color": COLOR_PURPLE
    },
    {
        "name": "Damp Rag", "qty": "5x", "quest": "Bare Necessities (Eloise)",
        "container": "Stone Grave / Tooling Bin", "chance": "23.8%", "rarity": "Rare",
        "icon": "damp_rag", "cont": "tooling_bin", "color": COLOR_PURPLE
    },
    # BLUE (Uncommon 40% - 60%)
    {
        "name": "Flour", "qty": "20x", "quest": "Making Dough (Eloise)",
        "container": "Flour Sack", "chance": "47.6%", "rarity": "Uncommon",
        "icon": "flour", "cont": "flour_sack", "color": COLOR_BLUE
    },
    {
        "name": "Opium", "qty": "1x", "quest": "A Touch of Bribery (Mr Sweet)",
        "container": "Jacques Medicinals", "chance": "47.6%", "rarity": "Uncommon",
        "icon": "opium", "cont": "physician_bag", "color": COLOR_BLUE
    },
    {
        "name": "Charcoal", "qty": "15x", "quest": "Last Embers (Eloise)",
        "container": "Pile of Ash / Old Stove", "chance": "52.6%", "rarity": "Uncommon",
        "icon": "charcoal", "cont": "pile_of_ash", "color": COLOR_BLUE
    },
    # GREY (Most Common / 100% Guaranteed Creature Trophies)
    {
        "name": "Dreg Head", "qty": "10x", "quest": "Tissue and Blood (Piro)",
        "container": "Enemy: Common Dreg", "chance": "100%", "rarity": "Guaranteed",
        "icon": "dreg_head", "cont": None, "color": COLOR_GREY
    },
    {
        "name": "Waif Head", "qty": "10x", "quest": "Tissue and Blood (Piro)",
        "container": "Enemy: Lurking Waif", "chance": "100%", "rarity": "Guaranteed",
        "icon": "waif_head", "cont": None, "color": COLOR_GREY
    },
    {
        "name": "Shambler Hand", "qty": "5x", "quest": "Tissue and Blood (Piro)",
        "container": "Enemy: Heavy Shambler", "chance": "100%", "rarity": "Guaranteed",
        "icon": "shambler_hand", "cont": None, "color": COLOR_GREY
    },
    {
        "name": "Bloat Spine", "qty": "5x", "quest": "Tissue and Blood (Piro)",
        "container": "Enemy: Volatile Bloat", "chance": "100%", "rarity": "Guaranteed",
        "icon": "bloat_spine", "cont": None, "color": COLOR_GREY
    },
    {
        "name": "Brute Foot", "qty": "1x", "quest": "Tissue and Blood (Piro)",
        "container": "Enemy: Armored Brute", "chance": "100%", "rarity": "Guaranteed",
        "icon": "brute_foot", "cont": None, "color": COLOR_GREY
    },
    {
        "name": "Drooler Jaw", "qty": "1x", "quest": "Tissue and Blood (Piro)",
        "container": "Enemy: Acidic Drooler", "chance": "100%", "rarity": "Guaranteed",
        "icon": "drooler_jaw", "cont": None, "color": COLOR_GREY
    }
]

def draw_buyable_row(img, draw, box, item):
    x, y, w, h = box
    draw.rounded_rectangle([x, y, x+w, y+h], radius=6, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
    
    # Left rarity stripe
    draw.rounded_rectangle([x, y, x+4, y+h], radius=2, fill=item["color"])
    
    # Icon Frame
    icon_box_size = 52
    icon_x = x + 10
    icon_y = y + (h - icon_box_size) // 2
    draw.rounded_rectangle([icon_x, icon_y, icon_x+icon_box_size, icon_y+icon_box_size], radius=5, fill=BG_CARD_LIGHT, outline=BORDER_FOCUS, width=1)
    
    ico = get_item_icon(item["icon"])
    if ico:
        ico_res = ico.resize((icon_box_size-8, icon_box_size-8), Image.Resampling.LANCZOS)
        img.paste(ico_res, (icon_x+4, icon_y+4), ico_res)
        
    tx = icon_x + icon_box_size + 12
    
    # Line 1: Name + Qty
    draw.text((tx, y + 8), item["name"], font=F_ITEM_NAME, fill=COLOR_PARCHMENT)
    name_w = int(draw.textlength(item["name"], font=F_ITEM_NAME))
    badge_x = tx + name_w + 8
    
    qty_str = item["qty"]
    qty_w = int(draw.textlength(qty_str, font=F_QTY))
    draw.rounded_rectangle([badge_x, y + 7, badge_x + qty_w + 10, y + 25], radius=4, fill=(18, 18, 15), outline=item["color"], width=1)
    draw.text((badge_x + 5, y + 8), qty_str, font=F_QTY, fill=item["color"])
    
    # Stock Chance Pill on far right
    chance_str = f"Stock Chance: {item['chance']} ({item['rarity']})"
    cw = int(draw.textlength(chance_str, font=F_BADGE))
    cx = x + w - cw - 16
    draw.rounded_rectangle([cx - 6, y + 7, cx + cw + 6, y + 25], radius=4, fill=(18, 18, 15), outline=item["color"], width=1)
    draw.text((cx, y + 8), chance_str, font=F_BADGE, fill=item["color"])
    
    # Line 2: Merchant
    draw.text((tx, y + 32), "Merchant: ", font=F_DETAIL_BOLD, fill=COLOR_MUTED)
    draw.text((tx + 66, y + 32), item["merchant"], font=F_DETAIL_BOLD, fill=COLOR_GOLD)
    
    # Line 3: Quest
    draw.text((tx, y + 51), "Required For: ", font=F_DETAIL_BOLD, fill=COLOR_DIM)
    draw.text((tx + 86, y + 51), item["quest"], font=F_DETAIL_REG, fill=COLOR_PARCHMENT)


def draw_loot_row(img, draw, box, item):
    x, y, w, h = box
    draw.rounded_rectangle([x, y, x+w, y+h], radius=6, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
    
    # Left rarity stripe
    draw.rounded_rectangle([x, y, x+4, y+h], radius=2, fill=item["color"])
    
    # Icon Frame
    icon_box_size = 50
    icon_x = x + 10
    icon_y = y + (h - icon_box_size) // 2
    draw.rounded_rectangle([icon_x, icon_y, icon_x+icon_box_size, icon_y+icon_box_size], radius=5, fill=BG_CARD_LIGHT, outline=BORDER_FOCUS, width=1)
    
    ico = get_item_icon(item["icon"])
    if ico:
        ico_res = ico.resize((icon_box_size-8, icon_box_size-8), Image.Resampling.LANCZOS)
        img.paste(ico_res, (icon_x+4, icon_y+4), ico_res)
        
    c_offset_x = 0
    if item.get("cont"):
        c_ico = get_cont_icon(item["cont"])
        if c_ico:
            c_box_size = 36
            c_x = icon_x + icon_box_size + 6
            c_y = y + (h - c_box_size) // 2
            draw.rounded_rectangle([c_x, c_y, c_x+c_box_size, c_y+c_box_size], radius=4, fill=BG_CARD_LIGHT, outline=BORDER_SUBTLE, width=1)
            c_ico_res = c_ico.resize((c_box_size-6, c_box_size-6), Image.Resampling.LANCZOS)
            img.paste(c_ico_res, (c_x+3, c_y+3), c_ico_res)
            c_offset_x = c_box_size + 6
            
    tx = icon_x + icon_box_size + 12 + c_offset_x
    
    # Line 1: Name + Qty
    draw.text((tx, y + 6), item["name"], font=F_ITEM_NAME, fill=COLOR_PARCHMENT)
    name_w = int(draw.textlength(item["name"], font=F_ITEM_NAME))
    badge_x = tx + name_w + 8
    
    qty_str = item["qty"]
    qty_w = int(draw.textlength(qty_str, font=F_QTY))
    draw.rounded_rectangle([badge_x, y + 5, badge_x + qty_w + 10, y + 23], radius=4, fill=(18, 18, 15), outline=item["color"], width=1)
    draw.text((badge_x + 5, y + 6), qty_str, font=F_QTY, fill=item["color"])
    
    # Drop Rate Pill
    chance_str = f"Drop Rate: {item['chance']} ({item['rarity']})"
    cw = int(draw.textlength(chance_str, font=F_BADGE))
    cx = x + w - cw - 16
    draw.rounded_rectangle([cx - 6, y + 5, cx + cw + 6, y + 23], radius=4, fill=(18, 18, 15), outline=item["color"], width=1)
    draw.text((cx, y + 6), chance_str, font=F_BADGE, fill=item["color"])
    
    # Line 2: Container Type ONLY (no locations)
    draw.text((tx, y + 28), "Container: ", font=F_DETAIL_BOLD, fill=COLOR_MUTED)
    draw.text((tx + 72, y + 28), item["container"], font=F_DETAIL_BOLD, fill=COLOR_PARCHMENT)
    
    # Line 3: Quest
    draw.text((tx, y + 47), "Required For: ", font=F_DETAIL_BOLD, fill=COLOR_DIM)
    draw.text((tx + 86, y + 47), item["quest"], font=F_DETAIL_REG, fill=COLOR_GOLD)


def render():
    print("Generating updated visual directory with separated hubs, container types only, and strict Yellow->Grey rarity...")
    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG_CANVAS)
    draw = ImageDraw.Draw(img)
    
    # ================= TOP HEADER BAR =================
    draw.rectangle([0, 0, CANVAS_W, 68], fill=(16, 16, 13))
    draw.line([0, 68, CANVAS_W, 68], fill=COLOR_GOLD, width=2)
    
    # Clean Title
    draw.text((24, 18), "HUNGER COMPANION // MAIN QUEST ITEM & MERCHANT PROCUREMENT DIRECTORY", font=F_TITLE, fill=COLOR_GOLD)
    
    # Badges on Right
    badge_x = CANVAS_W - 440
    draw.rounded_rectangle([badge_x, 15, badge_x + 200, 51], radius=5, fill=(16, 38, 26), outline=(52, 211, 153), width=1)
    draw.text((badge_x + 14, 23), "✔ 10 BUYABLE ITEMS", font=F_BADGE, fill=(110, 231, 183))
    
    draw.rounded_rectangle([badge_x + 215, 15, badge_x + 420, 51], radius=5, fill=(48, 20, 22), outline=(248, 113, 113), width=1)
    draw.text((badge_x + 228, 23), "✖ 17 LOOT ONLY ITEMS", font=F_BADGE, fill=(252, 165, 165))
    
    # ================= TWO MAIN COLUMNS =================
    PAD_X = 20
    PAD_Y = 82
    COL_GAP = 20
    COL_W = (CANVAS_W - (PAD_X * 2) - COL_GAP) // 2 # 1250px
    COL_H = CANVAS_H - PAD_Y - 20 # 1338px
    
    COL1_X = PAD_X
    COL2_X = PAD_X + COL_W + COL_GAP
    
    # ------------------ COLUMN 1: BUYABLE ITEMS (SEPARATED HUBS) ------------------
    draw.rounded_rectangle([COL1_X, PAD_Y, COL1_X + COL_W, PAD_Y + COL_H], radius=8, fill=BG_PANEL, outline=BORDER_SUBTLE, width=1)
    
    # Col 1 Header
    draw.rectangle([COL1_X, PAD_Y, COL1_X + COL_W, PAD_Y + 48], fill=(20, 28, 22))
    draw.line([COL1_X, PAD_Y + 48, COL1_X + COL_W, PAD_Y + 48], fill=(52, 211, 153), width=2)
    draw.text((COL1_X + 16, PAD_Y + 12), "1. BUYABLE FROM MERCHANTS (10 ITEMS)", font=F_SEC_TITLE, fill=(110, 231, 183))
    
    c1_y = PAD_Y + 58
    
    # Subsection A: Outer Ramparts Merchants
    draw.text((COL1_X + 16, c1_y), "OUTER RAMPARTS MERCHANTS (STARTING HUB)", font=F_SUB_TITLE, fill=COLOR_GOLD)
    c1_y += 24
    
    CARD_H = 74
    CARD_GAP = 7
    
    for item in BUYABLE_OUTER_RAMPARTS:
        draw_buyable_row(img, draw, (COL1_X + 12, c1_y, COL_W - 24, CARD_H), item)
        c1_y += CARD_H + CARD_GAP
        
    c1_y += 14
    # Subsection B: The Cauldron Merchants
    draw.text((COL1_X + 16, c1_y), "THE CAULDRON MERCHANTS (PROGRESSION HUB)", font=F_SUB_TITLE, fill=COLOR_BLUE)
    c1_y += 24
    
    for item in BUYABLE_CAULDRON:
        draw_buyable_row(img, draw, (COL1_X + 12, c1_y, COL_W - 24, CARD_H), item)
        c1_y += CARD_H + CARD_GAP
        
    # ------------------ COLUMN 2: CANNOT BUY / LOOT ONLY (17 ITEMS) ------------------
    draw.rounded_rectangle([COL2_X, PAD_Y, COL2_X + COL_W, PAD_Y + COL_H], radius=8, fill=BG_PANEL, outline=BORDER_SUBTLE, width=1)
    
    # Col 2 Header
    draw.rectangle([COL2_X, PAD_Y, COL2_X + COL_W, PAD_Y + 48], fill=(28, 20, 22))
    draw.line([COL2_X, PAD_Y + 48, COL2_X + COL_W, PAD_Y + 48], fill=(248, 113, 113), width=2)
    draw.text((COL2_X + 16, PAD_Y + 12), "2. CANNOT BUY FROM MERCHANTS — LOOT ONLY (17 ITEMS)", font=F_SEC_TITLE, fill=(252, 165, 165))
    
    c2_y = PAD_Y + 58
    draw.text((COL2_X + 16, c2_y), "CONTAINER & CREATURE HARVEST TARGETS (NO LOCATIONS)", font=F_SUB_TITLE, fill=COLOR_GOLD)
    c2_y += 24
    
    CARD2_H = 68
    CARD2_GAP = 6
    
    for item in LOOT_ONLY_ITEMS:
        draw_loot_row(img, draw, (COL2_X + 12, c2_y, COL_W - 24, CARD2_H), item)
        c2_y += CARD2_H + CARD2_GAP
        
    # Save Image
    out_paths = [
        os.path.join(DOC_DIR, "merchant_quest_items_guide.png"),
        os.path.join(r"C:\Users\PC\Desktop\Hunger_Raid_Maps", "merchant_quest_items_guide.png"),
        os.path.join(r"C:\Users\PC\.gemini\antigravity\brain\31f232ba-f37d-4331-8fda-d6f94602b088", "merchant_quest_items_guide.png")
    ]
    
    for op in out_paths:
        try:
            os.makedirs(os.path.dirname(op), exist_ok=True)
            img.save(op, "PNG", optimize=True)
            print(f"Saved Image: {op}")
        except Exception as e:
            print(f"Error saving {op}: {e}")

if __name__ == "__main__":
    render()
