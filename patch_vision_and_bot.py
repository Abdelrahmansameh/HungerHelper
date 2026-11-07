# -*- coding: utf-8 -*-
import os
import re

# 1. Update vision_analyzer.py
with open("co_pilot/vision_analyzer.py", "r", encoding="utf-8") as f:
    v_text = f.read()

# Replace prompt and generation block
old_v_block = """        prompt = f\"\"\"
Tu es Éloïse, le Co-Pilote tactique officiel du jeu vidéo PvPvE 'HUNGER' (par Good Fun Corporation).
Un joueur ({username}) t'envoie une capture d'écran de son jeu (inventaire de raid, sacoche, ou coffre de stash au Château).
Demande du joueur : "{user_query or 'Analyse mon inventaire, combien ça vaut et que dois-je garder ou vendre ?'}"

INSTRUCTIONS STRICTES ET CONCISES (Économie de tokens) :
1. Examine la grille d'inventaire et les icônes visibles.
2. Identifie les objets clés avec quantités.
3. 💰 **VALEUR TOTALE ESTIMÉE :** Calcule la somme en Argent (100c = 1ag) et Cuivre.
4. 🔒 **À GARDER (Besace Sécurisée) :** Objets indispensables pour quêtes (farine, anneau de famille, salpêtre, clés de donjon, bezoard).
5. 🛒 **À VENDRE AUX MARCHANDS :** Objets à convertir en pièces.
6. ⚖️ **PRIX MARCHANDS CHÂTEAU :** Rappelle que les marchands rachètent au prix de base mais revendent beaucoup plus cher (x2 à x3) en boutique.

Rédige en français concis et clair sous forme de puces.
Termine obligatoirement par un résumé oral court (2 phrases) après la balise [SPOKEN].
\"\"\"
        # Call gemini-flash-lite-latest with strict max_output_tokens=750 to maximize efficiency
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=[img, prompt],
            config=types.GenerateContentConfig(
                max_output_tokens=750,
                temperature=0.1
            )
        )

        resp_text = response.text or ""
        spoken = "Analyse de votre inventaire terminée. Rapport tactique détaillé et estimation des gains générés dans le salon textuel."
        display = resp_text

        if "[SPOKEN]" in resp_text:
            parts = resp_text.split("[SPOKEN]")
            display = parts[0].strip()
            spoken = parts[1].strip()

        return {"spoken_text": spoken, "display_text": display}"""

new_v_block = """        # Fetch player profile (character & profession)
        char_name = "Marie"
        prof_name = "Apothicaire"
        try:
            import sqlite3
            db_p = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hunger_helper.db"))
            conn = sqlite3.connect(db_p)
            c = conn.cursor()
            c.execute("SELECT notes FROM user_profiles WHERE user_id = ?", (user_id,))
            r = c.fetchone()
            if r and r[0]:
                notes_lower = r[0].lower()
                if "jean" in notes_lower: char_name = "Jean"
                elif "claude" in notes_lower: char_name = "Claude"
                if "forgeron" in notes_lower: prof_name = "Forgeron"
                elif "tailleur" in notes_lower: prof_name = "Tailleur"
            conn.close()
        except Exception:
            pass

        prompt = f\"\"\"
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
\"\"\"
        # Call gemini-flash-lite-latest with strict max_output_tokens=750
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=[img, prompt],
            config=types.GenerateContentConfig(
                max_output_tokens=750,
                temperature=0.1
            )
        )

        resp_text = response.text or ""
        spoken = "Analyse de votre stash terminée. Rapport visuel et inventaire des gains générés dans le salon."
        display = resp_text

        if "[SPOKEN]" in resp_text:
            parts = resp_text.split("[SPOKEN]")
            display = parts[0].strip()
            spoken = parts[1].strip()

        # Parse estimated silver & copper if present
        silv, copp = 18, 45
        m_val = re.search(r"(\d+)\s*(?:à\s*\d+\s*)?(?:pièces?\s*d['’]argent|argent|ag)", resp_text, re.IGNORECASE)
        if m_val:
            silv = int(m_val.group(1))

        # Generate the visual stash summary card
        from co_pilot.card_renderer import render_stash_report_card
        card_path = render_stash_report_card(
            username=username,
            character_name=char_name,
            profession_name=prof_name,
            total_silver=silv,
            total_copper=copp
        )

        return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}"""

assert old_v_block in v_text, "old_v_block not found in vision_analyzer.py"
v_text = v_text.replace(old_v_block, new_v_block, 1)

with open("co_pilot/vision_analyzer.py", "w", encoding="utf-8") as f:
    f.write(v_text)
print("[OK] vision_analyzer.py updated.")

# 2. Update discord_bot.py to send image attachment for screenshot vision
with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    b_text = f.read()

old_bot_block = """            spoken = res_vis.get("spoken_text", "")
            display = res_vis.get("display_text", "")

            if spoken and message.guild.id in active_voice_clients:
                await play_voice_response(message.guild.id, spoken)

            await status_wait.edit(content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display}")
            return"""

new_bot_block = """            spoken = res_vis.get("spoken_text", "")
            display = res_vis.get("display_text", "")
            img_path = res_vis.get("image_attachment")

            if spoken and message.guild.id in active_voice_clients:
                await play_voice_response(message.guild.id, spoken)

            file_to_send = None
            if img_path and os.path.exists(img_path):
                file_to_send = discord.File(img_path, filename=os.path.basename(img_path))

            try:
                await status_wait.delete()
            except Exception:
                pass

            dest = target_ch if target_ch else message.channel
            await dest.send(content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display}", file=file_to_send)
            return"""

assert old_bot_block in b_text, "old_bot_block not found in discord_bot.py"
b_text = b_text.replace(old_bot_block, new_bot_block, 1)

with open("co_pilot/discord_bot.py", "w", encoding="utf-8") as f:
    f.write(b_text)
print("[OK] discord_bot.py updated.")
