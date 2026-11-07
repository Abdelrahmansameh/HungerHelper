import re

p = "co_pilot/brain.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

text_n = text.replace("\r\n", "\n")

# 1. Update is_french logic: By default False, unless explicitly asked in French!
old_fr = """        french_indicators = [
            "où", "dois", "faire", "quête", "quete", "montre", "objectif", "prochain",
            "qui", "combien", "comment", "donne", "mets", "affiche", "le raid", "la map",
            "de", "du", "des", "pour", "bonjour", "salut", "merci", "aide", "charbon", "farine",
            "salpetre", "pont", "forêt", "ferme", "est ce", "est-ce", "arme", "dégât", "degat",
            "donjon", "clef", "clé", "garder", "ajoute", "coffre", "marchand", "vendeur",
            "tais", "toi", "chut", "silence", "sortie", "sorties", "extraire", "je",
            "oublie", "recommence", "annule", "laisse", "vaut", "prix", "tactical",
            "lance", "part", "démarre", "demarre", "terminé", "termine", "fini", "reste",
            "ou", "trouve", "trouver", "se trouve", "besoin", "garde", "garder", "mettre", "coups", "coup", "deux", "coute", "coûte", "personnage", "sort", "fiche", "profil", "capacité", "capacite", "ma", "mon", "mes", "vendre", "stash", "inventaire"
        ]
        is_french = any(w in lowered for w in french_indicators)"""

new_fr = """        # By default, English for all text responses and image cards!
        # French ONLY when explicitly asked for French!
        is_french = any(w in lowered for w in [
            "en français", "en francais", "in french", "traduis en français", "traduis en francais",
            "réponds en français", "reponds en francais", "parle français", "parle francais"
        ])"""

if old_fr in text_n:
    text_n = text_n.replace(old_fr, new_fr)
    print("1. is_french logic updated to English-by-default.")
else:
    print("Warning: old_fr not found")

# 2. Add Top-Priority Map & Navigation Router right after small talk / raid timer
map_router_block = """
        # -------------------------------------------------------------------
        # 0.45 MAP & TACTICAL NAVIGATION ROUTER (TOP PRIORITY!)
        # Handles: "map de jaque", "map jb", "montre moi sarlat", "map sf", "sombre", "jacques folly", "donjon"
        # -------------------------------------------------------------------
        is_map_context = any(w in lowered for w in [
            "map", "carte", "plan", "route", "raid", "ou est", "où est", "where is",
            "montre moi", "montre", "affiche", "show", "trouve", "donne la map", "donne carte"
        ]) or any(k in lowered for k in ["sarlat", "jaque", "jacques", "jb", "sombre"])

        is_dungeon = any(w in lowered for w in ["dungeon", "donjon", "folly", "pit", "puits", "entree", "entrée", "entrées", "entrances"])
        is_jb = any(w in lowered for w in ["jaque", "jaques", "jacques", "jb", "pont jacques", "jacques bridge"]) and not is_dungeon
        is_sf = any(w in lowered for w in ["sarlat", "sf", "ferme de sarlat", "sarlat farm", "moulin"])
        is_sombre = any(w in lowered for w in ["sombre", "forest", "foret", "forêt", "sombre forest"])

        if is_map_context or is_dungeon:
            if is_dungeon:
                from co_pilot.card_renderer import render_dungeon_card
                img_path = render_dungeon_card(is_french=is_french)
                if is_french:
                    spoken = "Fiche d'accès au donjon de Jacques Folly avec les 3 portes d'entrée transmise."
                    display = (
                        "🏰 **ACCÈS AU DONJON : JACQUES FOLLY (SOUS-SOL DU PONT)**\n\n"
                        "• 📍 **Localisation :** Galeries souterraines sous le Bastion du Pont Jacques.\n"
                        "• 🚪 **3 Portes d'Entrée Officielles :**\n"
                        "  1. **North Iron Gate** (Bastion Nord du pont — X: 1835.9, Y: 505.5)\n"
                        "  2. **Courtyard Crypt Door** (Cour intérieure du fort — X: 1605.2, Y: 512.7)\n"
                        "  3. **Undercroft Iron Door** (Sous les arches du pont — X: 1418.4, Y: 337.5)\n"
                        "• 🔑 **Clé requise :** Clé de Jacques Folly (5 spawns le long de la chaussée du pont).\n"
                        "• 📦 **Conteneurs :** 174 coffres et caches d'armes intérieures.\n\n"
                        "🖼️ *(Carte d'entrée épurée traçant précisément les 3 portes jointe ci-dessous)*"
                    )
                else:
                    spoken = "Jacques Folly subterranean dungeon access card with all 3 entrance gates dispatched."
                    display = (
                        "🏰 **DUNGEON ACCESS : JACQUES FOLLY (SUBTERRANEAN BASTION)**\n\n"
                        "• 📍 **Location :** Subterranean chambers beneath Jacques Bridge Fort.\n"
                        "• 🚪 **3 Official Entrance Gates :**\n"
                        "  1. **North Iron Gate** (Bridge North Bastion — X: 1835.9, Y: 505.5)\n"
                        "  2. **Courtyard Crypt Door** (Fort Courtyard Grave — X: 1605.2, Y: 512.7)\n"
                        "  3. **Undercroft Iron Door** (Bridge Arch Sub-Level — X: 1418.4, Y: 337.5)\n"
                        "• 🔑 **Required Key :** Jacques Folly Key (5 spawns along bridge roadway & desks).\n"
                        "• 📦 **Loot Capacity :** 174 reinforced containers & weapon caches.\n\n"
                        "🖼️ *(Clean tactical access card plotting all 3 entrance gates attached below)*"
                    )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}

            elif is_jb:
                p_map = os.path.join(ROOT_DIR, "Raid_Maps", "raid2_map.jpg")
                if not os.path.exists(p_map):
                    p_map = os.path.join(ROOT_DIR, "output_maps", "raid2_speedrun_briefing.jpg")
                if is_french:
                    spoken = "Carte tactique du Pont Jacques transmise sur Discord."
                    display = (
                        "🗺️ **CARTE TACTIQUE : JACQUES BRIDGE (RAID 2)**\n\n"
                        "• 📍 **Zone :** Pont fortifié, garnison en ruines et berges Est de la rivière.\n"
                        "• 🎯 **Points Clés :** Bastion Fortifié, Camp des Ruines Gavroche, Donjon Jacques Folly.\n"
                        "• 📦 **Meilleurs Conteneurs :** Bureaux d'officiers, caisses d'armes lourdes et coffres forts.\n\n"
                        "🖼️ *(Carte tactique haute résolution 2400x1400 jointe ci-dessous)*"
                    )
                else:
                    spoken = "Jacques Bridge tactical briefing map dispatched."
                    display = (
                        "🗺️ **TACTICAL MAP : JACQUES BRIDGE (RAID 2)**\n\n"
                        "• 📍 **Zone :** Fortified river crossing, garrison ruins & East riverbank.\n"
                        "• 🎯 **Key Objectives :** Bastion Fort, Gavroche Ruins Camp, Jacques Folly Subterranean.\n"
                        "• 📦 **High-Tier Loot :** Officer desks, reinforced gun chests & heavy strongboxes.\n\n"
                        "🖼️ *(Full 2400x1400 tactical speedrun briefing map attached below)*"
                    )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}

            elif is_sf:
                p_map = os.path.join(ROOT_DIR, "Raid_Maps", "raid1_map.jpg")
                if not os.path.exists(p_map):
                    p_map = os.path.join(ROOT_DIR, "output_maps", "raid1_speedrun_briefing.jpg")
                if is_french:
                    spoken = "Carte tactique de Sarlat Farm avec la route haute densité de farine transmise."
                    display = (
                        "🗺️ **CARTE TACTIQUE : SARLAT FARM (ROUTE HAUTE DENSITÉ DE FARINE)**\n\n"
                        "• 📍 **Zone :** Terres agricoles, Moulin de Sarlat et grenier central.\n"
                        "• 🌾 **Densité de Farine :** Forte concentration de sacs au Moulin et au Grenier Central (47.6% de drop).\n"
                        "• 🏃 **Quête Associée :** Making Dough (20x Farine pour Éloïse au Château).\n\n"
                        "🖼️ *(Carte tactique haute résolution 2400x1400 jointe ci-dessous)*"
                    )
                else:
                    spoken = "Sarlat Farm tactical map with high-density flour farming route dispatched."
                    display = (
                        "🗺️ **TACTICAL MAP : SARLAT FARM (HIGH-DENSITY FLOUR ROUTE)**\n\n"
                        "• 📍 **Zone :** Farmlands, Windmill & Central Granary Clusters.\n"
                        "• 🌾 **Flour Sack Density :** Maximum container density at Central Granary & Mill (47.6% drop rate).\n"
                        "• 🏃 **Target Quest :** Making Dough (20x Flour for Eloise at Chateau Hub).\n\n"
                        "🖼️ *(Full 2400x1400 tactical speedrun briefing map attached below)*"
                    )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}

            elif is_sombre:
                p_map = os.path.join(ROOT_DIR, "Raid_Maps", "raid7_map.jpg")
                if not os.path.exists(p_map):
                    p_map = os.path.join(ROOT_DIR, "output_maps", "raid7_speedrun_briefing.jpg")
                if is_french:
                    spoken = "Carte tactique de Sombre Forêt transmise."
                    display = (
                        "🗺️ **CARTE TACTIQUE : SOMBRE FOREST (RAID 7)**\n\n"
                        "• 📍 **Zone :** Forêt profonde, camps de bûcherons et cercles de pierres rituelles.\n"
                        "• 🌲 **Menaces :** Meutes de baveux et brutes rôdant dans la brume.\n\n"
                        "🖼️ *(Carte tactique haute résolution 2400x1400 jointe ci-dessous)*"
                    )
                else:
                    spoken = "Sombre Forest tactical briefing map dispatched."
                    display = (
                        "🗺️ **TACTICAL MAP : SOMBRE FOREST (RAID 7)**\n\n"
                        "• 📍 **Zone :** Deep wilderness, Lumberjack Camps & Ancient Monoliths.\n"
                        "• 🌲 **Threats :** Drooler packs and roaming Brutes in the foggy undergrowth.\n\n"
                        "🖼️ *(Full 2400x1400 tactical speedrun briefing map attached below)*"
                    )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}
"""

anchor = "        # 0.5 COMBAT TTK & HIT CALCULATOR"
if anchor in text_n:
    text_n = text_n.replace(anchor, map_router_block + "\n        # 0.5 COMBAT TTK & HIT CALCULATOR")
    print("2. Top-priority Map Router added.")
else:
    print("Warning: anchor not found")

with open(p, "w", encoding="utf-8") as f:
    f.write(text_n)

print("BRAIN_PY_UPDATED_WITH_ROUTER")
