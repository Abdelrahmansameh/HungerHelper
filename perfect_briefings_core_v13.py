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
# ==========================================
def draw_container_shape(draw, shape, cx, cy, r, color, outline=(15, 20, 30), width=2):
    width = int(width)
    if shape == 'circle':
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color, outline=outline, width=width)
    elif shape == 'diamond':
        pts = [(cx, cy-r-2), (cx+r+2, cy), (cx, cy+r+2), (cx-r-2, cy)]
        draw.polygon(pts, fill=color, outline=outline, width=width)
    elif shape == 'square':
        draw.rectangle([cx-r+1, cy-r+1, cx+r-1, cy+r-1], fill=color, outline=outline, width=width)
    elif shape == 'ring':
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(25, 30, 40), outline=color, width=width+1)
        draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=color)
    elif shape == 'triangle':
        pts = [(cx, cy-r-1), (cx+r+1, cy+r), (cx-r-1, cy+r)]
        draw.polygon(pts, fill=color, outline=outline, width=width)
    elif shape == 'star':
        s1 = r + 3
        s2 = int(r * 0.4)
        pts = [
            (cx, cy-s1), (cx+s2, cy-s2), (cx+s1, cy), (cx+s2, cy+s2),
            (cx, cy+s1), (cx-s2, cy+s2), (cx-s1, cy), (cx-s2, cy-s2)
        ]
        draw.polygon(pts, fill=color, outline=outline, width=width)

# ==========================================
# SUGGESTION A: PROMINENT POI DISCOVERY MARKER
# 24x24 Radiant Gold Star + Callout Pill
# ==========================================
def draw_poi_marker(draw, cx, cy, label, offset_dir='top'):
    # Radiant 8-point gold star
    r_outer = 13
    r_inner = 5
    pts = []
    for i in range(8):
        angle = i * (math.pi / 4.0) - (math.pi / 2.0)
        pts.append((cx + math.cos(angle) * r_outer, cy + math.sin(angle) * r_outer))
        mid_angle = angle + (math.pi / 8.0)
        pts.append((cx + math.cos(mid_angle) * r_inner, cy + math.sin(mid_angle) * r_inner))
    
    # Outer dark halo
    draw.ellipse([cx-17, cy-17, cx+17, cy+17], fill=(16, 20, 28), outline=COLOR_STORY, width=2)
    # Gold star
    draw.polygon(pts, fill=COLOR_STORY, outline=(15, 20, 30), width=2)
    # Inner bright core
    draw.ellipse([cx-2, cy-2, cx+2, cy+2], fill=(255, 255, 255))
    
    # Callout Pill Badge
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
        draw.line([(cx, cy - 17), (cx, pill_y + pill_h)], fill=COLOR_STORY, width=2)
    elif offset_dir == 'bottom':
        pill_x = cx - pill_w // 2
        pill_y = cy + 20
        draw.line([(cx, cy + 17), (cx, pill_y)], fill=COLOR_STORY, width=2)
    elif offset_dir == 'right':
        pill_x = cx + 24
        pill_y = cy - pill_h // 2
        draw.line([(cx + 17, cy), (pill_x, cy)], fill=COLOR_STORY, width=2)
    else: # left
        pill_x = cx - pill_w - 24
        pill_y = cy - pill_h // 2
        draw.line([(cx - 17, cy), (pill_x + pill_w, cy)], fill=COLOR_STORY, width=2)
        
    # Clamp inside map bounds
    pill_x = max(MAP_X + 10, min(MAP_X + MAP_W - pill_w - 10, pill_x))
    pill_y = max(MAP_Y + 65, min(MAP_Y + MAP_H - pill_h - 10, pill_y))
    
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=6, fill=(12, 16, 24), outline=COLOR_STORY, width=2)
    draw.text((pill_x + pad_x, pill_y + pad_y - 2), tag, fill=COLOR_STORY, font=F_SMALL_BOLD)

# ==========================================
# SUGGESTION D: TACTICAL EXTRACTION VECTORS
# Semi-transparent dashed path + SPAWN & EXTRACT pills
# ==========================================
def draw_arrow_head(draw, center, direction, color, size=11):
    cx, cy = center
    ux, uy = direction
    px, py = -uy, ux
    tip_x, tip_y = cx + ux * size, cy + uy * size
    base_x, base_y = cx - ux * (size * 0.4), cy - uy * (size * 0.4)
    left_x, left_y = base_x + px * (size * 0.6), base_y + py * (size * 0.6)
    right_x, right_y = base_x - px * (size * 0.6), base_y - py * (size * 0.6)
    draw.polygon([(tip_x, tip_y), (left_x, left_y), (right_x, right_y)], fill=color)

def draw_dashed_vector(draw, pts, color=(56, 189, 248), width=3, dash_len=14, gap_len=8):
    if len(pts) < 2:
        return
        
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            continue
        ux, uy = dx / dist, dy / dist
        curr = 0
        while curr < dist:
            end = min(curr + dash_len, dist)
            sx, sy = x1 + ux * curr, y1 + uy * curr
            ex, ey = x1 + ux * end, y1 + uy * end
            draw.line([(sx, sy), (ex, ey)], fill=color, width=int(width))
            curr += dash_len + gap_len
            
        # Draw directional chevron at 40% and 75% along each segment
        draw_arrow_head(draw, (x1 + ux * (dist * 0.4), y1 + uy * (dist * 0.4)), (ux, uy), color, size=11)
        if dist > 350:
            draw_arrow_head(draw, (x1 + ux * (dist * 0.75), y1 + uy * (dist * 0.75)), (ux, uy), color, size=11)

    # 1. SPAWN Pill at pts[0]
    sx, sy = pts[0]
    sp_w, sp_h = 100, 28
    draw.rounded_rectangle([sx-sp_w//2, sy-sp_h//2, sx+sp_w//2, sy+sp_h//2], radius=6, fill=(16, 75, 42), outline=(34, 197, 94), width=2)
    # Green flag graphic
    draw.line([(sx-36, sy-8), (sx-36, sy+9)], fill=(255, 255, 255), width=2)
    draw.polygon([(sx-36, sy-8), (sx-24, sy-4), (sx-36, sy)], fill=(34, 197, 94))
    draw.text((sx-16, sy-9), "SPAWN", fill=(255, 255, 255), font=F_BADGE)

    # 2. EXTRACT Pill at pts[-1]
    ex, ey = pts[-1]
    ex_w, ex_h = 110, 28
    draw.rounded_rectangle([ex-ex_w//2, ey-ex_h//2, ex+ex_w//2, ey+ex_h//2], radius=6, fill=(14, 55, 75), outline=(56, 189, 248), width=2)
    # Cyan extract gate graphic
    draw.rectangle([ex-40, ey-8, ex-30, ey+8], fill=(20, 35, 50), outline=(56, 189, 248), width=1)
    draw.text((ex-22, ey-9), "EXTRACT", fill=(255, 255, 255), font=F_BADGE)

# ==========================================
# FETCH ALL MAP LOOT POINTS FROM DATABASE
# ==========================================
def get_map_loot_from_db(map_name):
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
# ==========================================
def render_questline_progression_bar(draw, current_raid_id, grouped_turnin_label=None):
    bar_x = MAP_X + 16
    bar_y = MAP_Y + 12
    bar_w = MAP_W - 32
    bar_h = 44
    
    draw.rounded_rectangle([bar_x, bar_y, bar_x+bar_w, bar_y+bar_h], radius=8, fill=(11, 15, 24), outline=(51, 65, 85), width=2)
    draw.text((bar_x+16, bar_y+12), "QUESTLINE PROGRESSION:", fill=(160, 180, 205), font=F_SMALL_BOLD)
    
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
            lbl = f"\u2713 {s_name}"
            draw.text((cur_x, bar_y+13), lbl, fill=(34, 197, 94), font=F_SMALL)
            cur_x += int(draw.textlength(lbl, font=F_SMALL)) + 18
            draw.text((cur_x-10, bar_y+13), "\u2794", fill=(70, 85, 105), font=F_SMALL)
        elif s_id == current_raid_id:
            active_text = grouped_turnin_label if grouped_turnin_label else f"ACTIVE: {s_name}"
            tw = int(draw.textlength(active_text, font=F_SMALL_BOLD)) + 20
            draw.rounded_rectangle([cur_x-4, bar_y+6, cur_x+tw, bar_y+bar_h-6], radius=6, fill=(45, 38, 12), outline=COLOR_SACK, width=2)
            draw.text((cur_x+6, bar_y+12), active_text, fill=COLOR_SACK, font=F_SMALL_BOLD)
            cur_x += tw + 18
            if s_id < 7:
                draw.text((cur_x-10, bar_y+13), "\u2794", fill=(70, 85, 105), font=F_SMALL)
        else:
            draw.text((cur_x, bar_y+13), s_name, fill=(120, 135, 155), font=F_SMALL)
            cur_x += int(draw.textlength(s_name, font=F_SMALL)) + 18
            if s_id < 7:
                draw.text((cur_x-10, bar_y+13), "\u2794", fill=(60, 75, 95), font=F_SMALL)

print("V13 Core Ready.")
