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
F_CALLOUT_TITLE = load_font(SANS_BOLD, 17)
F_BADGE = load_font(SANS_BOLD, 12)

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

def draw_arrow(draw, start, end, color=(255, 234, 0), width=3):
    x1, y1 = start
    x2, y2 = end
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 16
    arrow_angle = math.pi / 6
    
    ax1 = x2 - arrow_len * math.cos(angle - arrow_angle)
    ay1 = y2 - arrow_len * math.sin(angle - arrow_angle)
    ax2 = x2 - arrow_len * math.cos(angle + arrow_angle)
    ay2 = y2 - arrow_len * math.sin(angle + arrow_angle)
    
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)

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

# Render Enhanced Legend with colored drop rates (Red -> Orange -> Green)
def render_tactical_legend(draw, canvas, legend_items):
    lx = MAP_X + 16
    ly = MAP_Y + 16
    lw = 470
    lh = 50 + len(legend_items) * 36 + 65
    
    # Outer box
    draw.rounded_rectangle([lx, ly, lx+lw, ly+lh], radius=10, fill=(10, 15, 25), outline=(70, 85, 110), width=2)
    
    # Header
    draw.text((lx+16, ly+10), "MAP CONTAINER & DROP RATE KEY", fill=COLOR_PRIO1, font=F_CARD_TITLE)
    
    # Drop rate scale explanation
    draw.rounded_rectangle([lx+14, ly+34, lx+lw-14, ly+86], radius=6, fill=(16, 22, 34), outline=(40, 50, 70), width=1)
    
    # Priority Scale: Yellow -> Purple -> Blue
    draw.ellipse([lx+22, ly+42, lx+32, ly+52], fill=COLOR_PRIO1)
    draw.text((lx+38, ly+40), "P1: Raid Goal (Yellow)", fill=COLOR_PRIO1, font=F_TINY)
    draw.ellipse([lx+170, ly+42, lx+180, ly+52], fill=COLOR_PRIO2)
    draw.text((lx+186, ly+40), "P2: Rare/Bribery (Purple)", fill=COLOR_PRIO2, font=F_TINY)
    draw.ellipse([lx+328, ly+42, lx+338, ly+52], fill=COLOR_PRIO3)
    draw.text((lx+344, ly+40), "P3: Prep (Blue)", fill=COLOR_PRIO3, font=F_TINY)
    
    # Drop Rate Color Code: Red -> Orange -> Green
    draw.text((lx+22, ly+64), "Drop Rate Scale: ", fill=(180, 195, 215), font=F_TINY)
    draw.text((lx+118, ly+64), "■ <20% (Red)", fill=(239, 68, 68), font=F_TINY)
    draw.text((lx+208, ly+64), "■ 20-49% (Orange)", fill=(249, 115, 22), font=F_TINY)
    draw.text((lx+328, ly+64), "■ 50-100% (Green)", fill=(34, 197, 94), font=F_TINY)

    # Item Rows
    cur_y = ly + 94
    for cont_title, cont_ico, item_title, item_ico, rate_str, role_tag in legend_items:
        # Border uses priority or standard subtle border
        is_p1 = "Primary" in role_tag or "Q2" in role_tag or "Quest" in role_tag
        is_p2 = "Hardest" in role_tag or "Bribery" in role_tag
        border_col = COLOR_PRIO1 if is_p1 else (COLOR_PRIO2 if is_p2 else COLOR_PRIO3)
        
        c_img = CONTAINER_IMGS.get(cont_ico)
        paste_icon_safe(canvas, c_img, (lx+18, cur_y, 30, 30), bg_color=(15, 20, 30), border_color=border_col, border_w=2)
        
        # Target item icon
        i_img = ITEM_IMGS.get(item_ico)
        paste_icon_safe(canvas, i_img, (lx+54, cur_y, 30, 30), bg_color=(15, 20, 30), border_color=(70, 85, 105), border_w=1)
        
        # Container -> Item
        draw.text((lx+92, cur_y+1), f"{cont_title}", fill=(255, 255, 255), font=F_SMALL_BOLD)
        draw.text((lx+92, cur_y+16), f"➔ {item_title}", fill=(200, 215, 235), font=F_SMALL)
        
        # Drop Rate in distinct Red / Orange / Green color
        rate_col = get_rate_color(rate_str)
        draw.text((lx+310, cur_y+7), rate_str, fill=rate_col, font=F_BODY_BOLD)
        
        # Role tag
        draw.text((lx+370, cur_y+7), role_tag, fill=(160, 175, 195), font=F_SMALL)
        
        cur_y += 36

# Render Summary Callout showing BOTH Container and Item side-by-side
# ONLY shows spawn badge if spawn rate is LESS than 100%!
def render_summary_callout(draw, canvas, callout):
    bx = callout['box_x']
    by = callout['box_y']
    tx = callout['target_x']
    ty = callout['target_y']
    color = callout.get('color', COLOR_PRIO1)
    
    cw = 420
    ch = 94
    
    # Outer box
    draw.rounded_rectangle([bx, by, bx+cw, by+ch], radius=8, fill=(11, 16, 26), outline=color, width=2)
    
    # Container image (Left)
    c_img = CONTAINER_IMGS.get(callout.get('cont_img'))
    paste_icon_safe(canvas, c_img, (bx+10, by+10, 54, 54), bg_color=(16, 24, 38), border_color=color, border_w=2)
    
    # Arrow icon between container and item
    draw.text((bx+68, by+26), "➔", fill=(200, 215, 235), font=F_CARD_TITLE)
    
    # Item image (Right of arrow)
    i_img = ITEM_IMGS.get(callout.get('item_img'))
    paste_icon_safe(canvas, i_img, (bx+92, by+10, 54, 54), bg_color=(20, 28, 44), border_color=(70, 85, 105), border_w=1)
    
    # Labels & Info
    text_x = bx + 156
    draw.text((text_x, by+8), callout['title'], fill=(255, 255, 255), font=F_CALLOUT_TITLE)
    draw.text((text_x, by+32), callout['count_text'], fill=color, font=F_BODY_BOLD)
    
    # ONLY show spawn badge if lower than 100%!
    is_100 = callout.get('is_100', True)
    if not is_100:
        badge_text = callout.get('spawn_badge', "CHANCE SPAWN (~38%)")
        badge_bg = (185, 28, 28) # Red alert for low spawn
        bw = int(draw.textlength(badge_text, font=F_BADGE)) + 12
        draw.rounded_rectangle([text_x, by+54, text_x+bw, by+72], radius=4, fill=badge_bg)
        draw.text((text_x+6, by+56), badge_text, fill=(255, 255, 255), font=F_BADGE)
    
    if 'sub_text' in callout and callout['sub_text']:
        sub_y = by + 56 if is_100 else by + 74
        draw.text((text_x, sub_y), callout['sub_text'], fill=(180, 195, 215), font=F_TINY)

    # Arrow connecting callout to target points
    start_x = bx + cw if tx > bx + cw else (bx if tx < bx else bx + cw//2)
    start_y = by + ch//2
    draw_arrow(draw, (start_x, start_y), (tx, ty), color=color, width=2)

print("V8 Core Ready.")
