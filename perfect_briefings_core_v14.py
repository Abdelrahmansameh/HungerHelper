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
PRIO_PURPLE = (192, 132, 252)  # Priority 2: Next Immediate Quest Objective
PRIO_BLUE   = (56, 189, 248)   # Priority 3: Secondary Upcoming Quest Objective
PRIO_GREEN  = (74, 222, 128)   # Priority 4: Tertiary Upcoming Quest Objective
PRIO_GREY   = (148, 163, 184)  # Priority 5: General / Secondary Loot

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
# SHAPES COMMUNICATE QUEST ROLE & RAID SENSITIVITY
# ==========================================
def draw_container_shape(draw, shape, cx, cy, r, color, outline=(15, 20, 30), width=2):
    width = int(width)
    if shape == 'circle':
        # Active Raid Objective Container
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color, outline=outline, width=width)
    elif shape == 'diamond':
        # Future Banked Quest Item Container
        pts = [(cx, cy-r-2), (cx+r+2, cy), (cx, cy+r+2), (cx-r-2, cy)]
        draw.polygon(pts, fill=color, outline=outline, width=width)
    elif shape == 'ring':
        # General / Secondary Loot Container
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(20, 26, 38), outline=color, width=width+1)
        draw.ellipse([cx-2, cy-2, cx+2, cy+2], fill=color)
    elif shape == 'star':
        # Radiant Story POI Trigger
        s1 = r + 3
        s2 = int(r * 0.4)
        pts = [
            (cx, cy-s1), (cx+s2, cy-s2), (cx+s1, cy), (cx+s2, cy+s2),
            (cx, cy+s1), (cx-s2, cy+s2), (cx-s1, cy), (cx-s2, cy-s2)
        ]
        draw.polygon(pts, fill=color, outline=outline, width=width)

# ==========================================
# PROMINENT POI DISCOVERY MARKER (RADIAL GOLD STAR + PILL)
# ==========================================
def draw_poi_marker(draw, cx, cy, label, offset_dir='top'):
    r_outer = 13
    r_inner = 5
    pts = []
    for i in range(8):
        angle = i * (math.pi / 4.0) - (math.pi / 2.0)
        pts.append((cx + math.cos(angle) * r_outer, cy + math.sin(angle) * r_outer))
        mid_angle = angle + (math.pi / 8.0)
        pts.append((cx + math.cos(mid_angle) * r_inner, cy + math.sin(mid_angle) * r_inner))
    
    draw.ellipse([cx-17, cy-17, cx+17, cy+17], fill=(16, 20, 28), outline=PRIO_YELLOW, width=2)
    draw.polygon(pts, fill=PRIO_YELLOW, outline=(15, 20, 30), width=2)
    draw.ellipse([cx-2, cy-2, cx+2, cy+2], fill=(255, 255, 255))
    
    tag = f"\u2726 {label.upper()}"
    tw = int(draw.textlength(tag, font=F_SMALL_BOLD))
    th = 16
    pad_x = 10
    pad_y = 6
    pill_w = tw + pad_x * 2
    pill_h = th + pad_y * 2
    
    if offset_dir == 'top':
        pill_x = cx - pill_w // 2
        pill_y = cy - pill_h - 16
        draw.line([(cx, cy - 17), (cx, pill_y + pill_h)], fill=PRIO_YELLOW, width=2)
    elif offset_dir == 'bottom':
        pill_x = cx - pill_w // 2
        pill_y = cy + 20
        draw.line([(cx, cy + 17), (cx, pill_y)], fill=PRIO_YELLOW, width=2)
    elif offset_dir == 'right':
        pill_x = cx + 24
        pill_y = cy - pill_h // 2
        draw.line([(cx + 17, cy), (pill_x, cy)], fill=PRIO_YELLOW, width=2)
    else: # left
        pill_x = cx - pill_w - 24
        pill_y = cy - pill_h // 2
        draw.line([(cx - 17, cy), (pill_x + pill_w, cy)], fill=PRIO_YELLOW, width=2)
        
    pill_x = max(MAP_X + 10, min(MAP_X + MAP_W - pill_w - 10, pill_x))
    pill_y = max(MAP_Y + 65, min(MAP_Y + MAP_H - pill_h - 10, pill_y))
    
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=6, fill=(12, 16, 24), outline=PRIO_YELLOW, width=2)
    draw.text((pill_x + pad_x, pill_y + pad_y - 2), tag, fill=PRIO_YELLOW, font=F_SMALL_BOLD)

# ==========================================
# FETCH FILTERED MAP LOOT (NO UNDERCROFT, ONLY ACTIVE RAID RELEVANT)
# ==========================================
def get_filtered_loot_from_db(map_name, container_priority_map):
    if not os.path.exists(DB_PATH):
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
        # User requirement: remove undercroft containers down-right on Sarlat map
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
# QUESTLINE PROGRESSION HUD BAR (TRUE STORYLINE PROGRESSION)
# ==========================================
def render_questline_progression_bar(draw, current_raid_id, active_label=None):
    bar_x = MAP_X + 16
    bar_y = MAP_Y + 12
    bar_w = MAP_W - 32
    bar_h = 44
    
    draw.rounded_rectangle([bar_x, bar_y, bar_x+bar_w, bar_y+bar_h], radius=8, fill=(11, 15, 24), outline=(51, 65, 85), width=2)
    draw.text((bar_x+16, bar_y+13), "QUEST PROGRESSION:", fill=(160, 180, 205), font=F_SMALL_BOLD)
    
    # 7 Distinct Deployments across the Eloise Storyline
    steps = [
        (1, "Q2: Flour"),
        (2, "Q3: Gavroche Camp"),
        (3, "Q4: Charcoal & Q5 Recon"),
        (4, "Q8: Candle & Bribery"),
        (5, "Q10: Sinai 1-3 (Sarlat)"),
        (6, "Q10: Sinai 4-5 (Bridge)"),
        (7, "Q10: Sinai 6-7 (Finale)")
    ]
    
    cur_x = bar_x + 205
    for s_id, s_name in steps:
        if s_id < current_raid_id:
            lbl = f"\u2713 {s_name}"
            draw.text((cur_x, bar_y+13), lbl, fill=(34, 197, 94), font=F_SMALL)
            cur_x += int(draw.textlength(lbl, font=F_SMALL)) + 16
            draw.text((cur_x-9, bar_y+13), "\u2794", fill=(70, 85, 105), font=F_SMALL)
        elif s_id == current_raid_id:
            txt = active_label if active_label else f"ACTIVE: {s_name}"
            tw = int(draw.textlength(txt, font=F_SMALL_BOLD)) + 20
            draw.rounded_rectangle([cur_x-4, bar_y+6, cur_x+tw, bar_y+bar_h-6], radius=6, fill=(45, 38, 12), outline=PRIO_YELLOW, width=2)
            draw.text((cur_x+6, bar_y+12), txt, fill=PRIO_YELLOW, font=F_SMALL_BOLD)
            cur_x += tw + 16
            if s_id < 7:
                draw.text((cur_x-9, bar_y+13), "\u2794", fill=(70, 85, 105), font=F_SMALL)
        else:
            draw.text((cur_x, bar_y+13), s_name, fill=(110, 125, 145), font=F_SMALL)
            cur_x += int(draw.textlength(s_name, font=F_SMALL)) + 16
            if s_id < 7:
                draw.text((cur_x-9, bar_y+13), "\u2794", fill=(55, 70, 90), font=F_SMALL)

print("V14 Core Ready.")
