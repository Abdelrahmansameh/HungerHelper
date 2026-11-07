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

# Strict Quest Priority Palette: Yellow -> Purple -> Blue -> Green -> Grey
PRIO_YELLOW = (250, 204, 21)   # Top Priority: Active Quest Objective (Must Complete)
PRIO_PURPLE = (192, 132, 252)  # Priority 2: Focus Target / Next Required Pre-Farm
PRIO_BLUE   = (56, 189, 248)   # Priority 3: Secondary Upcoming Quest Objective
PRIO_GREEN  = (74, 222, 128)   # Priority 4: Tertiary Upcoming Quest Objective
PRIO_GREY   = (148, 163, 184)  # Priority 5: General Loot

def load_font(name_list, size):
    for f in name_list:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()

SANS_BOLD = ["C:\\Windows\\Fonts\\segoeuib.ttf", "C:\\Windows\\Fonts\\arialbd.ttf", "C:\\Windows\\Fonts\\tahomabd.ttf"]
SANS_REG = ["C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\tahoma.ttf"]

F_HEADER_TITLE = load_font(SANS_BOLD, 28)
F_HEADER_TAG = load_font(SANS_BOLD, 16)
F_SECTION_TITLE = load_font(SANS_BOLD, 22)
F_CARD_TITLE = load_font(SANS_BOLD, 18)
F_BODY_BOLD = load_font(SANS_BOLD, 16)
F_BODY = load_font(SANS_REG, 15)
F_SMALL_BOLD = load_font(SANS_BOLD, 13)
F_SMALL = load_font(SANS_REG, 13)
F_TINY = load_font(SANS_REG, 12)

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

def fit_text(draw, text, font, max_w):
    if draw.textlength(text, font=font) <= max_w:
        return text
    while len(text) > 3 and draw.textlength(text + "...", font=font) > max_w:
        text = text[:-1]
    return text + "..."

def paste_icon_safe(target_img, icon_img, box, bg_color=None, border_color=None, border_w=1, radius=6):
    border_w = int(border_w)
    x, y, w, h = box
    if bg_color:
        draw = ImageDraw.Draw(target_img)
        draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=bg_color, outline=border_color, width=border_w)
    
    if icon_img is None:
        return
        
    pad = 3
    iw, ih = w - (pad * 2), h - (pad * 2)
    ico_resized = icon_img.resize((iw, ih), Image.Resampling.LANCZOS)
    target_img.paste(ico_resized, (x+pad, y+pad), ico_resized)

# ==========================================
# MAP ICONS: 
# ACTIVE OBJECTIVE = CIRCLE WITH WIDER OUTER CIRCLE LINE
# FUTURE / BANKED  = SIMPLE CIRCLE
# (NO LETTER INDICATION AS REQUESTED)
# ==========================================
def draw_container_shape(draw, shape, cx, cy, r, color, outline=(10, 14, 20), width=2):
    width = int(width)
    if shape in ('wide_circle', 'active', 'square'):
        # Active Raid Objective: Circle with a wider outer circle line
        r_out = r + 4
        # High contrast dark backing
        draw.ellipse([cx-r_out-1, cy-r_out-1, cx+r_out+1, cy+r_out+1], outline=(10, 14, 20), width=5)
        # Outer wide circle line
        draw.ellipse([cx-r_out, cy-r_out, cx+r_out, cy+r_out], outline=color, width=3)
        # Inner core filled circle
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color, outline=(10, 14, 20), width=2)
    else:
        # Future quests / normal containers: Simple filled circle
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color, outline=outline, width=width)

# ==========================================
# PROMINENT POI DISCOVERY MARKER (RADIAL GOLD CIRCLE WITH WIDE OUTER LINE + PILL)
# ==========================================
def draw_poi_marker(draw, cx, cy, label, offset_dir='top'):
    r_core = 13
    r_out = 18
    
    # Active POI is a highlighted Circle with a wide outer gold circle line
    draw.ellipse([cx-r_out-1, cy-r_out-1, cx+r_out+1, cy+r_out+1], outline=(10, 14, 20), width=5)
    draw.ellipse([cx-r_out, cy-r_out, cx+r_out, cy+r_out], outline=PRIO_YELLOW, width=3)
    draw.ellipse([cx-r_core, cy-r_core, cx+r_core, cy+r_core], fill=PRIO_YELLOW, outline=(10, 14, 20), width=2)
    # Central dark dot
    draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(10, 14, 20))

    tag = f"{label.upper()}"
    tw = int(draw.textlength(tag, font=F_SMALL_BOLD))
    th = 16
    pad_x = 10
    pad_y = 6
    pill_w = tw + pad_x * 2
    pill_h = th + pad_y * 2
    
    if offset_dir == 'top':
        pill_x = cx - pill_w // 2
        pill_y = cy - pill_h - 22
        draw.line([(cx, cy - r_out - 2), (cx, pill_y + pill_h)], fill=PRIO_YELLOW, width=2)
    elif offset_dir == 'bottom':
        pill_x = cx - pill_w // 2
        pill_y = cy + 24
        draw.line([(cx, cy + r_out + 2), (cx, pill_y)], fill=PRIO_YELLOW, width=2)
    elif offset_dir == 'right':
        pill_x = cx + 26
        pill_y = cy - pill_h // 2
        draw.line([(cx + r_out + 2, cy), (pill_x, cy)], fill=PRIO_YELLOW, width=2)
    else: # left
        pill_x = cx - pill_w - 26
        pill_y = cy - pill_h // 2
        draw.line([(cx - r_out - 2, cy), (pill_x + pill_w, cy)], fill=PRIO_YELLOW, width=2)
        
    pill_x = max(MAP_X + 10, min(MAP_X + MAP_W - pill_w - 10, pill_x))
    pill_y = max(MAP_Y + 65, min(MAP_Y + MAP_H - pill_h - 10, pill_y))
    
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=6, fill=(12, 16, 24), outline=PRIO_YELLOW, width=2)
    draw.text((pill_x + pad_x, pill_y + pad_y - 2), tag, fill=PRIO_YELLOW, font=F_SMALL_BOLD)

# ==========================================
# FETCH FILTERED MAP LOOT
# ==========================================
def get_filtered_loot_from_db(map_name, container_priority_map):
    if not os.path.exists(DB_PATH) or not container_priority_map:
        return []
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
    SELECT DISTINCT title, x, y 
    FROM map_points 
    WHERE map_name = ? AND point_type = 'loot';
    ''', (map_name,))
    rows = c.fetchall()
    conn.close()
    
    classified = []
    for title, x, y in rows:
        if map_name == 'Sarlat Farm' and x > 3200 and y > 3000:
            continue
            
        for c_key, c_info in container_priority_map.items():
            if c_info['keyword'] in title:
                classified.append({
                    'x': x, 'y': y,
                    'type': c_key,
                    'shape': c_info['shape'],
                    'color': c_info['color'],
                    'is_prio': c_info.get('is_prio', False),
                    'label': c_info['label']
                })
                break
                
    return classified

# ==========================================
# QUESTLINE PROGRESSION HUD BAR (EVENLY SPACED 7 COLUMNS)
# ==========================================
def render_questline_progression_bar(draw, current_raid_id):
    bar_x = MAP_X + 16
    bar_y = MAP_Y + 10
    bar_w = MAP_W - 32
    bar_h = 44
    
    draw.rounded_rectangle([bar_x, bar_y, bar_x+bar_w, bar_y+bar_h], radius=8, fill=(11, 15, 24), outline=(51, 65, 85), width=2)
    
    steps = [
        (1, "R1: 20x Flour"),
        (2, "R2: Camp & Charcoal"),
        (3, "R3: Fort & Supplies"),
        (4, "R4: Candle & Bribery"),
        (5, "R5: Sinai Books 1-3"),
        (6, "R6: Sinai Books 4-5"),
        (7, "R7: Sinai Finale")
    ]
    
    pad_total = 14
    inner_w = bar_w - (pad_total * 2)
    gap = 8
    card_w = (inner_w - (gap * 6)) // 7
    card_h = 32
    
    for i, (s_id, s_name) in enumerate(steps):
        cx = bar_x + pad_total + i * (card_w + gap)
        cy = bar_y + 6
        
        if s_id < current_raid_id:
            # COMPLETED
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=5, fill=(16, 32, 22), outline=(34, 197, 94), width=1)
            lbl = f"[DONE] {s_name}"
            tw = draw.textlength(lbl, font=F_SMALL_BOLD)
            draw.text((cx + (card_w - tw)/2, cy + 8), lbl, fill=(74, 222, 128), font=F_SMALL_BOLD)
        elif s_id == current_raid_id:
            # ACTIVE CURRENT RAID
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=5, fill=(52, 42, 12), outline=PRIO_YELLOW, width=2)
            lbl = f"ACTIVE: {s_name}"
            tw = draw.textlength(lbl, font=F_SMALL_BOLD)
            draw.text((cx + (card_w - tw)/2, cy + 8), lbl, fill=PRIO_YELLOW, font=F_SMALL_BOLD)
        else:
            # UPCOMING
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=5, fill=(16, 20, 28), outline=(45, 58, 78), width=1)
            lbl = s_name
            tw = draw.textlength(lbl, font=F_SMALL)
            draw.text((cx + (card_w - tw)/2, cy + 8), lbl, fill=(130, 145, 165), font=F_SMALL)
            
        if i < 6:
            draw.text((cx + card_w + 1, cy + 8), ">", fill=(70, 85, 105), font=F_SMALL_BOLD)

print("V19 Core Ready.")
