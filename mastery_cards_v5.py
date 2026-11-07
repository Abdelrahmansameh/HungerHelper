from co_pilot.card_store import stored_card
import os
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)
import perfect_briefings_core_v25 as core
core.preload_assets()

OUT_DIR = os.path.join(ROOT_DIR, "output_maps")
os.makedirs(OUT_DIR, exist_ok=True)
BRAIN_DIR = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49"

def safe_paste(canvas, img, box):
    if img is None:
        return
    x, y, w, h = box
    im = img.convert("RGBA")
    im.thumbnail((w, h), Image.Resampling.LANCZOS)
    px = x + (w - im.width) // 2
    py = y + (h - im.height) // 2
    canvas.paste(im, (px, py), im.split()[3])

def save_and_sync(canvas: Image.Image, filename: str) -> str:
    out_p = os.path.join(OUT_DIR, filename)
    canvas.convert("RGB").save(out_p, quality=95)
    if os.path.exists(BRAIN_DIR):
        brain_p = os.path.join(BRAIN_DIR, filename)
        canvas.convert("RGB").save(brain_p, quality=95)
    return out_p

# ===========================================================================
# 1. ALL 5 MASTERIES VIEW (IMAGE 1)
# ===========================================================================
@stored_card('player_name', 'level', 'spent_points')
def render_all_5_mastery_trees_card(
    player_name: str = "Hugo",
    level: int = 100,
    spent_points: int = 91
) -> str:
    CARD_W = 1860
    CARD_H = 1000

    canvas = Image.new("RGBA", (CARD_W, CARD_H), (10, 10, 12, 255))
    draw = ImageDraw.Draw(canvas)

    # Ambient borders
    draw.rectangle([0, 0, CARD_W, CARD_H], fill=(10, 10, 12))
    draw.rectangle([4, 4, CARD_W - 5, CARD_H - 5], outline=core.COLOR_GOLD, width=2)
    draw.rectangle([8, 8, CARD_W - 9, CARD_H - 9], outline=(35, 32, 24), width=1)

    # Header bar
    draw.rounded_rectangle([18, 14, CARD_W - 18, 70], radius=8, fill=(16, 16, 20), outline=(45, 42, 32), width=1)

    # Top Tabs for ALL 5 Trees
    tabs = [
        ("CUNNING", "0/72", (220, 200, 140), False),
        ("PHYSIOLOGY", "18/83", (255, 170, 190), True),
        ("SURVIVAL", "36/78", (215, 185, 255), True),
        ("MARTIAL", "0/74", (170, 220, 255), False),
        ("ARMS", "37/71", (170, 255, 220), True),
    ]

    tx = 30
    tw = 210
    for name, pts_str, col, is_act in tabs:
        box = [tx, 22, tx + tw, 62]
        bg_col = (32, 28, 34) if is_act else (14, 14, 16)
        border_col = col if is_act else (55, 52, 45)
        draw.rounded_rectangle(box, radius=6, fill=bg_col, outline=border_col, width=2 if is_act else 1)
        # Draw geometric diamond icon (Zero missing-glyph tofu boxes)
        cx, cy = box[0] + 16, box[1] + 20
        d_pts = [(cx, cy - 5), (cx + 5, cy), (cx, cy + 5), (cx - 5, cy)]
        draw.polygon(d_pts, fill=col if is_act else (100, 100, 90))
        draw.text((box[0] + 26, box[1] + 11), name, fill=col if is_act else (130, 130, 120), font=core.F_SMALL_BOLD)
        draw.text((box[2] - 56, box[1] + 11), pts_str, fill=col if is_act else (110, 110, 100), font=core.F_SMALL_BOLD)
        tx += tw + 14

    # Player info on right
    p_info = f"BUILD : {player_name.upper()} (LVL {level})  |  POINTS ALLOCATED : {spent_points} / 100"
    draw.text((tx + 25, 32), p_info, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)

    # All 5 Trees in 5 Columns
    all_trees = [
        ("CUNNING", "assets/masteries/templates/cunning_base.png", (220, 200, 140), 0, False),
        ("PHYSIOLOGY", "assets/masteries/templates/physiology_base.png", (255, 170, 190), 18, True),
        ("SURVIVAL", "assets/masteries/templates/survival_base.png", (215, 185, 255), 36, True),
        ("MARTIAL", "assets/masteries/templates/martial_base.png", (170, 220, 255), 0, False),
        ("ARMS", "assets/masteries/templates/arms_base.png", (170, 255, 220), 37, True),
    ]

    col_w = 348
    col_gap = 14
    panel_y = 86
    panel_h = CARD_H - 104

    tree_crops = {
        "CUNNING": (35, 108, 420, 970),
        "PHYSIOLOGY": (35, 108, 420, 970),
        "SURVIVAL": (30, 108, 520, 970),
        "MARTIAL": (35, 108, 720, 970),
        "ARMS": (85, 108, 620, 970)
    }

    for i, (t_name, t_path, t_col, t_pts, is_act) in enumerate(all_trees):
        px = 24 + i * (col_w + col_gap)
        p_box = [px, panel_y, px + col_w, panel_y + panel_h]

        bg_card = (14, 14, 16) if is_act else (10, 10, 12)
        border_c = t_col if is_act else (40, 38, 32)
        draw.rounded_rectangle(p_box, radius=8, fill=bg_card, outline=border_c, width=2 if is_act else 1)

        # Header banner inside column (Clean spacing - zero text collisions)
        hdr_bg = (28, 24, 30) if is_act else (16, 16, 18)
        draw.rounded_rectangle([p_box[0] + 6, p_box[1] + 6, p_box[2] - 6, p_box[1] + 44], radius=6, fill=hdr_bg, outline=border_c, width=1)
        draw.text((p_box[0] + 14, p_box[1] + 13), t_name, fill=t_col if is_act else (120, 120, 110), font=core.F_SECTION_TITLE)
        draw.text((p_box[2] - 82, p_box[1] + 13), f"{t_pts} Pts", fill=core.COLOR_GOLD if is_act else (100, 100, 90), font=core.F_SMALL_BOLD)

        # Paste Tree Nodes with exact content bounding box (Tiers I - VIII)
        if os.path.exists(t_path):
            tree_im = Image.open(t_path).convert("RGBA")
            crop_box = tree_crops.get(t_name, (35, 85, 500, 970))
            crop_nodes = tree_im.crop(crop_box)

            if not is_act:
                # Dim unallocated trees
                gray = crop_nodes.convert("L").convert("RGBA")
                dimmed = [(int(p[0] * 0.35), int(p[1] * 0.35), int(p[2] * 0.35), p[3]) for p in gray.getdata()]
                gray.putdata(dimmed)
                crop_nodes = gray

            target_rect = [p_box[0] + 10, p_box[1] + 52, p_box[2] - 10, p_box[3] - 10]
            # Scale proportionally to fit target width and height
            avail_w = target_rect[2] - target_rect[0]
            avail_h = target_rect[3] - target_rect[1]
            scale = min(avail_w / crop_nodes.width, avail_h / crop_nodes.height)
            nw = int(crop_nodes.width * scale)
            nh = int(crop_nodes.height * scale)
            resized = crop_nodes.resize((nw, nh), Image.Resampling.LANCZOS)
            px_paste = target_rect[0] + (avail_w - nw) // 2
            py_paste = target_rect[1] + (avail_h - nh) // 2
            canvas.paste(resized, (px_paste, py_paste), resized.split()[3])

    return save_and_sync(canvas, "build_all_trees_highlighted.jpg")


# ===========================================================================
# 2. STATS BREAKDOWN (IMAGE 2) - NATURALLY GROUPED WITHOUT FLUFF
# ===========================================================================
@stored_card('player_name', 'level')
def render_build_stats_summary_card(
    player_name: str = "Hugo",
    level: int = 100
) -> str:
    CARD_W = 1200
    CARD_H = 720

    canvas = Image.new("RGBA", (CARD_W, CARD_H), (10, 10, 12, 255))
    draw = ImageDraw.Draw(canvas)

    # Borders
    draw.rectangle([0, 0, CARD_W, CARD_H], fill=(10, 10, 12))
    draw.rectangle([4, 4, CARD_W - 5, CARD_H - 5], outline=core.COLOR_GOLD, width=2)
    draw.rectangle([8, 8, CARD_W - 9, CARD_H - 9], outline=(35, 32, 24), width=1)

    # Header
    draw.rounded_rectangle([18, 14, CARD_W - 18, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    tag = "BUILD SUMMARY"
    tag_w = int(draw.textlength(tag, font=core.F_SMALL_BOLD)) + 24
    draw.rounded_rectangle([28, 22, 28 + tag_w, 60], radius=5, fill=(40, 32, 20), outline=core.COLOR_GOLD, width=1)
    draw.text((40, 31), tag, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((44 + tag_w, 27), f"CUMULATIVE STATS : {player_name.upper()} (LEVEL {level})", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    # 4 Quadrants naturally grouping the allocated points:
    quads = [
        {
            "title": "STAMINA & MOBILITY (Physiology)",
            "color": (255, 170, 190),
            "box": [30, 88, 585, 380],
            "stats": [
                ("Sprint Speed", "+15%", "Increased sprint movement velocity"),
                ("Sprint Stamina Drain", "-25%", "Significantly extended running duration"),
                ("Natural Stamina Regen", "+30%", "Faster recovery rate while walking/resting"),
                ("Vaulting & Obstacle Agility", "+40%", "Smooth climbing and obstacle clearance")
            ]
        },
        {
            "title": "VITALITY & FIELD SURVIVAL (Physiology & Survival)",
            "color": (215, 185, 255),
            "box": [615, 88, CARD_W - 30, 380],
            "stats": [
                ("Maximum Health (HP)", "+25 HP", "Base vitality pool increased"),
                ("Bleed Clotting Rate", "-35%", "Reduced bleeding duration from cuts"),
                ("Bandage Application Speed", "+20%", "Faster field dressing in combat"),
                ("Field Medic Healing", "+15%", "Enhanced effectiveness from all health kits")
            ]
        },
        {
            "title": "SQUAD MEDIC & REST RESILIENCE (Survival)",
            "color": (180, 230, 180),
            "box": [30, 400, 585, CARD_H - 25],
            "stats": [
                ("Surgeon (5/5) Revive Speed", "+25%", "Rapid revival of downed squadmates in combat"),
                ("Revive Instant Health Burst", "+30 HP", "Allies stand up with immediate health buffer"),
                ("Campfire Rest Recovery", "+50%", "Accelerated health and stamina regen at camps"),
                ("Tier VIII Survival Mastery", "ACTIVE", "Ultimate survival endurance threshold unlocked")
            ]
        },
        {
            "title": "HEAVY WEAPONS & COMBAT (Arms)",
            "color": (170, 255, 220),
            "box": [615, 400, CARD_W - 30, CARD_H - 25],
            "stats": [
                ("Deft Strikes (5/5) 2H Melee Cost", "-25%", "Reduced energy consumption on 2H light attacks"),
                ("Two-Handed Attack Speed", "+15%", "Faster follow-up strikes and combo resets"),
                ("Poise & Stagger Impact", "+20%", "Higher stagger probability against armored foes"),
                ("Tier VIII Arms Mastery", "ACTIVE", "Apex weapon efficiency and penetration active")
            ]
        }
    ]

    for q in quads:
        box = q["box"]
        col = q["color"]
        draw.rounded_rectangle(box, radius=8, fill=(14, 14, 18), outline=col, width=2)

        # Title banner
        draw.rounded_rectangle([box[0] + 6, box[1] + 6, box[2] - 6, box[1] + 42], radius=6, fill=(24, 20, 26), outline=col, width=1)
        draw.text((box[0] + 16, box[1] + 12), q["title"], fill=col, font=core.F_SECTION_TITLE)

        sy = box[1] + 52
        for s_name, s_val, s_sub in q["stats"]:
            row_box = [box[0] + 10, sy, box[2] - 10, sy + 48]
            draw.rounded_rectangle(row_box, radius=5, fill=(18, 18, 22), outline=(40, 38, 30), width=1)

            draw.text((row_box[0] + 12, row_box[1] + 8), s_name, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
            draw.text((row_box[0] + 12, row_box[1] + 28), s_sub, fill=(160, 160, 145), font=core.F_BODY)

            vw = int(draw.textlength(s_val, font=core.F_SMALL_BOLD)) + 20
            v_box = [row_box[2] - vw - 10, row_box[1] + 10, row_box[2] - 10, row_box[3] - 10]
            draw.rounded_rectangle(v_box, radius=4, fill=(35, 28, 16), outline=core.COLOR_GOLD, width=1)
            draw.text((v_box[0] + 10, v_box[1] + 6), s_val, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

            sy += 54

    return save_and_sync(canvas, "build_stats_summary.jpg")


if __name__ == "__main__":
    print("Testing mastery_cards_v5...")
    p1 = render_all_5_mastery_trees_card()
    p2 = render_build_stats_summary_card()
    print("p1:", p1)
    print("p2:", p2)
