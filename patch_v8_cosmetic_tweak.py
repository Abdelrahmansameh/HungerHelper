with open("universal_v8_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('f"COSMETIC CRAFTING PROFILE : {skin_name.upper()} ({target_name.upper()})"', 'f"COSMETIC PROFILE : {skin_name.upper()} ({target_name.upper()})"')
text = text.replace('drop_info = "The Chateau Hub (100% Guaranteed World Discovery in Artisan Quarters)" if "peasant" in skin_name.lower() else "Expedition Weapon Chests & Chateau Hub Discovery"',
                    'drop_info = "The Chateau Hub (100% Guaranteed World Discovery)" if "peasant" in skin_name.lower() else "Expedition Weapon Chests & Chateau Discovery"')

with open("universal_v8_engine.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Applied cosmetic card title and drop_info tweak.")
