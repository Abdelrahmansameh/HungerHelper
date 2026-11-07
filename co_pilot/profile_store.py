import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from co_pilot.knowledge_db import get_connection, search_quests, search_talents

def init_profile_db():
    """Ensure user profile and progression tables exist."""
    conn = get_connection()
    c = conn.cursor()
    
    # User Profile table
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            notes TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # User Quests progression
    # status: 'available', 'active', 'completed'
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_quests (
            user_id TEXT NOT NULL,
            quest_slug TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('available', 'active', 'completed')),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, quest_slug),
            FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
        )
    """)
    
    # User Talents
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_talents (
            user_id TEXT NOT NULL,
            talent_id TEXT NOT NULL,
            allocated_points INTEGER DEFAULT 1,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, talent_id),
            FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
        )
    """)
    
    # Custom Item Wishlist / Stash tracking
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_tracked_items (
            user_id TEXT NOT NULL,
            item_slug TEXT NOT NULL,
            item_name TEXT NOT NULL,
            target_count INTEGER DEFAULT 1,
            current_count INTEGER DEFAULT 0,
            notes TEXT,
            PRIMARY KEY (user_id, item_slug),
            FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
        )
    """)
    
    conn.commit()
    conn.close()

def get_or_create_profile(user_id: str, display_name: str = "Player") -> Dict[str, Any]:
    """Retrieve user profile or initialize a fresh profile."""
    init_profile_db()
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT user_id, display_name, level, notes FROM user_profiles WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        c.execute("""
            INSERT INTO user_profiles (user_id, display_name, level)
            VALUES (?, ?, 1)
        """, (user_id, display_name))
        
        # Initialize root quests (quests with no prerequisites) as 'available'
        c.execute("""
            SELECT slug FROM quests WHERE prerequisite_slug IS NULL OR prerequisite_slug = ''
        """)
        root_quests = [r["slug"] for r in c.fetchall()]
        for slug in root_quests:
            c.execute("""
                INSERT OR IGNORE INTO user_quests (user_id, quest_slug, status)
                VALUES (?, ?, 'available')
            """, (user_id, slug))
            
        conn.commit()
        profile = {"user_id": user_id, "display_name": display_name, "level": 1, "notes": None}
    else:
        profile = dict(row)
        
    conn.close()
    return profile

def update_user_level(user_id: str, new_level: int) -> int:
    """Update player level."""
    get_or_create_profile(user_id)
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE user_profiles 
        SET level = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE user_id = ?
    """, (new_level, user_id))
    conn.commit()
    conn.close()
    return new_level

def set_quest_status(user_id: str, quest_query: str, new_status: str) -> Dict[str, Any]:
    """
    Set quest status to 'active' or 'completed'.
    When 'completed', automatically unlocks follow-up quests.
    """
    get_or_create_profile(user_id)
    # Match quest
    matches = search_quests(quest_query, limit=1)
    if not matches:
        return {"success": False, "message": f"Could not find any quest matching '{quest_query}'"}
    
    quest = matches[0]
    quest_slug = quest["slug"]
    quest_name = quest["name"]
    
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("""
        INSERT INTO user_quests (user_id, quest_slug, status, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id, quest_slug) DO UPDATE SET 
            status = excluded.status,
            updated_at = CURRENT_TIMESTAMP
    """, (user_id, quest_slug, new_status))
    
    unlocked = []
    if new_status == "completed":
        # Find follow-up quests where this quest is prerequisite
        c.execute("SELECT slug, name FROM quests WHERE prerequisite_slug = ?", (quest_slug,))
        follow_ups = c.fetchall()
        for f in follow_ups:
            f_slug = f["slug"]
            c.execute("""
                INSERT OR IGNORE INTO user_quests (user_id, quest_slug, status)
                VALUES (?, ?, 'available')
            """, (user_id, f_slug))
            unlocked.append(f["name"])
            
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "quest_slug": quest_slug,
        "quest_name": quest_name,
        "status": new_status,
        "unlocked_quests": unlocked
    }

def allocate_talent_points(user_id: str, talent_query: str, points: int = 1) -> Dict[str, Any]:
    """Allocate talent points to a talent node."""
    get_or_create_profile(user_id)
    matches = search_talents(talent_query, limit=1)
    if not matches:
        return {"success": False, "message": f"Could not find any talent matching '{talent_query}'"}
        
    t = matches[0]
    t_id = t["id"]
    t_name = t["name"]
    max_pts = t["max_points"]
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT allocated_points FROM user_talents WHERE user_id = ? AND talent_id = ?", (user_id, t_id))
    row = c.fetchone()
    current_pts = row["allocated_points"] if row else 0
    new_pts = min(max_pts, current_pts + points)
    
    c.execute("""
        INSERT INTO user_talents (user_id, talent_id, allocated_points, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id, talent_id) DO UPDATE SET
            allocated_points = excluded.allocated_points,
            updated_at = CURRENT_TIMESTAMP
    """, (user_id, t_id, new_pts))
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "talent_id": t_id,
        "talent_name": t_name,
        "points": new_pts,
        "max_points": max_pts,
        "mastery": t["mastery_name"]
    }

def get_user_progression_summary(user_id: str) -> Dict[str, Any]:
    """Get full progression summary for voice prompt context."""
    profile = get_or_create_profile(user_id)
    conn = get_connection()
    c = conn.cursor()
    
    # Active quests
    c.execute("""
        SELECT q.slug, q.name, q.giver, q.location
        FROM user_quests uq
        JOIN quests q ON uq.quest_slug = q.slug
        WHERE uq.user_id = ? AND uq.status = 'active'
    """, (user_id,))
    active_quests = [dict(r) for r in c.fetchall()]
    
    # Completed quests count
    c.execute("SELECT count(*) FROM user_quests WHERE user_id = ? AND status = 'completed'", (user_id,))
    completed_count = c.fetchone()[0]
    
    # Available next quests
    c.execute("""
        SELECT q.slug, q.name, q.giver, q.location
        FROM user_quests uq
        JOIN quests q ON uq.quest_slug = q.slug
        WHERE uq.user_id = ? AND uq.status = 'available'
        LIMIT 10
    """, (user_id,))
    available_quests = [dict(r) for r in c.fetchall()]
    
    # Talents
    c.execute("""
        SELECT t.name, t.mastery_slug, m.name as mastery_name, ut.allocated_points, t.max_points
        FROM user_talents ut
        JOIN talents t ON ut.talent_id = t.id
        JOIN masteries m ON t.mastery_slug = m.slug
        WHERE ut.user_id = ? AND ut.allocated_points > 0
    """, (user_id,))
    talents = [dict(r) for r in c.fetchall()]
    
    conn.close()
    
    return {
        "user_id": user_id,
        "display_name": profile["display_name"],
        "level": profile["level"],
        "active_quests": active_quests,
        "available_quests": available_quests,
        "completed_count": completed_count,
        "talents": talents
    }

def get_needed_quest_items(user_id: str) -> List[Dict[str, Any]]:
    """
    Get items needed for all of the player's active quests,
    indicating whether each item can be bought from a merchant or must be looted.
    """
    summary = get_user_progression_summary(user_id)
    active_slugs = [q["slug"] for q in summary["active_quests"]]
    if not active_slugs:
        return []
        
    conn = get_connection()
    c = conn.cursor()
    
    placeholders = ",".join("?" for _ in active_slugs)
    c.execute(f"""
        SELECT DISTINCT q.name as quest_name, qo.description, qo.required_item
        FROM quest_objectives qo
        JOIN quests q ON qo.quest_id = q.id
        WHERE q.slug IN ({placeholders}) AND qo.required_item IS NOT NULL AND qo.required_item != ''
    """, active_slugs)
    
    needed = []
    for r in c.fetchall():
        item_slug = r["required_item"]
        c.execute("""
            SELECT npc_slug, item_name, price_copper, price_silver, category 
            FROM npc_items 
            WHERE item_name LIKE ? OR npc_slug LIKE ?
        """, (f"%{item_slug.replace('-', ' ')}%", f"%{item_slug}%"))
        merchants = [dict(m) for m in c.fetchall()]
        
        needed.append({
            "quest_name": r["quest_name"],
            "description": r["description"],
            "item_slug": item_slug,
            "merchants": merchants,
            "buyable_in_town": len(merchants) > 0
        })
        
    conn.close()
    return needed

if __name__ == "__main__":
    init_profile_db()
    test_user = "test_player_42"
    print(f"Initializing profile for {test_user}...")
    p = get_or_create_profile(test_user, "Alex")
    print("Initial profile:", p)
    
    # Mark 'A Warm Welcome' active, then complete
    res = set_quest_status(test_user, "A Warm Welcome", "completed")
    print("\nCompleted quest result:")
    print("Status:", res["status"])
    print("Unlocked quests:", res["unlocked_quests"])
    
    # Allocate talent
    t_res = allocate_talent_points(test_user, "Discerning", 2)
    print("\nAllocated talent:", t_res)
    
    # Set level
    update_user_level(test_user, 5)
    
    # Summary
    summary = get_user_progression_summary(test_user)
    print("\nProgression Summary:")
    print(f"Player: {summary['display_name']} (Lvl {summary['level']})")
    print(f"Completed Quests: {summary['completed_count']}")
    print(f"Available Quests: {[q['name'] for q in summary['available_quests']]}")
    print(f"Talents: {[f'{t['name']} ({t['allocated_points']}/{t['max_points']})' for t in summary['talents']]}")
