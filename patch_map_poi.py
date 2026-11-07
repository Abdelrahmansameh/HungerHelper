with open("co_pilot/map_generator.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update STOPWORDS in generate_location_poi_map
old_stopwords = """    STOPWORDS = {
        "ou", "o\\ufffd", "où", "est", "ce", "que", "je", "peux", "trouver", "trouve", "sont", "localisation",
        "position", "carte", "map", "le", "la", "les", "un", "une", "des", "du", "de", "d",
        "pour", "avec", "dans", "sur", "sous", "par", "qui", "quoi", "quel", "quelle", "quels",
        "where", "is", "are", "can", "find", "how", "to", "get", "the", "in", "on", "at", "for", "item"
    }"""

new_stopwords = """    STOPWORDS = {
        "ou", "o\\ufffd", "où", "est", "ce", "que", "je", "peux", "trouver", "trouve", "sont", "localisation",
        "position", "carte", "map", "le", "la", "les", "un", "une", "des", "du", "de", "d",
        "pour", "avec", "dans", "sur", "sous", "par", "qui", "quoi", "quel", "quelle", "quels",
        "where", "is", "are", "can", "find", "how", "to", "get", "the", "in", "on", "at", "for", "item",
        "skin", "skins", "peasant", "burden", "heavy", "ammo", "munition", "munitions", "cost", "coute"
    }"""

text = text.replace(old_stopwords, new_stopwords)

# 2. Update fallback when not matched_points
old_fallback = """    if not matched_points:
        # Fallback to general item farm map
        return generate_item_farm_map("flour", "Sarlat Farm")"""

new_fallback = """    if not matched_points:
        from universal_v8_engine import get_pure_blank_map
        clean_map = get_pure_blank_map(target_map)
        intel = {
            "title": f"TACTICAL RECON : {target_map.upper()}",
            "map_name": target_map,
            "focus": f"General expedition recon on {target_map}",
            "drops": [
                f"• Clean tactical base map for {target_map} dispatched.",
                "• No specific POI or waypoint was recognized for this query.",
                "• Specify a landmark, enemy, container, or quest objective to plot dynamic coordinates."
            ]
        }
        return clean_map, intel"""

text = text.replace(old_fallback, new_fallback)

with open("co_pilot/map_generator.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated map_generator.py POI lookup and fallback successfully!")
