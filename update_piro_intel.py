import sqlite3, json

conn = sqlite3.connect('hunger_helper.db')
cur = conn.cursor()

raw_json = json.dumps({
    "name": "Piro's Lens",
    "name_fr": "Lentille de Piro",
    "rarity": "Uncommon",
    "category": "Quest Item",
    "lore": "A finely crafted optical monocle lens belonging to Piro, lost in the infested ruins.",
    "quests": ["Seeing Clearly"],
    "location": "Jacques Bridge - Rat's Nest Cave (X: 1491.15, Y: 3535.74)"
})

cur.execute("""
    INSERT OR REPLACE INTO companion_items_cache 
    (slug, name_en, name_fr, category, rarity, lore_desc, usage_desc, base_value, sell_silver, sell_copper, max_stack, best_container, best_creature, vendor_buy, quests_needed, image_filename, raw_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "piro-s-lens",
    "Piro's Lens",
    "Lentille de Piro",
    "Quest Item",
    "Uncommon",
    "A finely crafted optical monocle lens belonging to Piro, lost in the infested ruins.",
    "Required for quest 'Seeing Clearly' (Giver: Piro). Keep in Secure Pouch!",
    1, 0, 1, 1,
    "Rat's Nest Cave (Jacques Bridge)",
    "X: 1491.15, Y: 3535.74 (Cave Entrance X: 1602, Y: 3552)",
    "Quest Exclusive (Giver: Piro)",
    '["Seeing Clearly"]',
    "T_UI_Item_PirosLens.png",
    raw_json
))

conn.commit()
print("Updated Piro's Lens in companion_items_cache!")
