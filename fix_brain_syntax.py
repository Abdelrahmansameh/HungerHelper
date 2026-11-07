with open('co_pilot/brain.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_block = '''                if is_french:
                    v_str = f" Achat disponible chez {comp_intel['vendor_buy']}." if comp_intel.get("vendor_buy") else ""
                    spoken = f"Le {comp_intel['name_en']} ({comp_intel['rarity']}) se vend {s_s} argent {s_c} cuivre.{v_str} Fiche transmise."
                    display = (
                        f"💰 **FICHE OFFICIELLE : {comp_intel['name_en'].upper()}**\\n\\n"
                        f"• Rareté : **{comp_intel['rarity']}** | Catégorie : **{comp_intel['category']}**\\n"
                        f"• Valeur de Revente : **{s_s} Argent {s_c} Cuivre**\\n"
                        f"• Achat Château : **{comp_intel.get('vendor_buy') or 'Loot exclusif en raid'}**\\n"
                        f"• Butin & Conteneurs : **{comp_intel.get('best_container') or 'Conteneurs de raid'}**\\n"
                        f"• Description In-Game : *« {comp_intel.get('lore_desc', '')[:100]} »*\\n\\n"
                        f"🖼️ *Fiche visuelle Hunger Companion jointe ci-dessous.*"
                    )
                else:
                    spoken = f"The {comp_intel['name_en']} ({comp_intel['rarity']}) sells for {s_s} silver {s_c} copper. Card dispatched."
                    display = f"💰 **OFFICIAL ITEM PROFILE : {comp_intel['name_en'].upper()}**\\n• Sell Price: **{s_s} Silver {s_c} Copper**"
                return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}
'''

start_idx = -1
for i, l in enumerate(lines):
    if 'if is_french:' in l and 'comp_intel' in lines[i+1]:
        start_idx = i
        break

assert start_idx != -1, 'start_idx not found'
end_idx = start_idx
while 'return {"spoken_text"' not in lines[end_idx]:
    end_idx += 1
end_idx += 1

lines[start_idx:end_idx] = [new_block]

with open('co_pilot/brain.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Fixed display string syntax in brain.py!')
