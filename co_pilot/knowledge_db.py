import sqlite3
import json
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hunger_helper.db"))
MASTERY_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mastery_data.json"))

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_knowledge_db():
    """Ensure talent/mastery tables exist and are populated from mastery_data.json."""
    conn = get_connection()
    c = conn.cursor()
    
    # Masteries table
    c.execute("""
        CREATE TABLE IF NOT EXISTS masteries (
            slug TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            color TEXT
        )
    """)
    
    # Talents table
    c.execute("""
        CREATE TABLE IF NOT EXISTS talents (
            id TEXT PRIMARY KEY,
            mastery_slug TEXT NOT NULL,
            tier INTEGER NOT NULL,
            name TEXT NOT NULL,
            desc TEXT,
            max_points INTEGER DEFAULT 1,
            node_order INTEGER DEFAULT 0,
            icon TEXT,
            values_json TEXT,
            req_id TEXT,
            req_pts INTEGER DEFAULT 0,
            FOREIGN KEY (mastery_slug) REFERENCES masteries(slug)
        )
    """)
    
    # Check if talents populated
    c.execute("SELECT count(*) FROM talents")
    if c.fetchone()[0] == 0 and os.path.exists(MASTERY_JSON):
        with open(MASTERY_JSON, "r", encoding="utf-8") as f:
            masteries_data = json.load(f)
        
        for m in masteries_data:
            c.execute("INSERT OR REPLACE INTO masteries (slug, name, color) VALUES (?, ?, ?)",
                      (m["slug"], m["name"], m.get("color")))
            for t in m.get("tiers", []):
                tier_idx = t.get("tier", 0)
                for node in t.get("nodes", []):
                    c.execute("""
                        INSERT OR REPLACE INTO talents 
                        (id, mastery_slug, tier, name, desc, max_points, node_order, icon, values_json, req_id, req_pts)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        node["id"],
                        m["slug"],
                        tier_idx,
                        node["name"],
                        node.get("desc"),
                        node.get("max", 1),
                        node.get("order", 0),
                        node.get("icon"),
                        json.dumps(node.get("values")) if node.get("values") else None,
                        node.get("reqId"),
                        node.get("reqPts", 0)
                    ))
        conn.commit()
    conn.close()

# ----------------- SEARCH & QUERY FUNCTIONS -----------------

def search_items(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search items and find all sources (drops, merchants) and quest usages."""
    cleaned_q = query.strip().lower()
    if cleaned_q in ["hand", "hands", "main", "mains", "melee", "weapon", "weapons", "arme", "armes"]:
        return []
    conn = get_connection()
    c = conn.cursor()
    q = f"%{query}%"
    
    c.execute("""
        SELECT slug, name, type, rarity 
        FROM items 
        WHERE name LIKE ? OR slug LIKE ?
        LIMIT ?
    """, (q, q, limit))
    items = [dict(r) for r in c.fetchall()]
    
    for item in items:
        # Drops
        c.execute("SELECT location, drop_rate, source FROM item_drops WHERE item_id = ?", (item["slug"],))
        item["drops"] = [dict(r) for r in c.fetchall()]
        
        # Merchants
        c.execute("""
            SELECT npc_slug, item_name, price_copper, price_silver, category 
            FROM npc_items 
            WHERE item_name LIKE ?
        """, (f"%{item['name']}%",))
        item["merchants"] = [dict(r) for r in c.fetchall()]
        
        # Quests requiring this item
        c.execute("""
            SELECT q.name AS quest_name, q.giver, qo.description 
            FROM quest_objectives qo
            JOIN quests q ON qo.quest_id = q.id
            WHERE qo.required_item LIKE ? OR qo.description LIKE ?
        """, (f"%{item['slug']}%", f"%{item['name']}%"))
        item["used_in_quests"] = [dict(r) for r in c.fetchall()]
        
    conn.close()
    return items

def search_quests(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search quests by title, slug, giver, or location."""
    conn = get_connection()
    c = conn.cursor()
    q = f"%{query}%"
    
    c.execute("""
        SELECT id, slug, name, giver, prerequisite_slug, location, reward_item, reward_quantity
        FROM quests
        WHERE name LIKE ? OR slug LIKE ? OR giver LIKE ?
        LIMIT ?
    """, (q, q, q, limit))
    quests = [dict(r) for r in c.fetchall()]
    
    for quest in quests:
        # Objectives
        c.execute("""
            SELECT obj_id, description, required_item 
            FROM quest_objectives 
            WHERE quest_id = ?
        """, (quest["id"],))
        quest["objectives"] = [dict(r) for r in c.fetchall()]
        
        # Map Points / Coordinates
        c.execute("""
            SELECT map_name, point_type, title, x, y, description
            FROM map_points
            WHERE quest_slug = ? OR title LIKE ?
        """, (quest["slug"], f"%{quest['name']}%"))
        quest["map_points"] = [dict(r) for r in c.fetchall()]
        
        # Prerequisite name if available
        if quest.get("prerequisite_slug"):
            c.execute("SELECT name FROM quests WHERE slug = ?", (quest["prerequisite_slug"],))
            prereq_row = c.fetchone()
            quest["prerequisite_name"] = prereq_row["name"] if prereq_row else quest["prerequisite_slug"]
        else:
            quest["prerequisite_name"] = None
            
        # Follow-up quests
        c.execute("SELECT slug, name FROM quests WHERE prerequisite_slug = ?", (quest["slug"],))
        quest["unlocks_quests"] = [dict(r) for r in c.fetchall()]
        
    conn.close()
    return quests

def search_talents(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search talents by name, mastery tree, or description."""
    init_knowledge_db()
    conn = get_connection()
    c = conn.cursor()
    q = f"%{query}%"
    
    c.execute("""
        SELECT t.id, t.mastery_slug, m.name AS mastery_name, t.tier, t.name, t.desc, 
               t.max_points, t.values_json, t.req_pts
        FROM talents t
        JOIN masteries m ON t.mastery_slug = m.slug
        WHERE t.name LIKE ? OR t.desc LIKE ? OR m.name LIKE ?
        LIMIT ?
    """, (q, q, q, limit))
    talents = [dict(r) for r in c.fetchall()]
    conn.close()
    return talents

def search_npcs(query: str) -> List[Dict[str, Any]]:
    """Search NPC roles, locations, and inventories."""
    conn = get_connection()
    c = conn.cursor()
    q = f"%{query}%"
    
    c.execute("""
        SELECT id, slug, name, location, role, description
        FROM npcs
        WHERE name LIKE ? OR slug LIKE ? OR role LIKE ?
    """, (q, q, q))
    npcs = [dict(r) for r in c.fetchall()]
    
    for npc in npcs:
        c.execute("""
            SELECT item_name, price_copper, price_silver, category
            FROM npc_items
            WHERE npc_slug = ?
        """, (npc["slug"],))
        npc["shop_inventory"] = [dict(r) for r in c.fetchall()]
        
    conn.close()
    return npcs

def get_map_objectives(map_name: str, quest_slugs: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Get all relevant points of interest/objectives on a given map."""
    conn = get_connection()
    c = conn.cursor()
    
    if quest_slugs:
        placeholders = ",".join("?" for _ in quest_slugs)
        query = f"""
            SELECT id, title, map_name, point_type, quest_slug, x, y, description
            FROM map_points
            WHERE map_name LIKE ? AND quest_slug IN ({placeholders})
        """
        params = [f"%{map_name}%"] + quest_slugs
    else:
        query = """
            SELECT id, title, map_name, point_type, quest_slug, x, y, description
            FROM map_points
            WHERE map_name LIKE ?
            LIMIT 100
        """
        params = [f"%{map_name}%"]
        
    c.execute(query, params)
    points = [dict(r) for r in c.fetchall()]
    conn.close()
    return points

if __name__ == "__main__":
    init_knowledge_db()
    print("Testing Knowledge DB queries...")
    print("\n--- Search Quest 'warm welcome' ---")
    quests = search_quests("warm welcome")
    for q in quests:
        print(f"Quest: {q['name']} (Giver: {q['giver']})")
        print(f"  Objectives: {len(q['objectives'])}")
        print(f"  Unlocks: {[u['name'] for u in q['unlocks_quests']]}")
        
    print("\n--- Search Talent 'discerning' ---")
    talents = search_talents("discerning")
    for t in talents:
        print(f"Talent: {t['name']} ({t['mastery_name']} Tier {t['tier']}) - Max: {t['max_points']}")
        print(f"  Desc: {t['desc']}")
        
    print("\n--- Search Item 'honey' ---")
    items = search_items("honey")
    for it in items:
        print(f"Item: {it['name']} ({it['type']}, {it['rarity']})")
        print(f"  Used in: {[u['quest_name'] for u in it['used_in_quests']]}")
