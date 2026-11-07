import re

with open("universal_v8_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

old_mat_check = """    # 0. Check materials & ingredients (e.g. "moist pouch sert a craft quel skin")
    mat_matches = []
    for k, v in db.items():
        mats = v.get("materials", [])
        for m in mats:
            m_name = m.get("name", "").lower()
            m_slug = m.get("slug", "").lower().replace("-", " ")
            if (m_name and m_name in q_low) or (m_slug and m_slug in q_low) or ("moist pouch" in q_low and "bacchus" in k):
                if v not in mat_matches:
                    mat_matches.append((m.get("name", "Ingredient"), v))
                break"""

new_mat_check = """    # 0. Check materials & ingredients (e.g. "moist pouch sert a craft quel skin")
    mat_matches = []
    is_ingredient_query = any(w in q_low for w in ["sert a", "sert à", "craft quel", "recipe", "recette", "ingredient", "ingrédient", "avec quel", "utilise", "utilisation"]) or "moist pouch" in q_low
    if is_ingredient_query:
        for k, v in db.items():
            mats = v.get("materials", [])
            for m in mats:
                m_name = m.get("name", "").lower()
                m_slug = m.get("slug", "").lower().replace("-", " ")
                m_match = (m_name and re.search(r'\\b' + re.escape(m_name) + r'\\b', q_low)) or (m_slug and re.search(r'\\b' + re.escape(m_slug) + r'\\b', q_low))
                if m_match or ("moist pouch" in q_low and "bacchus" in k):
                    if v not in mat_matches:
                        mat_matches.append((m.get("name", "Ingredient"), v))
                    break"""

if old_mat_check in text:
    text = text.replace(old_mat_check, new_mat_check)
    with open("universal_v8_engine.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("universal_v8_engine.py patched: ingredient check is now strict and word-bounded!")
else:
    print("old_mat_check not found!")
