import os, sys, math
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

# Priority Palette: Yellow -> Purple -> Blue
COLOR_PRIO1 = (255, 234, 0)   # Yellow
COLOR_PRIO2 = (168, 85, 247)  # Purple
COLOR_PRIO3 = (56, 189, 248)  # Blue

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
F_CARD_TITLE = load_font(SANS_BOLD, 17)
F_BODY_BOLD = load_font(SANS_BOLD, 15)
F_BODY = load_font(SANS_REG, 14)
F_SMALL_BOLD = load_font(SANS_BOLD, 13)
F_SMALL = load_font(SANS_REG, 13)
F_TINY = load_font(SANS_REG, 11)
F_BADGE = load_font(SANS_BOLD, 11)

DOC_DIR = r"C:\Users\PC\Documents\HungerHelper"
CONT_DIR = os.path.join(DOC_DIR, "assets", "containers")
ITEM_DIR = os.path.join(DOC_DIR, "assets", "items")

CONTAINER_IMGS = {}
ITEM_IMGS = {}

def preload_assets():
    if os.path.exists(CONT_DIR):
        for f in os.listdir(CONT_DIR):
            if f.endswith(('.webp', '.png')):
                try:
                    p = os.path.join(CONT_DIR, f)
                    CONTAINER_IMGS[f] = Image.open(p).convert("RGBA")
                except:
                    pass
    if os.path.exists(ITEM_DIR):
        for f in os.listdir(ITEM_DIR):
            if f.endswith(('.webp', '.png')):
                try:
                    p = os.path.join(ITEM_DIR, f)
                    ITEM_IMGS[f] = Image.open(p).convert("RGBA")
                except:
                    pass

preload_assets()

def paste_icon_safe(canvas, img_obj, box, bg_color=(15, 23, 42), border_color=(70, 85, 105), border_w=1):
    x, y, w, h = box
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([x, y, x+w, y+h], radius=6, fill=bg_color, outline=border_color, width=border_w)
    if img_obj:
        resized = img_obj.resize((w-6, h-6), Image.Resampling.LANCZOS)
        canvas.paste(resized, (x+3, y+3), resized)

# Drop Rate Colors: Red (<20%) -> Orange (20-49%) -> Green (>=50%)
def get_rate_color(rate_str):
    try:
        val = float(rate_str.replace('%', '').strip())
        if val >= 50.0:
            return (34, 197, 94)    # Green (High / 100%)
        elif val >= 20.0:
            return (249, 115, 22)   # Orange (Medium)
        else:
            return (239, 68, 68)    # Red (Low / Hardest)
    except:
        return (34, 197, 94) if "100" in rate_str else (255, 255, 255)

# Render Comprehensive Legend (All Information Neatly Structured in Legend)
def render_tactical_legend(draw, canvas, legend_data):
    """
    legend_data: {
      'map_title': "Sarlat Farm",
      'p1_items': [
        {'cont': "Flour Sack", 'c_ico': "flour_sack.webp", 'item': "20x Flour", 'i_ico': "flour.png", 'loc': "Master Granary (West) — 18 Spots", 'rate': "47.6%"},
        {'cont': "Flour Sack", 'c_ico': "flour_sack.webp", 'item': "20x Flour", 'i_ico': "flour.png", 'loc': "Village Granaries (East) — 14 Spots", 'rate': "47.6%"}
      ],
      'p2_items': [
        {'cont': "Bullion Box", 'c_ico': "bullion_box.webp", 'item': "Opium Pipe", 'i_ico': "opium_pipe.png", 'loc': "Farmhouse Bedroom Desks — 12 Spots", 'rate': "13.7%"},
        {'cont': "Wall Cabinet", 'c_ico': "wall_cabinet.webp", 'item': "China Bowl", 'i_ico': "china_bowl.png", 'loc': "Farmhouse & Church Walls — 4 Spots", 'rate': "16.1%"}
      ],
      'p3_items': [
        {'cont': "Pile of Ash", 'c_ico': "pile_of_ash.webp", 'item': "15x Charcoal", 'i_ico': "charcoal.png", 'loc': "Living Quarters Hearths — 15 Spots", 'rate': "52.6%"},
        {'cont': "Tooling Bin", 'c_ico': "tooling_bin.webp", 'item': "20x Saltpetre", 'i_ico': "saltpetre.png", 'loc': "Battery Workshops — 13 Spots", 'rate': "18.9%"}
      ]
    }
    """
    lx = MAP_X + 16
    ly = MAP_Y + 16
    lw = 540
    
    # Calculate height based on items
    total_rows = len(legend_data.get('p1_items', [])) + len(legend_data.get('p2_items', [])) + len(legend_data.get('p3_items', []))
    lh = 90 + total_rows * 42 + 40
    
    # Outer box
    draw.rounded_rectangle([lx, ly, lx+lw, ly+lh], radius=10, fill=(10, 15, 25), outline=(70, 85, 110), width=2)
    
    # Header
    draw.text((lx+16, ly+10), f"TACTICAL DIRECTORY & DROP ODDS  —  {legend_data.get('map_title', '')}", fill=COLOR_PRIO1, font=F_CARD_TITLE)
    
    # Legend Scale Bar
    draw.rounded_rectangle([lx+14, ly+34, lx+lw-14, ly+82], radius=6, fill=(16, 22, 34), outline=(40, 50, 70), width=1)
    
    # Row 1: Priority Colors (Yellow -> Purple -> Blue)
    draw.ellipse([lx+22, ly+42, lx+32, ly+52], fill=COLOR_PRIO1)
    draw.text((lx+38, ly+40), "P1: Raid Goal (Yellow)", fill=COLOR_PRIO1, font=F_TINY)
    draw.ellipse([lx+200, ly+42, lx+210, ly+52], fill=COLOR_PRIO2)
    draw.text((lx+216, ly+40), "P2: Rare Loot (Purple)", fill=COLOR_PRIO2, font=F_TINY)
    draw.ellipse([lx+370, ly+42, lx+380, ly+52], fill=COLOR_PRIO3)
    draw.text((lx+386, ly+40), "P3: Prep (Blue)", fill=COLOR_PRIO3, font=F_TINY)
    
    # Row 2: Drop Rate Scale (Red -> Orange -> Green)
    draw.text((lx+22, ly+62), "Drop Rates: ", fill=(180, 195, 215), font=F_TINY)
    draw.text((lx+100, ly+62), "■ <20% (Red)", fill=(239, 68, 68), font=F_TINY)
    draw.text((lx+200, ly+62), "■ 20-49% (Orange)", fill=(249, 115, 22), font=F_TINY)
    draw.text((lx+330, ly+62), "■ 50-100% (Green)", fill=(34, 197, 94), font=F_TINY)
    
    cur_y = ly + 90
    
    # Render Priority 1 Section
    p1_items = legend_data.get('p1_items', [])
    if p1_items:
        draw.text((lx+16, cur_y), "PRIORITY 1: RAID OBJECTIVE TARGETS (YELLOW)", fill=COLOR_PRIO1, font=F_SMALL_BOLD)
        cur_y += 18
        for itm in p1_items:
            cur_y = render_legend_row(draw, canvas, lx, cur_y, lw, itm, COLOR_PRIO1)
            
    # Render Priority 2 Section
    p2_items = legend_data.get('p2_items', [])
    if p2_items:
        draw.text((lx+16, cur_y), "PRIORITY 2: HARDEST DROPS & RARE LOOT (PURPLE)", fill=COLOR_PRIO2, font=F_SMALL_BOLD)
        cur_y += 18
        for itm in p2_items:
            cur_y = render_legend_row(draw, canvas, lx, cur_y, lw, itm, COLOR_PRIO2)

    # Render Priority 3 Section
    p3_items = legend_data.get('p3_items', [])
    if p3_items:
        draw.text((lx+16, cur_y), "PRIORITY 3: UPCOMING QUEST STASH PREP (BLUE)", fill=COLOR_PRIO3, font=F_SMALL_BOLD)
        cur_y += 18
        for itm in p3_items:
            cur_y = render_legend_row(draw, canvas, lx, cur_y, lw, itm, COLOR_PRIO3)

def render_legend_row(draw, canvas, lx, cur_y, lw, itm, prio_color):
    row_h = 36
    # Container icon
    c_img = CONTAINER_IMGS.get(itm.get('c_ico'))
    paste_icon_safe(canvas, c_img, (lx+18, cur_y, 30, 30), bg_color=(15, 20, 30), border_color=prio_color, border_w=2)
    
    # Item icon
    i_img = ITEM_IMGS.get(itm.get('i_ico'))
    paste_icon_safe(canvas, i_img, (lx+52, cur_y, 30, 30), bg_color=(15, 20, 30), border_color=(70, 85, 105), border_w=1)
    
    # Text info
    draw.text((lx+90, cur_y+1), f"{itm['cont']} ➔ {itm['item']}", fill=(255, 255, 255), font=F_SMALL_BOLD)
    draw.text((lx+90, cur_y+16), itm['loc'][:52], fill=(185, 200, 220), font=F_TINY)
    
    # Drop Rate percentage in colored font (Red -> Orange -> Green)
    rate_col = get_rate_color(itm['rate'])
    draw.text((lx+lw-75, cur_y+8), itm['rate'], fill=rate_col, font=F_BODY_BOLD)
    
    return cur_y + row_h + 4

# Compact Map Icon Badge (ZERO TEXT ON TERRAIN!)
def render_map_badge_no_text(canvas, target_x, target_y, cont_ico, item_ico, prio_color):
    """
    Renders a compact 36x36 container badge with a 22x22 item badge overlay on the map.
    NO text boxes on terrain!
    """
    bx = target_x - 18
    by = target_y - 18
    
    c_img = CONTAINER_IMGS.get(cont_ico)
    paste_icon_safe(canvas, c_img, (bx, by, 36, 36), bg_color=(12, 16, 24), border_color=prio_color, border_w=2)
    
    if item_ico:
        i_img = ITEM_IMGS.get(item_ico)
        paste_icon_safe(canvas, i_img, (bx+18, by+18, 22, 22), bg_color=(18, 24, 34), border_color=(70, 85, 105), border_w=1)

print("V9 Core Ready.")
