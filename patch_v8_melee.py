import re

with open("universal_v8_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Fix weapon card directional compass and price layout
old_block = """    icon_frame = [left_box[0] + 16, left_box[1] + 48, left_box[2] - 16, left_box[1] + 180]
    draw.rounded_rectangle(icon_frame, radius=8, fill=(16, 16, 13), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(w_img_p):
        safe_paste(canvas, Image.open(w_img_p), icon_frame)

    # Sell price
    raw_p = str(w.get("sell_price", "2 48")).split()
    s_s, s_c = (int(raw_p[0]), int(raw_p[1])) if len(raw_p) >= 2 else (int(raw_p[0]), 0)
    draw.text((left_box[0] + 20, icon_frame[3] + 10), "BASE MARKET VALUE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 20, icon_frame[3] + 28), f"\U0001f4b0 {s_s} Silver  {s_c} Copper", fill=core.PRIO_YELLOW, font=core.F_HEADER_TITLE)

    # Directional Attack Compass
    draw.text((left_box[0] + 20, icon_frame[3] + 64), "DIRECTIONAL ATTACK COMPASS :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    wheel_cx = (left_box[0] + left_box[2]) // 2
    wheel_cy = icon_frame[3] + 195
    rad = 85

    draw.ellipse([wheel_cx - rad, wheel_cy - rad, wheel_cx + rad, wheel_cy + rad], outline=(60, 55, 45), width=2)
    draw.line([(wheel_cx, wheel_cy - rad), (wheel_cx, wheel_cy + rad)], fill=(60, 55, 45), width=1)
    draw.line([(wheel_cx - rad, wheel_cy), (wheel_cx + rad, wheel_cy)], fill=(60, 55, 45), width=1)

    t_dmg = float(w.get("thrust_damage", 17.0))
    l_dmg = float(w.get("light_damage", 34.0))
    h_dmg = float(w.get("heavy_damage", 43.0))
    out_dmg = float(w.get("light_no_energy", 17.0))

    # Compass values
    draw.text((wheel_cx - 16, wheel_cy - rad - 20), f"↑ {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx - 16, wheel_cy + rad + 6), f"↓ {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx - rad - 38, wheel_cy - 8), f"← {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx + rad + 6, wheel_cy - 8), f"→ {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx - 28, wheel_cy - 8), f"Thrust: {t_dmg}", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TAG)"""

new_block = """    icon_frame = [left_box[0] + 16, left_box[1] + 48, left_box[2] - 16, left_box[1] + 175]
    draw.rounded_rectangle(icon_frame, radius=8, fill=(16, 16, 13), outline=core.BORDER_SUBTLE, width=1)
    if os.path.exists(w_img_p):
        safe_paste(canvas, Image.open(w_img_p), (icon_frame[0] + 8, icon_frame[1] + 8, icon_frame[2] - icon_frame[0] - 16, icon_frame[3] - icon_frame[1] - 16))

    # Sell price
    raw_p = str(w.get("sell_price", "2 48")).split()
    s_s, s_c = (int(raw_p[0]), int(raw_p[1])) if len(raw_p) >= 2 else (int(raw_p[0]), 0)
    draw.text((left_box[0] + 20, icon_frame[3] + 8), "BASE MARKET VALUE :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    draw.text((left_box[0] + 20, icon_frame[3] + 26), f"• {s_s} Silver  {s_c} Copper", fill=core.PRIO_YELLOW, font=core.F_CARD_TITLE)

    # Directional Attack Compass
    draw.text((left_box[0] + 20, icon_frame[3] + 56), "DIRECTIONAL ATTACK COMPASS :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    wheel_cx = (left_box[0] + left_box[2]) // 2
    wheel_cy = icon_frame[3] + 175
    rad = 75

    draw.ellipse([wheel_cx - rad, wheel_cy - rad, wheel_cx + rad, wheel_cy + rad], outline=(60, 55, 45), width=2)
    draw.line([(wheel_cx, wheel_cy - rad), (wheel_cx, wheel_cy + rad)], fill=(60, 55, 45), width=1)
    draw.line([(wheel_cx - rad, wheel_cy), (wheel_cx + rad, wheel_cy)], fill=(60, 55, 45), width=1)

    t_dmg = float(w.get("thrust_damage", 17.0))
    l_dmg = float(w.get("light_damage", 34.0))
    h_dmg = float(w.get("heavy_damage", 43.0))
    out_dmg = float(w.get("light_no_energy", 17.0))

    # Compass values
    draw.text((wheel_cx - 16, wheel_cy - rad - 20), f"↑ {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx - 16, wheel_cy + rad + 4), f"↓ {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx - rad - 38, wheel_cy - 8), f"← {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx + rad + 6, wheel_cy - 8), f"→ {l_dmg}", fill=(160, 220, 255), font=core.F_HEADER_TAG)
    draw.text((wheel_cx - 28, wheel_cy - 8), f"Thrust: {t_dmg}", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TAG)"""

if old_block in text:
    text = text.replace(old_block, new_block)
    print("Replaced melee weapon card block!")
else:
    print("Warning: old_block not found directly, checking regex...")

with open("universal_v8_engine.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated universal_v8_engine.py successfully!")
