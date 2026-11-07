with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Insert is_recipe_query right before is_skin_query
target_skin_block = '''        # 1.1 SKINS & COSMETICS (UNIVERSAL FOR ALL WEAPONS & CHARACTERS)
        # -------------------------------------------------------------------
        is_skin_query = any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "apparence", "outfit", "confection", "craft"]) or "craft quel" in lowered'''

new_recipe_and_skin_block = '''        # 1.05 RECIPES & SCHEMAS (UNIVERSAL FOR ALL 110 CRAFTING RECIPES)
        # -------------------------------------------------------------------
        is_recipe_query = any(w in lowered for w in ["recipe", "recette"]) or (
            any(w in lowered for w in ["metallurgist", "gunsmith", "outfitter", "artificer", "physician", "cook"]) and
            any(w in lowered for w in ["spear", "brioche", "armour", "plate", "carry", "helmet", "pack", "cuirass", "potion", "salve", "craft"])
        )
        if is_recipe_query:
            from universal_v8_engine import get_universal_recipe
            rec_res = get_universal_recipe(clean_text)
            if rec_res and rec_res["found"]:
                spoken = f"Crafting recipe dossier for {clean_text} dispatched. Placed loot and vendor intel attached."
                display = f"📜 **{rec_res['title']}**\\n\\n{rec_res['text']}\\n\\n*(Official recipe card attached below)*"
                return {
                    "spoken_text": spoken,
                    "display_text": display,
                    "image_attachments": [rec_res["card"]],
                    "image_attachment": rec_res["card"]
                }

        # 1.1 SKINS & COSMETICS (UNIVERSAL FOR ALL WEAPONS & CHARACTERS)
        # -------------------------------------------------------------------
        is_skin_query = any(w in lowered for w in ["skin", "skins", "cosmetique", "cosmétique", "tenue", "apparence", "outfit", "confection", "craft", "craft quel"]) or any(w in lowered for w in [
            "peasant burden", "peasant's burden", "bacchus wand", "recluse", "partisan", "hybernia", "loup", "basilisk", "solstice"
        ])'''

code = code.replace(target_skin_block, new_recipe_and_skin_block)

# 2. Update English item price display in Section 2 (around line 678)
old_en_price_display = '''                else:
                    spoken = f"The {comp_intel['name_en']} ({comp_intel['rarity']}) sells for {s_s} silver {s_c} copper. Card dispatched."
                    display = f"💰 **OFFICIAL ITEM PROFILE : {comp_intel['name_en'].upper()}**\\n• Sell Price: **{s_s} Silver {s_c} Copper**"'''

new_en_price_display = '''                else:
                    v_str = f" Available from {comp_intel['vendor_buy']}." if comp_intel.get("vendor_buy") else ""
                    spoken = f"The {comp_intel['name_en']} ({comp_intel['rarity']}) sells for {s_s} silver {s_c} copper.{v_str} Card dispatched."
                    display = (
                        f"💰 **OFFICIAL ITEM PROFILE : {comp_intel['name_en'].upper()}**\\n\\n"
                        f"• Rarity : **{comp_intel['rarity']}** | Category : **{comp_intel['category']}**\\n"
                        f"• Resale Value : **{s_s} Silver {s_c} Copper** (To Vendors)\\n"
                        f"• Chateau Availability : **{comp_intel.get('vendor_buy') or 'Not sold by merchants (Raid Loot Exclusive)'}**\\n"
                        f"• Best Drop Source : **{comp_intel.get('best_container') or 'Expedition Loot Containers'}**\\n"
                        f"• Lore : *« {comp_intel.get('lore_desc', '')[:120]} »*\\n\\n"
                        f"🖼️ *(High-resolution Hunger Companion item card attached below)*"
                    )'''

code = code.replace(old_en_price_display, new_en_price_display)

# 3. Update candidate search at bottom to check companion_items_cache directly
old_cand_search = '''                    else:
                        card_path = render_item_card(
                            it["name"], it["rarity"], 5, 0, it["type"],
                            "Objet d'expédition trouvable dans les conteneurs de raid. Utile pour l'artisanat.",
                            icon_name=f"{it['slug']}.png"
                        )
                        spoken = f"{it['name']} ({it['rarity']}). Fiche transmise." if is_french else f"{it['name']} ({it['rarity']}). Card dispatched."
                    return {"spoken_text": spoken, "display_text": f"📦 **{it['name']}** ({it['type']}, {it['rarity']})", "image_attachment": card_path}'''

new_cand_search = '''                    else:
                        from co_pilot.companion_intel import get_companion_item_intel
                        c_info = get_companion_item_intel(it["slug"])
                        s_sil = c_info.get("sell_silver", 0) if c_info else 5
                        s_cop = c_info.get("sell_copper", 50) if c_info else 0
                        card_path = render_item_card(it["name"], is_french=is_french)
                        spoken = f"{it['name']} ({it['rarity']}) sells for {s_sil} silver {s_cop} copper. Card dispatched."
                        display = (
                            f"📦 **OFFICIAL ITEM PROFILE : {it['name'].upper()}**\\n\\n"
                            f"• Rarity : **{it['rarity'].title()}** | Category : **{it['type'].title()}**\\n"
                            f"• Resale Value : **{s_sil} Silver {s_cop} Copper** (To Vendors)\\n"
                            f"• Raid Security : Keep in Secure Pouch if required for active progression.\\n\\n"
                            f"🖼️ *(High-resolution item card attached below)*"
                        )
                    return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}'''

code = code.replace(old_cand_search, new_cand_search)

with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated brain.py successfully!")
