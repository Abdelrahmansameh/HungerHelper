import os

brain_p = os.path.join("co_pilot", "brain.py")
with open(brain_p, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update character section & skin section
old_hero_skin_section = '''        # 1. CHARACTER & TACTICAL ABILITIES (All 6 Official Heroes: Eva, Gabriel, Hugo, Marie, Otto, Serine)
        # -------------------------------------------------------------------
        hero_names = ["serine", "serene", "gabriel", "hugo", "otto", "marie", "eva"]
        hero_keywords = ["tactical", "tactique", "capacité", "capacite", "ability", "personnage", "survivor", "hero", "héros", "classe", "sort", "pouvoir", "competence", "compétence", "profil", "fiche"]
        
        matched_hero = None
        for h in hero_names:
            if h in lowered:
                matched_hero = "serine" if h == "serene" else h
                break

        if matched_hero and any(w in lowered for w in hero_keywords):
            card_path = render_character_card(matched_hero)
            
            hero_spoken_fr = {
                "eva": "Eva est la chasseresse vagabonde : Marathon réduit la perte d'endurance, Lightfoot élimine les bruits de pas et Blind aveugle l'ennemi. Fiche visuelle transmise.",
                "gabriel": "Gabriel est le soldat de fortune : Charge renforce les coups en sprint, Line Infantry fortifie la défense et Sadist redonne de la vigueur. Fiche visuelle transmise.",
                "hugo": "Hugo est le berserker maniaque : Taste of Blood accélère les frappes sur cible saignante, Zealot booste les dégâts et Maniac résiste aux stuns. Fiche transmise.",
                "marie": "Marie est la nonne guerrière : Gentle Touch accélère les soins de 50%, Vespers dissipe le poison et Mending Prayer restaure 45 PV. Fiche transmise.",
                "otto": "Otto est le sapeur d'élite : Maintenance préserve la durabilité d'armure, Field Repairs répare les plaques et Masterwork renforce l'armure. Fiche transmise.",
                "serine": "Serine est l'empoisonneuse vaudou : Vodou Spirit confère 30% d'immunité poison, Rush est une ruée corrosive et Vodou Bomb inflige des dégâts de zone toxiques. Fiche transmise."
            }
            hero_spoken_en = {
                "eva": "Eva is the Vagabond Huntress: Marathon reduces stamina drain, Lightfoot silences footsteps, and Blind disorients enemies. Visual card dispatched.",
                "gabriel": "Gabriel is the Soldier of Fortune: Charge buffs sprint attacks, Line Infantry boosts defense, and Sadist restores vigor. Visual card dispatched.",
                "hugo": "Hugo is the Maniac: Taste of Blood speeds attacks against bleeding foes, Zealot boosts damage, and Maniac provides stun resistance. Visual card dispatched.",
                "marie": "Marie is the Warrior Nun: Gentle Touch speeds healing by 50%, Vespers clears poison, and Mending Prayer heals 45 HP. Visual card dispatched.",
                "otto": "Otto is the Sergeant-at-Arms: Maintenance preserves armor durability, Field Repairs mends armor plates, and Masterwork fortifies defenses. Visual card dispatched.",
                "serine": "Serine is the Vodou Poisoner: Vodou Spirit grants poison resistance, Rush is a corrosive dash, and Vodou Bomb deals area toxic damage. Visual card dispatched."
            }
            
            if is_french:
                spoken = hero_spoken_fr.get(matched_hero, f"Voici la fiche tactique officielle pour {matched_hero.title()}. Fiche visuelle transmise.")
                display = f"⚔️ **PROFIL OFFICIEL DU HÉROS : {matched_hero.upper()} (HUNGER COMPANION)**\\n*(Fiche de personnage complète et compétences générées ci-dessous)*"
            else:
                spoken = hero_spoken_en.get(matched_hero, f"Here is the official tactical profile for {matched_hero.title()}. Visual card dispatched.")
                display = f"⚔️ **OFFICIAL HERO PROFILE : {matched_hero.upper()} (HUNGER COMPANION)**\\n*(Full combat sheet and abilities attached below)*"
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 1.1 SKINS & COSMETICS (Marie, Jean, Claude, Weapons)
        # -------------------------------------------------------------------
        is_skin_query = any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "apparence", "outfit", "confection", "craft"]) and (any(k in lowered for k in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "apparence", "moist", "pouch", "bacchus", "longboy", "marie", "eva", "hugo", "otto", "gabriel", "serine", "spear", "lance"]) or "craft quel" in lowered)
        if is_skin_query:
            if any(w in lowered for w in ["spear", "lance"]):
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
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}'''

new_hero_skin_section = '''        # -------------------------------------------------------------------
        # 1. CHARACTER & TACTICAL ABILITIES (All 6 Official Heroes: Eva, Gabriel, Hugo, Marie, Otto, Serine)
        # -------------------------------------------------------------------
        hero_names = ["serine", "serene", "gabriel", "hugo", "otto", "marie", "eva"]
        hero_keywords = [
            "tactical", "tactique", "capacité", "capacite", "capacités", "capacites",
            "ability", "abilities", "skill", "skills", "personnage", "survivor", "hero",
            "héros", "heros", "classe", "sort", "sorts", "pouvoir", "pouvoirs", "competence",
            "compétence", "compétences", "profil", "profile", "fiche", "kit", "stats", "stat"
        ]
        
        matched_hero = None
        for h in hero_names:
            if h in lowered:
                matched_hero = "serine" if h == "serene" else h
                break

        if matched_hero and (any(w in lowered for w in hero_keywords) or len(clean_text.split()) <= 4):
            from universal_v7_engine import render_clean_character_card
            card_path = render_clean_character_card(matched_hero, is_french=is_french)
            
            hero_spoken_en = {
                "eva": "Eva is the Vagabond Huntress: Marathon reduces sprint drain, Lightfoot silences footsteps, and Blind disorients enemies.",
                "gabriel": "Gabriel is the Soldier of Fortune: Charge buffs sprint attacks, Line Infantry fortifies defense, and Sadist restores vigor.",
                "hugo": "Hugo is the Maniac: Taste of Blood speeds attacks against bleeding foes, Zealot boosts damage, and Maniac provides stun immunity.",
                "marie": "Marie is the Warrior Nun: Alchemical Pouch carries extra meds, Healing Salve heals 75 HP, and Acid Flask corrodes enemy armor.",
                "otto": "Otto is the Sergeant-at-Arms: Maintenance preserves armor durability, Field Repairs mends armor plates, and Masterwork fortifies defense.",
                "serine": "Serine is the Vodou Poisoner: Vodou Spirit grants poison immunity, Rush is a corrosive dash, and Vodou Bomb deals toxic area damage."
            }
            
            spoken = hero_spoken_en.get(matched_hero, f"Tactical profile for {matched_hero.title()} dispatched.")
            display = f"⚔️ **OFFICIAL HERO PROFILE : {matched_hero.upper()} (HUNGER COMPANION)**\\n*(Full abilities kit & unlocked prestige skins attached below)*"
            if is_french:
                spoken = f"Fiche tactique officielle pour {matched_hero.title()} transmise."
                display = f"⚔️ **PROFIL OFFICIEL DU HÉROS : {matched_hero.upper()}**\\n*(Kit de compétences et skins de haut niveau ci-dessous)*"
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 1.1 SKINS & COSMETICS (UNIVERSAL FOR ALL WEAPONS & CHARACTERS)
        # -------------------------------------------------------------------
        is_skin_query = any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "apparence", "outfit", "confection", "craft"]) or "craft quel" in lowered
        if is_skin_query:
            from universal_v7_engine import render_skins_for_target
            skin_res = render_skins_for_target(clean_text)
            
            if skin_res["has_skins"]:
                spoken = f"Cosmetic skins for {clean_text} dispatched."
                display = f"🎨 **{skin_res['title']}**\\n\\n{skin_res['text']}\\n\\n*(Visual crafting cards attached below)*"
                cards = skin_res["cards"]
                return {
                    "spoken_text": spoken,
                    "display_text": display,
                    "image_attachments": cards,
                    "image_attachment": cards[0] if cards else None
                }
            else:
                # Direct, clear message when weapon has no skins (e.g. Rapier, Shortsword)
                spoken = f"No craftable skins currently exist for this weapon in Hunger."
                display = f"🎨 **{skin_res['title']}**\\n\\n{skin_res['text']}"
                return {
                    "spoken_text": spoken,
                    "display_text": display,
                    "image_attachments": [],
                    "image_attachment": None
                }'''

text = text.replace(old_hero_skin_section.replace('\n', '\r\n'), new_hero_skin_section.replace('\n', '\r\n'))
text = text.replace(old_hero_skin_section, new_hero_skin_section)

# 2. Update Map Router to use universal clean maps without sidebars
old_map_section = '''        if is_map_context or is_dungeon:
            if is_dungeon:
                from co_pilot.card_renderer import render_dungeon_card
                img_path = render_dungeon_card(is_french=is_french)
                if is_french:
                    spoken = "Fiche d'accès au donjon de Jacques Folly avec les 3 portes d'entrée transmise."
                    display = (
                        "🏰 **ACCÈS AU DONJON : JACQUES FOLLY (SOUS-SOL DU PONT)**\\n\\n"
                        "• 📍 **Localisation :** Galeries souterraines sous le Bastion du Pont Jacques.\\n"
                        "• 🚪 **3 Portes d'Entrée Officielles :**\\n"
                        "  1. **North Iron Gate** (Bastion Nord du pont — X: 1835.9, Y: 505.5)\\n"
                        "  2. **Courtyard Crypt Door** (Cour intérieure du fort — X: 1605.2, Y: 512.7)\\n"
                        "  3. **Undercroft Iron Door** (Sous les arches du pont — X: 1418.4, Y: 337.5)\\n"
                        "• 🔑 **Clé requise :** Clé de Jacques Folly (5 spawns le long de la chaussée du pont).\\n"
                        "• 📦 **Conteneurs :** 174 coffres et caches d'armes intérieures.\\n\\n"
                        "🖼️ *(Carte d'entrée épurée traçant précisément les 3 portes jointe ci-dessous)*"
                    )
                else:
                    spoken = "Jacques Folly subterranean dungeon access card with all 3 entrance gates dispatched."
                    display = (
                        "🏰 **DUNGEON ACCESS : JACQUES FOLLY (SUBTERRANEAN BASTION)**\\n\\n"
                        "• 📍 **Location :** Subterranean chambers beneath Jacques Bridge Fort.\\n"
                        "• 🚪 **3 Official Entrance Gates :**\\n"
                        "  1. **North Iron Gate** (Bridge North Bastion — X: 1835.9, Y: 505.5)\\n"
                        "  2. **Courtyard Crypt Door** (Fort Courtyard Grave — X: 1605.2, Y: 512.7)\\n"
                        "  3. **Undercroft Iron Door** (Bridge Arch Sub-Level — X: 1418.4, Y: 337.5)\\n"
                        "• 🔑 **Required Key :** Jacques Folly Key (5 spawns along bridge roadway & desks).\\n"
                        "• 📦 **Loot Capacity :** 174 reinforced containers & weapon caches.\\n\\n"
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
                        "🗺️ **CARTE TACTIQUE : JACQUES BRIDGE (RAID 2)**\\n\\n"
                        "• 📍 **Zone :** Pont fortifié, garnison en ruines et berges Est de la rivière.\\n"
                        "• 🎯 **Points Clés :** Bastion Fortifié, Camp des Ruines Gavroche, Donjon Jacques Folly.\\n"
                        "• 📦 **Meilleurs Conteneurs :** Bureaux d'officiers, caisses d'armes lourdes et coffres forts.\\n\\n"
                        "🖼️ *(Carte tactique haute résolution 2400x1400 jointe ci-dessous)*"
                    )
                else:
                    spoken = "Jacques Bridge tactical briefing map dispatched."
                    display = (
                        "🗺️ **TACTICAL MAP : JACQUES BRIDGE (RAID 2)**\\n\\n"
                        "• 📍 **Zone :** Fortified river crossing, garrison ruins & East riverbank.\\n"
                        "• 🎯 **Key Objectives :** Bastion Fort, Gavroche Ruins Camp, Jacques Folly Subterranean.\\n"
                        "• 📦 **High-Tier Loot :** Officer desks, reinforced gun chests & heavy strongboxes.\\n\\n"
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
                        "🗺️ **CARTE TACTIQUE : SARLAT FARM (ROUTE HAUTE DENSITÉ DE FARINE)**\\n\\n"
                        "• 📍 **Zone :** Terres agricoles, Moulin de Sarlat et grenier central.\\n"
                        "• 🌾 **Densité de Farine :** Forte concentration de sacs au Moulin et au Grenier Central (47.6% de drop).\\n"
                        "• 🏃 **Quête Associée :** Making Dough (20x Farine pour Éloïse au Château).\\n\\n"
                        "🖼️ *(Carte tactique haute résolution 2400x1400 jointe ci-dessous)*"
                    )
                else:
                    spoken = "Sarlat Farm tactical map with high-density flour farming route dispatched."
                    display = (
                        "🗺️ **TACTICAL MAP : SARLAT FARM (HIGH-DENSITY FLOUR ROUTE)**\\n\\n"
                        "• 📍 **Zone :** Farmlands, Windmill & Central Granary Clusters.\\n"
                        "• 🌾 **Flour Sack Density :** Maximum container density at Central Granary & Mill (47.6% drop rate).\\n"
                        "• 🏃 **Target Quest :** Making Dough (20x Flour for Eloise at Chateau Hub).\\n\\n"
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
                        "🗺️ **CARTE TACTIQUE : SOMBRE FOREST (RAID 7)**\\n\\n"
                        "• 📍 **Zone :** Forêt profonde, camps de bûcherons et cercles de pierres rituelles.\\n"
                        "• 🌲 **Menaces :** Meutes de baveux et brutes rôdant dans la brume.\\n\\n"
                        "🖼️ *(Carte tactique haute résolution 2400x1400 jointe ci-dessous)*"
                    )
                else:
                    spoken = "Sombre Forest tactical briefing map dispatched."
                    display = (
                        "🗺️ **TACTICAL MAP : SOMBRE FOREST (RAID 7)**\\n\\n"
                        "• 📍 **Zone :** Deep wilderness, Lumberjack Camps & Ancient Monoliths.\\n"
                        "• 🌲 **Threats :** Drooler packs and roaming Brutes in the foggy undergrowth.\\n\\n"
                        "🖼️ *(Full 2400x1400 tactical speedrun briefing map attached below)*"
                    )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}'''

new_map_section = '''        if is_map_context or is_dungeon:
            from universal_v7_engine import get_clean_raid_map, render_authentic_dungeon_card
            if is_dungeon:
                img_path = render_authentic_dungeon_card(is_french=is_french)
                spoken = "Jacques Folly subterranean dungeon map dispatched with authentic entrance coordinates."
                display = (
                    "🏰 **DUNGEON ACCESS : JACQUES FOLLY (AUTHENTIC NORTHERN RIDGE SITES)**\\n\\n"
                    "• 📍 **Authentic Location :** Northwest of Vairon Quarry on northern wooded ridge.\\n"
                    "• 🚪 **Official Entrance Coordinates (Jacques Bridge - Raid 2) :**\\n"
                    "  1. **Jacques Folly Main Dungeon Entrance** (X: 1680.4, Y: 197.1)\\n"
                    "  2. **The Last Prisoner Crypt** (X: 1530.5, Y: 315.4)\\n"
                    "• 🔑 **Required Key :** Jacques Folly Key (3 Uses)\\n"
                    "• 📦 **Loot Capacity :** 174 reinforced subterranean containers.\\n\\n"
                    "🖼️ *(Authentic clean map inset attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": img_path}

            elif is_jb:
                p_map = get_clean_raid_map(2)
                spoken = "Jacques Bridge clean tactical map dispatched."
                display = (
                    "🗺️ **TACTICAL MAP : JACQUES BRIDGE (RAID 2 - CLEAN MAP)**\\n\\n"
                    "• 📍 **Zone :** Fortified bridge, garrison ruins & East riverbank.\\n"
                    "• 🎯 **Key Sites :** Bastion Crossing, Gavroche Ruins, Jacques Folly Ridge.\\n\\n"
                    "🖼️ *(Clean high-resolution map without sidebars attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}

            elif is_sf:
                p_map = get_clean_raid_map(1)
                spoken = "Sarlat Farm clean tactical map dispatched."
                display = (
                    "🗺️ **TACTICAL MAP : SARLAT FARM (RAID 1 - CLEAN MAP)**\\n\\n"
                    "• 📍 **Zone :** Farmlands, Windmill & Central Granary Clusters.\\n"
                    "• 🌾 **High-Density Flour Route :** Maximum sack clusters at Mill & Granary.\\n\\n"
                    "🖼️ *(Clean high-resolution map without sidebars attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}

            elif is_sombre:
                p_map = get_clean_raid_map(7)
                spoken = "Sombre Forest clean tactical map dispatched."
                display = (
                    "🗺️ **TACTICAL MAP : SOMBRE FOREST (RAID 7 - CLEAN MAP)**\\n\\n"
                    "• 📍 **Zone :** Deep wilderness, Lumberjack Camps & Ancient Monoliths.\\n"
                    "• 🌲 **Threats :** Drooler packs & roaming Brutes.\\n\\n"
                    "🖼️ *(Clean high-resolution map without sidebars attached below)*"
                )
                return {"spoken_text": spoken, "display_text": display, "image_attachment": p_map}'''

text = text.replace(old_map_section.replace('\n', '\r\n'), new_map_section.replace('\n', '\r\n'))
text = text.replace(old_map_section, new_map_section)

# 3. Update Stash section
old_stash_section = '''        # 1.2 STASH & INVENTORY ANALYSIS (TWO IMAGES: Highlighted Grid + Sell Manifest)
        # -------------------------------------------------------------------
        is_stash_query = any(w in lowered for w in ["stash", "réserve", "reserve", "mon coffre", "inventaire"]) and any(w in lowered for w in ["analyse", "vendre", "rapport", "combien", "valeur", "trier", "estimer", "garder"])
        if is_stash_query:
            from generate_perfect_v6 import render_perfect_stash_analysis
            p1, p2 = render_perfect_stash_analysis()
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
            return {"spoken_text": spoken, "display_text": display, "image_attachments": [p1, p2], "image_attachment": p1}'''

new_stash_section = '''        # 1.2 STASH & INVENTORY ANALYSIS (TWO IMAGES: Highlighted Grid + Sell Manifest)
        # -------------------------------------------------------------------
        is_stash_query = any(w in lowered for w in ["stash", "réserve", "reserve", "mon coffre", "inventaire"]) and any(w in lowered for w in ["analyse", "vendre", "rapport", "combien", "valeur", "trier", "estimer", "garder"])
        if is_stash_query:
            from universal_v7_engine import render_universal_stash_analysis
            p1, p2 = render_universal_stash_analysis(is_french=is_french)
            spoken = "Stash analysis complete: letters and sealed documents are strictly preserved for late-game character EXP. Two visual appraisal cards dispatched."
            display = (
                "📦 **STASH & INVENTORY TACTICAL APPRAISAL**\\n\\n"
                "• 🔒 **STRICT EXP RULE :** All letters, sealed documents, and books are **PRESERVED** for major late-game XP progression!\\n"
                "• 🛡️ **Gear Preserved :** All meds, armors, bags, ammo, and tools kept.\\n"
                "• 🛒 **Recommended to Sell :** Superfluous curios, church ornaments, duplicate orphan keys.\\n"
                "• 💰 **Estimated Net Proceeds :** `2 Silver 5 Copper`\\n\\n"
                "*(Two visual cards attached: 1. Modified screenshot with sell items highlighted in gold | 2. Clean liquidation manifest)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachments": [p1, p2], "image_attachment": p1}'''

text = text.replace(old_stash_section.replace('\n', '\r\n'), new_stash_section.replace('\n', '\r\n'))
text = text.replace(old_stash_section, new_stash_section)

# 4. Stopwords filter in candidate loop
old_cand_filter = '''            # 3. Check items (factual data)
            if len(cand) >= 3 and cand not in ["les", "des", "une", "pour"]:'''

new_cand_filter = '''            # 3. Check items (factual data)
            STOPWORDS = {
                "moi", "toi", "lui", "eux", "mon", "ton", "son", "mes", "tes", "ses",
                "les", "des", "une", "pour", "par", "qui", "que", "quoi", "est", "sont",
                "avec", "sans", "dans", "sur", "sous", "vers", "chez", "tout", "tous",
                "toute", "toutes", "quel", "quels", "quelle", "quelles", "combien",
                "montre", "montrer", "affiche", "afficher", "donne", "donner", "voir",
                "skills", "skill", "sort", "sorts", "classe", "classes", "hero", "heros",
                "héros", "perso", "persos", "personnage", "personnages", "carte", "cartes",
                "map", "maps", "skin", "skins", "arbre", "arbres", "build", "builds",
                "stats", "stat", "loot", "item", "items", "objet", "objets", "truc", "trucs",
                "the", "and", "for", "with", "from", "show", "tell", "what", "how", "give"
            }
            if len(cand) >= 3 and cand.lower() not in STOPWORDS:'''

text = text.replace(old_cand_filter.replace('\n', '\r\n'), new_cand_filter.replace('\n', '\r\n'))
text = text.replace(old_cand_filter, new_cand_filter)

with open(brain_p, "w", encoding="utf-8") as f:
    f.write(text)

print("Applied Universal V7 Engine to brain.py successfully!")
