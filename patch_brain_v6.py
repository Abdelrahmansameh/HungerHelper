import os

brain_p = os.path.join("co_pilot", "brain.py")
with open(brain_p, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if 'is_skin_query = any(w in lowered for w in ["skin"' in line:
        new_lines.append('        is_skin_query = any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "apparence", "outfit", "confection", "craft"]) and (any(k in lowered for k in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "apparence", "moist", "pouch", "bacchus", "longboy", "marie", "eva", "hugo", "otto", "gabriel", "serine", "spear", "lance"]) or "craft quel" in lowered)\n')
        i += 1
        continue
    if 'card_path = render_skin_card(clean_text, is_french)' in line and 'if is_skin_query:' in lines[i-1]:
        spear_block = '''            if any(w in lowered for w in ["spear", "lance"]):
                from generate_perfect_v6 import render_all_spear_skins
                spear_cards = render_all_spear_skins()
                if is_french:
                    spoken = "Voici les 3 skins officiels pour la Lance : Partisan, Hybernia et Peasant's Burden. 3 fiches transmises."
                    display = (
                        "🎨 **COLLECTION COMPLÈTE DES SKINS POUR LA LANCE (SPEAR)**\\n\\n"
                        "• 🗡️ **1. Partisan** (Cold Iron, Hartshorn, Cuir, Blacksand)\\n"
                        "• 🗡️ **2. Hybernia** (Cold Iron, Eau Distillée)\\n"
                        "• 🗡️ **3. Peasant's Burden** (Tent Peg, Solid Branch, Ficelle Impeccable)\\n\\n"
                        "*(3 fiches visuelles officielles transmises ci-dessous)*"
                    )
                else:
                    spoken = "Here are all 3 official skins for the Spear: Partisan, Hybernia, and Peasant's Burden. Visual cards dispatched."
                    display = (
                        "🎨 **ALL OFFICIAL SPEAR SKINS & CRAFTING FORMULAS**\\n\\n"
                        "• 🗡️ **1. Partisan** (Cold Iron, Hartshorn, Leather Trimmings, Blacksand)\\n"
                        "• 🗡️ **2. Hybernia** (Cold Iron, Distilled Water)\\n"
                        "• 🗡️ **3. Peasant's Burden** (Tent Peg, Solid Branch, Impeccable Twine)\\n\\n"
                        "*(3 full crafting cards attached below)*"
                    )
                return {
                    "spoken_text": spoken,
                    "display_text": display,
                    "image_attachments": spear_cards,
                    "image_attachment": spear_cards[0] if spear_cards else None
                }
            card_path = render_skin_card(clean_text, is_french)
'''
        new_lines.append(spear_block)
        i += 1
        continue
    if 'from test_dynamic_stash_two_images import render_dynamic_stash_two_images' in line:
        new_lines.append('            from generate_perfect_v6 import render_perfect_stash_analysis\n')
        new_lines.append('            p1, p2 = render_perfect_stash_analysis()\n')
        i += 2  # skip p1, p2 line
        continue

    new_lines.append(line)
    i += 1

with open(brain_p, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Updated brain.py cleanly with line processor!")
