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

# Hunger Companion Serif Titles & Clean Sans Body
F_HEADER_TITLE  = load_font(SERIF_BOLD, 28)
F_HEADER_TAG    = load_font(SANS_BOLD, 16)
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
# UNIFORM CIRCLE FORM FOR ALL COLORS (NO EXTRA OUTER CIRCLE PART!)
# COLOR & OUTLINE PRESERVED + SMALL IMAGE OF THE ITEM EMBEDDED
# ==========================================
def draw_container_shape(draw, cx, cy, r, color, item_img_name=None, canvas=None):
    # Single uniform circle form across all colors
    draw.ellipse([cx-r-1, cy-r-1, cx+r+1, cy+r+1], outline=(10, 10, 8), width=3)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(16, 16, 13), outline=color, width=2)
    
    if item_img_name and canvas and item_img_name in ITEM_IMGS:
        ico = ITEM_IMGS[item_img_name]
        sz = max(12, int(r * 1.35))
        ico_resized = ico.resize((sz, sz), Image.Resampling.LANCZOS)
        canvas.paste(ico_resized, (int(cx - sz/2), int(cy - sz/2)), ico_resized)
    else:
        draw.ellipse([cx-r+3, cy-r+3, cx+r-3, cy+r-3], fill=color)

# ==========================================
# PROMINENT POI DISCOVERY MARKER (CIRCULAR WITH EMBEDDED ITEM ICON + PILL)
# ==========================================
def draw_poi_marker(draw, cx, cy, label, offset_dir='top', item_img_name=None, canvas=None):
    r_core = 14
    
    draw.ellipse([cx-r_core-2, cy-r_core-2, cx+r_core+2, cy+r_core+2], outline=(10, 10, 8), width=4)
    draw.ellipse([cx-r_core, cy-r_core, cx+r_core, cy+r_core], fill=(16, 16, 13), outline=COLOR_GOLD, width=3)
    
    if item_img_name and canvas and item_img_name in ITEM_IMGS:
        ico = ITEM_IMGS[item_img_name]
        sz = 20
        ico_resized = ico.resize((sz, sz), Image.Resampling.LANCZOS)
        canvas.paste(ico_resized, (cx - sz//2, cy - sz//2), ico_resized)
    else:
        draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=COLOR_GOLD)

    tag = f"{label.upper()}"
    tw = int(draw.textlength(tag, font=F_SMALL_BOLD))
    th = 16
    pad_x = 10
    pad_y = 6
    pill_w = tw + pad_x * 2
    pill_h = th + pad_y * 2
    
    if offset_dir == 'top':
        pill_x = cx - pill_w // 2
        pill_y = cy - pill_h - 20
        draw.line([(cx, cy - r_core - 2), (cx, pill_y + pill_h)], fill=COLOR_GOLD, width=2)
    elif offset_dir == 'bottom':
        pill_x = cx - pill_w // 2
        pill_y = cy + 22
        draw.line([(cx, cy + r_core + 2), (cx, pill_y)], fill=COLOR_GOLD, width=2)
    elif offset_dir == 'right':
        pill_x = cx + 24
        pill_y = cy - pill_h // 2
        draw.line([(cx + r_core + 2, cy), (pill_x, cy)], fill=COLOR_GOLD, width=2)
    else: # left
        pill_x = cx - pill_w - 24
        pill_y = cy - pill_h // 2
        draw.line([(cx - r_core - 2, cy), (pill_x + pill_w, cy)], fill=COLOR_GOLD, width=2)
        
    pill_x = max(MAP_X + 10, min(MAP_X + MAP_W - pill_w - 10, pill_x))
    pill_y = max(MAP_Y + 65, min(MAP_Y + MAP_H - pill_h - 10, pill_y))
    
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
                # Deduplicate physical containers within 6 pixels of same type
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
# PLOT DECLUSTERED MAP MARKERS WITH LINES FOR OVERLAPPING POINTS
# ==========================================
def plot_declustered_points(draw, canvas, points, to_coord_fn):
    if not points:
        return
        
    # Convert points to screen coords
    screen_pts = []
    for pt in points:
        sx, sy = to_coord_fn(pt['x'], pt['y'])
        screen_pts.append({
            'sx': sx, 'sy': sy,
            'color': pt['color'],
            'item_img': pt['item_img'],
            'type': pt['type']
        })
        
    # Group into clusters within 22px
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
            # Distance check against any point in cluster
            for c_pt in cluster:
                d = math.hypot(c_pt['sx'] - screen_pts[j]['sx'], c_pt['sy'] - screen_pts[j]['sy'])
                if d < 22:
                    cluster.append(screen_pts[j])
                    assigned[j] = True
                    break
        clusters.append(cluster)
        
    # Render clusters
    for cluster in clusters:
        # Deduplicate same item type within the same cluster point
        unique_items = []
        seen_types = set()
        for p in cluster:
            if p['type'] not in seen_types:
                seen_types.add(p['type'])
                unique_items.append(p)
                
        if len(unique_items) == 1:
            # Single isolated container: Draw directly on spawn
            p = unique_items[0]
            draw_container_shape(draw, p['sx'], p['sy'], 12, p['color'], item_img_name=p['item_img'], canvas=canvas)
        else:
            # Multiple containers in one spot:
            # Draw anchor dot at spawn, fan out markers side-by-side with connecting line
            cx = int(sum(p['sx'] for p in cluster) / len(cluster))
            cy = int(sum(p['sy'] for p in cluster) / len(cluster))
            
            # Subtle gold anchor dot at exact spawn point
            draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=COLOR_GOLD, outline=(10, 10, 8), width=1)
            
            k = len(unique_items)
            spacing = 26
            # Offset horizontally or vertically based on room
            offset_y = -24 if cy > MAP_Y + 120 else 24
            
            for idx, p in enumerate(unique_items):
                offset_x = int((idx - (k - 1) / 2.0) * spacing)
                tx = cx + offset_x
                ty = cy + offset_y
                
                # Clean connecting line from spawn to marker
                draw.line([(cx, cy), (tx, ty)], fill=COLOR_GOLD, width=2)
                
                # Draw marker of equal uniform size
                draw_container_shape(draw, tx, ty, 12, p['color'], item_img_name=p['item_img'], canvas=canvas)

# ==========================================
# QUESTLINE PROGRESSION HUD BAR (MATCHES QUEST TITLES)
# ==========================================
def render_questline_progression_bar(draw, current_raid_id):
    bar_x = MAP_X + 16
    bar_y = MAP_Y + 10
    bar_w = MAP_W - 32
    bar_h = 44
    
    draw.rounded_rectangle([bar_x, bar_y, bar_x+bar_w, bar_y+bar_h], radius=8, fill=(16, 16, 13), outline=BORDER_SUBTLE, width=2)
    
    steps = [
        (1, "Q2: Making Dough"),
        (2, "Q3-4: Camp & Charcoal"),
        (3, "Q5-6: Fort & Supplies"),
        (4, "Q8-9: Candle & Bribery"),
        (5, "Q10: Sinai Part 1"),
        (6, "Q10: Sinai Part 2"),
        (7, "Q10: Sinai Finale")
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
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=5, fill=(16, 26, 18), outline=(34, 197, 94), width=1)
            lbl = f"[DONE] {s_name}"
            tw = draw.textlength(lbl, font=F_SMALL_BOLD)
            draw.text((cx + (card_w - tw)/2, cy + 8), lbl, fill=(74, 222, 128), font=F_SMALL_BOLD)
        elif s_id == current_raid_id:
            # ACTIVE CURRENT RAID
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=5, fill=(38, 32, 16), outline=COLOR_GOLD, width=2)
            lbl = f"ACTIVE: {s_name}"
            tw = draw.textlength(lbl, font=F_SMALL_BOLD)
            draw.text((cx + (card_w - tw)/2, cy + 8), lbl, fill=COLOR_GOLD, font=F_SMALL_BOLD)
        else:
            # UPCOMING
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=5, fill=(21, 21, 18), outline=BORDER_SUBTLE, width=1)
            lbl = s_name
            tw = draw.textlength(lbl, font=F_SMALL)
            draw.text((cx + (card_w - tw)/2, cy + 8), lbl, fill=COLOR_MUTED, font=F_SMALL)
            
        if i < 6:
            draw.text((cx + card_w + 1, cy + 8), ">", fill=COLOR_DIM, font=F_SMALL_BOLD)

print("V21 Core Ready.")
