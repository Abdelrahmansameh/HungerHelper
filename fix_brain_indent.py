with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    content = f.read()

# Let's replace the whole section between 1.1 SKINS & COSMETICS and 2. ITEM SELL PRICE
start_marker = "        # 1.1 SKINS & COSMETICS (Marie, Jean, Claude, Weapons)\n        # -------------------------------------------------------------------"
end_marker = "        # 2. ITEM SELL PRICE & VALUE CARD"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

assert idx_start != -1 and idx_end != -1, "Markers not found!"

clean_block = '''        # 1.1 SKINS & COSMETICS (Marie, Jean, Claude, Weapons)
        # -------------------------------------------------------------------
        is_skin_query = any(w in lowered for w in ["skin", "skins", "cosmétique", "cosmetique", "tenue", "apparence", "outfit", "confection", "craft"]) and (any(k in lowered for k in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "apparence", "moist", "pouch", "bacchus", "longboy", "marie", "eva", "hugo", "otto", "gabriel", "serine"]) or "craft quel" in lowered)
        if is_skin_query:
            card_path = render_skin_card(clean_text, is_french)
            if any(w in lowered for w in ["moist", "pouch", "poche", "bacchus", "longboy"]):
                if is_french:
                    spoken = "Le Moist Pouch sert à confectionner le skin Épique Bacchus' Wand pour le pistolet Longboy. Fiche de fabrication transmise."
                    display = (
                        "🎨 **FICHE DE FABRICATION COSMÉTIQUE : BACCHUS' WAND (LONGBOY)**\\n\\n"
                        "• 🔫 **Objet Support :** Pistolet Longboy *(Nouveau modèle 3D / Meshswap)*\\n"
                        "• 💎 **Rareté :** Épique *(Atelier d'Artisanat au Château)*\\n"
                        "• 📜 **Déblocage :** Schéma requis au Château + 210 Pièces de Cuivre\\n"
                        "• 🎒 **Rôle du Moist Pouch :** Ingrédient obligatoire (1x requis avec Gelée Royale, Tige Polie, Perle Blanche et Défense d'Ivoire).\\n\\n"
                        "*(Fiche visuelle officielle avec l'aperçu du skin et les icônes de chaque ingrédient jointe ci-dessous)*"
                    )
                else:
                    spoken = "Moist Pouch is required to craft the Epic skin Bacchus' Wand for the Longboy pistol. Crafting profile attached."
                    display = (
                        "🎨 **COSMETIC CRAFT PROFILE : BACCHUS' WAND (LONGBOY)**\\n\\n"
                        "• 🔫 **Target Weapon :** Longboy Pistol (Meshswap 3D model)\\n"
                        "• 💎 **Rarity :** Epic (Artisan Workshop)\\n"
                        "• 📜 **Unlock :** Schema required + 210 Copper fee\\n"
                        "• 🎒 **Moist Pouch Role :** 1x Required Material (with Royal Jelly, Polished Rod, White Pearl, Ivory Tusk)."
                    )
            elif is_french:
                spoken = "Fiche cosmétique transmise avec les ingrédients exacts et conditions de fabrication au Château."
                display = "🎨 **FICHE DE CONFECTION COSMÉTIQUE & SKINS :**\\n*(Aperçu du skin et ingrédients requis affichés ci-dessous)*"
            else:
                spoken = "Cosmetic skin card generated with exact materials and unlock requirements."
                display = "🎨 **COSMETIC SKIN UNLOCK PROFILE :**"
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
'''

content = content[:idx_start] + clean_block + content[idx_end:]

with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed indentation and string escapes in co_pilot/brain.py!")
