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

def draw_arrow(draw, start, end, color=(0, 229, 255), width=3):
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

# Drop Rate Number Color Helper
def get_rate_color(rate_str):
    try:
        val = float(rate_str.replace('%', '').strip())
        if val >= 99.0:
            return (34, 197, 94) # Green 100%
        elif val >= 40.0:
            return (56, 189, 248) # Cyan / Sky Blue (Common)
        elif val >= 20.0:
            return (251, 191, 36) # Amber / Yellow (Medium)
        else:
            return (248, 113, 113) # Coral Red (Rare / Hardest)
    except:
        return (255, 255, 255)

# Render Enhanced Legend with colored drop rate percentages & clear outline explanation
def render_tactical_legend(draw, canvas, legend_items):
    lx = MAP_X + 16
    ly = MAP_Y + 16
    lw = 470
    lh = 50 + len(legend_items) * 36 + 65
    
    # Outer box
    draw.rounded_rectangle([lx, ly, lx+lw, ly+lh], radius=10, fill=(10, 15, 25), outline=(70, 85, 110), width=2)
    
    # Header
    draw.text((lx+16, ly+10), "MAP CONTAINER & DROP RATE KEY", fill=(255, 234, 0), font=F_CARD_TITLE)
    
    # Spawn Rate Outline Rule Explanation
    draw.rounded_rectangle([lx+14, ly+34, lx+lw-14, ly+86], radius=6, fill=(16, 22, 34), outline=(40, 50, 70), width=1)
    
    # Cyan border = 100% guaranteed
    draw.rounded_rectangle([lx+22, ly+42, lx+38, ly+58], radius=3, fill=(12, 18, 28), outline=(0, 229, 255), width=2)
    draw.text((lx+46, ly+42), "Solid Cyan / Amber Border = 100% Guaranteed Spawn Spot", fill=(0, 229, 255), font=F_TINY)
    
    # Grey border = Variable spawn
    draw.rounded_rectangle([lx+22, ly+64, lx+38, ly+80], radius=3, fill=(12, 18, 28), outline=(130, 145, 165), width=2)
    draw.text((lx+46, ly+64), "Metallic Silver / Grey Border = Variable Spawn (~38% Chance)", fill=(180, 195, 215), font=F_TINY)

    # Item Rows
    cur_y = ly + 94
    for cont_title, cont_ico, item_title, item_ico, rate_str, role_tag in legend_items:
        # Container icon with spawn outline
        is_100 = "100%" in rate_str or "Q2" in role_tag or "Primary" in role_tag or "Hardest" in role_tag
        border_col = (0, 229, 255) if is_100 else (130, 145, 165)
        
        c_img = CONTAINER_IMGS.get(cont_ico)
        paste_icon_safe(canvas, c_img, (lx+18, cur_y, 30, 30), bg_color=(15, 20, 30), border_color=border_col, border_w=2)
        
        # Target item icon
        i_img = ITEM_IMGS.get(item_ico)
        paste_icon_safe(canvas, i_img, (lx+54, cur_y, 30, 30), bg_color=(15, 20, 30), border_color=(70, 85, 105), border_w=1)
        
        # Container -> Item
        draw.text((lx+92, cur_y+1), f"{cont_title}", fill=(255, 255, 255), font=F_SMALL_BOLD)
        draw.text((lx+92, cur_y+16), f"➔ {item_title}", fill=(200, 215, 235), font=F_SMALL)
        
        # Drop Rate in distinct high-visibility color
        rate_col = get_rate_color(rate_str)
        draw.text((lx+310, cur_y+7), rate_str, fill=rate_col, font=F_BODY_BOLD)
        
        # Role tag
        draw.text((lx+370, cur_y+7), role_tag, fill=(160, 175, 195), font=F_SMALL)
        
        cur_y += 36

# Render Summary Callout showing BOTH Container and Item side-by-side
def render_summary_callout(draw, canvas, callout):
    bx = callout['box_x']
    by = callout['box_y']
    tx = callout['target_x']
    ty = callout['target_y']
    color = callout.get('color', (0, 229, 255))
    
    cw = 420
    ch = 100
    
    # Outer box
    draw.rounded_rectangle([bx, by, bx+cw, by+ch], radius=8, fill=(11, 16, 26), outline=color, width=2)
    
    # Container image (Left) with spawn outline
    is_100 = callout.get('is_100', True)
    c_border = (0, 229, 255) if is_100 else (130, 145, 165)
    c_img = CONTAINER_IMGS.get(callout.get('cont_img'))
    paste_icon_safe(canvas, c_img, (bx+10, by+10, 54, 54), bg_color=(16, 24, 38), border_color=c_border, border_w=2)
    
    # Arrow icon between container and item
    draw.text((bx+68, by+26), "➔", fill=(200, 215, 235), font=F_CARD_TITLE)
    
    # Item image (Right of arrow)
    i_img = ITEM_IMGS.get(callout.get('item_img'))
    paste_icon_safe(canvas, i_img, (bx+92, by+10, 54, 54), bg_color=(20, 28, 44), border_color=(70, 85, 105), border_w=1)
    
    # Labels & Info
    text_x = bx + 156
    draw.text((text_x, by+8), callout['title'], fill=(255, 255, 255), font=F_CALLOUT_TITLE)
    draw.text((text_x, by+30), callout['count_text'], fill=color, font=F_BODY_BOLD)
    
    # Spawn Rate Badge (Compact)
    badge_text = callout.get('spawn_badge', "100% GUARANTEED" if is_100 else "VARIABLE (~38%)")
    badge_bg = (16, 185, 129) if is_100 else (120, 135, 155)
    bw = int(draw.textlength(badge_text, font=F_BADGE)) + 12
    draw.rounded_rectangle([text_x, by+54, text_x+bw, by+72], radius=4, fill=badge_bg)
    draw.text((text_x+6, by+56), badge_text, fill=(255, 255, 255) if is_100 else (15, 23, 42), font=F_BADGE)
    
    if 'sub_text' in callout and callout['sub_text']:
        draw.text((text_x, by+78), callout['sub_text'], fill=(180, 195, 215), font=F_TINY)

    # Arrow connecting callout to target points
    start_x = bx + cw if tx > bx + cw else (bx if tx < bx else bx + cw//2)
    start_y = by + ch//2
    draw_arrow(draw, (start_x, start_y), (tx, ty), color=color, width=2)

print("V7 Core Ready.")
