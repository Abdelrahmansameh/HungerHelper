with open('co_pilot/map_generator.py', 'r', encoding='utf-8') as f:
    text = f.read()

piro_lens_block = '''    # 1.4 Specialized Handler: Piro's Lens (Quest: Seeing Clearly)
    if any(k in q for k in ["lens", "lentille", "seeing clearly", "seeing-clearly"]):
        map_name = "Jacques Bridge"
        map_img = JACQUES_MAP
        out_path = os.path.join(OUT_DIR, "dynamic_piro_lens_location_map.jpg")
        cfg = {
            "title": "LOCATION : PIRO'S LENS (QUEST: SEEING CLEARLY)",
            "map_name": "Jacques Bridge",
            "map_img": map_img,
            "tag": "QUEST RECON",
            "header_cards": [
                ("Zone", "South-East Ruins (Rat's Nest Cave)"),
                ("Objective", "Find Piro's Lens (ID_Uncommon_PirosLens)"),
                ("Giver", "Piro (Chateau Hub)")
            ],
            "story_pois": [
                {"x": 1602.00, "y": 3552.00, "label": "Rat's Nest Cave Entrance", "offset_dir": "bottom", "cont_img": "strongbox.webp"},
                {"x": 1491.15, "y": 3535.74, "label": "Piro's Lens", "offset_dir": "top", "cont_img": "gold_key.png"}
            ],
            "points": [
                {"x": 1602.00, "y": 3552.00, "type": "objective", "color": core.PRIO_PURPLE, "cont_img": "strongbox.webp"},
                {"x": 1491.15, "y": 3535.74, "type": "objective", "color": core.COLOR_GOLD, "cont_img": "gold_key.png"}
            ],
            "active_objectives": [
                {"title": "Enter the Rat's Nest Cave at Jacques Bridge South-East", "cont_img": "strongbox.webp", "item_img": "gold_key.png"},
                {"title": "Recover Piro's Lens inside the cave", "cont_img": "gold_key.png", "item_img": "gold_key.png"}
            ],
            "priority_focus": {
                "title": "Rat's Nest Cave & Piro's Lens",
                "c_ico": "strongbox.webp",
                "i_ico": "gold_key.png",
                "color": core.COLOR_GOLD
            },
            "rotation_steps": [
                {"step": "Deploy on Jacques Bridge and advance towards the South-East ruins.", "color": core.PRIO_YELLOW},
                {"step": "Locate the Cave entrance (X: 1602, Y: 3552) leading into the subterranean den.", "color": core.PRIO_PURPLE},
                {"step": "Retrieve Piro's Lens (X: 1491, Y: 3535) and store in Secure Pouch.", "color": core.PRIO_GREY}
            ],
            "directory": [
                {"color": core.COLOR_GOLD, "cont": "Piro's Lens", "c_ico": "gold_key.png", "item": "Optical Monocle Lens", "rate": "100%", "spots": "X: 1491.15, Y: 3535.74"},
                {"color": core.PRIO_PURPLE, "cont": "Cave Entrance", "c_ico": "strongbox.webp", "item": "Rat's Nest Cave", "rate": "100%", "spots": "X: 1602.00, Y: 3552.00"}
            ],
            "roadmap": [
                {"quest": "Seeing Clearly", "items": [("Piro's Lens (x1)", "gold_key.png")]}
            ]
        }
        render_dynamic_v25_briefing(cfg, out_path)
        conn.close()
        intel = {
            "title": "Piro's Lens (Jacques Bridge)",
            "map_name": "Jacques Bridge",
            "focus": "Rat's Nest Cave (X: 1491.15, Y: 3535.74)",
            "drops": [
                "• **Piro's Lens Location** (`X: 1491.15, Y: 3535.74`) : Inside the subterranean Rat's Nest Cave at Jacques Bridge South-East.",
                "• **Cave Entrance** (`X: 1602.00, Y: 3552.00`) : Primary entrance to the cave.",
                "• **Associated Quest** : *Seeing Clearly* (Giver: Piro at Chateau Hub).",
                "• **Safe Pouch Rule** : Keep in Secure Pouch (Quest Item, Non-droppable)!"
            ]
        }
        return out_path, intel

'''

target_str = '    # 1.5 Specialized Handler: Piro\'s Convoy / Nest / Cart on Jacques Bridge\n    if "piro" in q:'
replacement_str = piro_lens_block + '    # 1.5 Specialized Handler: Piro\'s Convoy (Remains of the Day / Return to the Convoy)\n    if "piro" in q and not any(k in q for k in ["lens", "lentille"]):'

if target_str in text:
    text = text.replace(target_str, replacement_str)
    print("Added Piro's Lens specialized handler to map_generator.py!")
else:
    print("target_str not found in map_generator.py")

with open('co_pilot/map_generator.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved co_pilot/map_generator.py!")
