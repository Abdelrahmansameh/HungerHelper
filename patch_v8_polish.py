with open("universal_v8_engine.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Fix material icon lookup in render_pure_english_cosmetic_card
old_mat_ico = '''        m_slug = mat.get("slug", mat["name"].lower().replace(' ', '-'))
        m_ico_p = os.path.join(ROOT_DIR, "assets", "items", f"T_UI_Item_{mat['name'].replace(' ', '')}.png")
        if not os.path.exists(m_ico_p):
            m_ico_p = os.path.join(ROOT_DIR, "assets", "items", f"{m_slug}.png")
        if os.path.exists(m_ico_p):
            safe_paste(canvas, Image.open(m_ico_p), (ico_b[0] + 3, ico_b[1] + 3, 38, 38))'''

new_mat_ico = '''        m_slug = mat.get("slug", mat["name"].lower().replace(' ', '-'))
        m_clean = mat['name'].lower().replace(' ', '_').replace('-', '_')
        cand_icons = [
            f"T_UI_Item_{mat['name'].replace(' ', '')}.png",
            f"{m_slug}.png",
            f"{m_clean}.png",
            "thick_branch.png" if "branch" in m_clean else "",
            "T_UI_Item_SolidBranch.png" if "branch" in m_clean else ""
        ]
        m_ico_p = None
        for ci in cand_icons:
            if ci and os.path.exists(os.path.join(ROOT_DIR, "assets", "items", ci)):
                m_ico_p = os.path.join(ROOT_DIR, "assets", "items", ci)
                break
        if m_ico_p and os.path.exists(m_ico_p):
            safe_paste(canvas, Image.open(m_ico_p), (ico_b[0] + 3, ico_b[1] + 3, 38, 38))'''

code = code.replace(old_mat_ico, new_mat_ico)

# 2. Fix pill text in render_pure_english_cosmetic_card
old_pill2 = 'draw.text((left_box[0] + 20, ty + 5), "Vendor Availability : Not Sold by Merchants (Raid Drop)", fill=(210, 205, 220), font=core.F_HEADER_TAG)'
new_pill2 = 'draw.text((left_box[0] + 20, ty + 5), "Vendor Stock : Raid Drop (Not Sold by Merchants)", fill=(210, 205, 220), font=core.F_HEADER_TAG)'
code = code.replace(old_pill2, new_pill2)

# 3. Fix recipe card title wrap in render_recipe_card
old_rec_title = 'draw.text((left_box[0] + 16, ty), title[:26], fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)'
new_rec_title = '''if len(title) > 24:
        words = title.split()
        mid = len(words) // 2
        l1 = " ".join(words[:mid])
        l2 = " ".join(words[mid:])
        draw.text((left_box[0] + 16, ty), l1, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
        ty += 22
        draw.text((left_box[0] + 16, ty), l2, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)
    else:
        draw.text((left_box[0] + 16, ty), title, fill=core.COLOR_PARCHMENT, font=core.F_CARD_TITLE)'''
code = code.replace(old_rec_title, new_rec_title)

with open("universal_v8_engine.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated universal_v8_engine.py!")
