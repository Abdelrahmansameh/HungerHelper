with open("co_pilot/brain.py", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

target = '        is_skin_query = any(w in lowered for w in ["skin", "skins", "cosmétique", "cosmetique", "tenue", "apparence", "outfit"])'
if target not in content:
    # try with whatever accent representation
    import re
    match = re.search(r'is_skin_query = any\(w in lowered for w in \["skin".*?\]\)', content)
    if match:
        print("Found match:", match.group(0))
        target = match.group(0)

replacement = '''is_skin_query = any(w in lowered for w in ["skin", "skins", "cosmétique", "cosmetique", "tenue", "apparence", "outfit", "confection", "craft"]) and any(k in lowered for k in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "apparence", "moist", "pouch", "bacchus", "longboy", "marie", "eva", "hugo", "otto", "gabriel", "serine"])'''

idx = content.find(target)
print("Index in brain.py:", idx)

# Find end of is_skin_query block (return ...)
idx_end = content.find('return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}', idx)
idx_end += len('return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}')

new_block = '''is_skin_query = any(w in lowered for w in ["skin", "skins", "cosmétique", "cosmetique", "tenue", "apparence", "outfit", "confection", "craft"]) and (any(k in lowered for k in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "apparence", "moist", "pouch", "bacchus", "longboy", "marie", "eva", "hugo", "otto", "gabriel", "serine"]) or "craft quel" in lowered)
        if is_skin_query:
            card_path = render_skin_card(clean_text, is_french)
            if any(w in lowered for w in ["moist", "pouch", "poche", "bacchus", "longboy"]):
                if is_french:
                    spoken = "Le Moist Pouch sert à confectionner le skin Épique Bacchus' Wand pour le pistolet Longboy. Fiche de fabrication transmise."
                    display = (
                        "🎨 **FICHE DE FABRICATION COSMÉTIQUE : BACCHUS' WAND (LONGBOY)**\n\n"
                        "• 🔫 **Objet Support :** Pistolet Longboy *(Nouveau modèle 3D / Meshswap)*\n"
                        "• 💎 **Rareté :** Épique *(Atelier d'Artisanat au Château)*\n"
                        "• 📜 **Déblocage :** Schéma requis au Château + 210 Pièces de Cuivre\n"
                        "• 🎒 **Rôle du Moist Pouch :** Ingrédient obligatoire (1x requis avec Gelée Royale, Tige Polie, Perle Blanche et Défense d'Ivoire).\n\n"
                        "*(Fiche visuelle officielle avec l'aperçu du skin et les icônes de chaque ingrédient jointe ci-dessous)*"
                    )
                else:
                    spoken = "Moist Pouch is required to craft the Epic skin Bacchus' Wand for the Longboy pistol. Crafting profile attached."
                    display = (
                        "🎨 **COSMETIC CRAFT PROFILE : BACCHUS' WAND (LONGBOY)**\n\n"
                        "• 🔫 **Target Weapon :** Longboy Pistol (Meshswap 3D model)\n"
                        "• 💎 **Rarity :** Epic (Artisan Workshop)\n"
                        "• 📜 **Unlock :** Schema required + 210 Copper fee\n"
                        "• 🎒 **Moist Pouch Role :** 1x Required Material (with Royal Jelly, Polished Rod, White Pearl, Ivory Tusk)."
                    )
            elif is_french:
                spoken = "Fiche cosmétique transmise avec les ingrédients exacts et conditions de fabrication au Château."
                display = "🎨 **FICHE DE CONFECTION COSMÉTIQUE & SKINS :**\n*(Aperçu du skin et ingrédients requis affichés ci-dessous)*"
            else:
                spoken = "Cosmetic skin card generated with exact materials and unlock requirements."
                display = "🎨 **COSMETIC SKIN UNLOCK PROFILE :**"
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}'''

content = content[:idx] + new_block + content[idx_end:]

with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated brain.py successfully!")
