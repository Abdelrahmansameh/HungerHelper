with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Replace emoji in safe pouch rule to eliminate tofu box
code = code.replace('"🔒 KEEP IN SECURE POUCH"', '"SECURE POUCH (NON-DROPPABLE)"')
code = code.replace('"🔒 À GARDER EN BESACE SÉCURISÉE"', '"BESACE SÉCURISÉE (NON-PERDABLE)"')
code = code.replace('"🎒 Standard Backpack (Droppable)"', '"Standard Backpack (Droppable)"')
code = code.replace('"🎒 Sac classique (Perdable)"', '"Sac d\'expédition (Perdable)"')

# 2. English quest box utility
old_quest_box = '''    else:
        draw.text((q_box[0] + 16, q_box[1] + 38), "• Aucun prérequis de quête directe.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
        draw.text((q_box[0] + 16, q_box[1] + 64), "• Utilité : Recettes de cuisine au Château ou revente pour des pièces.", fill=(180, 180, 160), font=core.F_BODY)'''

new_quest_box = '''    else:
        if not is_french:
            draw.text((q_box[0] + 16, q_box[1] + 38), "• Direct Quest Pre-requisite : None required.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
            draw.text((q_box[0] + 16, q_box[1] + 64), "• Utility : Crafting recipes at Chateau or sold to vendors for coin.", fill=(180, 180, 160), font=core.F_BODY)
        else:
            draw.text((q_box[0] + 16, q_box[1] + 38), "• Aucun prérequis de quête directe.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
            draw.text((q_box[0] + 16, q_box[1] + 64), "• Utilité : Recettes de cuisine au Château ou revente pour des pièces.", fill=(180, 180, 160), font=core.F_BODY)'''

code = code.replace(old_quest_box, new_quest_box)

# 3. Clean drop rate display (Élevé -> High if not french)
code = code.replace("Rate : {drop_rate}", "Rate : {drop_rate.replace('Élevé', 'High')}")

with open("co_pilot/card_renderer.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated card_renderer.py!")
