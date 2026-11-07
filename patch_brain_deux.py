import os

p = "co_pilot/brain.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

# 1. In weapon checks, remove "deux" so it doesn't get hijacked into Zweihänder
old_w1 = 'for w_name in ["zweihander", "zwei", "deux mains", "deux-mains", "deux", "spear", "lance", "hallebarde", "halberd", "dagger", "dague", "sword", "épée", "axe", "hache", "mace", "masse"]:'
new_w1 = 'for w_name in ["zweihander", "zwei", "deux mains", "deux-mains", "spear", "lance", "hallebarde", "halberd", "dagger", "dague", "sword", "épée", "axe", "hache", "mace", "masse"]:'

assert old_w1 in text, "old_w1 not found"
text = text.replace(old_w1, new_w1, 1)

old_t_w = 't_w = "zweihander" if w_name in ["zweihander", "zwei", "deux mains", "deux-mains", "deux"] else "spear" if w_name in ["spear", "lance"] else w_name'
new_t_w = 't_w = "zweihander" if w_name in ["zweihander", "zwei", "deux mains", "deux-mains"] else "spear" if w_name in ["spear", "lance"] else w_name'

assert old_t_w in text, "old_t_w not found"
text = text.replace(old_t_w, new_t_w, 1)

# Also in weapon_res:
old_wn = 'for wn in ["zweihander", "zwei", "deux mains", "deux", "spear", "lance", "halberd", "hallebarde", "sabre", "dagger", "dague", "axe", "hache"]:'
new_wn = 'for wn in ["zweihander", "zwei", "deux mains", "deux-mains", "spear", "lance", "halberd", "hallebarde", "sabre", "dagger", "dague", "axe", "hache"]:'
if old_wn in text:
    text = text.replace(old_wn, new_wn, 1)

old_wn_tw = 'w_target = "zweihander" if wn in ["deux", "zwei", "deux mains"] else wn'
new_wn_tw = 'w_target = "zweihander" if wn in ["zwei", "deux mains", "deux-mains"] else wn'
if old_wn_tw in text:
    text = text.replace(old_wn_tw, new_wn_tw, 1)

# 2. In is_price_query, check companion intel for any item query (e.g. "deux", "farine", "family ring")
old_cand_block = """            # 3. Check general items from search candidates
            cand_items = extract_key_search_terms(clean_text)
            matched_item = None
            for cand in cand_items:
                c.execute("SELECT * FROM items WHERE slug = ? OR name LIKE ? LIMIT 1", (cand, f"%{cand}%"))
                it_row = c.fetchone()
                if it_row:
                    matched_item = it_row
                    break

            conn.close()"""

new_cand_block = """            # 3. Check live Hunger Companion intel first
            conn.close()
            from co_pilot.companion_intel import get_companion_item_intel, normalize_query_to_slug
            comp_slug = normalize_query_to_slug(clean_text)
            comp_intel = get_companion_item_intel(comp_slug)
            if comp_intel:
                self.last_queried_item = comp_intel["name_en"]
                card_path = render_item_card(comp_intel["slug"])
                s_s = comp_intel["sell_silver"]
                s_c = comp_intel["sell_copper"]
                if is_french:
                    v_str = f" Achat disponible chez {comp_intel['vendor_buy']}." if comp_intel.get("vendor_buy") else ""
                    spoken = f"Le {comp_intel['name_en']} ({comp_intel['rarity']}) se vend {s_s} argent {s_c} cuivre.{v_str} Fiche transmise."
                    display = (
                        f"💰 **FICHE OFFICIELLE : {comp_intel['name_en'].upper()}**\n\n"
                        f"• Rareté : **{comp_intel['rarity']}** | Catégorie : **{comp_intel['category']}**\n"
                        f"• Valeur de Revente : **{s_s} Argent {s_c} Cuivre**\n"
                        f"• Achat Château : **{comp_intel.get('vendor_buy') or 'Loot exclusif en raid'}**\n"
                        f"• Butin & Conteneurs : **{comp_intel.get('best_container') or 'Conteneurs de raid'}**\n"
                        f"• Description In-Game : *« {comp_intel.get('lore_desc', '')[:100]} »*\n\n"
                        f"🖼️ *Fiche visuelle Hunger Companion jointe ci-dessous.*"
                    )
                else:
                    spoken = f"The {comp_intel['name_en']} ({comp_intel['rarity']}) sells for {s_s} silver {s_c} copper. Card dispatched."
                    display = f"💰 **OFFICIAL ITEM PROFILE : {comp_intel['name_en'].upper()}**\n• Sell Price: **{s_s} Silver {s_c} Copper**"
                return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

            conn = get_connection()
            c = conn.cursor()
            cand_items = extract_key_search_terms(clean_text)
            matched_item = None
            for cand in cand_items:
                c.execute("SELECT * FROM items WHERE slug = ? OR name LIKE ? LIMIT 1", (cand, f"%{cand}%"))
                it_row = c.fetchone()
                if it_row:
                    matched_item = it_row
                    break
            conn.close()"""

assert old_cand_block in text, "old_cand_block not found"
text = text.replace(old_cand_block, new_cand_block, 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("Patch applied successfully to co_pilot/brain.py!")
