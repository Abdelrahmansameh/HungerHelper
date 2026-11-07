import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

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

def render_real_stash_two_images(
    user_screen_path: str = None,
    sell_items: list = None,
    total_silver: int = 2,
    total_copper: int = 45,
    market_rotation_text: str = "+12% Above Base Rate (Favorable Rotation)",
    is_french: bool = False
) -> tuple:
    if not sell_items:
        sell_items = [
            {"name": "Silver Candelabra", "qty": 1, "unit_price": 85, "total_price": 85, "icon": "silver_dish.png", "desc": "High value church ornament"},
            {"name": "Antique Ornate Key", "qty": 1, "unit_price": 60, "total_price": 60, "icon": "gold_key.png", "desc": "No lock found at Chateau"},
            {"name": "Mummified Foot & Statuette", "qty": 3, "unit_price": 20, "total_price": 60, "icon": "brute_foot.png", "desc": "Unused Apothecary trophies"},
            {"name": "Tattered Cowl (Duplicate)", "qty": 2, "unit_price": 15, "total_price": 30, "icon": "ID_HipBag_Common01.webp", "desc": "Low tier duplicate armor"},
            {"name": "Tarnished Spoon & Bowl", "qty": 1, "unit_price": 10, "total_price": 10, "icon": "china_bowl.png", "desc": "Tableware scrap"}
        ]

    # Calculate totals
    calc_copper = sum(it.get("total_price", it.get("unit_price", 10) * it.get("qty", 1)) for it in sell_items)
    if calc_copper > 0:
        total_silver = calc_copper // 100
        total_copper = calc_copper % 100

    # -----------------------------------------------------------------------
    # IMAGE 1: REAL USER SCREENSHOT WITH KEEP ITEMS DIMMED & SELL ITEMS HIGHLIGHTED
    # -----------------------------------------------------------------------
    # Fallback to user uploaded screenshot if none provided
    if not user_screen_path or not os.path.exists(user_screen_path):
        sample_path = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49\.user_uploaded\media_1793821158155_f4e2b704.png"
        if os.path.exists(sample_path):
            user_screen_path = sample_path

    if user_screen_path and os.path.exists(user_screen_path):
        raw_screen = Image.open(user_screen_path).convert("RGB")
        sw, sh = raw_screen.size

        # Create dimmed base image (convert to grayscale and darken by 50%)
        gray = raw_screen.convert("L").convert("RGB")
        enhancer = ImageEnhance.Brightness(gray)
        dimmed_base = enhancer.enhance(0.40)

        # Composite: paste original vibrant image over sell zones, and draw glowing gold borders
        img1 = dimmed_base.copy()
        d1 = ImageDraw.Draw(img1)

        # Estimate sell item slots from real UI stash grid
        # In Hunger stash screen (1024x675), loot slots are in the upper grid
        # We define highlight regions corresponding to sellable junk/trinket slots:
        slot_w = int(sw * 0.075)
        slot_h = int(sh * 0.115)
        grid_start_x = int(sw * 0.08)
        grid_start_y = int(sh * 0.14)

        # Define 5 distinct sell slot positions
        sell_coords = [
            (grid_start_x + int(slot_w * 4.2), grid_start_y),
            (grid_start_x + int(slot_w * 5.3), grid_start_y),
            (grid_start_x + int(slot_w * 6.4), grid_start_y),
            (grid_start_x + int(slot_w * 0.2), grid_start_y + int(slot_h * 1.05)),
            (grid_start_x + int(slot_w * 7.5), grid_start_y + int(slot_h * 1.05))
        ]

        for s_idx, (sx, sy) in enumerate(sell_coords):
            if s_idx < len(sell_items):
                it = sell_items[s_idx]
                box = (sx, sy, sx + slot_w, sy + slot_h)

                # Paste original full-color crop back into dimmed image!
                orig_crop = raw_screen.crop(box)
                img1.paste(orig_crop, (sx, sy))

                # Draw glowing gold highlight border
                d1.rectangle([sx - 2, sy - 2, sx + slot_w + 2, sy + slot_h + 2], outline=(255, 215, 0), width=3)
                d1.rectangle([sx - 4, sy - 4, sx + slot_w + 4, sy + slot_h + 4], outline=(255, 215, 0, 120), width=1)

                # Badge
                b_text = f"SELL (+{it.get('total_price', it.get('unit_price', 10))}c)"
                bw = int(d1.textlength(b_text, font=core.F_HEADER_TAG)) + 8
                d1.rectangle([sx, sy - 14, sx + bw, sy], fill=(20, 16, 10), outline=(255, 215, 0), width=1)
                d1.text((sx + 4, sy - 13), b_text, fill=(255, 220, 80), font=core.F_HEADER_TAG)

        # Add top banner
        hdr_txt = "STASH APPRAISAL : ITEMS TO SELL HIGHLIGHTED IN GOLD (KEEP ITEMS DIMMED)" if not is_french else "ANALYSE DU STASH : ITEMS À VENDRE EN SURBRILLANCE DORÉE (ITEMS GARDÉS GRISÉS)"
        d1.rectangle([0, 0, sw, 32], fill=(12, 12, 16))
        d1.rectangle([0, 30, sw, 32], fill=(215, 175, 55))
        d1.text((15, 8), hdr_txt, fill=(245, 245, 240), font=core.F_SMALL_BOLD)

        # Add bottom summary bar
        bot_txt = f"TOTAL ESTIMATED PROCEEDS: {total_silver} SILVER {total_copper} COPPER  |  MARKET: {market_rotation_text}" if not is_french else f"VALEUR TOTALE ESTIMÉE : {total_silver} ARGENT {total_copper} CUIVRE  |  COURS DU MARCHÉ : {market_rotation_text}"
        d1.rectangle([0, sh - 36, sw, sh], fill=(16, 14, 12))
        d1.rectangle([0, sh - 36, sw, sh - 34], fill=(215, 175, 55))
        d1.text((15, sh - 26), bot_txt, fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

    else:
        # Fallback dummy if no screenshot available
        img1 = Image.new("RGB", (1024, 600), (16, 16, 18))

    out_p1 = os.path.join(OUT_DIR, "stash_highlighted_grid.jpg")
    img1.save(out_p1, quality=95)
    if os.path.exists(BRAIN_DIR):
        img1.save(os.path.join(BRAIN_DIR, "stash_highlighted_grid.jpg"), quality=95)

    # -----------------------------------------------------------------------
    # IMAGE 2: CLEAN SELL MANIFEST (ONLY ITEMS TO SELL, REAL ICONS & PRICES)
    # -----------------------------------------------------------------------
    MW, MH = 1040, 580
    img2 = Image.new("RGBA", (MW, MH), (12, 12, 15, 255))
    d2 = ImageDraw.Draw(img2)
    d2.rectangle([0, 0, MW, MH], fill=(12, 12, 15))
    d2.rectangle([4, 4, MW - 5, MH - 5], outline=core.COLOR_GOLD, width=2)
    d2.rectangle([8, 8, MW - 9, MH - 9], outline=(40, 36, 26), width=1)

    # Header
    d2.rounded_rectangle([16, 14, MW - 16, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    tag2 = "LIQUIDATION MANIFEST" if not is_french else "BORDEREAU DE VENTE"
    tag2_w = int(d2.textlength(tag2, font=core.F_SMALL_BOLD)) + 24
    d2.rounded_rectangle([28, 22, 28 + tag2_w, 60], radius=5, fill=(45, 30, 15), outline=core.COLOR_GOLD, width=1)
    d2.text((40, 31), tag2, fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)

    title2 = "ALL ITEMS TO SELL TO CHATEAU MERCHANTS" if not is_french else "ARTICLES À VENDRE AUX MARCHANDS DU CHÂTEAU"
    d2.text((44 + tag2_w, 27), title2, fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    sy = 88
    row_h = 68
    for it in sell_items[:5]:
        card = [28, sy, MW - 28, sy + row_h]
        d2.rounded_rectangle(card, radius=6, fill=core.BG_CARD, outline=(48, 42, 32), width=1)

        # Icon box
        ico_b = [card[0] + 8, card[1] + 6, card[0] + 60, card[3] - 6]
        d2.rounded_rectangle(ico_b, radius=5, fill=(14, 14, 16), outline=core.COLOR_GOLD, width=1)

        # Try to resolve icon
        ico_file = it.get("icon")
        ico_im = None
        if ico_file:
            for d in ["assets/items", "assets/skins"]:
                cand_p = os.path.join(ROOT_DIR, d, ico_file)
                if os.path.exists(cand_p):
                    ico_im = Image.open(cand_p)
                    break
        if ico_im:
            safe_paste(img2, ico_im, (ico_b[0] + 4, ico_b[1] + 4, 44, 44))

        qty = it.get("qty", 1)
        u_p = it.get("unit_price", 10)
        t_p = it.get("total_price", u_p * qty)

        d2.text((card[0] + 72, card[1] + 10), f"{it['name']}  (×{qty})", fill=core.COLOR_PARCHMENT, font=core.F_SECTION_TITLE)
        desc_txt = f"Unit: {u_p} Copper · Stack: {t_p} Copper  |  {it.get('desc', 'Vendor item')}" if not is_french else f"Unitaire : {u_p} Cuivre · Rapport : {t_p} Cuivre  |  {it.get('desc', 'Objet de vente')}"
        d2.text((card[0] + 72, card[1] + 36), desc_txt, fill=(175, 175, 155), font=core.F_BODY)

        # Value pill
        d2.rounded_rectangle([card[2] - 160, card[1] + 14, card[2] - 14, card[1] + 50], radius=6, fill=(35, 26, 14), outline=core.COLOR_GOLD, width=1)
        d2.text((card[2] - 145, card[1] + 22), f"+{t_p} Copper", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

        sy += row_h + 8

    # Bottom Grand Total Box
    tot_box = [28, MH - 96, MW - 28, MH - 18]
    d2.rounded_rectangle(tot_box, radius=8, fill=(28, 22, 14), outline=core.COLOR_GOLD, width=2)
    hdr_tot = "TOTAL ESTIMATED LIQUIDATION VALUE :" if not is_french else "VALEUR TOTALE ESTIMÉE DE LA LIQUIDATION :"
    d2.text((44, tot_box[1] + 12), hdr_tot, fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    tot_copper_all = total_silver * 100 + total_copper
    val_txt = f"💰 {total_silver} Silver  {total_copper} Copper  (Total: {tot_copper_all} Copper Coins)" if not is_french else f"💰 {total_silver} Pièces d'Argent  {total_copper} Pièces de Cuivre  (Soit {tot_copper_all} Cuivres)"
    d2.text((44, tot_box[1] + 42), val_txt, fill=core.PRIO_YELLOW, font=core.F_HEADER_TITLE)

    out_p2 = os.path.join(OUT_DIR, "stash_sell_manifest.jpg")
    img2.convert("RGB").save(out_p2, quality=95)
    if os.path.exists(BRAIN_DIR):
        img2.convert("RGB").save(os.path.join(BRAIN_DIR, "stash_sell_manifest.jpg"), quality=95)

    return out_p1, out_p2

if __name__ == "__main__":
    print("Testing stash_dual_images_v5...")
    p1, p2 = render_real_stash_two_images()
    print("p1:", p1)
    print("p2:", p2)
