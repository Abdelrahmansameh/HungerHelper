with open("co_pilot/companion_intel.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update ITEM_ALIASES with exact slugs
code = code.replace('"peasant\'s burden": "peasants-burden"', '"peasant\'s burden": "peasant-s-burden-spear"')
code = code.replace('"peasant burden": "peasants-burden"', '"peasant burden": "peasant-s-burden-spear"')
code = code.replace('"fardeau du paysan": "peasants-burden"', '"fardeau du paysan": "peasant-s-burden-spear"')

extra_aliases = '''    "peasant\'s burden spear": "peasant-s-burden-spear",
    "peasant burden spear": "peasant-s-burden-spear",
    "metallurgist recipe spear": "metallurgist-recipe-spear",
    "metallurgist recipe": "metallurgist-recipe-spear",
    "spear recipe": "metallurgist-recipe-spear",
    "recette de lance": "metallurgist-recipe-spear",
    "cook recipe brioche": "cook-recipe-brioche",
    "brioche recipe": "cook-recipe-brioche",
    "artificer recipe damascus armour plate": "artificer-recipe-damascus-armour-plate",
    "damascus armour plate recipe": "artificer-recipe-damascus-armour-plate",'''

code = code.replace('"peasant burden": "peasant-s-burden-spear",', '"peasant burden": "peasant-s-burden-spear",\n' + extra_aliases)

# 2. Update normalize_query_to_slug sorting
old_norm = '''    for k, v in ITEM_ALIASES.items():
        if k in clean:
            return v'''

new_norm = '''    for k in sorted(ITEM_ALIASES.keys(), key=len, reverse=True):
        if k in clean:
            return ITEM_ALIASES[k]'''

code = code.replace(old_norm, new_norm)

# 3. Update get_companion_item_intel exact match first
old_query = '''    cur.execute("SELECT * FROM companion_items_cache WHERE slug = ? OR name_en LIKE ? OR name_fr LIKE ? LIMIT 1",
                (slug, f"%{slug}%", f"%{slug}%"))
    row = cur.fetchone()'''

new_query = '''    cur.execute("SELECT * FROM companion_items_cache WHERE slug = ? LIMIT 1", (slug,))
    row = cur.fetchone()
    if not row:
        cur.execute("SELECT * FROM companion_items_cache WHERE slug LIKE ? OR name_en LIKE ? OR name_fr LIKE ? LIMIT 1",
                    (f"%{slug}%", f"%{slug}%", f"%{slug}%"))
        row = cur.fetchone()'''

code = code.replace(old_query, new_query)

with open("co_pilot/companion_intel.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated companion_intel.py!")
