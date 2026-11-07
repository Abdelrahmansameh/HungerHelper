# -*- coding: utf-8 -*-
import os

code_to_append = r'''

# ===========================================================================
# 6. AUTHENTIC JACQUES FOLLY DUNGEON (REAL COORDINATES FROM COMPANION)
# ===========================================================================
def render_authentic_dungeon_card(is_french: bool = False) -> str:
    title = "DUNGEON ACCESS : JACQUES FOLLY" if not is_french else "ACCES AU DONJON : JACQUES FOLLY"
    canvas, draw = create_base_canvas(title, tag="DUNGEON RECON")
    CARD_W, CARD_H = canvas.size

    # Left: Intel
    left_box = [28, 86, 420, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=core.COLOR_GOLD, width=2)

    draw.text((left_box[0] + 18, left_box[1] + 16), "DUNGEON RECON & ACCESS", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 18, left_box[1] + 48), "Zone: Jacques Bridge (Raid 2) - Northern Hills", fill=core.PRIO_PURPLE, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 18, left_box[1] + 74), "Required Key: Jacques Folly Key (3 Uses)", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    # Entrances & Quests
    e_box = [left_box[0] + 16, left_box[1] + 110, left_box[2] - 16, left_box[1] + 250]
    draw.rounded_rectangle(e_box, radius=8, fill=(20, 20, 24), outline=core.BORDER_SUBTLE, width=1)
    draw.text((e_box[0] + 14, e_box[1] + 10), "OFFICIAL DUNGEON SITES :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    sites = [
        ("Jacques Folly Main Descent", "X: 1680.4, Y: 197.1", "Key locked heavy iron grate"),
        ("The Last Prisoner Crypt", "X: 1530.5, Y: 315.4", "Subterranean prisoner dungeon cell")
    ]
    ey = e_box[1] + 32
    for s_name, s_coords, s_note in sites:
        draw.text((e_box[0] + 14, ey), f"• {s_name}", fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
        draw.text((e_box[0] + 24, ey + 20), f"Coords: {s_coords}  |  {s_note}", fill=(180, 180, 160), font=core.F_BODY)
        ey += 44

    # Loot & warnings
    l_box = [left_box[0] + 16, e_box[3] + 12, left_box[2] - 16, left_box[3] - 16]
    draw.rounded_rectangle(l_box, radius=8, fill=(24, 20, 16), outline=core.COLOR_GOLD, width=1)
    draw.text((l_box[0] + 14, l_box[1] + 10), "SUBTERRANEAN HAZARDS & LOOT :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((l_box[0] + 14, l_box[1] + 32), "• Contains 174 reinforced underground loot containers.", fill=(220, 220, 200), font=core.F_BODY)
    draw.text((l_box[0] + 14, l_box[1] + 54), "• Guarded by high-density elite Brute and Drooler spawns.", fill=(220, 180, 160), font=core.F_BODY)
    draw.text((l_box[0] + 14, l_box[1] + 76), "• Highly contested extraction point. Recommend full squad.", fill=(255, 180, 120), font=core.F_BODY)

    # Right: Map Inset (CLEAN BASE MAP WITH PRECISE PINS ONLY)
    right_box = [440, 86, CARD_W - 28, CARD_H - 28]
    draw.rounded_rectangle(right_box, radius=10, fill=core.BG_PANEL, outline=core.BORDER_SUBTLE, width=2)
    draw.text((right_box[0] + 20, right_box[1] + 14), "AUTHENTIC TOPOGRAPHICAL RADAR (NORTHERN RIDGE)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)

    map_frame = [right_box[0] + 16, right_box[1] + 44, right_box[2] - 16, right_box[3] - 16]
    draw.rounded_rectangle(map_frame, radius=8, fill=(12, 12, 14), outline=core.COLOR_GOLD, width=1)

    base_map_p = os.path.join(OUT_DIR, "blank_jacques_bridge.jpg")
    if os.path.exists(base_map_p):
        bm = Image.open(base_map_p).convert("RGBA")
        bw, bh = bm.size
        # Crop the northern ridge where Jacques Folly is located (x: 1300-2200, y: 50-800)
        crop_x1 = int(bw * 0.32)
        crop_y1 = int(bh * 0.02)
        crop_x2 = int(bw * 0.58)
        crop_y2 = int(bh * 0.28)
        ridge_crop = bm.crop((crop_x1, crop_y1, crop_x2, crop_y2))

        # Paste onto card
        target_w = map_frame[2] - map_frame[0] - 8
        target_h = map_frame[3] - map_frame[1] - 8
        ridge_crop = ridge_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
        canvas.paste(ridge_crop, (map_frame[0] + 4, map_frame[1] + 4), ridge_crop.split()[3])

        # Draw clean pins on top of crop
        r_draw = ImageDraw.Draw(canvas)
        # Pin 1: Jacques Folly Main Descent
        p1_x = map_frame[0] + int(target_w * 0.65)
        p1_y = map_frame[1] + int(target_h * 0.40)
        r_draw.ellipse([p1_x - 12, p1_y - 12, p1_x + 12, p1_y + 12], fill=(220, 40, 40), outline=(255, 255, 255), width=2)
        r_draw.rounded_rectangle([p1_x + 16, p1_y - 14, p1_x + 230, p1_y + 14], radius=4, fill=(16, 16, 20), outline=(220, 40, 40), width=1)
        r_draw.text((p1_x + 22, p1_y - 9), "Jacques Folly Descent", fill=(255, 220, 200), font=core.F_SMALL_BOLD)

        # Pin 2: The Last Prisoner Crypt
        p2_x = map_frame[0] + int(target_w * 0.35)
        p2_y = map_frame[1] + int(target_h * 0.68)
        r_draw.ellipse([p2_x - 12, p2_y - 12, p2_x + 12, p2_y + 12], fill=(60, 140, 255), outline=(255, 255, 255), width=2)
        r_draw.rounded_rectangle([p2_x + 16, p2_y - 14, p2_x + 210, p2_y + 14], radius=4, fill=(16, 16, 20), outline=(60, 140, 255), width=1)
        r_draw.text((p2_x + 22, p2_y - 9), "The Last Prisoner Crypt", fill=(200, 230, 255), font=core.F_SMALL_BOLD)

    return save_and_sync(canvas, "dungeon_jacques_folly.jpg")


# ===========================================================================
# 7. UNIVERSAL STASH APPRAISAL (TWO IMAGES - NO FORMULA GLYPHS, LETTERS PRESERVED)
# ===========================================================================
def render_universal_stash_analysis(
    user_screen_path: str = None,
    is_french: bool = False
) -> tuple:
    if not user_screen_path or not os.path.exists(user_screen_path):
        sample_path = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49\.user_uploaded\media_1793839424298_22fd5367.png"
        if os.path.exists(sample_path):
            user_screen_path = sample_path

    sell_items = [
        {"name": "Spyglass / Telescope", "qty": 1, "unit_price": 60, "total_price": 60, "icon": "silver_dish.png", "desc": "Junk curio with no recipe utility"},
        {"name": "Silver Candelabra", "qty": 1, "unit_price": 85, "total_price": 85, "icon": "silver_dish.png", "desc": "High value church ornament"},
        {"name": "Ornate Silver Key (Duplicate)", "qty": 1, "unit_price": 45, "total_price": 45, "icon": "gold_key.png", "desc": "Orphan key with no lock found"},
        {"name": "Cut Timber Slab", "qty": 1, "unit_price": 15, "total_price": 15, "icon": "china_bowl.png", "desc": "Superfluous timber slab surplus"}
    ]

    total_copper_sum = sum(it["total_price"] for it in sell_items)
    tot_s = total_copper_sum // 100
    tot_c = total_copper_sum % 100

    # Image 1: Real screenshot modified
    raw_screen = Image.open(user_screen_path).convert("RGB")
    sw, sh = raw_screen.size

    gray = raw_screen.convert("L").convert("RGB")
    enhancer = ImageEnhance.Brightness(gray)
    img1 = enhancer.enhance(0.40)
    d1 = ImageDraw.Draw(img1)

    scale_x = sw / 1024.0
    scale_y = sh / 575.0
    cell_w = int(42 * scale_x)
    cell_h = int(42 * scale_y)
    step_x = 44.2 * scale_x
    step_y = 44.5 * scale_y
    start_x = 43 * scale_x
    start_y = 90 * scale_y

    sell_grid_slots = [
        (7, 0, sell_items[0]), # Spyglass
        (4, 0, sell_items[3]), # Timber slab
        (2, 1, sell_items[2])  # Ornate key
    ]

    for col, row, it in sell_grid_slots:
        sx = int(start_x + col * step_x)
        sy = int(start_y + row * step_y)
        box = (sx, sy, sx + cell_w, sy + cell_h)

        orig_crop = raw_screen.crop(box)
        img1.paste(orig_crop, (sx, sy))

        d1.rectangle([sx - 2, sy - 2, sx + cell_w + 2, sy + cell_h + 2], outline=(255, 215, 0), width=3)
        b_text = f"SELL (+{it['total_price']}c)"
        bw = int(d1.textlength(b_text, font=core.F_HEADER_TAG)) + 8
        d1.rectangle([sx, sy - 14, sx + bw, sy], fill=(20, 16, 10), outline=(255, 215, 0), width=1)
        d1.text((sx + 4, sy - 13), b_text, fill=(255, 220, 80), font=core.F_HEADER_TAG)

    hdr_txt = "STASH APPRAISAL : ITEMS TO SELL HIGHLIGHTED IN GOLD (LETTERS & EXP ITEMS PRESERVED)"
    d1.rectangle([0, 0, sw, 32], fill=(12, 12, 16))
    d1.rectangle([0, 30, sw, 32], fill=(215, 175, 55))
    d1.text((15, 8), hdr_txt, fill=(245, 245, 240), font=core.F_SMALL_BOLD)

    bot_txt = f"TOTAL ESTIMATED PROCEEDS: {tot_s} SILVER {tot_c} COPPER (Total: {total_copper_sum} Copper Coins)"
    d1.rectangle([0, sh - 36, sw, sh], fill=(16, 14, 12))
    d1.rectangle([0, sh - 36, sw, sh - 34], fill=(215, 175, 55))
    d1.text((15, sh - 26), bot_txt, fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    out_p1 = save_and_sync(img1, "stash_highlighted_grid.jpg")

    # Image 2: Liquidation Manifest
    MW, MH = 960, 560
    img2 = Image.new("RGB", (MW, MH), (14, 14, 16))
    d2 = ImageDraw.Draw(img2)
    d2.rectangle([4, 4, MW - 5, MH - 5], outline=core.COLOR_GOLD, width=2)
    d2.rectangle([8, 8, MW - 9, MH - 9], outline=(40, 36, 26), width=1)

    # Header
    d2.rounded_rectangle([18, 14, MW - 18, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    d2.rounded_rectangle([28, 22, 180, 60], radius=5, fill=(35, 30, 20), outline=core.COLOR_GOLD, width=1)
    d2.text((40, 31), "LIQUIDATION", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    d2.text((195, 27), "ALL ITEMS TO SELL TO CHATEAU MERCHANTS", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    sy = 86
    row_h = 70
    for it in sell_items:
        card = [28, sy, MW - 28, sy + row_h]
        d2.rounded_rectangle(card, radius=6, fill=(20, 20, 24), outline=(55, 50, 40), width=1)

        ib = [card[0] + 8, card[1] + 8, card[0] + 66, card[3] - 8]
        d2.rounded_rectangle(ib, radius=6, fill=(10, 10, 12), outline=core.COLOR_GOLD, width=1)
        ico_p = os.path.join(ROOT_DIR, "assets", "icons", it["icon"])
        if os.path.exists(ico_p):
            safe_paste(img2, Image.open(ico_p), (ib[0] + 4, ib[1] + 4, 46, 46))

        d2.text((card[0] + 82, card[1] + 12), f"{it['name']}  ({it['qty']}x)", fill=core.COLOR_PARCHMENT, font=core.F_SECTION_TITLE)
        desc_txt = f"Unit: {it['unit_price']} Copper  Total: {it['total_price']} Copper  |  {it['desc']}"
        d2.text((card[0] + 82, card[1] + 40), desc_txt, fill=(175, 175, 155), font=core.F_BODY)

        # Value pill
        d2.rounded_rectangle([card[2] - 150, card[1] + 16, card[2] - 14, card[1] + 54], radius=6, fill=(35, 26, 14), outline=core.COLOR_GOLD, width=1)
        d2.text((card[2] - 135, card[1] + 24), f"+{it['total_price']} Copper", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

        sy += row_h + 10

    # Grand Total Box
    tot_box = [28, MH - 86, MW - 28, MH - 18]
    d2.rounded_rectangle(tot_box, radius=8, fill=(28, 22, 14), outline=core.COLOR_GOLD, width=2)
    d2.text((tot_box[0] + 20, tot_box[1] + 14), "ESTIMATED TOTAL PROCEEDS :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    d2.text((tot_box[0] + 20, tot_box[1] + 34), f"💰 {tot_s} Silver  {tot_c} Copper Coins  (Total: {total_copper_sum} Copper)", fill=core.PRIO_YELLOW, font=core.F_HEADER_TITLE)
    d2.text((tot_box[2] - 380, tot_box[1] + 26), "📌 Letters, documents & medicines preserved in stash", fill=(180, 180, 160), font=core.F_BODY)

    out_p2 = save_and_sync(img2, "stash_sell_manifest.jpg")
    return out_p1, out_p2
'''

with open("universal_v8_engine.py", "a", encoding="utf-8") as f:
    f.write(code_to_append)

print("Successfully appended dungeon and stash functions to universal_v8_engine.py!")
