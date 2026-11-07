with open("co_pilot/vision_analyzer.py", "r", encoding="utf-8") as f:
    text = f.read()

text_n = text.replace("\r\n", "\n")

target = """        # Generate the TWO visual stash images (1: highlighted grid, 2: sell manifest)
        from test_dynamic_stash_two_images import render_dynamic_stash_two_images
        from test_parse_sell import parse_sell_items
        parsed_items, silv, copp = parse_sell_items(resp_text)

        p1, p2 = render_dynamic_stash_two_images(
            sell_items=parsed_items,
            total_silver=silv,
            total_copper=copp,
            market_rotation_text="+12% par rapport au cours de base (Rotation très favorable)",
            user_screen_path=image_path
        )"""

replacement = """        # Generate the TWO visual stash images (1: highlighted grid, 2: sell manifest)
        from stash_dual_images_v5 import render_real_stash_two_images
        from test_parse_sell import parse_sell_items
        parsed_items, silv, copp = parse_sell_items(resp_text)

        p1, p2 = render_real_stash_two_images(
            user_screen_path=image_path,
            sell_items=parsed_items,
            total_silver=silv,
            total_copper=copp,
            market_rotation_text="+12% Above Base Rate (Favorable Rotation)" if not is_french else "+12% au-dessus du cours de base (Rotation favorable)",
            is_french=is_french
        )"""

if target in text_n:
    text_n = text_n.replace(target, replacement)
    with open("co_pilot/vision_analyzer.py", "w", encoding="utf-8") as f:
        f.write(text_n)
    print("VISION_ANALYZER_PATCHED_SUCCESSFULLY")
else:
    print("target not found in vision_analyzer")
