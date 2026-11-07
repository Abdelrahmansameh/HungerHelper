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
F_HEADER_TITLE  = load_font(SERIF_BOLD, 26)
F_HEADER_TAG    = load_font(SANS_BOLD, 15)
F_HEADER_STEP   = load_font(SANS_BOLD, 15)
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
# BIGGER CONTAINER IMAGE BADGES (r=24, icon=34x34)
# ==========================================
def draw_container_shape(draw, cx, cy, r, color, cont_img_name=None, canvas=None):
    draw.ellipse([cx-r-2, cy-r-2, cx+r+2, cy+r+2], outline=(10, 10, 8), width=3)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(16, 16, 13), outline=color, width=3)
    
    if cont_img_name and canvas and cont_img_name in CONTAINER_IMGS:
        ico = CONTAINER_IMGS[cont_img_name]
        sz = max(24, int(r * 1.4))
        ico_resized = ico.resize((sz, sz), Image.Resampling.LANCZOS)
        canvas.paste(ico_resized, (int(cx - sz/2), int(cy - sz/2)), ico_resized)
    else:
        draw.ellipse([cx-r+6, cy-r+6, cx+r-6, cy+r-6], fill=color)

# ==========================================
# PROMINENT POI DISCOVERY MARKER:
# - Dot on the exact POI coordinate (never hidden!)
# - Badge & Pill in proximity (offset) with connecting line
# ==========================================
def draw_poi_marker(draw, cx, cy, label, offset_dir='top', cont_img_name=None, canvas=None):
    # 1. Prominent Anchor Dot on the EXACT terrain coordinate (so building/altar is visible!)
    draw.ellipse([cx-7, cy-7, cx+7, cy+7], fill=(10, 10, 8))
    draw.ellipse([cx-5, cy-5, cx+5, cy+5], fill=COLOR_GOLD)

    r_core = 22
    tag = f"{label.upper()}"
    tw = int(draw.textlength(tag, font=F_SMALL_BOLD))
    th = 16
    pad_x = 10
    pad_y = 6
    pill_w = tw + pad_x * 2
    pill_h = th + pad_y * 2
    
    # Position badge & pill in proximity
    if offset_dir == 'top':
        badge_x = cx
        badge_y = cy - 42
        pill_x = cx - pill_w // 2
        pill_y = badge_y - r_core - pill_h - 4
        draw.line([(cx, cy - 6), (badge_x, badge_y + r_core)], fill=COLOR_GOLD, width=3)
        draw.line([(badge_x, badge_y - r_core), (badge_x, pill_y + pill_h)], fill=COLOR_GOLD, width=2)
    elif offset_dir == 'bottom':
        badge_x = cx
        badge_y = cy + 42
        pill_x = cx - pill_w // 2
        pill_y = badge_y + r_core + 6
        draw.line([(cx, cy + 6), (badge_x, badge_y - r_core)], fill=COLOR_GOLD, width=3)
        draw.line([(badge_x, badge_y + r_core), (badge_x, pill_y)], fill=COLOR_GOLD, width=2)
    elif offset_dir == 'right':
        badge_x = cx + 46
        badge_y = cy
        pill_x = badge_x + r_core + 6
        pill_y = cy - pill_h // 2
        draw.line([(cx + 6, cy), (badge_x - r_core, cy)], fill=COLOR_GOLD, width=3)
        draw.line([(badge_x + r_core, cy), (pill_x, cy)], fill=COLOR_GOLD, width=2)
    else: # left
        badge_x = cx - 46
        badge_y = cy
        pill_x = badge_x - r_core - pill_w - 6
        pill_y = cy - pill_h // 2
        draw.line([(cx - 6, cy), (badge_x + r_core, cy)], fill=COLOR_GOLD, width=3)
        draw.line([(badge_x - r_core, cy), (pill_x + pill_w, cy)], fill=COLOR_GOLD, width=2)
        
    pill_x = max(MAP_X + 10, min(MAP_X + MAP_W - pill_w - 10, pill_x))
    pill_y = max(MAP_Y + 10, min(MAP_Y + MAP_H - pill_h - 10, pill_y))
    
    # Draw Badge
    draw_container_shape(draw, badge_x, badge_y, r_core, COLOR_GOLD, cont_img_name=cont_img_name, canvas=canvas)
    
    # Draw Pill
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
                    'cont_img': c_info.get('cont_img'),
                    'is_prio': c_info.get('is_prio', False),
                    'label': c_info['label']
                })
                break
                
    return classified

# ==========================================
# PLOT DECLUSTERED MAP MARKERS:
# 1. IMAGES AT PROXIMITY (NOT HIDING POI/TERRAIN)
# 2. LINES RADIATE OUTWARD (NEVER CROSSING EACH OTHER)
# 3. CONTAINER SPAWN DOTS ALWAYS VISIBLE AT EXACT COORDINATE
# 4. GUARANTEED ZERO BADGE OVERLAPS (Relaxation >= 52px)
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
            'cont_img': pt.get('cont_img'),
            'type': pt['type']
        })
        
    # 1. Proximity clustering (threshold = 28px)
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
                if d < 28:
                    cluster.append(screen_pts[j])
                    assigned[j] = True
                    break
        clusters.append(cluster)
        
    # 2. Generate Badges at Proximity (Offset by 44px so POI is never covered!)
    all_badges = []
    for cluster in clusters:
        cx = sum(p['sx'] for p in cluster) / len(cluster)
        cy = sum(p['sy'] for p in cluster) / len(cluster)
        
        by_type = {}
        for p in cluster:
            by_type.setdefault(p['type'], []).append(p)
            
        num_types = len(by_type)
        
        # Sort container types by average angular position from cluster center
        # This GUARANTEES that lines radiate outward without crossing each other!
        type_order = []
        for t_key, pts_of_type in by_type.items():
            avg_x = sum(p['sx'] for p in pts_of_type) / len(pts_of_type)
            avg_y = sum(p['sy'] for p in pts_of_type) / len(pts_of_type)
            ang = math.atan2(avg_y - cy, avg_x - cx) if math.hypot(avg_y - cy, avg_x - cx) > 1 else 0
            type_order.append((ang, t_key, pts_of_type))
        type_order.sort(key=lambda item: item[0])
        
        r_offset = 46.0
        for t_idx, (_, t_key, pts_of_type) in enumerate(type_order):
            top_p = pts_of_type[0]
            spawns = [(p['sx'], p['sy']) for p in pts_of_type]
            
            # Non-crossing radial distribution
            if num_types == 1:
                # Place single badge offset toward map perimeter
                ang = math.atan2(cy - (MAP_Y + MAP_H/2), cx - (MAP_X + MAP_W/2))
                bx = cx + r_offset * math.cos(ang)
                by = cy + r_offset * math.sin(ang)
            else:
                ang = -math.pi/2 + (t_idx / float(num_types)) * (2 * math.pi)
                bx = cx + r_offset * math.cos(ang)
                by = cy + r_offset * math.sin(ang)
                
            all_badges.append({
                'bx': bx, 'by': by,
                'color': top_p['color'],
                'cont_img': top_p['cont_img'],
                'spawns': spawns
            })
            
    # 3. Global Collision Relaxation (Guarantee NO Badges Overlap Each Other!)
    MIN_DIST = 52.0 # Minimum distance between badge centers for r=24
    for _ in range(50):
        overlap_found = False
        for i in range(len(all_badges)):
            for j in range(i + 1, len(all_badges)):
                dx = all_badges[i]['bx'] - all_badges[j]['bx']
                dy = all_badges[i]['by'] - all_badges[j]['by']
                d = math.hypot(dx, dy)
                if d < 0.001:
                    dx, dy = 1.0, 0.0
                    d = 1.0
                if d < MIN_DIST:
                    overlap_found = True
                    overlap = (MIN_DIST - d) * 0.5
                    all_badges[i]['bx'] += (dx / d) * overlap
                    all_badges[i]['by'] += (dy / d) * overlap
                    all_badges[j]['bx'] -= (dx / d) * overlap
                    all_badges[j]['by'] -= (dy / d) * overlap
                    
        # Clamp to map viewport safely
        for b in all_badges:
            b['bx'] = max(MAP_X + 28, min(MAP_X + MAP_W - 28, b['bx']))
            b['by'] = max(MAP_Y + 28, min(MAP_Y + MAP_H - 28, b['by']))
            
        if not overlap_found:
            break
            
    # 4. Render Step A: Connecting Lines FIRST (so badges sit cleanly on top of line ends)
    for b in all_badges:
        bx = int(b['bx'])
        by = int(b['by'])
        color = b['color']
        for sx, sy in b['spawns']:
            draw.line([(bx, by), (sx, sy)], fill=color, width=4)
            
    # 4. Render Step B: Container Spawn Dots on Exact Terrain POIs (Never hidden!)
    seen_dots = set()
    for b in all_badges:
        color = b['color']
        for sx, sy in b['spawns']:
            if (sx, sy) in seen_dots:
                continue
            seen_dots.add((sx, sy))
            draw.ellipse([sx-7, sy-7, sx+7, sy+7], fill=(10, 10, 8))
            draw.ellipse([sx-5, sy-5, sx+5, sy+5], fill=color)
            
    # 4. Render Step C: Container Shape Badges (r=24) at Proximity
    for b in all_badges:
        bx = int(b['bx'])
        by = int(b['by'])
        draw_container_shape(draw, bx, by, 24, b['color'], cont_img_name=b['cont_img'], canvas=canvas)

# ==========================================
# FULL-WIDTH TOP BAR PROGRESSION (ENTIRE TOP BAR SPAN)
# ==========================================
def render_header_progression_bar(draw, current_raid_id):
    # Left: Clean Raid Number Pill
    tag_txt = f"RAID {current_raid_id} OF 7"
    pill_tw = int(draw.textlength(tag_txt, font=F_HEADER_TAG))
    draw.rounded_rectangle([20, 17, 20 + pill_tw + 24, 61], radius=6, fill=BG_CARD, outline=COLOR_GOLD, width=1)
    draw.text((32, 28), tag_txt, fill=COLOR_GOLD, font=F_HEADER_TAG)

    steps = [
        (1, "Raid 1: Q2 Making Dough"),
        (2, "Raid 2: Q3-4 Camp & Charcoal"),
        (3, "Raid 3: Q5-6 Fort & Supplies"),
        (4, "Raid 4: Q8-9 Candle & Bribery"),
        (5, "Raid 5: Q10 Sinai Part 1"),
        (6, "Raid 6: Q10 Sinai Part 2"),
        (7, "Raid 7: Q10 Sinai Finale")
    ]
    
    start_x = 20 + pill_tw + 40
    end_x = CANVAS_W - 24 # 2376
    total_w = end_x - start_x
    gap = 14
    num_cards = 7
    card_w = int((total_w - (num_cards - 1) * gap) / num_cards)
    card_h = 44
    cy = 17
    
    for i, (s_id, s_name) in enumerate(steps):
        cx = start_x + i * (card_w + gap)
        
        if s_id < current_raid_id:
            # COMPLETED
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=6, fill=(16, 28, 18), outline=(34, 197, 94), width=1)
            tw = draw.textlength(s_name, font=F_HEADER_STEP)
            draw.text((cx + (card_w - tw)/2, cy + 12), s_name, fill=(74, 222, 128), font=F_HEADER_STEP)
        elif s_id == current_raid_id:
            # ACTIVE CURRENT RAID
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=6, fill=(40, 34, 16), outline=COLOR_GOLD, width=2)
            tw = draw.textlength(s_name, font=F_BODY_BOLD)
            draw.text((cx + (card_w - tw)/2, cy + 11), s_name, fill=COLOR_GOLD, font=F_BODY_BOLD)
        else:
            # UPCOMING
            draw.rounded_rectangle([cx, cy, cx+card_w, cy+card_h], radius=6, fill=(20, 20, 16), outline=BORDER_SUBTLE, width=1)
            tw = draw.textlength(s_name, font=F_SMALL)
            draw.text((cx + (card_w - tw)/2, cy + 13), s_name, fill=COLOR_MUTED, font=F_SMALL)
            
        if i < 6:
            draw.text((cx + card_w + 3, cy + 13), ">", fill=COLOR_DIM, font=F_SMALL_BOLD)

print("V25 Core Ready.")
