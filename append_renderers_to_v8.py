import os
import re

ENGINE_PATH = "universal_v8_engine.py"

with open(ENGINE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Fix any \ufffd corrupted characters
content = content.replace("\ufffd", "-")

new_renderers = '''

# ===========================================================================
# 11. BAGS & BACKPACKS (ALL 29 BAGS - CAPACITY, SLOTS & RESALE VALUES)
# ===========================================================================
def render_bag_card(bag_slug_or_name: str) -> str:
    """Render high-resolution bag profile card with exact slot count, rarity, and sell value."""
    clean = bag_slug_or_name.lower().replace(" ", "-").replace("'", "")
    conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
    c = conn.cursor()
    c.execute("SELECT slug, name, rarity, slots, sell_silver, sell_copper FROM bags_full WHERE slug LIKE ? OR name LIKE ? LIMIT 1",
              (f"%{clean}%", f"%{bag_slug_or_name}%"))
    row = c.fetchone()
    conn.close()

    if not row:
        row = ("coldstream-pack", "Coldstream Pack", "Legendary", 22, 280, 0)

    slug, name, rarity, slots, s_s, s_c = row
    rarity_cap = rarity.capitalize()
    theme_color = core.PRIO_PURPLE if rarity_cap in ["Epic", "Legendary"] else core.COLOR_GOLD

    canvas, draw = create_base_canvas(f"BAG DOSSIER : {name.upper()}", tag="EXPEDITION GEAR", border_col=theme_color)
    CARD_W, CARD_H = canvas.size

    # Left Box: Bag Icon & Badge
    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_color, width=2)

    bag_img_path = os.path.join(ROOT_DIR, "assets", "items", "ID_BackBag_Epic01.webp" if slots >= 12 else "ID_HipBag_Common01.webp")
    if os.path.exists(bag_img_path):
        try:
            b_img = Image.open(bag_img_path).convert("RGBA").resize((280, 280), Image.Resampling.LANCZOS)
            canvas.paste(b_img, (left_box[0] + 36, left_box[1] + 30), b_img)
        except Exception:
            pass

    draw.rounded_rectangle([left_box[0] + 24, left_box[3] - 110, left_box[2] - 24, left_box[3] - 68],
                           radius=6, fill=(24, 20, 32), outline=theme_color, width=1)
    draw.text((left_box[0] + 36, left_box[3] - 100), f"RARITY : {rarity_cap.upper()}", fill=theme_color, font=core.F_SMALL_BOLD)
    draw.text((left_box[0] + 36, left_box[3] - 50), "GEAR TYPE : INVENTORY CONTAINER", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TAG)

    rx = 404
    rw = CARD_W - 28 - rx

    # Box 1: Slots
    b1 = [rx, 86, rx + rw, 196]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=theme_color, width=2)
    draw.text((b1[0] + 20, b1[1] + 16), "INVENTORY CAPACITY", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((b1[0] + 20, b1[1] + 52), f"{slots} INVENTORY SLOTS", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((b1[0] + 20, b1[1] + 82), "Expands squad carrying capacity for raid expeditions and loot transport.", fill=(180, 180, 180), font=core.F_BODY)

    # Box 2: Resale Value
    b2 = [rx, 212, rx + rw, 322]
    draw.rounded_rectangle(b2, radius=8, fill=(22, 22, 28), outline=(60, 50, 35), width=1)
    draw.text((b2[0] + 20, b2[1] + 16), "BASE RESALE VALUE (TO MERCHANTS)", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    val_str = f"{s_s} Silver {s_c} Copper" if s_s > 0 else f"{s_c} Copper"
    draw.text((b2[0] + 20, b2[1] + 52), val_str, fill=(255, 215, 0), font=core.F_HEADER_TITLE)
    draw.text((b2[0] + 20, b2[1] + 82), "Official sell price to Chateau merchants. Resale value is fixed.", fill=(180, 180, 180), font=core.F_BODY)

    # Box 3: Security & Survival Rule
    b3 = [rx, 338, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b3, radius=8, fill=(24, 18, 18), outline=(90, 40, 40), width=1)
    draw.text((b3[0] + 20, b3[1] + 16), "RAID LOSS & SAFE POUCH RULES", fill=(240, 110, 110), font=core.F_SECTION_TITLE)
    draw.text((b3[0] + 20, b3[1] + 52), "* Standard Backpack (Droppable on death).", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b3[0] + 20, b3[1] + 82), "* Keep essential quest items and keys in your Secure Pouch.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b3[0] + 20, b3[1] + 112), "* Crafted at Chateau Outfitter Workshop or found in high-tier stashes.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"bag_card_{slug}.jpg")


# ===========================================================================
# 12. TRAPS & HAZARDS (DAMAGE, RADIUS & DISARM TACTICS)
# ===========================================================================
def render_trap_hazard_card(trap_slug_or_name: str) -> str:
    """Render high-resolution tactical hazard dossier."""
    clean = trap_slug_or_name.lower().replace(" ", "-").replace("'", "")
    conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
    c = conn.cursor()
    c.execute("SELECT slug, name, damage, radius, spots FROM traps_full WHERE slug LIKE ? OR name LIKE ? LIMIT 1",
              (f"%{clean}%", f"%{trap_slug_or_name}%"))
    row = c.fetchone()
    conn.close()

    if not row:
        row = ("explosive-trap", "Explosive Trap", "60", "4 m", 115)

    slug, name, damage, radius, spots = row
    theme_color = (200, 60, 60)

    canvas, draw = create_base_canvas(f"HAZARD DOSSIER : {name.upper()}", tag="TACTICAL THREAT", border_col=theme_color)
    CARD_W, CARD_H = canvas.size

    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=(28, 14, 14), outline=theme_color, width=2)
    draw.text((left_box[0] + 24, left_box[1] + 24), "TACTICAL HAZARD", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 70), name.upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 120), "ALERT : Lethal field trap deployed in combat sectors.", fill=(220, 180, 180), font=core.F_BODY)
    draw.text((left_box[0] + 24, left_box[1] + 160), f"Map Frequency : {spots} locations", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    rx = 404
    rw = CARD_W - 28 - rx

    b1 = [rx, 86, rx + rw, 210]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=theme_color, width=1)
    draw.text((b1[0] + 20, b1[1] + 16), "DETONATION STATS", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((b1[0] + 20, b1[1] + 52), f"Base Damage : {damage} DMG", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((b1[0] + 20, b1[1] + 86), f"Trigger Radius : {radius}", fill=(255, 200, 100), font=core.F_HEADER_TAG)

    b2 = [rx, 226, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b2, radius=8, fill=(22, 22, 28), outline=core.COLOR_GOLD, width=1)
    draw.text((b2[0] + 20, b2[1] + 16), "TACTICAL MITIGATION & DISARM", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((b2[0] + 20, b2[1] + 56), "* Shoot from a safe perimeter using firearms or thrown objects.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b2[0] + 20, b2[1] + 90), "* Never sprint blindly through dense brush or doorway thresholds.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b2[0] + 20, b2[1] + 124), "* Can be weaponized against trailing pursuers or enemy squads.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"trap_card_{slug}.jpg")


# ===========================================================================
# 13. STATUS EFFECTS (BLEED, POISON, BUFFS & TREATMENT)
# ===========================================================================
def render_status_effect_card(effect_slug_or_name: str) -> str:
    """Render high-resolution status effect dossier."""
    clean = effect_slug_or_name.lower().replace(" ", "-").replace("'", "")
    conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
    c = conn.cursor()
    c.execute("SELECT slug, name, category, effect_type FROM status_effects_full WHERE slug LIKE ? OR name LIKE ? LIMIT 1",
              (f"%{clean}%", f"%{effect_slug_or_name}%"))
    row = c.fetchone()
    conn.close()

    if not row:
        row = ("light-bleed", "Light Bleed", "Status Effect", "Light Bleed Bleed Timed Affects Damage Bleed Timed x1 Damage")

    slug, name, cat, eff_type = row
    theme_color = core.PRIO_PURPLE

    canvas, draw = create_base_canvas(f"STATUS EFFECT : {name.upper()}", tag="COMBAT MODIFIER", border_col=theme_color)
    CARD_W, CARD_H = canvas.size

    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_color, width=2)
    draw.text((left_box[0] + 24, left_box[1] + 24), "COMBAT CONDITION", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 70), name.upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 120), f"Category : {cat}", fill=core.COLOR_GOLD, font=core.F_BODY)

    rx = 404
    rw = CARD_W - 28 - rx

    b1 = [rx, 86, rx + rw, 230]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=theme_color, width=1)
    draw.text((b1[0] + 20, b1[1] + 16), "MECHANICS & DAMAGE DYNAMICS", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((b1[0] + 20, b1[1] + 52), eff_type[:60], fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b1[0] + 20, b1[1] + 86), "Drains health over duration; bypasses passive armor resistance.", fill=(200, 200, 180), font=core.F_BODY)

    b2 = [rx, 246, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b2, radius=8, fill=(22, 22, 28), outline=core.COLOR_GOLD, width=1)
    draw.text((b2[0] + 20, b2[1] + 16), "TREATMENT & MEDICAL PROTOCOL", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((b2[0] + 20, b2[1] + 56), "* Apply Clean Bandage immediately to stop hemorrhage.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b2[0] + 20, b2[1] + 90), "* Ingestion of Physician Ointment restores health recovery.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"status_card_{slug}.jpg")


# ===========================================================================
# 14. GATHERING NODES (CHANCE, YIELDS & LOCATIONS)
# ===========================================================================
def render_gathering_card(node_slug_or_name: str) -> str:
    """Render high-resolution gathering node reconnaissance card."""
    clean = node_slug_or_name.lower().replace(" ", "-").replace("'", "")
    conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
    c = conn.cursor()
    c.execute("SELECT slug, name, chance, yield_range FROM gathering_full WHERE slug LIKE ? OR name LIKE ? LIMIT 1",
              (f"%{clean}%", f"%{node_slug_or_name}%"))
    row = c.fetchone()
    conn.close()

    if not row:
        row = ("garlic-bulb", "Garlic Bulb", "90 %", "2-6")

    slug, name, chance, yield_r = row
    theme_color = (60, 160, 90)

    canvas, draw = create_base_canvas(f"GATHERING RECON : {name.upper()}", tag="RESOURCE HARVEST", border_col=theme_color)
    CARD_W, CARD_H = canvas.size

    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=(16, 26, 18), outline=theme_color, width=2)
    draw.text((left_box[0] + 24, left_box[1] + 24), "HARVESTABLE RESOURCE", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 70), name.upper(), fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((left_box[0] + 24, left_box[1] + 120), "Primary Habitats: Sarlat Farm, Garnier Fields, Sombre Forest", fill=(180, 220, 180), font=core.F_BODY)

    rx = 404
    rw = CARD_W - 28 - rx

    b1 = [rx, 86, rx + rw, 220]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=theme_color, width=1)
    draw.text((b1[0] + 20, b1[1] + 16), "NODE HARVEST METRICS", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((b1[0] + 20, b1[1] + 52), f"Success Rate : {chance}", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((b1[0] + 20, b1[1] + 86), f"Yield Range : {yield_r} Units Per Harvest", fill=(255, 215, 0), font=core.F_HEADER_TAG)

    b2 = [rx, 236, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b2, radius=8, fill=(22, 22, 28), outline=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((b2[0] + 20, b2[1] + 16), "CHATEAU PROFESSION UTILITY", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((b2[0] + 20, b2[1] + 56), "* Key ingredient for Cook profession stamina provisions.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b2[0] + 20, b2[1] + 90), "* Required for high-tier Artificer and Physician elixirs.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"gathering_card_{slug}.jpg")


# ===========================================================================
# 15. CONTAINERS & FIELD LOOT (SPOTS, VARIETY & TACTICS)
# ===========================================================================
def render_container_card(container_slug_or_name: str) -> str:
    """Render high-resolution container intel card."""
    clean = container_slug_or_name.lower().replace(" ", "-").replace("'", "")
    conn = sqlite3.connect(os.path.join(ROOT_DIR, "hunger_helper.db"))
    c = conn.cursor()
    c.execute("SELECT slug, name, spots, items_count FROM containers_full WHERE slug LIKE ? OR name LIKE ? LIMIT 1",
              (f"%{clean}%", f"%{container_slug_or_name}%"))
    row = c.fetchone()
    conn.close()

    if not row:
        row = ("munitions-crate", "Munitions Crate", 646, 9)

    slug, name, spots, items_count = row
    theme_color = core.COLOR_GOLD

    canvas, draw = create_base_canvas(f"CONTAINER INTEL : {name.upper()}", tag="LOOT RECON", border_col=theme_color)
    CARD_W, CARD_H = canvas.size

    left_box = [28, 86, 380, CARD_H - 28]
    draw.rounded_rectangle(left_box, radius=10, fill=core.BG_CARD, outline=theme_color, width=2)

    c_img_name = slug.replace("-", "_") + ".webp"
    c_img_p = os.path.join(ROOT_DIR, "assets", "containers", c_img_name)
    if os.path.exists(c_img_p):
        try:
            c_img = Image.open(c_img_p).convert("RGBA").resize((280, 280), Image.Resampling.LANCZOS)
            canvas.paste(c_img, (left_box[0] + 36, left_box[1] + 30), c_img)
        except Exception:
            pass

    draw.text((left_box[0] + 24, left_box[3] - 70), "CONTAINER CLASS : FIELD LOOT", fill=core.COLOR_GOLD, font=core.F_HEADER_TAG)

    rx = 404
    rw = CARD_W - 28 - rx

    b1 = [rx, 86, rx + rw, 220]
    draw.rounded_rectangle(b1, radius=8, fill=(22, 22, 28), outline=theme_color, width=1)
    draw.text((b1[0] + 20, b1[1] + 16), "SPAWN DISTRIBUTION", fill=theme_color, font=core.F_SECTION_TITLE)
    draw.text((b1[0] + 20, b1[1] + 52), f"Total World Spots : {spots} Locations", fill=core.COLOR_PARCHMENT, font=core.F_HEADER_TITLE)
    draw.text((b1[0] + 20, b1[1] + 86), f"Loot Pool Variety : {items_count} Unique Item Types", fill=(255, 215, 0), font=core.F_HEADER_TAG)

    b2 = [rx, 236, rx + rw, CARD_H - 28]
    draw.rounded_rectangle(b2, radius=8, fill=(22, 22, 28), outline=(60, 50, 35), width=1)
    draw.text((b2[0] + 20, b2[1] + 16), "TOP RAID MAPS & TACTICS", fill=core.COLOR_GOLD, font=core.F_SECTION_TITLE)
    draw.text((b2[0] + 20, b2[1] + 56), "* Sarlat Farm, Jacques Bridge, Sombre Forest, Chateau Catacombs.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)
    draw.text((b2[0] + 20, b2[1] + 90), "* Always prioritize searching munitions and strongboxes for high value schemas.", fill=core.COLOR_PARCHMENT, font=core.F_BODY)

    return save_and_sync(canvas, f"container_card_{slug}.jpg")
'''

with open(ENGINE_PATH, "w", encoding="utf-8") as f:
    f.write(content + new_renderers)

print("Updated universal_v8_engine.py with 5 new renderers successfully.")
