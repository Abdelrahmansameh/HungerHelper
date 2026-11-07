import json
import sqlite3

with open("data/all_hunger_items_cards.json", "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Total items in all_hunger_items_cards.json: {len(items)}")

# Category map to human friendly
cat_names = {
    "weapon": "Weapons",
    "armour": "Armour",
    "bag": "Bags",
    "medicine": "Medicine",
    "food": "Food & Rations",
    "drink": "Beverages",
    "trinket": "Trinkets & Curios",
    "tool": "Tools",
    "ammunition": "Ammunition",
    "material": "Materials & Loot",
    "schema": "Schemas & Recipes",
    "quest_item": "Quest Items",
    "key": "Keys",
    "cosmetic": "Cosmetics",
    "currency": "Currency",
    "misc": "Misc"
}

# Connect to DB and update
conn = sqlite3.connect("hunger_helper.db")
c = conn.cursor()

# Ensure schema columns
c.execute("PRAGMA table_info(companion_items_cache)")
cols = [r[1] for r in c.fetchall()]
print("Cache table columns:", cols)

# Populate items table and companion_items_cache
inserted_items = 0
inserted_cache = 0

for slug, data in items.items():
    title = data.get("t", slug.replace("-", " ").title())
    rarity = data.get("r", "common").title()
    cat_code = data.get("c", "material")
    category = cat_names.get(cat_code, cat_code.title())
    sell_value = data.get("v", 0) # in copper
    
    # Calculate silver and copper
    # In Hunger: 1 silver = 100 copper, 1 gold = 100 silver = 10000 copper
    sell_silver = (sell_value % 10000) // 100
    sell_copper = sell_value % 100
    if sell_value >= 10000:
        sell_silver += (sell_value // 10000) * 100

    # 1. Insert or ignore into items table
    c.execute("""
        INSERT INTO items (slug, name, type, rarity)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(slug) DO UPDATE SET
            name = excluded.name,
            type = excluded.type,
            rarity = excluded.rarity
    """, (slug, title, cat_code, rarity.lower()))
    inserted_items += 1

    # 2. Determine best drop intel / placed loot / mob drop
    desc = f"Official {rarity} {category} item discovered during expeditions in The Hunger."
    best_source = "Expedition Loot Containers"
    vendor_buy = "Not sold by vendors (Raid loot exclusive)"
    
    # Specific known high-rate items
    if "peasant-s-burden" in slug:
        category = "Cosmetic Schema (Spear)"
        desc = "Discover this Schema whilst in the Chateau to add Peasant's Burden to your Appearance menu."
        best_source = "Dreg Farmer (Always 100% Drop) · Garnier's Farm, Sarlat Farm"
        vendor_buy = "Not sold by vendors (Raid drop exclusive · Sells for 18c)"
    elif "bacchus-wand" in slug:
        category = "Cosmetic Schema (Longboy)"
        desc = "Epic weapon skin schema for the Longboy rifle. Forged at Chateau Artisan Workshop."
        best_source = "Elite Raid Safes & Scavenger Caches"
        vendor_buy = "Not sold by vendors (Sells for 2s 10c)"
    elif "solstice-vepr" in slug:
        category = "Cosmetic Schema (Vepr)"
        desc = "Epic weapon skin schema for the Vepr shotgun."
        best_source = "Elite Weapon Caches & Boss Encounters"
        vendor_buy = "Not sold by vendors (Sells for 21s 61c)"
    elif "metallurgist-recipe-spear" in slug:
        category = "Crafting Recipe (Spear Lv 185)"
        desc = "Unlocks crafting recipe for Spear (Lv 185) at the Chateau Metallurgist."
        best_source = "Placed World Loot: Sarlat Farm (Dupo Farrier) · 1/6.7 (14.9%)"
        vendor_buy = "Henri (Chateau Hub) · 92 Silver (Sells for 9s 20c)"
    elif "metallurgist-recipe" in slug:
        category = "Crafting Recipe (Weapons)"
        desc = f"Unlocks weapon forging recipe at Chateau Metallurgist."
        best_source = "Placed World Loot in Workshop / Forge Ruins (High Rate)"
        vendor_buy = "Henri (Chateau Hub)"
    elif "gunsmith-recipe" in slug:
        category = "Crafting Recipe (Firearms)"
        desc = f"Unlocks firearm crafting recipe at Chateau Gunsmith."
        best_source = "Placed World Loot in Armory / Garrison Ruins (High Rate)"
        vendor_buy = "Voyant the Rifleman (Chateau Hub)"
    elif "cook-recipe" in slug:
        category = "Cooking Recipe (Provisions)"
        desc = f"Unlocks culinary recipe at Chateau Kitchens."
        best_source = "Placed World Loot in Kitchen / Manor Cabinets"
        vendor_buy = "Reynauld (Chateau Hub)"
    elif "heavy-ammunition" in slug:
        category = "Ammunition"
        desc = "Dense military shot for high-caliber pistols and rifles."
        best_source = "Munitions Crates (High Rate) · Sarlat Farm, Jacques Bridge"
        vendor_buy = "Voyant the Rifleman, Piro, Reynauld (0s 2c)"
    elif "piro-s-lens" in slug:
        category = "Quest Item"
        desc = "Piro's lost optical monocle lens required for quest Seeing Clearly."
        best_source = "Rat's Nest Cave (Jacques Bridge South-East ruins · X: 1491, Y: 3535)"
        vendor_buy = "Not sold by vendors (Quest Exclusive · Safe Pouch)"
    elif cat_code == "key":
        desc = f"Key opening locked doors, crypts, or gates in expedition raids."
        best_source = "Key Spawns & Elite Scavengers (1/8.2)"
    elif cat_code == "quest_item":
        desc = f"Special mission objective item. Keep in your Secure Pouch!"
        best_source = "Dedicated Quest Location / Fixed Objective"

    # Insert or replace into companion_items_cache
    c.execute("""
        INSERT INTO companion_items_cache (
            slug, name_en, name_fr, category, rarity, lore_desc, usage_desc,
            base_value, sell_silver, sell_copper, best_container, vendor_buy
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(slug) DO UPDATE SET
            name_en = excluded.name_en,
            name_fr = excluded.name_fr,
            category = excluded.category,
            rarity = excluded.rarity,
            lore_desc = excluded.lore_desc,
            base_value = excluded.base_value,
            sell_silver = excluded.sell_silver,
            sell_copper = excluded.sell_copper,
            best_container = excluded.best_container,
            vendor_buy = excluded.vendor_buy
    """, (
        slug, title, title, category, rarity, desc,
        f"Used in expeditions, crafting at Chateau, or sold for {sell_silver}s {sell_copper}c.",
        sell_value, sell_silver, sell_copper, best_source, vendor_buy
    ))
    inserted_cache += 1

conn.commit()

c.execute("SELECT COUNT(*) FROM items")
total_items = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM companion_items_cache")
total_cache = c.fetchone()[0]

conn.close()

print(f"Successfully populated database!")
print(f"Total items in items table: {total_items}")
print(f"Total items in companion_items_cache: {total_cache}")
