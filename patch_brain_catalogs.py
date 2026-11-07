import os
import re

BRAIN_PATH = "co_pilot/brain.py"

with open(BRAIN_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update pending_term check to dismiss if new question is asked
old_pending = '''        # If user was explaining a term after Eloise asked (within 25s window):
        if self.pending_term and (time.time() - self.pending_term_time < 25.0):'''

new_pending = '''        # If user starts a new question, clear pending term immediately
        is_new_question = any(clean_text.lower().startswith(w) for w in [
            "c'est quoi", "c quoi", "qu'est ce que", "quest ce que", "ou ", "ou est", "combien",
            "montre", "quel", "quelle", "quels", "quelles", "carte", "stats", "degat", "degats",
            "who", "where", "what", "how", "show", "give", "tell"
        ])
        if is_new_question:
            self.pending_term = None
            self.pending_confirmation = None

        # If user was explaining a term after Eloise asked (within 25s window):
        if self.pending_term and (time.time() - self.pending_term_time < 25.0):'''

if old_pending in code:
    code = code.replace(old_pending, new_pending, 1)
    print("Patched pending_term handling.")
else:
    print("Warning: old_pending not found.")

# 2. Add the 5 new catalog handlers right before "2. ITEM SELL PRICE & VALUE CARD"
target_sec = '''        # -------------------------------------------------------------------
        # 2. ITEM SELL PRICE & VALUE CARD (e.g. "combien se vend cet item", "combien coute le deux")
        # -------------------------------------------------------------------'''

new_sections = '''        # -------------------------------------------------------------------
        # 1.21 BAGS & CAPACITY (ALL 29 BAGS - CAPACITY, SLOTS & RESALE VALUES)
        # e.g. "combien de slots a coldstream pack", "ludwig's drumcase", "moist pouch"
        # -------------------------------------------------------------------
        conn_b = sqlite3.connect("hunger_helper.db")
        c_b = conn_b.cursor()
        c_b.execute("SELECT slug, name, rarity, slots, sell_silver, sell_copper FROM bags_full")
        all_bags = c_b.fetchall()
        conn_b.close()

        matched_bag = None
        for b_slug, b_name, b_rar, b_slots, b_ss, b_sc in all_bags:
            b_name_clean = b_name.lower().replace("'", "").replace("-", " ")
            clean_q_spaced = clean_text.lower().replace("'", "").replace("-", " ")
            if (re.search(r'\\b' + re.escape(b_slug) + r'\\b', clean_text.lower()) or
                re.search(r'\\b' + re.escape(b_name.lower()) + r'\\b', clean_text.lower()) or
                re.search(r'\\b' + re.escape(b_name_clean) + r'\\b', clean_q_spaced) or
                (b_slug.replace("-", " ") in clean_q_spaced and len(b_slug) > 5)):
                # If asking about recipe or craft, let recipe handler take it
                if any(w in lowered for w in ["recette", "recipe", "craft quel skin", "sert a craft"]):
                    continue
                matched_bag = (b_slug, b_name, b_rar, b_slots, b_ss, b_sc)
                break

        if matched_bag:
            b_slug, b_name, b_rar, b_slots, b_ss, b_sc = matched_bag
            self.last_queried_item = b_name
            from universal_v8_engine import render_bag_card
            card_path = render_bag_card(b_slug)
            val_txt = f"{b_ss} silver {b_sc} copper" if b_ss > 0 else f"{b_sc} copper"
            val_txt_fr = f"{b_ss} argent {b_sc} cuivre" if b_ss > 0 else f"{b_sc} cuivre"
            if is_french:
                spoken = f"Le {b_name} ({b_rar}) possède {b_slots} emplacements d'inventaire et se revend {val_txt_fr} aux marchands du Château."
                display = (
                    f"🎒 **FICHE DE BESACE : {b_name.upper()}**\\n\\n"
                    f"• Rareté : **{b_rar}**\\n"
                    f"• Capacité : **{b_slots} Emplacements d'inventaire**\\n"
                    f"• Prix de Revente : **{val_txt_fr}** (aux marchands)\\n"
                    f"• Règle de Sécurité : Besace standard (perdable à la mort). Placez les clés et items vitaux dans la besace sécurisée !\\n\\n"
                    f"🖼️ *(Fiche de besace haute résolution jointe ci-dessous)*"
                )
            else:
                spoken = f"{b_name} ({b_rar}) provides {b_slots} inventory slots and sells for {val_txt} to Chateau vendors."
                display = (
                    f"🎒 **OFFICIAL BAG DOSSIER : {b_name.upper()}**\\n\\n"
                    f"• Rarity : **{b_rar}**\\n"
                    f"• Capacity : **{b_slots} Inventory Slots**\\n"
                    f"• Resale Value : **{val_txt}** (To Merchants)\\n"
                    f"• Loss Rules : Standard Backpack (Droppable on death). Place vital keys and quest tokens in your Safe Pouch!\\n\\n"
                    f"🖼️ *(High-resolution bag card attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 1.22 TRAPS & FIELD HAZARDS (ALL 12 TRAPS)
        # e.g. "explosive trap", "piege explosif", "poison trap", "broken glass"
        # -------------------------------------------------------------------
        conn_t = sqlite3.connect("hunger_helper.db")
        c_t = conn_t.cursor()
        c_t.execute("SELECT slug, name, damage, radius, spots FROM traps_full")
        all_traps = c_t.fetchall()
        conn_t.close()

        matched_trap = None
        for t_slug, t_name, t_dmg, t_rad, t_spots in all_traps:
            t_name_clean = t_name.lower().replace("-", " ")
            clean_q_spaced = clean_text.lower().replace("-", " ")
            if (re.search(r'\\b' + re.escape(t_slug) + r'\\b', clean_text.lower()) or
                re.search(r'\\b' + re.escape(t_name.lower()) + r'\\b', clean_text.lower()) or
                re.search(r'\\b' + re.escape(t_name_clean) + r'\\b', clean_q_spaced)):
                if "strap" in clean_q_spaced and "trap" not in clean_q_spaced:
                    continue
                matched_trap = (t_slug, t_name, t_dmg, t_rad, t_spots)
                break

        if matched_trap:
            t_slug, t_name, t_dmg, t_rad, t_spots = matched_trap
            from universal_v8_engine import render_trap_hazard_card
            card_path = render_trap_hazard_card(t_slug)
            dmg_str = f"deals {t_dmg} damage" if t_dmg != "N/A" else "acts as an environmental hazard"
            dmg_str_fr = f"inflige {t_dmg} dégâts" if t_dmg != "N/A" else "agit comme piège d'alerte environnemental"
            rad_str = f"with a {t_rad} radius" if t_rad != "N/A" else ""
            rad_str_fr = f"avec un rayon de {t_rad}" if t_rad != "N/A" else ""
            if is_french:
                spoken = f"{t_name} {dmg_str_fr} {rad_str_fr} sur {t_spots} emplacements de raid."
                display = (
                    f"💥 **DOSSIER PIÈGE & DANGER : {t_name.upper()}**\\n\\n"
                    f"• Dégâts : **{t_dmg} DMG**\\n"
                    f"• Rayon d'Activation : **{t_rad}**\\n"
                    f"• Fréquence Mondiale : **{t_spots} Emplacements répertoriés**\\n"
                    f"• Conseil Tactique : Déclenchez à distance avec des armes à feu ou cailloux pour éviter les dégâts d'escouade.\\n\\n"
                    f"🖼️ *(Fiche tactique de piège jointe ci-dessous)*"
                )
            else:
                spoken = f"{t_name} {dmg_str} {rad_str} across {t_spots} world locations."
                display = (
                    f"💥 **HAZARD DOSSIER : {t_name.upper()}**\\n\\n"
                    f"• Base Damage : **{t_dmg} DMG**\\n"
                    f"• Blast Radius : **{t_rad}**\\n"
                    f"• World Locations : **{t_spots} Map Spots**\\n"
                    f"• Tactical Protocol : Trigger remotely with ranged fire or throwables to secure chokepoints.\\n\\n"
                    f"🖼️ *(Hazard intel card attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 1.23 STATUS EFFECTS & COMBAT CONDITIONS (ALL 36 EFFECTS)
        # e.g. "c'est quoi light bleed", "heavy poison", "status effect blind"
        # -------------------------------------------------------------------
        conn_e = sqlite3.connect("hunger_helper.db")
        c_e = conn_e.cursor()
        c_e.execute("SELECT slug, name, category, effect_type FROM status_effects_full")
        all_effects = c_e.fetchall()
        conn_e.close()

        matched_eff = None
        for e_slug, e_name, e_cat, e_type in all_effects:
            e_name_clean = e_name.lower().replace("-", " ")
            clean_q_spaced = clean_text.lower().replace("-", " ")
            if (re.search(r'\\b' + re.escape(e_slug) + r'\\b', clean_text.lower()) or
                re.search(r'\\b' + re.escape(e_name.lower()) + r'\\b', clean_text.lower()) or
                re.search(r'\\b' + re.escape(e_name_clean) + r'\\b', clean_q_spaced)):
                matched_eff = (e_slug, e_name, e_cat, e_type)
                break

        if matched_eff:
            e_slug, e_name, e_cat, e_type = matched_eff
            from universal_v8_engine import render_status_effect_card
            card_path = render_status_effect_card(e_slug)
            if is_french:
                spoken = f"{e_name} est un effet de statut ({e_cat}). {e_type[:60]}."
                display = (
                    f"🩸 **EFFET DE STATUT : {e_name.upper()}**\\n\\n"
                    f"• Catégorie : **{e_cat}**\\n"
                    f"• Mécaniques : **{e_type}**\\n"
                    f"• Traitement : Appliquez des bandages propres ou onguents de médecin immédiatement.\\n\\n"
                    f"🖼️ *(Fiche de statut jointe ci-dessous)*"
                )
            else:
                spoken = f"{e_name} is a {e_cat} condition. {e_type[:60]}."
                display = (
                    f"🩸 **STATUS EFFECT DOSSIER : {e_name.upper()}**\\n\\n"
                    f"• Classification : **{e_cat}**\\n"
                    f"• Impact & Dynamics : **{e_type}**\\n"
                    f"• Treatment : Apply Clean Bandage for Bleed or Physician Antivenom for Poison.\\n\\n"
                    f"🖼️ *(High-resolution status card attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 1.24 GATHERING NODES & NATURAL RESOURCES (ALL 32 NODES)
        # e.g. "ou trouver garlic bulb", "cueillette lavender", "clove bud"
        # -------------------------------------------------------------------
        conn_g = sqlite3.connect("hunger_helper.db")
        c_g = conn_g.cursor()
        c_g.execute("SELECT slug, name, chance, yield_range FROM gathering_full")
        all_nodes = c_g.fetchall()
        conn_g.close()

        matched_node = None
        for g_slug, g_name, g_chance, g_yield in all_nodes:
            g_name_clean = g_name.lower().replace("-", " ")
            clean_q_spaced = clean_text.lower().replace("-", " ")
            if (re.search(r'\\b' + re.escape(g_slug) + r'\\b', clean_text.lower()) or
                re.search(r'\\b' + re.escape(g_name.lower()) + r'\\b', clean_text.lower()) or
                re.search(r'\\b' + re.escape(g_name_clean) + r'\\b', clean_q_spaced)):
                matched_node = (g_slug, g_name, g_chance, g_yield)
                break

        if matched_node:
            g_slug, g_name, g_chance, g_yield = matched_node
            from universal_v8_engine import render_gathering_card
            card_path = render_gathering_card(g_slug)
            if is_french:
                spoken = f"{g_name} a un taux de récolte de {g_chance} et donne {g_yield} unités par plante. Récoltable principalement à Sarlat Farm et Sombre Forest."
                display = (
                    f"🌿 **RESSOURCE & CUEILLETTE : {g_name.upper()}**\\n\\n"
                    f"• Chance de Récolte : **{g_chance}**\\n"
                    f"• Rendement par Récolte : **{g_yield} Unités**\\n"
                    f"• Zones Principales : **Sarlat Farm, Garnier's Fields, Sombre Forest**\\n"
                    f"• Métiers : Ingrédient indispensable pour les recettes de Cuisinier et Apothicaire.\\n\\n"
                    f"🖼️ *(Fiche de cueillette jointe ci-dessous)*"
                )
            else:
                spoken = f"{g_name} has a {g_chance} harvest chance yielding {g_yield} units per node. Plentiful at Sarlat Farm."
                display = (
                    f"🌿 **GATHERING RECON : {g_name.upper()}**\\n\\n"
                    f"• Harvest Rate : **{g_chance} Success**\\n"
                    f"• Yield Range : **{g_yield} Units Per Harvest**\\n"
                    f"• Primary Habitats : **Sarlat Farm, Garnier's Fields, Sombre Forest**\\n"
                    f"• Profession Utility : High-tier Cook provisions and Physician remedies.\\n\\n"
                    f"🖼️ *(Gathering reconnaissance card attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        # -------------------------------------------------------------------
        # 1.25 CONTAINERS & FIELD LOOT (ALL 67 CONTAINERS)
        # e.g. "munitions crate", "spots oak barrel", "armour chest"
        # -------------------------------------------------------------------
        conn_cnt = sqlite3.connect("hunger_helper.db")
        c_cnt = conn_cnt.cursor()
        c_cnt.execute("SELECT slug, name, spots, items_count FROM containers_full")
        all_containers = c_cnt.fetchall()
        conn_cnt.close()

        matched_cont = None
        for c_slug, c_name, c_spots, c_icnt in all_containers:
            c_name_clean = c_name.lower().replace("-", " ")
            clean_q_spaced = clean_text.lower().replace("-", " ")
            if any(w in lowered for w in ["conteneur", "container", "caisse", "coffre", "baril", "spots"]):
                if (re.search(r'\\b' + re.escape(c_slug) + r'\\b', clean_text.lower()) or
                    re.search(r'\\b' + re.escape(c_name.lower()) + r'\\b', clean_text.lower()) or
                    re.search(r'\\b' + re.escape(c_name_clean) + r'\\b', clean_q_spaced)):
                    matched_cont = (c_slug, c_name, c_spots, c_icnt)
                    break
            elif len(c_name.split()) >= 2:
                if (re.search(r'\\b' + re.escape(c_slug) + r'\\b', clean_text.lower()) or
                    re.search(r'\\b' + re.escape(c_name.lower()) + r'\\b', clean_text.lower()) or
                    re.search(r'\\b' + re.escape(c_name_clean) + r'\\b', clean_q_spaced)):
                    matched_cont = (c_slug, c_name, c_spots, c_icnt)
                    break

        if matched_cont:
            c_slug, c_name, c_spots, c_icnt = matched_cont
            from universal_v8_engine import render_container_card
            card_path = render_container_card(c_slug)
            if is_french:
                spoken = f"{c_name} apparaît sur {c_spots} emplacements de raid et contient {c_icnt} types d'objets."
                display = (
                    f"📦 **CONTENEUR DE RAID : {c_name.upper()}**\\n\\n"
                    f"• Emplacements Mondiaux : **{c_spots} Spawns répertoriés**\\n"
                    f"• Variété de Butin : **{c_icnt} Variétés d'objets**\\n"
                    f"• Cartes Recommandées : Sarlat Farm, Jacques Bridge, Sombre Forest.\\n\\n"
                    f"🖼️ *(Fiche de conteneur jointe ci-dessous)*"
                )
            else:
                spoken = f"{c_name} appears in {c_spots} world spots containing {c_icnt} loot varieties."
                display = (
                    f"📦 **CONTAINER INTEL : {c_name.upper()}**\\n\\n"
                    f"• World Locations : **{c_spots} Spawn Points**\\n"
                    f"• Loot Variety : **{c_icnt} Unique Item Types**\\n"
                    f"• Best Maps : Sarlat Farm, Jacques Bridge, Sombre Forest.\\n\\n"
                    f"🖼️ *(Container reconnaissance card attached below)*"
                )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

''' + target_sec

if target_sec in code:
    code = code.replace(target_sec, new_sections, 1)
    print("Inserted new catalog handlers before Section 2.")
else:
    print("Warning: target_sec not found.")

with open(BRAIN_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved co_pilot/brain.py successfully.")
