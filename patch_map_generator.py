# -*- coding: utf-8 -*-
with open("co_pilot/map_generator.py", "r", encoding="utf-8") as f:
    text = f.read()

old_block = '''    # 2. General database lookup in map_points
    tokens = [t for t in q.replace("ou", "").replace("se", "").replace("trouve", "").replace("trouver", "").replace("o\ufffd", "").split() if len(t) > 2]
    matched_points = []
    target_map = target_map_hint or "Jacques Bridge"

    for tok in tokens:
        c.execute("""
            SELECT map_name, title, point_type, x, y, description
            FROM map_points
            WHERE title LIKE ? OR quest_slug LIKE ? OR description LIKE ?
            LIMIT 5
        """, (f"%{tok}%", f"%{tok}%", f"%{tok}%"))
        pts_found = c.fetchall()
        if pts_found:
            matched_points = [dict(p) for p in pts_found]
            target_map = matched_points[0]["map_name"]
            break'''

# Let's find by substring
idx = text.find("# 2. General database lookup in map_points")
assert idx != -1, "General database lookup not found"
end_idx = text.find("conn.close()", idx)

new_block = '''    # 1.5 Specialized Handler: Piro's Convoy / Nest / Cart on Jacques Bridge
    if "piro" in q:
        map_name = "Jacques Bridge"
        map_img = JACQUES_MAP
        out_path = os.path.join(OUT_DIR, "dynamic_piro_convoy_location_map.jpg")
        cfg = {
            "title": "LOCATION : PIRO'S CONVOY & SITE (JACQUES BRIDGE)",
            "map_name": "Jacques Bridge",
            "map_img": map_img,
            "tag": "QUEST RECON",
            "header_cards": [
                ("Zone", "Southwest Riverbank"),
                ("Quests", "Remains of the Day / Return to the Convoy"),
                ("Giver", "Piro (Chateau Hub)")
            ],
            "story_pois": [
                {"x": 848.20, "y": 3084.90, "label": "Piro's Convoy Ruins", "offset_dir": "bottom", "cont_img": "strongbox.webp"}
            ],
            "points": [
                {"x": 848.20, "y": 3084.90, "type": "objective", "color": core.PRIO_YELLOW, "cont_img": "strongbox.webp"}
            ],
            "active_objectives": [
                {"title": "Locate Piro's missing convoy on Jacques Bridge", "cont_img": "strongbox.webp", "item_img": "gold_key.png"}
            ],
            "priority_focus": {
                "title": "Piro's Convoy (Southwest riverbank)",
                "c_ico": "strongbox.webp",
                "i_ico": "gold_key.png",
                "color": core.PRIO_PURPLE
            },
            "rotation_steps": [
                {"step": "Deploy on Jacques Bridge and advance along the Southwest riverbank road.", "color": core.PRIO_YELLOW},
                {"step": "Neutralize infected scavengers surrounding the overturned supply cart.", "color": core.PRIO_PURPLE},
                {"step": "Secure mission objective and extract safely.", "color": core.PRIO_GREY}
            ],
            "directory": [
                {"color": core.PRIO_YELLOW, "cont": "Piro's Convoy", "c_ico": "strongbox.webp", "item": "Quest Site", "rate": "100%", "spots": "X: 848.2, Y: 3084.9"}
            ],
            "roadmap": [
                {"quest": "Remains of the Day", "items": [("Crude Ampoule (x15)", "fresh_egg.png")]}
            ]
        }
        render_dynamic_v25_briefing(cfg, out_path)
        conn.close()
        intel = {
            "title": "Piro's Convoy (Jacques Bridge)",
            "map_name": "Jacques Bridge",
            "focus": "Southwest Riverbank (X: 848.2, Y: 3084.9)",
            "drops": [
                "• **Piro's Missing Convoy** (`X: 848.20, Y: 3084.90`) : Overturned wagon ruins on southwest riverbank road.",
                "• **Associated Quests** : *Remains of the Day* & *Return to the Convoy* (Giver: Piro at Chateau Hub).",
                "• **Reward** : 15x Crude Ampoules & Chateau Reputation."
            ]
        }
        return out_path, intel

    # 2. General database lookup in map_points with strict stopword filtering
    STOPWORDS = {
        "ou", "o\\ufffd", "où", "est", "ce", "que", "je", "peux", "trouver", "trouve", "sont", "localisation",
        "position", "carte", "map", "le", "la", "les", "un", "une", "des", "du", "de", "d",
        "pour", "avec", "dans", "sur", "sous", "par", "qui", "quoi", "quel", "quelle", "quels",
        "where", "is", "are", "can", "find", "how", "to", "get", "the", "in", "on", "at", "for", "item"
    }
    raw_tokens = re.sub(r"[^\\w\\s-]", " ", q).split()
    tokens = [t for t in raw_tokens if len(t) >= 3 and t.lower() not in STOPWORDS]
    matched_points = []
    target_map = target_map_hint or "Jacques Bridge"

    for tok in tokens:
        c.execute("""
            SELECT map_name, title, point_type, x, y, description
            FROM map_points
            WHERE title LIKE ? OR quest_slug LIKE ? OR description LIKE ?
            LIMIT 5
        """, (f"%{tok}%", f"%{tok}%", f"%{tok}%"))
        pts_found = c.fetchall()
        if pts_found:
            matched_points = [dict(p) for p in pts_found]
            target_map = matched_points[0]["map_name"]
            break'''

text = text[:idx] + new_block + "\n    " + text[end_idx:]

with open("co_pilot/map_generator.py", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] map_generator.py updated with Piro's Convoy and stopword filtering!")
