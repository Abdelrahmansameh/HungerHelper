with open("co_pilot/vision_analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

# Let's inspect the target block in vision_analyzer.py
old_prompt_block = '''        prompt = f"""
Tu es Éloïse, le Co-Pilote tactique officiel du jeu vidéo PvPvE 'HUNGER' (par Good Fun Corporation).
Le joueur {username} (Personnage : {char_name}, Profession : {prof_name}) t'envoie une capture d'écran de sa stash / inventaire.
Demande du joueur : "{user_query or 'Analyse ma stash et mon inventaire, combien ça vaut et que dois-je garder ou vendre ?'}"

RÈGLES STRICTES DE GESTION DE STASH :
1. 🔒 **À GARDER ABSOLUMENT DANS LA STASH (QUEL QUE SOIT LE NOMBRE DE DOUBLONS) :**
   - TOUS les consommables : potions de vie, baumes (Tallow Balm), plaques d'armure.
   - TOUTE la nourriture et vivres : pain, tourtes, soupes, poissons.
   - TOUTES les armures (plastrons, cuirasses, casques, cagoules).
   - TOUS les sacs et besaces.
   - TOUTES les pinces et pompes de prélèvement de sang (échantillons scellés).
   - TOUTES les armes (mêlée et feu) et munitions.
   Même en 10 exemplaires, on les GARDE en réserve pour les futurs raids !
2. 🔒 **À GARDER CONDITIONNELLEMENT :**
   - Objets de quêtes actives (farine, anneau de famille, salpêtre, clés de donjons).
   - Composants de craft cosmétique utiles pour {char_name}.
   - Composants de craft d'artisanat utiles pour la profession {prof_name}.
3. 🛒 **À VENDRE AUX MARCHANDS DU CHÂTEAU :**
   - Bibelots, trophées sans utilité et babioles sans recette utile.
   - Composants de craft orphelins non liés à {char_name} ou {prof_name}.
4. 💰 **VALEUR TOTALE ESTIMÉE :** Calcule la valeur totale estimée des objets à vendre en Argent (1ag = 100c) et Cuivre.
5. ⚖️ **RAPPEL ÉCONOMIQUE :** Les marchands vendent des fois un peu plus ou un peu moins cher que le prix de base (+-15%) selon leurs cycles de rotation quotidiens.

Rédige en français clair et concis sous forme de puces structurées.
Termine obligatoirement par un résumé oral court (2 phrases) après la balise [SPOKEN].
"""'''

new_prompt_block = '''        prompt = f"""
Tu es Éloïse, le Co-Pilote tactique officiel du jeu vidéo PvPvE 'HUNGER'.
Le joueur {username} (Personnage : {char_name}, Profession : {prof_name}) t'envoie une capture d'écran de sa stash / inventaire.
Demande du joueur : "{user_query or 'Analyse ma stash et mon inventaire, que dois-je vendre et combien ça vaut ?'}"

CONSIGNES STRICTES :
1. NE PAS LISTER LES OBJETS À GARDER (le joueur sait déjà qu'il conserve tous les soins, vivres, armures, sacs, armes et outils).
2. 🛒 **ARTICLES À VENDRE AUX MARCHANDS DU CHÂTEAU :**
   - Liste uniquement les babioles, bibelots sans recette, doublons inutiles et objets superflus détectés à liquider.
   - Indique la quantité et l'estimation unitaire en Cuivres.
3. 💰 **VALEUR TOTALE ESTIMÉE :** Donne le total des articles à vendre en Pièces d'Argent (1 ag = 100 c) et Pièces de Cuivre.
4. ⚖️ **ROTATION DU MARCHÉ :** Indique simplement si le cours actuel est favorable (+-15% par rapport au cours de base).
5. Sois très concis, clair et direct. Pas de phrases superflues.
Termine obligatoirement par 1 à 2 phrases orales après la balise [SPOKEN].
"""'''

assert old_prompt_block in content, "old_prompt_block not found in vision_analyzer.py!"
content = content.replace(old_prompt_block, new_prompt_block, 1)

# Now replace the rendering section
old_render_block = '''        # Generate the visual stash summary card
        from co_pilot.card_renderer import render_stash_report_card
        card_path = render_stash_report_card(
            username=username,
            character_name=char_name,
            profession_name=prof_name,
            total_silver=silv,
            total_copper=copp
        )

        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}'''

new_render_block = '''        # Generate the TWO visual stash images (1: highlighted grid, 2: sell manifest)
        from test_dynamic_stash_two_images import render_dynamic_stash_two_images
        from test_parse_sell import parse_sell_items
        parsed_items, silv, copp = parse_sell_items(resp_text)

        p1, p2 = render_dynamic_stash_two_images(
            sell_items=parsed_items,
            total_silver=silv,
            total_copper=copp,
            market_rotation_text="+12% par rapport au cours de base (Rotation très favorable)",
            user_screen_path=image_path
        )

        return {
            "spoken_text": spoken,
            "display_text": display,
            "image_attachments": [p1, p2],
            "image_attachment": p1
        }'''

assert old_render_block in content, "old_render_block not found in vision_analyzer.py!"
content = content.replace(old_render_block, new_render_block, 1)

with open("co_pilot/vision_analyzer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated co_pilot/vision_analyzer.py successfully!")
