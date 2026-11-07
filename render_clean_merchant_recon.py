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

# Strict 5-Color Order for Highlights & Badges
PRIO_YELLOW = (250, 204, 21)   # #facc15 - Guaranteed / Prio 1
PRIO_PURPLE = (192, 132, 252)  # #c084fc - High Chance / Prio 2
PRIO_BLUE   = (56, 189, 248)   # #38bdf8 - Moderate Chance / Prio 3
PRIO_GREEN  = (74, 222, 128)   # #4ade80 - Uncommon Chance / Prio 4
PRIO_GREY   = (148, 163, 184)  # #94a3b8 - Trophy / Passive / Prio 5

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
F_SEC_TITLE   = load_font(SERIF_BOLD, 19)
F_SUB_TITLE   = load_font(SANS_BOLD, 13)
F_ITEM_NAME   = load_font(SERIF_BOLD, 16)
F_QTY         = load_font(SANS_BOLD, 13)
F_STATUS      = load_font(SANS_BOLD, 11)
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

# DATA DEFINITIONS
BUYABLE_ITEMS = [
    # Outer Ramparts
    {
        "name": "Heavy Ammunition", "qty": "10x", "quest": "Bearing Arms (Reynauld)",
        "hub": "Outer Ramparts", "merchant": "Reynauld / Piro", "chance": "100%", "chance_lbl": "Guaranteed",
        "price": "~2c each", "icon": "heavy_ammunition", "color": PRIO_YELLOW
    },
    {
        "name": "Thick Branch", "qty": "2x", "quest": "Child's Play (Louis)",
        "hub": "Outer Ramparts", "merchant": "Reynauld", "chance": "100%", "chance_lbl": "Guaranteed",
        "price": "~18c each", "icon": "thick_branch", "color": PRIO_YELLOW
    },
    {
        "name": "Tavern Wine", "qty": "3x", "quest": "Sweet Lubrication (Mr Sweet)",
        "hub": "Outer Ramparts", "merchant": "Mr Sweet", "chance": "100%", "chance_lbl": "Guaranteed",
        "price": "~18c each", "icon": "tavern_wine", "color": PRIO_YELLOW
    },
    {
        "name": "Thin Mead", "qty": "3x", "quest": "Sweet Lubrication (Mr Sweet)",
        "hub": "Outer Ramparts", "merchant": "Mr Sweet", "chance": "100%", "chance_lbl": "Guaranteed",
        "price": "~11c each", "icon": "thin_mead", "color": PRIO_YELLOW
    },
    {
        "name": "Seamstress Needle", "qty": "5x", "quest": "Under the Skin (Piro)",
        "hub": "Outer Ramparts", "merchant": "Octave de Villiers", "chance": "85%", "chance_lbl": "High Chance",
        "price": "~15c each", "icon": "seamstress_needle", "color": PRIO_PURPLE
    },
    {
        "name": "Sealed Bloodbag", "qty": "1x", "quest": "Under the Skin (Piro)",
        "hub": "Outer Ramparts", "merchant": "Piro / Dr. Moreau", "chance": "55%", "chance_lbl": "Moderate",
        "price": "~5s 31c", "icon": "sealed_bloodbag", "color": PRIO_BLUE
    },
    {
        "name": "Longboy Weapon", "qty": "1x", "quest": "A Long Boy (Mr Sweet)",
        "hub": "Outer Ramparts", "merchant": "Piro / Reynauld", "chance": "35%", "chance_lbl": "Uncommon",
        "price": "~1s 31c", "icon": "longboy", "color": PRIO_GREEN
    },
    # Cauldron
    {
        "name": "Saltpetre", "qty": "20x", "quest": "Bare Necessities (Eloise)",
        "hub": "The Cauldron", "merchant": "Doctor Lucien Moreau", "chance": "75%", "chance_lbl": "High Chance",
        "price": "~3c each", "icon": "saltpetre", "color": PRIO_PURPLE
    },
    {
        "name": "Tallow Balm", "qty": "10x", "quest": "Bare Necessities (Eloise)",
        "hub": "The Cauldron", "merchant": "Doctor Lucien Moreau", "chance": "70%", "chance_lbl": "High Chance",
        "price": "~6c each", "icon": "tallow_balm", "color": PRIO_PURPLE
    },
    {
        "name": "Fresh Egg", "qty": "5x", "quest": "Gardon's Gambit (Louis)",
        "hub": "The Cauldron", "merchant": "Grillard", "chance": "80%", "chance_lbl": "High Chance",
        "price": "~16c each", "icon": "fresh_egg", "color": PRIO_PURPLE
    },
    {
        "name": "Hartshorn", "qty": "2x", "quest": "Of Blight & Bezoars (Piro)",
        "hub": "The Cauldron", "merchant": "Doctor Lucien Moreau", "chance": "45%", "chance_lbl": "Moderate",
        "price": "~1s 10c", "icon": "hartshorn", "color": PRIO_BLUE
    },
    {
        "name": "Bezoar", "qty": "3x", "quest": "Of Blight & Bezoars (Piro)",
        "hub": "The Cauldron", "merchant": "Doctor Lucien Moreau", "chance": "35%", "chance_lbl": "Uncommon",
        "price": "~15c each", "icon": "bezoar", "color": PRIO_GREEN
    }
]

LOOT_ITEMS = [
    # Containers
    {
        "name": "Flour", "qty": "20x", "quest": "Making Dough (Eloise)",
        "target": "Flour Sacks (Granaries / Sarlat)", "chance": "47.6%", "chance_lbl": "Flour Sack",
        "icon": "flour", "cont": "flour_sack", "color": PRIO_YELLOW
    },
    {
        "name": "Charcoal", "qty": "15x", "quest": "Last Embers (Eloise)",
        "target": "Piles of Ash (Manor Hearths)", "chance": "52.6%", "chance_lbl": "Pile of Ash",
        "icon": "charcoal", "cont": "pile_of_ash", "color": PRIO_PURPLE
    },
    {
        "name": "Damp Rag", "qty": "5x", "quest": "Bare Necessities (Eloise)",
        "target": "Stone Graves / Tooling Bins / Desks", "chance": "23.8%", "chance_lbl": "Grave / Bin",
        "icon": "damp_rag", "cont": "tooling_bin", "color": PRIO_BLUE
    },
    {
        "name": "Silver Dish", "qty": "1x", "quest": "Under the Skin (Piro)",
        "target": "Wall Cabinets / Strongboxes (Locked)", "chance": "23.8%", "chance_lbl": "Cabinet / Box",
        "icon": "silver_dish", "cont": "strongbox", "color": PRIO_BLUE
    },
    {
        "name": "Glass Vial", "qty": "1x", "quest": "Under the Skin (Piro)",
        "target": "Physician's Cabinets / Clinics", "chance": "20.4%", "chance_lbl": "Physician Kit",
        "icon": "glass_vial", "cont": "physician_bag", "color": PRIO_BLUE
    },
    {
        "name": "China Bowl", "qty": "1x", "quest": "A Touch of Bribery (Mr Sweet)",
        "target": "Wall Cabinets (Château 2nd Floor)", "chance": "16.1%", "chance_lbl": "Wall Cabinet",
        "icon": "china_bowl", "cont": "wall_cabinet", "color": PRIO_GREEN
    },
    {
        "name": "Opium Pipe", "qty": "1x", "quest": "A Touch of Bribery (Mr Sweet)",
        "target": "Bullion Boxes / Jewellery Boxes", "chance": "13.7%", "chance_lbl": "Bullion Box",
        "icon": "opium_pipe", "cont": "wall_cabinet", "color": PRIO_GREEN
    },
    {
        "name": "Arsenic", "qty": "1x", "quest": "Of Blight & Bezoars (Piro)",
        "target": "Jacques Medicinals / Infirmary Jars", "chance": "10.6%", "chance_lbl": "Medicinals",
        "icon": "arsenic", "cont": "jacques_medicinals", "color": PRIO_GREEN
    },
    {
        "name": "Opium", "qty": "1x", "quest": "A Touch of Bribery (Mr Sweet)",
        "target": "Jacques Medicinals (Field Hospital)", "chance": "47.6%", "chance_lbl": "Medicinals",
        "icon": "opium", "cont": "physician_bag", "color": PRIO_PURPLE
    },
    # Trophies
    {
        "name": "Dreg Head", "qty": "10x", "quest": "Tissue and Blood (Piro)",
        "target": "Common Dregs (All Maps / Trenches)", "chance": "100%", "chance_lbl": "Head Harvest",
        "icon": "dreg_head", "cont": None, "color": PRIO_GREY
    },
    {
        "name": "Waif Head", "qty": "10x", "quest": "Tissue and Blood (Piro)",
        "target": "Lurking Waifs (Ruins / Rubble / Roofs)", "chance": "100%", "chance_lbl": "Head Harvest",
        "icon": "waif_head", "cont": None, "color": PRIO_GREY
    },
    {
        "name": "Shambler Hand", "qty": "5x", "quest": "Tissue and Blood (Piro)",
        "target": "Heavy Shamblers (Patrol Corridors)", "chance": "100%", "chance_lbl": "Arm Harvest",
        "icon": "shambler_hand", "cont": None, "color": PRIO_GREY
    },
    {
        "name": "Bloat Spine", "qty": "5x", "quest": "Tissue and Blood (Piro)",
        "target": "Volatile Bloats (Snipe from range)", "chance": "100%", "chance_lbl": "Spine Harvest",
        "icon": "bloat_spine", "cont": None, "color": PRIO_GREY
    },
    {
        "name": "Brute Foot", "qty": "1x", "quest": "Tissue and Blood (Piro)",
        "target": "Armored Brutes (Fortress Gates)", "chance": "100%", "chance_lbl": "Leg Harvest",
        "icon": "brute_foot", "cont": None, "color": PRIO_GREY
    },
    {
        "name": "Drooler Jaw", "qty": "1x", "quest": "Tissue and Blood (Piro)",
        "target": "Acidic Droolers (Waterways / Canals)", "chance": "100%", "chance_lbl": "Jaw Harvest",
        "icon": "drooler_jaw", "cont": None, "color": PRIO_GREY
    }
]

def draw_buyable_card(img, draw, box, item):
    x, y, w, h = box
    draw.rounded_rectangle([x, y, x+w, y+h], radius=6, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
    
    # Left stripe uses the item's priority color (Yellow, Purple, Blue, Green, Grey)
    draw.rounded_rectangle([x, y, x+4, y+h], radius=2, fill=item["color"])
    
    # Icon Frame
    icon_box_size = 56
    icon_x = x + 10
    icon_y = y + (h - icon_box_size) // 2
    draw.rounded_rectangle([icon_x, icon_y, icon_x+icon_box_size, icon_y+icon_box_size], radius=5, fill=BG_CARD_LIGHT, outline=BORDER_FOCUS, width=1)
    
    ico = get_item_icon(item["icon"])
    if ico:
        ico_res = ico.resize((icon_box_size-8, icon_box_size-8), Image.Resampling.LANCZOS)
        img.paste(ico_res, (icon_x+4, icon_y+4), ico_res)
        
    tx = icon_x + icon_box_size + 12
    
    # Line 1: Item Name + Qty Badge + Hub Tag
    draw.text((tx, y + 8), item["name"], font=F_ITEM_NAME, fill=COLOR_PARCHMENT)
    name_w = int(draw.textlength(item["name"], font=F_ITEM_NAME))
    badge_x = tx + name_w + 8
    
    qty_str = item["qty"]
    qty_w = int(draw.textlength(qty_str, font=F_QTY))
    draw.rounded_rectangle([badge_x, y + 7, badge_x + qty_w + 10, y + 25], radius=4, fill=(18, 18, 15), outline=item["color"], width=1)
    draw.text((badge_x + 5, y + 8), qty_str, font=F_QTY, fill=item["color"])
    
    # Stock Chance Pill on far right
    chance_str = f"Stock Chance: {item['chance']} ({item['chance_lbl']})"
    cw = int(draw.textlength(chance_str, font=F_BADGE))
    cx = x + w - cw - 16
    draw.rounded_rectangle([cx - 6, y + 7, cx + cw + 6, y + 25], radius=4, fill=(16, 38, 26), outline=item["color"], width=1)
    draw.text((cx, y + 8), chance_str, font=F_BADGE, fill=item["color"])
    
    # Line 2: Merchant & Hub Location
    draw.text((tx, y + 33), "Merchant: ", font=F_DETAIL_BOLD, fill=COLOR_MUTED)
    m_info = f"{item['merchant']}  •  Location: {item['hub']}  ({item['price']})"
    draw.text((tx + 66, y + 33), m_info, font=F_DETAIL_BOLD, fill=COLOR_GOLD)
    
    # Line 3: Quest
    draw.text((tx, y + 54), "Required For: ", font=F_DETAIL_BOLD, fill=COLOR_DIM)
    draw.text((tx + 86, y + 54), item["quest"], font=F_DETAIL_REG, fill=COLOR_PARCHMENT)


def draw_loot_card(img, draw, box, item):
    x, y, w, h = box
    draw.rounded_rectangle([x, y, x+w, y+h], radius=6, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
    
    # Left stripe
    draw.rounded_rectangle([x, y, x+4, y+h], radius=2, fill=item["color"])
    
    # Icon Frame
    icon_box_size = 56
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
            c_box_size = 40
            c_x = icon_x + icon_box_size + 6
            c_y = y + (h - c_box_size) // 2
            draw.rounded_rectangle([c_x, c_y, c_x+c_box_size, c_y+c_box_size], radius=4, fill=BG_CARD_LIGHT, outline=BORDER_SUBTLE, width=1)
            c_ico_res = c_ico.resize((c_box_size-6, c_box_size-6), Image.Resampling.LANCZOS)
            img.paste(c_ico_res, (c_x+3, c_y+3), c_ico_res)
            c_offset_x = c_box_size + 6
            
    tx = icon_x + icon_box_size + 12 + c_offset_x
    
    # Line 1: Item Name + Qty Badge
    draw.text((tx, y + 8), item["name"], font=F_ITEM_NAME, fill=COLOR_PARCHMENT)
    name_w = int(draw.textlength(item["name"], font=F_ITEM_NAME))
    badge_x = tx + name_w + 8
    
    qty_str = item["qty"]
    qty_w = int(draw.textlength(qty_str, font=F_QTY))
    draw.rounded_rectangle([badge_x, y + 7, badge_x + qty_w + 10, y + 25], radius=4, fill=(18, 18, 15), outline=item["color"], width=1)
    draw.text((badge_x + 5, y + 8), qty_str, font=F_QTY, fill=item["color"])
    
    # Drop Rate Pill on far right
    chance_str = f"Drop Rate: {item['chance']} ({item['chance_lbl']})"
    cw = int(draw.textlength(chance_str, font=F_BADGE))
    cx = x + w - cw - 16
    draw.rounded_rectangle([cx - 6, y + 7, cx + cw + 6, y + 25], radius=4, fill=(38, 20, 22), outline=item["color"], width=1)
    draw.text((cx, y + 8), chance_str, font=F_BADGE, fill=item["color"])
    
    # Line 2: Target Container or Enemy
    draw.text((tx, y + 33), "Raid Target: ", font=F_DETAIL_BOLD, fill=COLOR_MUTED)
    draw.text((tx + 78, y + 33), item["target"], font=F_DETAIL_BOLD, fill=COLOR_PARCHMENT)
    
    # Line 3: Quest
    draw.text((tx, y + 54), "Required For: ", font=F_DETAIL_BOLD, fill=COLOR_DIM)
    draw.text((tx + 86, y + 54), item["quest"], font=F_DETAIL_REG, fill=COLOR_GOLD)


def render():
    print("Rendering clearly organized layout: Buyable vs Not Buyable with Merchant Stock Chances...")
    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG_CANVAS)
    draw = ImageDraw.Draw(img)
    
    # ================= TOP HEADER BAR =================
    draw.rectangle([0, 0, CANVAS_W, 70], fill=(16, 16, 13))
    draw.line([0, 70, CANVAS_W, 70], fill=COLOR_GOLD, width=2)
    
    # Clean Title
    draw.text((24, 18), "HUNGER COMPANION // MAIN QUEST ITEM & MERCHANT PROCUREMENT RECON", font=F_TITLE, fill=COLOR_GOLD)
    
    # Status Counter Badges on Top Right
    badge_x = CANVAS_W - 440
    draw.rounded_rectangle([badge_x, 16, badge_x + 200, 52], radius=5, fill=(16, 38, 26), outline=(52, 211, 153), width=1)
    draw.text((badge_x + 14, 24), "✔ 12 BUYABLE ITEMS", font=F_BADGE, fill=(110, 231, 183))
    
    draw.rounded_rectangle([badge_x + 215, 16, badge_x + 420, 52], radius=5, fill=(48, 20, 22), outline=(248, 113, 113), width=1)
    draw.text((badge_x + 228, 24), "✖ 15 LOOT ONLY ITEMS", font=F_BADGE, fill=(252, 165, 165))
    
    # ================= TWO MAIN PANELS =================
    PAD_X = 20
    PAD_Y = 86
    COL_GAP = 20
    COL_W = (CANVAS_W - (PAD_X * 2) - COL_GAP) // 2 # 1250px
    COL_H = CANVAS_H - PAD_Y - 24 # 1330px
    
    COL1_X = PAD_X
    COL2_X = PAD_X + COL_W + COL_GAP
    
    # ----------------- PANEL 1: BUYABLE ITEMS (LEFT) -----------------
    draw.rounded_rectangle([COL1_X, PAD_Y, COL1_X + COL_W, PAD_Y + COL_H], radius=8, fill=BG_PANEL, outline=BORDER_SUBTLE, width=1)
    
    # Header Bar
    draw.rectangle([COL1_X, PAD_Y, COL1_X + COL_W, PAD_Y + 54], fill=(20, 28, 22))
    draw.line([COL1_X, PAD_Y + 54, COL1_X + COL_W, PAD_Y + 54], fill=(52, 211, 153), width=2)
    draw.text((COL1_X + 16, PAD_Y + 12), "1. BUYABLE FROM MERCHANTS (12 ITEMS)", font=F_SEC_TITLE, fill=(110, 231, 183))
    draw.text((COL1_X + 16, PAD_Y + 34), "Check merchant stocks on each hub reset • Stock chances shown per item", font=F_SUB_TITLE, fill=COLOR_MUTED)
    
    c1_y = PAD_Y + 68
    CARD_H = 78
    CARD_GAP = 8
    
    for item in BUYABLE_ITEMS:
        draw_buyable_card(img, draw, (COL1_X + 12, c1_y, COL_W - 24, CARD_H), item)
        c1_y += CARD_H + CARD_GAP
        
    # ----------------- PANEL 2: NOT BUYABLE / LOOT ONLY (RIGHT) -----------------
    draw.rounded_rectangle([COL2_X, PAD_Y, COL2_X + COL_W, PAD_Y + COL_H], radius=8, fill=BG_PANEL, outline=BORDER_SUBTLE, width=1)
    
    # Header Bar
    draw.rectangle([COL2_X, PAD_Y, COL2_X + COL_W, PAD_Y + 54], fill=(28, 20, 22))
    draw.line([COL2_X, PAD_Y + 54, COL2_X + COL_W, PAD_Y + 54], fill=(248, 113, 113), width=2)
    draw.text((COL2_X + 16, PAD_Y + 12), "2. CANNOT BUY FROM MERCHANTS — LOOT ONLY (15 ITEMS)", font=F_SEC_TITLE, fill=(252, 165, 165))
    draw.text((COL2_X + 16, PAD_Y + 34), "Never sold by merchants • Must target specific container nodes or harvest from elites", font=F_SUB_TITLE, fill=COLOR_MUTED)
    
    c2_y = PAD_Y + 68
    CARD2_H = 72
    CARD2_GAP = 7
    
    for item in LOOT_ITEMS:
        draw_loot_card(img, draw, (COL2_X + 12, c2_y, COL_W - 24, CARD2_H), item)
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
