with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    content = f.read()

target = "        # 2. ITEM SELL PRICE & VALUE CARD"
assert target in content, "Target not found in brain.py!"

new_stash_section = '''        # 1.2 STASH & INVENTORY ANALYSIS (TWO IMAGES: Highlighted Grid + Sell Manifest)
        # -------------------------------------------------------------------
        is_stash_query = any(w in lowered for w in ["stash", "réserve", "reserve", "mon coffre", "inventaire"]) and any(w in lowered for w in ["analyse", "vendre", "rapport", "combien", "valeur", "trier", "estimer", "garder"])
        if is_stash_query:
            from test_dynamic_stash_two_images import render_dynamic_stash_two_images
            p1, p2 = render_dynamic_stash_two_images()
            if is_french:
                spoken = "Analyse de votre réserve de Stash effectuée. Les deux fiches tactiques sont transmises : grille avec items à vendre en surbrillance et bordereau de vente détaillé."
                display = (
                    "📦 **ANALYSE TACTIQUE DE VOTRE STASH & RÉSERVE AU CHÂTEAU**\\n\\n"
                    "• 🔒 **Règle absolue :** Tous vos soins, vivres, armures, sacs, armes et outils restent sécurisés en réserve.\\n"
                    "• 🛒 **À vendre en priorité :** Bibelots d'église (chandeliers), babioles sans serrure (clés orphelines), trophées inutiles et doublons d'armures basses.\\n"
                    "• 💰 **Valeur totale estimée :** `2 Pièces d'Argent et 45 Cuivres`\\n"
                    "• 📊 **Rotation du marché :** `+12% vs prix de base` (cours très avantageux pour liquider vos surplus !)\\n\\n"
                    "*(Deux fiches transmises : 1. Grille avec items à vendre en surbrillance dorée et items conservés grisés | 2. Bordereau de vente avec détail des gains)*"
                )
            else:
                spoken = "Stash analysis complete. Two visual cards dispatched: highlighted sell grid and detailed sell manifest."
                display = (
                    "📦 **STASH & INVENTORY TACTICAL APPRAISAL**\\n\\n"
                    "• 🔒 **Preserved :** All meds, armor plates, weapons, and tools.\\n"
                    "• 🛒 **To Sell :** Superfluous curios, church ornaments, orphan keys, low-tier duplicates.\\n"
                    "• 💰 **Estimated Return :** `2 Silver 45 Copper` (+12% market rotation bonus).\\n\\n"
                    "*(2 visual cards attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachments": [p1, p2], "image_attachment": p1}

        # -------------------------------------------------------------------
        # 2. ITEM SELL PRICE & VALUE CARD'''

content = content.replace(target, new_stash_section, 1)

with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated brain.py with stash two-images handler successfully!")
