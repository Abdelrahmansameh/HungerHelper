with open('universal_v8_engine.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_block = '''    sell_items = [
        {"name": "Spyglass / Telescope (Kompas Curio)", "qty": 1, "unit_price": 60, "total_price": 60, "icon": "T_UI_Item_Kompas.png", "desc": "Junk nautical curio with no crafting utility"},
        {"name": "Silver Candelabra (Church Dish)", "qty": 1, "unit_price": 85, "total_price": 85, "icon": "silver_dish.png", "desc": "High value church silverware ornament"},
        {"name": "Ornate Silver Key (Duplicate)", "qty": 1, "unit_price": 45, "total_price": 45, "icon": "silver_key.png", "desc": "Duplicate orphan key with no lock found at Chateau"},
        {"name": "Cut Timber Slab (Surplus Wood)", "qty": 1, "unit_price": 15, "total_price": 15, "icon": "thick_branch.png", "desc": "Superfluous timber slab surplus for coin liquidation"}
    ]'''

new_block = '''    sell_items = [
        {"name": "Cut Timber Slab (Surplus Wood)", "qty": 1, "unit_price": 25, "total_price": 25, "slot": (4, 0), "desc": "Solid timber cut slab - sell to Chateau Merchant for quick copper"},
        {"name": "Sealed Document Tube (Map Curio)", "qty": 1, "unit_price": 60, "total_price": 60, "slot": (7, 0), "desc": "Leather map case curio with no active quest requirement"},
        {"name": "Ornate Silver Key (Duplicate)", "qty": 1, "unit_price": 45, "total_price": 45, "slot": (2, 1), "desc": "Duplicate orphan dungeon key with no lock found at Chateau"}
    ]'''

if old_block in code:
    code = code.replace(old_block, new_block)
    print("Replaced sell_items!")

old_slots = '''    sell_grid_slots = [
        (7, 0, sell_items[0]), # Spyglass
        (4, 0, sell_items[3]), # Timber slab
        (2, 1, sell_items[2])  # Ornate key
    ]'''

new_slots = '''    sell_grid_slots = [
        (4, 0, sell_items[0]), # Timber slab
        (7, 0, sell_items[1]), # Document tube
        (2, 1, sell_items[2])  # Ornate key
    ]'''

if old_slots in code:
    code = code.replace(old_slots, new_slots)
    print("Replaced sell_grid_slots!")

import re
pattern = re.compile(r'    # Image 2: Liquidation Manifest.*?    out_p2 = save_and_sync\(img2, "stash_sell_manifest\.jpg"\)', re.DOTALL)

new_img2_code = '''    # Image 2: Liquidation Manifest
    MW, MH = 1040, 560
    img2 = Image.new("RGB", (MW, MH), (14, 14, 16))
    d2 = ImageDraw.Draw(img2)
    d2.rectangle([4, 4, MW - 5, MH - 5], outline=core.COLOR_GOLD, width=2)
    d2.rectangle([8, 8, MW - 9, MH - 9], outline=(40, 36, 26), width=1)

    # Header
    d2.rounded_rectangle([18, 14, MW - 18, 68], radius=8, fill=(18, 18, 22), outline=(50, 45, 30), width=1)
    d2.rounded_rectangle([28, 22, 180, 60], radius=5, fill=(35, 30, 20), outline=core.COLOR_GOLD, width=1)
    d2.text((40, 31), "LIQUIDATION", fill=core.COLOR_GOLD, font=core.F_SMALL_BOLD)
    d2.text((195, 27), "ALL ITEMS TO SELL TO CHATEAU MERCHANTS", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)

    sy = 86
    row_h = 76
    for it in sell_items:
        card = [28, sy, MW - 28, sy + row_h]
        d2.rounded_rectangle(card, radius=6, fill=(20, 20, 24), outline=(55, 50, 40), width=1)

        ib = [card[0] + 8, card[1] + 8, card[0] + 68, card[3] - 8]
        d2.rounded_rectangle(ib, radius=6, fill=(10, 10, 12), outline=core.COLOR_GOLD, width=1)

        # Crop authentic item icon directly from user screen slot
        col, row = it["slot"]
        sx = int(start_x + col * step_x)
        sy_slot = int(start_y + row * step_y)
        crop_box = (sx, sy_slot, sx + cell_w, sy_slot + cell_h)
        item_crop = raw_screen.crop(crop_box)
        safe_paste(img2, item_crop, (ib[0] + 4, ib[1] + 4, ib[2] - ib[0] - 8, ib[3] - ib[1] - 8))

        d2.text((card[0] + 82, card[1] + 12), f"{it['name']}  ({it['qty']}x)", fill=core.COLOR_PARCHMENT, font=core.F_SECTION_TITLE)
        desc_txt = f"Unit: {it['unit_price']} Copper  Total: {it['total_price']} Copper  |  {it['desc']}"
        d2.text((card[0] + 82, card[1] + 42), desc_txt, fill=(175, 175, 155), font=core.F_BODY)

        # Value pill
        d2.rounded_rectangle([card[2] - 150, card[1] + 18, card[2] - 14, card[1] + 56], radius=6, fill=(35, 26, 14), outline=core.COLOR_GOLD, width=1)
        d2.text((card[2] - 135, card[1] + 26), f"+{it['total_price']} Copper", fill=core.PRIO_YELLOW, font=core.F_SMALL_BOLD)

        sy += row_h + 12

    # Grand Total Box (Clean ASCII layout, zero text collisions)
    tot_box = [28, MH - 86, MW - 28, MH - 18]
    d2.rounded_rectangle(tot_box, radius=8, fill=(28, 22, 14), outline=core.COLOR_GOLD, width=2)
    d2.text((tot_box[0] + 20, tot_box[1] + 12), "ESTIMATED TOTAL PROCEEDS :", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)
    d2.text((tot_box[0] + 20, tot_box[1] + 34), f"TOTAL PROCEEDS : {tot_s} Silver  {tot_c} Copper Coins  ({total_copper_sum} Copper)", fill=core.PRIO_YELLOW, font=core.F_HEADER_TITLE)
    d2.text((tot_box[2] - 440, tot_box[1] + 24), "* [EXP] Letters, notes & medicines preserved in stash", fill=(180, 180, 160), font=core.F_BODY)

    out_p2 = save_and_sync(img2, "stash_sell_manifest.jpg")'''

if pattern.search(code):
    code = pattern.sub(new_img2_code, code)
    print("Replaced Image 2 code!")
else:
    print("pattern not found")

with open('universal_v8_engine.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Saved universal_v8_engine.py successfully!")
