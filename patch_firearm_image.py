with open('universal_v8_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_specs_block = '''    specs = [
        ("Base Damage (<=40m)", f"{f_data['damage']} dmg"),
        ("Headshot Critical", f"{f_data['headshot']} critical dmg"),
        ("Magazine Capacity", f"{f_data['clip']} round(s)"),
        ("Fire Rate Interval", f_data["rate"]),
        ("Tactical Reload", f"{f_data['reload']} cycle"),
        ("Ammunition Type", f_data["ammo"]),
        ("Chateau Market Value", f_data["sell"]),
        ("Merchant Acquisition", f_data["vendor"][:24])
    ]

    sy = ico_frame[3] + 32
    for lbl, val in specs:
        draw.text((left_box[0] + 16, sy), f"* {lbl} :", fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
        draw.text((left_box[0] + 170, sy), val, fill=core.PRIO_YELLOW if "dmg" in val else (180, 180, 160), font=core.F_BODY)
        sy += 27'''

new_specs_block = '''    specs = [
        ("Base Damage", f"{f_data['damage']} dmg"),
        ("Headshot Crit", f"{f_data['headshot']} dmg"),
        ("Mag Capacity", f"{f_data['clip']} round(s)"),
        ("Fire Interval", f_data["rate"]),
        ("Reload Time", f"{f_data['reload']}"),
        ("Ammo Type", f_data["ammo"]),
        ("Market Value", f_data["sell"]),
        ("Vendor Buy", f_data["vendor"][:22])
    ]

    sy = ico_frame[3] + 30
    for lbl, val in specs:
        draw.text((left_box[0] + 16, sy), f"• {lbl} :", fill=core.COLOR_PARCHMENT, font=core.F_SMALL_BOLD)
        draw.text((left_box[0] + 175, sy), val, fill=core.PRIO_YELLOW if "dmg" in val else (180, 180, 160), font=core.F_BODY)
        sy += 26'''

if old_specs_block in code:
    code = code.replace(old_specs_block, new_specs_block)
    print("Cleaned specs layout!")
else:
    print("old_specs_block not matched!")

# Also fix bottom advice wrapping
old_advice = '''    draw.text((tip_b[0] + 14, tip_b[1] + 6), f"• Ballistic Combat Advice : With {f_data['name']}, always aim for the head to maximize critical multiplier.", fill=core.COLOR_GOLD, font=core.F_BODY)
    draw.text((tip_b[0] + 14, tip_b[1] + 24), f"Chambering: {f_data['ammo']}. Ensure full reload cover before engaging armored targets.", fill=(180, 175, 160), font=core.F_BODY)'''

new_advice = '''    draw.text((tip_b[0] + 14, tip_b[1] + 6), f"• Combat Advice : With {f_data['name']}, aim for the head to maximize critical multiplier.", fill=core.COLOR_GOLD, font=core.F_BODY)
    draw.text((tip_b[0] + 14, tip_b[1] + 24), f"• Chambering : {f_data['ammo']}. Ensure cover before reloading against armored targets.", fill=(180, 175, 160), font=core.F_BODY)'''

if old_advice in code:
    code = code.replace(old_advice, new_advice)
    print("Cleaned advice wrapping!")

with open('universal_v8_engine.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved universal_v8_engine.py!")
