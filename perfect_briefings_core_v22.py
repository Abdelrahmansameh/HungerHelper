import os, sys, math, sqlite3
from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 2400
CANVAS_H = 1400

# Top Header Bar
HEADER_H = 78

# Map occupies left 68%, clean view with NO HUD overlay!
MAP_X = 20
MAP_Y = 88
MAP_W = 1630
MAP_H = 1292

# Right Briefing Panel occupies remaining 31%
PANEL_X = 1670
PANEL_Y = 88
PANEL_W = 710
PANEL_H = 1292

# Hunger Companion Authentic Colors
BG_CANVAS     = (11, 11, 9)       # #0b0b09 (Deep Obsidian)
BG_PANEL      = (21, 21, 18)      # #151512 (Dark Card Panel)
BG_CARD       = (28, 28, 24)      # #1c1c18 (Card surface)
BG_CARD_LIGHT = (36, 36, 30)      # #24241e
BORDER_SUBTLE = (48, 44, 36)      # #302c24 (Antique Bronze border)
BORDER_FOCUS  = (80, 72, 55)      # #504837

COLOR_GOLD      = (229, 192, 123) # #e5c07b (Hunger Companion Title Gold)
COLOR_PARCHMENT = (240, 235, 224) # #f0ebe0
COLOR_MUTED     = (168, 160, 145) # #a8a091
COLOR_DIM       = (125, 118, 105) # #7d7669

# Strict Quest Priority Palette
PRIO_YELLOW = (250, 204, 21)   # Priority 1: Active Objective
PRIO_PURPLE = (192, 132, 252)  # Priority 2: Focus Target
PRIO_BLUE   = (56, 189, 248)   # Priority 3: Secondary Target
PRIO_GREEN  = (74, 222, 128)   # Priority 4: Tertiary Target
PRIO_GREY   = (148, 163, 184)  # Priority 5: Extract / Secondary

def load_font(name_list, size):
    for f in name_list:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()

SERIF_BOLD = ["C:\\Windows\\Fonts\\georgiab.ttf", "C:\\Windows\\Fonts\\cambriab.ttf", "C:\\Windows\\Fonts\\timesbd.ttf"]
SERIF_REG  = ["C:\\Windows\\Fonts\\georgia.ttf", "C:\\Windows\\Fonts\\cambria.ttc", "C:\\Windows\\Fonts\\times.ttf"]
SANS_BOLD  = ["C:\\Windows\\Fonts\\segoeuib.ttf", "C:\\Windows\\Fonts\\arialbd.ttf", "C:\\Windows\\Fonts\\tahomabd.ttf"]
SANS_REG   = ["C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\tahoma.ttf"]

# Consistent Typography across all raids
F_HEADER_TITLE  = load_font(SERIF_BOLD, 24)
F_HEADER_TAG    = load_font(SANS_BOLD, 15)
F_SECTION_TITLE = load_font(SERIF_BOLD, 22)
F_CARD_TITLE    = load_font(SERIF_BOLD, 18)
F_BODY_BOLD     = load_font(SANS_BOLD, 16)
F_BODY          = load_font(SANS_REG, 15)
F_SMALL_BOLD    = load_font(SANS_BOLD, 14)
F_SMALL         = load_font(SANS_REG, 13)
F_TINY          = load_font(SANS_REG, 12)

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
        
    pad = 3
    iw, ih = w - (pad * 2), h - (pad * 2)
    ico_resized = icon_img.resize((iw, ih), Image.Resampling.LANCZOS)
    target_img.paste(ico_resized, (x+pad, y+pad), ico_resized)

# ==========================================
# MAP ICONS: 
# BIGGER IMAGES, UNIFORM CIRCLE (NO EXTRA OUTER PART)
# RADIUS = 16, EMBEDDED ITEM ICON = 22x22
# ==========================================
def draw_container_shape(draw, cx, cy, r, color, item_img_name=None, canvas=None):
    draw.ellipse([cx-r-1, cy-r-1, cx+r+1, cy+r+1], outline=(10, 10, 8), width=3)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(16, 16, 13), outline=color, width=2)
    
    if item_img_name and canvas and item_img_name in ITEM_IMGS:
        ico = ITEM_IMGS[item_img_name]
        sz = max(16, int(r * 1.38))
        ico_resized = ico.resize((sz, sz), Image.Resampling.LANCZOS)
        canvas.paste(ico_resized, (int(cx - sz/2), int(cy - sz/2)), ico_resized)
    else:
        draw.ellipse([cx-r+4, cy-r+4, cx+r-4, cy+r-4], fill=color)

# ==========================================
# PROMINENT POI DISCOVERY MARKER (BIGGER ITEM ICON + GOLD PILL)
# ==========================================
def draw_poi_marker(draw, cx, cy, label, offset_dir='top', item_img_name=None, canvas=None):
    r_core = 16
    
    draw.ellipse([cx-r_core-2, cy-r_core-2, cx+r_core+2, cy+r_core+2], outline=(10, 10, 8), width=4)
    draw.ellipse([cx-r_core, cy-r_core, cx+r_core, cy+r_core], fill=(16, 16, 13), outline=COLOR_GOLD, width=3)
    
    if item_img_name and canvas and item_img_name in ITEM_IMGS:
        ico = ITEM_IMGS[item_img_name]
        sz = 22
        ico_resized = ico.resize((sz, sz), Image.Resampling.LANCZOS)
        canvas.paste(ico_resized, (cx - sz//2, cy - sz//2), ico_resized)
    else:
        draw.ellipse([cx-5, cy-5, cx+5, cy+5], fill=COLOR_GOLD)

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
        draw.line([(cx, cy - r_core - 2), (cx, pill_y + pill_h)], fill=COLOR_GOLD, width=2)
    elif offset_dir == 'bottom':
        pill_x = cx - pill_w // 2
        pill_y = cy + 24
        draw.line([(cx, cy + r_core + 2), (cx, pill_y)], fill=COLOR_GOLD, width=2)
    elif offset_dir == 'right':
        pill_x = cx + 26
        pill_y = cy - pill_h // 2
        draw.line([(cx + r_core + 2, cy), (pill_x, cy)], fill=COLOR_GOLD, width=2)
    else: # left
        pill_x = cx - pill_w - 26
        pill_y = cy - pill_h // 2
        draw.line([(cx - r_core - 2, cy), (pill_x + pill_w, cy)], fill=COLOR_GOLD, width=2)
        
    pill_x = max(MAP_X + 10, min(MAP_X + MAP_W - pill_w - 10, pill_x))
    pill_y = max(MAP_Y + 10, min(MAP_Y + MAP_H - pill_h - 10, pill_y))
    
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=6, fill=(18, 18, 15), outline=COLOR_GOLD, width=2)
    draw.text((pill_x + pad_x, pill_y + pad_y - 2), tag, fill=COLOR_GOLD, font=F_SMALL_BOLD)

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
    seen = set()
    for title, x, y in rows:
        if map_name == 'Sarlat Farm' and x > 3200 and y > 3000:
            continue
            
        for c_key, c_info in container_priority_map.items():
            if c_info['keyword'] in title:
                coord_key = (c_key, int(round(x / 6.0)), int(round(y / 6.0)))
                if coord_key in seen:
                    continue
                seen.add(coord_key)
                
                classified.append({
                    'x': x, 'y': y,
                    'type': c_key,
                    'color': c_info['color'],
                    'item_img': c_info.get('item_img'),
                    'is_prio': c_info.get('is_prio', False),
                    'label': c_info['label']
                })
                break
                
    return classified

# ==========================================
# PLOT DECLUSTERED MAP MARKERS:
# LARGER MARKERS (r=16), RADIAL FAN WITH PRIORITY-COLORED LINES
# ==========================================
def plot_declustered_points(draw, canvas, points, to_coord_fn):
    if not points:
        return
        
    screen_pts = []
    for pt in points:
        sx, sy = to_coord_fn(pt['x'], pt['y'])
        screen_pts.append({
            'sx': sx, 'sy': sy,
            'color': pt['color'],
            'item_img': pt['item_img'],
            'type': pt['type']
        })
        
    clusters = []
    assigned = [False] * len(screen_pts)
    
    for i in range(len(screen_pts)):
        if assigned[i]:
            continue
        cluster = [screen_pts[i]]
        assigned[i] = True
        
        for j in range(i + 1, len(screen_pts)):
            if assigned[j]:
                continue
            for c_pt in cluster:
                d = math.hypot(c_pt['sx'] - screen_pts[j]['sx'], c_pt['sy'] - screen_pts[j]['sy'])
                if d < 26:
                    cluster.append(screen_pts[j])
                    assigned[j] = True
                    break
        clusters.append(cluster)
        
    for cluster in clusters:
        unique_items = []
        seen_types = set()
        for p in cluster:
            if p['type'] not in seen_types:
                seen_types.add(p['type'])
                unique_items.append(p)
                
        if len(unique_items) == 1:
            # Single container: draw directly on spawn
            p = unique_items[0]
            draw_container_shape(draw, p['sx'], p['sy'], 16, p['color'], item_img_name=p['item_img'], canvas=canvas)
        else:
            # Multiple containers: Anchor dot + radial fan with priority-colored lines
            cx = int(sum(p['sx'] for p in cluster) / len(cluster))
            cy = int(sum(p['sy'] for p in cluster) / len(cluster))
            
            top_color = unique_items[0]['color']
            draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=top_color, outline=(10, 10, 8), width=1)
            
            k = len(unique_items)
            r_orbit = 38
            
            for idx, p in enumerate(unique_items):
                theta = -math.pi/2 + (idx - (k - 1) / 2.0) * (math.pi / max(1.2, float(k)))
                tx = cx + int(r_orbit * math.cos(theta))
                ty = cy + int(r_orbit * math.sin(theta))
                
                # Keep within map viewport
                tx = max(MAP_X + 22, min(MAP_X + MAP_W - 22, tx))
                ty = max(MAP_Y + 22, min(MAP_Y + MAP_H - 22, ty))
                
                # Connecting line with the exact priority color!
                draw.line([(cx, cy), (tx, ty)], fill=p['color'], width=2)
                
                # Draw uniform larger marker
                draw_container_shape(draw, tx, ty, 16, p['color'], item_img_name=p['item_img'], canvas=canvas)

# ==========================================
# HEADER PROGRESSION BAR (UPPER RIGHT, NO 'DONE'/'ACTIVE' PREFIX)
# ==========================================
def render_header_progression_bar(draw, current_raid_id):
    steps = [
        (1, "Q2: Making Dough"),
        (2, "Q3-4: Camp & Charcoal"),
        (3, "Q5-6: Fort & Supplies"),
        (4, "Q8-9: Candle & Bribery"),
        (5, "Q10: Sinai Part 1"),
        (6, "Q10: Sinai Part 2"),
        (7, "Q10: Sinai Finale")
    ]
    
    total_w = 1534
    start_x = CANVAS_W - total_w - 24
    start_y = 18
    card_w = 208
    card_h = 42
    gap = 10
    
    for i, (s_id, s_name) in enumerate(steps):
        cx = start_x + i * (card_w + gap)
        cy = start_y
        
        if s_id < current_raid_id:
            # COMPLETED
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=6, fill=(16, 28, 18), outline=(34, 197, 94), width=1)
            tw = draw.textlength(s_name, font=F_SMALL_BOLD)
            draw.text((cx + (card_w - tw)/2, cy + 12), s_name, fill=(74, 222, 128), font=F_SMALL_BOLD)
        elif s_id == current_raid_id:
            # ACTIVE CURRENT RAID
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=6, fill=(40, 34, 16), outline=COLOR_GOLD, width=2)
            tw = draw.textlength(s_name, font=F_BODY_BOLD)
            draw.text((cx + (card_w - tw)/2, cy + 11), s_name, fill=COLOR_GOLD, font=F_BODY_BOLD)
        else:
            # UPCOMING
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=6, fill=(20, 20, 16), outline=BORDER_SUBTLE, width=1)
            tw = draw.textlength(s_name, font=F_SMALL)
            draw.text((cx + (card_w - tw)/2, cy + 12), s_name, fill=COLOR_MUTED, font=F_SMALL)
            
        if i < 6:
            draw.text((cx + card_w + 2, cy + 12), ">", fill=COLOR_DIM, font=F_SMALL_BOLD)

print("V22 Core Ready.")
