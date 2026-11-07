with open('universal_v8_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Update tip_box in render_pure_english_cosmetic_card
old_tip = '''    # Bottom tip
    tip_box = [right_box[0] + 16, right_box[3] - 64, right_box[2] - 16, right_box[3] - 14]
    draw.rounded_rectangle(tip_box, radius=8, fill=(20, 18, 14), outline=core.COLOR_GOLD, width=1)
    draw.text((tip_box[0] + 14, tip_box[1] + 8), "💡 Eloise Tactical Tip : Keep all required ingredients in your Stash at the Chateau.", fill=core.COLOR_GOLD, font=core.F_BODY)'''

new_tip = '''    # Bottom tip: World Spawn & Drop Location
    tip_box = [right_box[0] + 16, right_box[3] - 64, right_box[2] - 16, right_box[3] - 14]
    draw.rounded_rectangle(tip_box, radius=8, fill=(20, 18, 14), outline=core.COLOR_GOLD, width=1)
    drop_info = "The Chateau (100% Guaranteed World Discovery)" if "peasant" in skin_name.lower() else "Expedition Weapon Caches & Chateau Hub Discovery"
    draw.text((tip_box[0] + 14, tip_box[1] + 8), f"• World Spawn / Drop Intel : {drop_info}", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    draw.text((tip_box[0] + 14, tip_box[1] + 28), f"• Artisan Workshop : Octave de Villiers (Chateau) | Blueprint Fee : {fee_digits} Copper", fill=(190, 185, 170), font=core.F_BODY)'''

if old_tip in text:
    text = text.replace(old_tip, new_tip)
    print("Updated cosmetic card tip with world spawn drop intel!")
else:
    print("old_tip not matched in cosmetic card")

# Update get_universal_skins text
old_resp_text = '''            resp_text = (
                f"• 🎨 **{v['name']}** ({v.get('rarity', 'Rare')} cosmetic skin for **{v.get('target')}**)\\n"
                f"  - 📍 **Where to Craft :** Chateau Artisan Workshop (Octave de Villiers)\\n"
                f"  - 🪙 **Schema Crafting Fee :** {fee_clean}\\n"
                f"  - 📦 **Required Materials :** {m_str}\\n"
                f"  - 📜 *« {v.get('lore', 'Authentic Hunger cosmetic blueprint.')} »*"
            )'''

new_resp_text = '''            drop_intel = "The Chateau Hub (100% Fixed World Discovery in Artisan Quarters)" if "peasant" in k_norm else "Expedition Weapon Chests & Chateau Discovery"
            resp_text = (
                f"• 🎨 **{v['name']}** ({v.get('rarity', 'Rare')} cosmetic skin for **{v.get('target')}**)\\n"
                f"  - 📍 **World Spawn / Drop Intel :** {drop_intel}\\n"
                f"  - 🔨 **Crafting Workshop :** Chateau Artisan Workshop (Octave de Villiers)\\n"
                f"  - 🪙 **Blueprint Schema Fee :** {fee_clean}\\n"
                f"  - 📦 **Required Materials :** {m_str}\\n"
                f"  - 📜 *« {v.get('lore', 'Authentic Hunger cosmetic blueprint.')} »*"
            )'''

if old_resp_text in text:
    text = text.replace(old_resp_text, new_resp_text)
    print("Updated get_universal_skins response text with drop intel!")
else:
    print("old_resp_text not matched")

with open('universal_v8_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved universal_v8_engine.py!")
