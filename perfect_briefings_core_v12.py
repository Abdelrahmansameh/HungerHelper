import os, sys, math, sqlite3
from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 2400
CANVAS_H = 1400

# Map occupies left 68%
MAP_X = 20
MAP_Y = 82
MAP_W = 1630
MAP_H = 1298

# Right Briefing Panel occupies remaining 31%
PANEL_X = 1670
PANEL_Y = 82
PANEL_W = 710
PANEL_H = 1298

# Container Color Palette: Matching natural container visuals!
COLOR_SACK = (255, 215, 0)        # Warm Golden Yellow (Flour / Food Sacks)
COLOR_BULLION = (168, 85, 247)     # Royal Purple (Bullion / Jewellery Boxes - Opium Pipe ⭐)
COLOR_CABINET = (56, 189, 248)     # Sky Cyan / Porcelain (Wall Cabinets - China Bowl ⭐)
COLOR_ASH = (249, 115, 22)         # Ember Orange (Piles of Ash - Charcoal)
COLOR_TOOLING = (45, 212, 191)     # Industrial Teal (Tooling Bins - Saltpetre)
COLOR_STORY = (250, 204, 21)       # Radiant Gold (Quest Story POIs / Triggers)

def load_font(name_list, size):
    for f in name_list:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()

SANS_BOLD = ["C:\\Windows\\Fonts\\segoeuib.ttf", "C:\\Windows\\Fonts\\arialbd.ttf", "C:\\Windows\\Fonts\\tahomabd.ttf"]
SANS_REG = ["C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\tahoma.ttf"]

F_HEADER_TITLE = load_font(SANS_BOLD, 30)
F_HEADER_TAG = load_font(SANS_BOLD, 16)
F_SECTION_TITLE = load_font(SANS_BOLD, 20)
F_CARD_TITLE = load_font(SANS_BOLD, 18)
F_BODY_BOLD = load_font(SANS_BOLD, 16)
F_BODY = load_font(SANS_REG, 15)
F_SMALL_BOLD = load_font(SANS_BOLD, 14)
F_SMALL = load_font(SANS_REG, 13)
F_TINY = load_font(SANS_REG, 12)
F_BADGE = load_font(SANS_BOLD, 12)

DOC_DIR = r"C:\Users\PC\Documents\HungerHelper"
CONT_DIR = os.path.join(DOC_DIR, "assets", "containers")
ITEM_DIR = os.path.join(DOC_DIR, "assets", "items")
DB_PATH = os.path.join(DOC_DIR, "hunger_helper.db")

CONTAINER_IMGS = {}
ITEM_IMGS = {}

def preload_assets():
    if os.path.exists(CONT_DIR):
        for f in os.listdir(CONT_DIR):
            if f.endswith(('.png', '.webp', '.jpg')):
                try:
                    p = os.path.join(CONT_DIR, f)
                    CONTAINER_IMGS[f] = Image.open(p).convert("RGBA")
                except Exception:
                    pass
    if os.path.exists(ITEM_DIR):
        for f in os.listdir(ITEM_DIR):
            if f.endswith(('.png', '.webp', '.jpg')):
                try:
                    p = os.path.join(ITEM_DIR, f)
                    ITEM_IMGS[f] = Image.open(p).convert("RGBA")
                except Exception:
                    pass

preload_assets()

def paste_icon_safe(target_img, icon_img, box, bg_color=None, border_color=None, border_w=1, radius=6):
    border_w = int(border_w)
    x, y, w, h = box
    if bg_color:
        draw = ImageDraw.Draw(target_img)
        draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=bg_color, outline=border_color, width=border_w)
    
    if icon_img is None:
        return
        
    pad = 4
    iw, ih = w - (pad * 2), h - (pad * 2)
    ico_resized = icon_img.resize((iw, ih), Image.Resampling.LANCZOS)
    target_img.paste(ico_resized, (x+pad, y+pad), ico_resized)

def get_rate_color(rate_str):
    try:
        val = float(rate_str.replace('%', '').strip())
        if val < 20.0:
            return (239, 68, 68)   # Red (<20%: Rare)
        elif val < 50.0:
            return (249, 115, 22)  # Orange (20-49%: Medium)
        else:
            return (34, 197, 94)   # Green (50-100%: High)
    except:
        return (255, 255, 255)

# ==========================================
# CUSTOM SHAPE DRAWING FOR MAP & DIRECTORY
# Differentiates every container type cleanly!
# ==========================================
def draw_container_shape(draw, shape, cx, cy, r, color, outline=(15, 20, 30), width=2):
    width = int(width)
    """
    Renders distinct shapes on the map terrain:
    - circle: Sacks & Food Barrels (Yellow)
    - diamond: Bullion / Jewellery Box (Purple ⭐ High Priority)
    - square: Wall Cabinets (Sky Cyan ⭐ High Priority)
    - ring: Pile of Ash (Ember Orange)
    - triangle: Tooling Bins (Teal)
    - star: Quest Story POIs (Radiant Gold)
    """
    if shape == 'circle':
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color, outline=outline, width=width)
    elif shape == 'diamond':
        # Diamond for Bullion Boxes
        pts = [(cx, cy-r-2), (cx+r+2, cy), (cx, cy+r+2), (cx-r-2, cy)]
        draw.polygon(pts, fill=color, outline=outline, width=width)
    elif shape == 'square':
        # Square for Wall Cabinets
        draw.rectangle([cx-r+1, cy-r+1, cx+r-1, cy+r-1], fill=color, outline=outline, width=width)
    elif shape == 'ring':
        # Ash Fireplace Ring
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(25, 30, 40), outline=color, width=width+1)
        draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=color)
    elif shape == 'triangle':
        # Tooling Bin
        pts = [(cx, cy-r-1), (cx+r+1, cy+r), (cx-r-1, cy+r)]
        draw.polygon(pts, fill=color, outline=outline, width=width)
    elif shape == 'star':
        # Quest Objective POI
        s1 = r + 3
        s2 = int(r * 0.4)
        pts = [
            (cx, cy-s1), (cx+s2, cy-s2), (cx+s1, cy), (cx+s2, cy+s2),
            (cx, cy+s1), (cx-s2, cy+s2), (cx-s1, cy), (cx-s2, cy-s2)
        ]
        draw.polygon(pts, fill=color, outline=outline, width=width)

# ==========================================
# FETCH ALL MAP LOOT POINTS FROM DATABASE
# ==========================================
def get_map_loot_from_db(map_name):
    """
    Directly queries hunger_helper.db for all real container points
    and classifies them by shape and representative color.
    """
    if not os.path.exists(DB_PATH):
        return []
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
    SELECT DISTINCT title, x, y 
    FROM map_points 
    WHERE map_name = ? AND point_type = 'loot' AND (
        title LIKE 'Flour %' OR title LIKE 'Opium Pipe %' OR title LIKE 'China Bowl %' OR title LIKE 'Charcoal %' OR title LIKE 'Saltpetre %' OR title LIKE 'Bone Char %'
    );
    ''', (map_name,))
    rows = c.fetchall()
    conn.close()
    
    classified = []
    for title, x, y in rows:
        if 'Flour Sack' in title:
            classified.append({'x': x, 'y': y, 'type': 'flour_sack', 'shape': 'circle', 'color': COLOR_SACK, 'label': 'Flour Sack', 'is_100': True})
        elif 'Bullion Box' in title or 'Jewellery Box' in title:
            classified.append({'x': x, 'y': y, 'type': 'bullion_box', 'shape': 'diamond', 'color': COLOR_BULLION, 'label': 'Bullion / Jewellery Box', 'is_prio': True, 'is_100': True})
        elif 'Wall Cabinet' in title:
            classified.append({'x': x, 'y': y, 'type': 'wall_cabinet', 'shape': 'square', 'color': COLOR_CABINET, 'label': 'Wall Cabinet', 'is_prio': True, 'is_100': True})
        elif 'Pile of Ash' in title:
            classified.append({'x': x, 'y': y, 'type': 'pile_of_ash', 'shape': 'ring', 'color': COLOR_ASH, 'label': 'Pile of Ash', 'is_100': True})
        elif 'Tooling Bin' in title:
            classified.append({'x': x, 'y': y, 'type': 'tooling_bin', 'shape': 'triangle', 'color': COLOR_TOOLING, 'label': 'Tooling Bin', 'is_100': True})
            
    return classified

# ==========================================
# QUESTLINE PROGRESSION HUD BAR (ON MAP TOP)
# Displays full questline with active grouped turn-ins!
# ==========================================
def render_questline_progression_bar(draw, current_raid_id, grouped_turnin_label=None):
    """
    Renders a sleek, high-visibility Questline Progression HUD bar across the top of the map.
    Shows the journey from Q1 Hub -> Q2 Flour -> Q3 Gavroche -> Q4 Charcoal -> Q5 Map -> Q6 Medical -> Q8 Candle -> Q9 Bribery -> Q10 Books -> Q11 Crossing!
    """
    bar_x = MAP_X + 16
    bar_y = MAP_Y + 12
    bar_w = MAP_W - 32
    bar_h = 44
    
    # Dark frosted glass HUD
    draw.rounded_rectangle([bar_x, bar_y, bar_x+bar_w, bar_y+bar_h], radius=8, fill=(11, 15, 24), outline=(51, 65, 85), width=2)
    
    # Tag
    draw.text((bar_x+16, bar_y+12), "QUESTLINE PROGRESSION:", fill=(160, 180, 205), font=F_SMALL_BOLD)
    
    # 7 Main Phases matching the 7 Raids
    steps = [
        (1, "Q2: Flour"),
        (2, "Q3: Gavroche & Q2 Turn-in"),
        (3, "Q4: Charcoal"),
        (4, "Q8: Candle & Contraband"),
        (5, "Q10: Sinai Books 1-3"),
        (6, "Q10: Sinai Books 4-5"),
        (7, "Q10: Finale Books 6-7")
    ]
    
    cur_x = bar_x + 230
    for s_id, s_name in steps:
        if s_id < current_raid_id:
            # Completed
            lbl = f"✓ {s_name}"
            draw.text((cur_x, bar_y+13), lbl, fill=(34, 197, 94), font=F_SMALL)
            cur_x += int(draw.textlength(lbl, font=F_SMALL)) + 18
            draw.text((cur_x-10, bar_y+13), "➔", fill=(70, 85, 105), font=F_SMALL)
        elif s_id == current_raid_id:
            # Current Active Raid (Highlighted with bright Yellow badge)
            active_text = grouped_turnin_label if grouped_turnin_label else f"ACTIVE: {s_name}"
            tw = int(draw.textlength(active_text, font=F_SMALL_BOLD)) + 20
            draw.rounded_rectangle([cur_x-4, bar_y+6, cur_x+tw, bar_y+bar_h-6], radius=6, fill=(45, 38, 12), outline=COLOR_SACK, width=2)
            draw.text((cur_x+6, bar_y+12), active_text, fill=COLOR_SACK, font=F_SMALL_BOLD)
            cur_x += tw + 18
            if s_id < 7:
                draw.text((cur_x-10, bar_y+13), "➔", fill=(70, 85, 105), font=F_SMALL)
        else:
            # Upcoming
            draw.text((cur_x, bar_y+13), s_name, fill=(120, 135, 155), font=F_SMALL)
            cur_x += int(draw.textlength(s_name, font=F_SMALL)) + 18
            if s_id < 7:
                draw.text((cur_x-10, bar_y+13), "➔", fill=(60, 75, 95), font=F_SMALL)

print("V12 Core Ready.")
