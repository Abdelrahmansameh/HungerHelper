with open("universal_v8_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

old_tip = """    # Bottom tip: World Spawn & Drop Location
    tip_box = [right_box[0] + 16, right_box[3] - 64, right_box[2] - 16, right_box[3] - 14]
    draw.rounded_rectangle(tip_box, radius=8, fill=(20, 18, 14), outline=core.COLOR_GOLD, width=1)
    drop_info = "The Chateau (100% Guaranteed World Discovery)" if "peasant" in skin_name.lower() else "Expedition Weapon Caches & Chateau Hub Discovery"
    draw.text((tip_box[0] + 14, tip_box[1] + 8), f"• World Spawn / Drop Intel : {drop_info}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((tip_box[0] + 14, tip_box[1] + 28), f"• Artisan Workshop : Octave de Villiers (Chateau) | Blueprint Fee : {fee_digits} Copper", fill=(190, 185, 170), font=core.F_BODY)
    draw.text((tip_box[0] + 14, tip_box[1] + 28), "Never sell these rare crafting parts to roaming merchants before forging your skin!", fill=(180, 175, 160), font=core.F_BODY)"""

new_tip = """    # Bottom tip: World Spawn & Drop Location (Zero Text Collision)
    tip_box = [right_box[0] + 16, right_box[3] - 76, right_box[2] - 16, right_box[3] - 12]
    draw.rounded_rectangle(tip_box, radius=8, fill=(20, 18, 14), outline=core.COLOR_GOLD, width=1)
    drop_info = "The Chateau Hub (100% Guaranteed World Discovery in Artisan Quarters)" if "peasant" in skin_name.lower() else "Expedition Weapon Chests & Chateau Hub Discovery"
    draw.text((tip_box[0] + 14, tip_box[1] + 8), f"• World Spawn / Drop Intel : {drop_info}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((tip_box[0] + 14, tip_box[1] + 28), f"• Workshop : Octave de Villiers (Chateau) | Schema Fee : {fee_digits} Copper", fill=(210, 205, 190), font=core.F_BODY)
    draw.text((tip_box[0] + 14, tip_box[1] + 48), "• Note : Store rare crafting ingredients in your Chateau Stash until ready to forge.", fill=(175, 170, 155), font=core.F_BODY)"""

if old_tip in text:
    text = text.replace(old_tip, new_tip)
    print("Patched tip box in universal_v8_engine.py successfully!")
else:
    print("Warning: old_tip block not matched directly!")

with open("universal_v8_engine.py", "w", encoding="utf-8") as f:
    f.write(text)
