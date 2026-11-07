import os

BRAIN_PATH = "co_pilot/brain.py"

with open(BRAIN_PATH, "r", encoding="utf-8") as f:
    text = f.read()

target = '''        # -------------------------------------------------------------------
        # 12. RANDOM LORE & GAME FACTS
        # -------------------------------------------------------------------
        if any(w in lowered for w in ["fait aleatoire", "fait aléatoire", "random fact", "saviez-vous", "saviez vous", "lore"]):
            return answer_random_fact_query(is_french)'''

replacement = '''        # -------------------------------------------------------------------
        # 12. CANONICAL GAME LORE & WORLDBUILDING (THE HUNGER UNIVERSE)
        # e.g. "c'est quoi the hunger", "qui est marie", "histoire du chateau", "lore des dregs"
        # -------------------------------------------------------------------
        from co_pilot.lore_engine import answer_lore_query
        lore_res = answer_lore_query(clean_text, is_french)
        if lore_res:
            return lore_res

        if any(w in lowered for w in ["fait aleatoire", "fait aléatoire", "random fact", "saviez-vous", "saviez vous"]):
            return answer_random_fact_query(is_french)'''

if target in text:
    text = text.replace(target, replacement, 1)
    with open(BRAIN_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("Patched brain.py with canonical lore engine successfully.")
else:
    print("Target not found.")
