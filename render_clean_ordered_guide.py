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

# Strict 5-Color Priority Order
PRIO_YELLOW = (250, 204, 21)   # #facc15 (Priority 1)
PRIO_PURPLE = (192, 132, 252)  # #c084fc (Priority 2)
PRIO_BLUE   = (56, 189, 248)   # #38bdf8 (Priority 3)
PRIO_GREEN  = (74, 222, 128)   # #4ade80 (Priority 4)
PRIO_GREY   = (148, 163, 184)  # #94a3b8 (Priority 5)

# Status Badges
COLOR_BUYABLE_TEXT = (110, 231, 183) # Mint green
COLOR_BUYABLE_BG   = (16, 42, 28)
COLOR_BUYABLE_BDR  = (52, 211, 153)

COLOR_LOOT_TEXT    = (252, 165, 165) # Soft red
COLOR_LOOT_BG      = (48, 20, 22)
COLOR_LOOT_BDR     = (248, 113, 113)

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
F_COL_TITLE   = load_font(SERIF_BOLD, 18)
F_COL_SUB     = load_font(SANS_BOLD, 12)
F_ITEM_NAME   = load_font(SERIF_BOLD, 17)
F_QTY         = load_font(SANS_BOLD, 14)
F_STATUS      = load_font(SANS_BOLD, 11)
F_DETAIL_BOLD = load_font(SANS_BOLD, 13)
F_DETAIL_REG  = load_font(SANS_REG, 13)
F_SMALL       = load_font(SANS_REG, 12)

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

# 5 Priority Groups in strict order: Yellow -> Purple -> Blue -> Green -> Grey
TIERS = [
    {
        "name": "PRIORITY 1: YELLOW",
        "sub": "PRIMARY OBJECTIVES & CORE GEAR",
        "color": PRIO_YELLOW,
        "items": [
            {
                "name": "Flour",
                "qty": "20x",
                "quest": "Making Dough (Eloise)",
                "buyable": False,
                "source": "Flour Sacks (Granaries / Sarlat)",
                "icon": "flour",
                "cont": "flour_sack"
            },
            {
                "name": "Heavy Ammunition",
                "qty": "10x",
                "quest": "Bearing Arms (Reynauld)",
                "buyable": True,
                "source": "Reynauld / Piro (Outer Ramparts)",
                "icon": "heavy_ammunition",
                "cont": None
            },
            {
                "name": "Longboy Weapon",
                "qty": "1x",
                "quest": "A Long Boy (Mr Sweet)",
                "buyable": True,
                "source": "Piro / Reynauld (Outer Ramparts)",
                "icon": "longboy",
                "cont": None
            },
            {
                "name": "Thick Branch",
                "qty": "2x",
                "quest": "Child's Play (Louis)",
                "buyable": True,
                "source": "Reynauld (Outer Ramparts)",
                "icon": "thick_branch",
                "cont": None
            },
            {
                "name": "Fresh Egg",
                "qty": "5x",
                "quest": "Gardon's Gambit (Louis)",
                "buyable": True,
                "source": "Grillard (Cauldron)",
                "icon": "fresh_egg",
                "cont": None
            }
        ]
    },
    {
        "name": "PRIORITY 2: PURPLE",
        "sub": "HEARTHS & ALCHEMICAL REAGENTS",
        "color": PRIO_PURPLE,
        "items": [
            {
                "name": "Charcoal",
                "qty": "15x",
                "quest": "Last Embers (Eloise)",
                "buyable": False,
                "source": "Piles of Ash (Manor Hearths)",
                "icon": "charcoal",
                "cont": "pile_of_ash"
            },
            {
                "name": "Silver Dish",
                "qty": "1x",
                "quest": "Under the Skin (Piro)",
                "buyable": False,
                "source": "Strongboxes (Officers' Desks)",
                "icon": "silver_dish",
                "cont": "strongbox"
            },
            {
                "name": "Bezoar",
                "qty": "3x",
                "quest": "Of Blight & Bezoars (Piro)",
                "buyable": True,
                "source": "Doctor Lucien Moreau (Cauldron)",
                "icon": "bezoar",
                "cont": None
            },
            {
                "name": "Hartshorn",
                "qty": "2x",
                "quest": "Of Blight & Bezoars (Piro)",
                "buyable": True,
                "source": "Doctor Lucien Moreau (Cauldron)",
                "icon": "hartshorn",
                "cont": None
            },
            {
                "name": "Seamstress Needle",
                "qty": "5x",
                "quest": "Under the Skin (Piro)",
                "buyable": True,
                "source": "Octave de Villiers (Outer Ramparts)",
                "icon": "seamstress_needle",
                "cont": None
            }
        ]
    },
    {
        "name": "PRIORITY 3: BLUE",
        "sub": "APOTHECARY & CLINIC REAGENTS",
        "color": PRIO_BLUE,
        "items": [
            {
                "name": "Saltpetre",
                "qty": "20x",
                "quest": "Bare Necessities (Eloise)",
                "buyable": True,
                "source": "Doctor Lucien Moreau (Cauldron)",
                "icon": "saltpetre",
                "cont": None
            },
            {
                "name": "Tallow Balm",
                "qty": "10x",
                "quest": "Bare Necessities (Eloise)",
                "buyable": True,
                "source": "Doctor Lucien Moreau (Cauldron)",
                "icon": "tallow_balm",
                "cont": None
            },
            {
                "name": "Sealed Bloodbag",
                "qty": "1x",
                "quest": "Under the Skin (Piro)",
                "buyable": True,
                "source": "Piro / Dr. Moreau (Hub/Cauldron)",
                "icon": "sealed_bloodbag",
                "cont": None
            },
            {
                "name": "Damp Rag",
                "qty": "5x",
                "quest": "Bare Necessities (Eloise)",
                "buyable": False,
                "source": "Tooling Bins (Workshops/Desks)",
                "icon": "damp_rag",
                "cont": "tooling_bin"
            },
            {
                "name": "Glass Vial",
                "qty": "1x",
                "quest": "Under the Skin (Piro)",
                "buyable": False,
                "source": "Physician Bags (Clinics)",
                "icon": "glass_vial",
                "cont": "physician_bag"
            },
            {
                "name": "Arsenic",
                "qty": "1x",
                "quest": "Of Blight & Bezoars (Piro)",
                "buyable": False,
                "source": "Jacques Medicinals (Infirmaries)",
                "icon": "arsenic",
                "cont": "jacques_medicinals"
            }
        ]
    },
    {
        "name": "PRIORITY 4: GREEN",
        "sub": "CONTRABAND & TAVERN GOODS",
        "color": PRIO_GREEN,
        "items": [
            {
                "name": "China Bowl",
                "qty": "1x",
                "quest": "A Touch of Bribery (Mr Sweet)",
                "buyable": False,
                "source": "Wall Cabinets (Château Interior)",
                "icon": "china_bowl",
                "cont": "wall_cabinet"
            },
            {
                "name": "Opium Pipe",
                "qty": "1x",
                "quest": "A Touch of Bribery (Mr Sweet)",
                "buyable": False,
                "source": "Wall Cabinets / Desks (Manors)",
                "icon": "opium_pipe",
                "cont": "wall_cabinet"
            },
            {
                "name": "Opium",
                "qty": "1x",
                "quest": "A Touch of Bribery (Mr Sweet)",
                "buyable": False,
                "source": "Physician Bags (Field Hospitals)",
                "icon": "opium",
                "cont": "physician_bag"
            },
            {
                "name": "Tavern Wine",
                "qty": "3x",
                "quest": "Sweet Lubrication (Mr Sweet)",
                "buyable": True,
                "source": "Mr Sweet (Outer Ramparts)",
                "icon": "tavern_wine",
                "cont": None
            },
            {
                "name": "Thin Mead",
                "qty": "3x",
                "quest": "Sweet Lubrication (Mr Sweet)",
                "buyable": True,
                "source": "Mr Sweet (Outer Ramparts)",
                "icon": "thin_mead",
                "cont": None
            }
        ]
    },
    {
        "name": "PRIORITY 5: GREY",
        "sub": "BESTIARY CREATURE TROPHIES",
        "color": PRIO_GREY,
        "items": [
            {
                "name": "Dreg Head",
                "qty": "10x",
                "quest": "Tissue and Blood (Piro)",
                "buyable": False,
                "source": "Harvest: Common Dregs (All Maps)",
                "icon": "dreg_head",
                "cont": None
            },
            {
                "name": "Waif Head",
                "qty": "10x",
                "quest": "Tissue and Blood (Piro)",
                "buyable": False,
                "source": "Harvest: Lurking Waifs (Ruins)",
                "icon": "waif_head",
                "cont": None
            },
            {
                "name": "Shambler Hand",
                "qty": "5x",
                "quest": "Tissue and Blood (Piro)",
                "buyable": False,
                "source": "Harvest: Heavy Shamblers",
                "icon": "shambler_hand",
                "cont": None
            },
            {
                "name": "Bloat Spine",
                "qty": "5x",
                "quest": "Tissue and Blood (Piro)",
                "buyable": False,
                "source": "Harvest: Volatile Bloats",
                "icon": "bloat_spine",
                "cont": None
            },
            {
                "name": "Brute Foot",
                "qty": "1x",
                "quest": "Tissue and Blood (Piro)",
                "buyable": False,
                "source": "Harvest: Armored Brutes (Gates)",
                "icon": "brute_foot",
                "cont": None
            },
            {
                "name": "Drooler Jaw",
                "qty": "1x",
                "quest": "Tissue and Blood (Piro)",
                "buyable": False,
                "source": "Harvest: Acidic Droolers (Canals)",
                "icon": "drooler_jaw",
                "cont": None
            }
        ]
    }
]

def draw_item_card(img, draw, box, item, tier_color):
    x, y, w, h = box
    
    # Outer card background
    draw.rounded_rectangle([x, y, x+w, y+h], radius=7, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)
    
    # Left accent stripe in the tier color (Yellow, Purple, Blue, Green, Grey)
    draw.rounded_rectangle([x, y, x+4, y+h], radius=2, fill=tier_color)
    
    # Item Icon
    icon_box_size = 56
    icon_x = x + 12
    icon_y = y + (h - icon_box_size) // 2
    draw.rounded_rectangle([icon_x, icon_y, icon_x+icon_box_size, icon_y+icon_box_size], radius=6, fill=BG_CARD_LIGHT, outline=BORDER_FOCUS, width=1)
    
    ico = get_item_icon(item["icon"])
    if ico:
        ico_res = ico.resize((icon_box_size-8, icon_box_size-8), Image.Resampling.LANCZOS)
        img.paste(ico_res, (icon_x+4, icon_y+4), ico_res)
        
    c_offset_x = 0
    if item.get("cont"):
        c_ico = get_cont_icon(item["cont"])
        if c_ico:
            c_box_size = 40
            cx = icon_x + icon_box_size + 6
            cy = y + (h - c_box_size) // 2
            draw.rounded_rectangle([cx, cy, cx+c_box_size, cy+c_box_size], radius=5, fill=BG_CARD_LIGHT, outline=BORDER_SUBTLE, width=1)
            c_ico_res = c_ico.resize((c_box_size-6, c_box_size-6), Image.Resampling.LANCZOS)
            img.paste(c_ico_res, (cx+3, cy+3), c_ico_res)
            c_offset_x = c_box_size + 6
            
    tx = icon_x + icon_box_size + 12 + c_offset_x
    
    # Line 1: Item Name + Qty Badge
    draw.text((tx, y + 10), item["name"], font=F_ITEM_NAME, fill=COLOR_PARCHMENT)
    name_w = int(draw.textlength(item["name"], font=F_ITEM_NAME))
    badge_x = tx + name_w + 8
    
    qty_str = item["qty"]
    qty_w = int(draw.textlength(qty_str, font=F_QTY))
    draw.rounded_rectangle([badge_x, y + 9, badge_x + qty_w + 10, y + 27], radius=4, fill=(18, 18, 15), outline=tier_color, width=1)
    draw.text((badge_x + 5, y + 10), qty_str, font=F_QTY, fill=tier_color)
    
    # Line 2: Status Pill (BUYABLE vs CANNOT BUY)
    is_buy = item["buyable"]
    status_text = "✔ BUYABLE" if is_buy else "✖ CANNOT BUY"
    stat_color = COLOR_BUYABLE_TEXT if is_buy else COLOR_LOOT_TEXT
    stat_bg    = COLOR_BUYABLE_BG if is_buy else COLOR_LOOT_BG
    stat_bdr   = COLOR_BUYABLE_BDR if is_buy else COLOR_LOOT_BDR
    
    stat_w = int(draw.textlength(status_text, font=F_STATUS))
    draw.rounded_rectangle([tx, y + 36, tx + stat_w + 12, y + 54], radius=4, fill=stat_bg, outline=stat_bdr, width=1)
    draw.text((tx + 6, y + 38), status_text, font=F_STATUS, fill=stat_color)
    
    # Line 3: Vendor or Source Location
    lbl = "Vendor: " if is_buy else "Source: "
    draw.text((tx, y + 62), lbl, font=F_DETAIL_BOLD, fill=COLOR_MUTED)
    draw.text((tx + int(draw.textlength(lbl, font=F_DETAIL_BOLD)), y + 62), item["source"], font=F_DETAIL_REG, fill=COLOR_PARCHMENT if not is_buy else tier_color)
    
    # Line 4: Quest & Giver
    draw.text((tx, y + 84), "Quest: ", font=F_DETAIL_BOLD, fill=COLOR_DIM)
    draw.text((tx + int(draw.textlength("Quest: ", font=F_DETAIL_BOLD)), y + 84), item["quest"], font=F_SMALL, fill=COLOR_GOLD)


def render():
    print("Generating strictly ordered Yellow -> Purple -> Blue -> Green -> Grey visual guide...")
    img = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG_CANVAS)
    draw = ImageDraw.Draw(img)
    
    # ================= TOP HEADER BAR (CLEAN, NO EXTRA UP-LEFT SUBTITLE) =================
    draw.rectangle([0, 0, CANVAS_W, 70], fill=(16, 16, 13))
    draw.line([0, 70, CANVAS_W, 70], fill=COLOR_GOLD, width=2)
    
    # Clean Title (No extra subtitle)
    draw.text((24, 18), "HUNGER COMPANION // MAIN QUEST ITEM & MERCHANT DIRECTORY", font=F_TITLE, fill=COLOR_GOLD)
    
    # Badges on Right
    badge_x = CANVAS_W - 430
    draw.rounded_rectangle([badge_x, 16, badge_x + 195, 52], radius=5, fill=COLOR_BUYABLE_BG, outline=COLOR_BUYABLE_BDR, width=1)
    draw.text((badge_x + 14, 24), "✔ 12 BUYABLE ITEMS", font=F_BADGE, fill=COLOR_BUYABLE_TEXT)
    
    draw.rounded_rectangle([badge_x + 210, 16, badge_x + 410, 52], radius=5, fill=COLOR_LOOT_BG, outline=COLOR_LOOT_BDR, width=1)
    draw.text((badge_x + 224, 24), "✖ 15 LOOT ONLY ITEMS", font=F_BADGE, fill=COLOR_LOOT_TEXT)
    
    # ================= 5 COLUMNS: YELLOW, PURPLE, BLUE, GREEN, GREY =================
    PAD_X = 20
    PAD_Y = 86
    COL_GAP = 12
    NUM_COLS = 5
    COL_W = (CANVAS_W - (PAD_X * 2) - (COL_GAP * (NUM_COLS - 1))) // NUM_COLS # ~492px
    COL_H = CANVAS_H - PAD_Y - 24 # 1330px
    
    CARD_H = 114
    CARD_GAP = 10
    
    for i, tier in enumerate(TIERS):
        cx = PAD_X + i * (COL_W + COL_GAP)
        t_color = tier["color"]
        
        # Panel Background
        draw.rounded_rectangle([cx, PAD_Y, cx + COL_W, PAD_Y + COL_H], radius=8, fill=BG_PANEL, outline=BORDER_SUBTLE, width=1)
        
        # Column Header Bar with tier accent line
        draw.rectangle([cx, PAD_Y, cx + COL_W, PAD_Y + 54], fill=(22, 22, 18))
        draw.line([cx, PAD_Y + 54, cx + COL_W, PAD_Y + 54], fill=t_color, width=2)
        
        # Priority Header text
        draw.text((cx + 14, PAD_Y + 10), tier["name"], font=F_COL_TITLE, fill=t_color)
        draw.text((cx + 14, PAD_Y + 33), tier["sub"], font=F_COL_SUB, fill=COLOR_MUTED)
        
        # Render each item card in this tier
        cy = PAD_Y + 66
        for item in tier["items"]:
            draw_item_card(img, draw, (cx + 10, cy, COL_W - 20, CARD_H), item, t_color)
            cy += CARD_H + CARD_GAP
            
    # Save Image (NO bottom-left text, NO up-left extra text, NO speedrun logistics)
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
