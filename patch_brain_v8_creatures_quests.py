# -*- coding: utf-8 -*-
with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Insert Quest Chaining before Section 5.0
target_chain_str = "# 5.0 QUEST INTEL CARD"
idx_chain = text.find(target_chain_str)
assert idx_chain != -1, "Section 5.0 not found"

quest_chain_code = '''        # 4.9 QUEST CHAINING / NEXT QUEST IN PROGRESSION ("quel quete viens apres...")
        if any(w in lowered for w in ["apres celle de", "après celle de", "qui vient après", "qui viens après", "apres", "après", "after"]) and any(w in lowered for w in ["sweet", "opium", "pipe", "bowl", "china", "bribery"]):
            from universal_v8_engine import render_dynamic_quest_contract_card
            card_p = render_dynamic_quest_contract_card("down-from-mount-sinai")
            spoken = "The quest following Mr Sweet's 'A Touch of Bribery' is 'Down From Mount Sinai' given by Eloise at Chateau."
            display = (
                "📜 **QUEST PROGRESSION : NEXT CONTRACT (HUNGER COMPANION)**\\n\\n"
                "• ⬅️ **Completed Prerequisite :** **A Touch of Bribery** (Mr Sweet · Gather 1x Opium, 1x Opium Pipe, 1x China Bowl)\\n"
                "• ➡️ **Next Unlocked Quest :** **Down From Mount Sinai** (Giver: Eloise at Chateau Hub)\\n"
                "• 🎯 **Mission Objectives :** Recover the 7 lost treatises and historical records:\\n"
                "  1. *Catechisme of Christian Doctrine (1567)*\\n"
                "  2. *Census of 1806*\\n"
                "  3. *The Spirit of the Laws (Montesquieu)*\\n"
                "  4. *Course in Agriculture (Rozier)*\\n"
                "  5. *Codex Medicamentarius (Mortuary Record)*\\n"
                "  6. *Course in Civil Architecture (Rondelet)*\\n"
                "  7. *Natural History (Buffon)*\\n"
                "• 🗺️ **Raid Maps :** Search book cabinets across Jacques Bridge, Sarlat Farm, and Sombre Forest.\\n\\n"
                "*(Authentic mission contract card attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_p}

        '''

text = text[:idx_chain] + quest_chain_code + text[idx_chain:]

# 2. Update Creature Routing (Section 8.1)
old_creature_start = "# 8.1 CREATURE & MINIBOSS COMBAT INTEL"
c_idx = text.find(old_creature_start)
assert c_idx != -1, "Section 8.1 not found"
c_end = text.find("# 9. TALENT ADVICE", c_idx)
assert c_end != -1, "Section 9 not found"

new_creature_block = '''# 8.1 CREATURE & MINIBOSS COMBAT INTEL (Bloaters, Shamblers, Droolers, Brutes, Minibosses)
        # -------------------------------------------------------------------
        creature_keywords = [
            "bloat", "bloater", "boursouflé", "boursoufle", "shambler", "titubant", "traîne-pas",
            "traine-pas", "iron-shambler", "drooler", "drawler", "baveux", "brute", "pitchskin",
            "peau-de-poix", "peau de poix", "pale lady", "dame pale", "dame pâle", "dreg", "waif",
            "miséreux", "misereux", "hound", "miniboss", "monstre", "créature", "creature", "boss"
        ]
        is_creature_query = any(ck in lowered for ck in creature_keywords) and (
            any(w in lowered for w in [
                "pv", "vie", "degat", "dégât", "battre", "tuer", "vaincre", "comment", "c'est quoi",
                "stats", "faiblesse", "faiblesses", "point faible", "points faibles", "loot", "drop",
                "info", "boss", "qui est", "quels sont", "tactique", "fiche", "astuce", "conseil",
                "stratégie", "strategie", "montre moi", "montre", "show"
            ]) or "baveux" in lowered or "drooler" in lowered or "brute" in lowered or "bloater" in lowered or "bloat" in lowered or "shambler" in lowered or "monstre" in lowered
        )

        if is_creature_query and not any(w in lowered for w in ["map", "carte"]):
            from universal_v8_engine import render_universal_creature_card, CREATURES_DATABASE

            c_target = "drooler"
            if any(w in lowered for w in ["bloat", "bloater", "boursoufl"]):
                c_target = "bloat"
            elif any(w in lowered for w in ["shambler", "titubant", "traîne", "traine"]):
                c_target = "shambler"
            elif "brute" in lowered:
                c_target = "brute"
            elif any(w in lowered for w in ["drooler", "drawler", "baveux"]):
                c_target = "drooler"
            elif any(w in lowered for w in ["pitchskin", "peau"]):
                c_target = "pitchskin"
            elif any(w in lowered for w in ["pale", "pâle", "dame"]):
                c_target = "pale-lady"
            elif "dreg" in lowered:
                c_target = "dreg"
            elif "waif" in lowered:
                c_target = "waif"

            card_path = render_universal_creature_card(c_target, is_french=False)
            c_info = CREATURES_DATABASE.get(c_target, CREATURES_DATABASE["bloat"])

            spoken = f"{c_info['name_en']} has {c_info['health']} HP. Primary weak point is {c_info['weak_point']}. Creature profile dispatched."
            display = (
                f"👾 **CREATURE PROFILE : {c_info['name_en'].upper()} (HUNGER COMPANION)**\\n\\n"
                f"• 🩸 **Health Pool :** **{c_info['health']} HP**\\n"
                f"• 🎯 **Critical Weak Point :** **{c_info['weak_point']}**\\n"
                f"• 💥 **Attack Damage :** **{c_info['damage']}** | ⚡ **Movement Speed :** {c_info['speed']}\\n"
                f"• 🎁 **Trophy & Drops :** **{c_info['trophy_name']}** ({c_info['trophy_rate']})\\n"
                f"• 💡 **Combat Tactics :** {c_info['tactics']}\\n\\n"
                f"*(Authentic 3D creature render & harvest card attached below)*"
            )
            return {"spoken_text": spoken, "display_text": display, "image_attachment": card_path}

        '''

text = text[:c_idx] + new_creature_block + text[c_end:]

# 3. Fix line where "ou" in lowered triggered quest check
old_ou_bug = '''            if quests and any(w in lowered for w in ["qu\ufffdte", "quete", "quest", "gavroche", "trouve", "trouver", "o\ufffd", "ou"]):'''
# Find the exact string in text
idx_ou = text.find("if quests and any(w in lowered for w in [")
assert idx_ou != -1, "quests condition not found in brain.py"
end_ou = text.find("]:", idx_ou) + 2

new_ou_cond = '''if quests and (re.search(r"\\b(qu[eèé]te|quest|quests)\\b", lowered) or "gavroche" in lowered):'''
text = text[:idx_ou] + new_ou_cond + text[end_ou:]

with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] co_pilot/brain.py successfully updated with all V8 creatures and quest chaining logic!")
