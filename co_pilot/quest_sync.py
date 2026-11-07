import sqlite3
import re
from typing import Dict, List, Optional, Tuple, Any

DB_PATH = "hunger_helper.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def sync_player_quests(user_id: str, display_name: str, active_quest_names_or_slugs: List[str]):
    """
    Syncs player quest state:
    - Sets active quests to 'in_progress'
    - Traverses prerequisite_slug backwards to mark predecessors as 'completed'
    - Identifies next upcoming quests in the chain
    - Updates user_tracked_items with required items for active & upcoming quests
    """
    conn = get_db()
    c = conn.cursor()

    # Ensure user exists in user_profiles
    c.execute("""
        INSERT INTO user_profiles (user_id, display_name, level, updated_at)
        VALUES (?, ?, 100, datetime('now'))
        ON CONFLICT(user_id) DO UPDATE SET display_name = ?, updated_at = datetime('now')
    """, (user_id, display_name, display_name))

    # Match quest names/slugs in DB
    c.execute("SELECT id, slug, name, giver, prerequisite_slug FROM quests")
    all_quests = {q["slug"]: dict(q) for q in c.fetchall()}

    matched_active_slugs = set()
    for cand in active_quest_names_or_slugs:
        cand_low = cand.lower().strip()
        for slug, q in all_quests.items():
            if slug == cand_low or q["name"].lower() == cand_low or cand_low in q["name"].lower():
                matched_active_slugs.add(slug)
                break

    # Backward traversal to mark completed
    completed_slugs = set()
    for act_slug in matched_active_slugs:
        curr = all_quests.get(act_slug)
        while curr and curr.get("prerequisite_slug"):
            pre_slug = curr["prerequisite_slug"]
            if pre_slug in all_quests:
                completed_slugs.add(pre_slug)
                curr = all_quests[pre_slug]
            else:
                break

    # Forward check for upcoming
    upcoming_slugs = set()
    for slug, q in all_quests.items():
        if q.get("prerequisite_slug") in matched_active_slugs and slug not in matched_active_slugs:
            upcoming_slugs.add(slug)

    # Save to user_quests
    for slug in completed_slugs:
        c.execute("""
            INSERT INTO user_quests (user_id, quest_slug, status, updated_at)
            VALUES (?, ?, 'completed', datetime('now'))
            ON CONFLICT(user_id, quest_slug) DO UPDATE SET status = 'completed', updated_at = datetime('now')
        """, (user_id, slug))

    for slug in matched_active_slugs:
        c.execute("""
            INSERT INTO user_quests (user_id, quest_slug, status, updated_at)
            VALUES (?, ?, 'active', datetime('now'))
            ON CONFLICT(user_id, quest_slug) DO UPDATE SET status = 'active', updated_at = datetime('now')
        """, (user_id, slug))

    for slug in upcoming_slugs:
        c.execute("""
            INSERT INTO user_quests (user_id, quest_slug, status, updated_at)
            VALUES (?, ?, 'available', datetime('now'))
            ON CONFLICT(user_id, quest_slug) DO UPDATE SET status = 'available', updated_at = datetime('now')
        """, (user_id, slug))

    # Clear old tracked items for this user and repopulate
    c.execute("DELETE FROM user_tracked_items WHERE user_id = ?", (user_id,))

    # Find required items for active and upcoming quests
    relevant_slugs = list(matched_active_slugs) + list(upcoming_slugs)
    if relevant_slugs:
        placeholders = ",".join("?" * len(relevant_slugs))
        c.execute(f"""
            SELECT qo.required_item, qo.description, q.name as quest_name, uq.status
            FROM quest_objectives qo
            JOIN quests q ON qo.quest_id = q.id
            JOIN user_quests uq ON q.slug = uq.quest_slug AND uq.user_id = ?
            WHERE q.slug IN ({placeholders}) AND qo.required_item IS NOT NULL
        """, [user_id] + relevant_slugs)
        
        for row in c.fetchall():
            it_slug = row["required_item"]
            desc = row["description"]
            q_name = row["quest_name"]
            status = row["status"]
            # Extract quantity from description like 'Find 3xWindfall' or '10x'
            m_qty = re.search(r"(\d+)\s*x", desc, re.I)
            qty = int(m_qty.group(1)) if m_qty else 1
            it_name = it_slug.replace("-", " ").title()

            c.execute("""
                INSERT INTO user_tracked_items (user_id, item_slug, item_name, target_count, current_count, notes)
                VALUES (?, ?, ?, ?, 0, ?)
            """, (user_id, it_slug, it_name, qty, f"Pour '{q_name}' ({status})"))

    conn.commit()
    conn.close()
    return {
        "active": list(matched_active_slugs),
        "completed": list(completed_slugs),
        "upcoming": list(upcoming_slugs)
    }

def check_player_item_need(query_user_id_or_name: str, item_query: str) -> Dict[str, Any]:
    """Checks whether a specific player or anyone in the squad needs an item."""
    conn = get_db()
    c = conn.cursor()

    # Find user
    c.execute("SELECT user_id, display_name FROM user_profiles WHERE user_id = ? OR lower(display_name) LIKE ?", 
              (query_user_id_or_name, f"%{query_user_id_or_name.lower()}%"))
    u_row = c.fetchone()
    if not u_row:
        # Check all tracked items if user not found
        target_uid = None
        user_name = query_user_id_or_name
    else:
        target_uid = u_row["user_id"]
        user_name = u_row["display_name"]

    item_clean = item_query.lower().strip()
    
    # Query tracked items
    if target_uid:
        c.execute("""
            SELECT item_name, target_count, notes 
            FROM user_tracked_items 
            WHERE user_id = ? AND (lower(item_slug) LIKE ? OR lower(item_name) LIKE ?)
        """, (target_uid, f"%{item_clean}%", f"%{item_clean}%"))
        rows = c.fetchall()
    else:
        c.execute("""
            SELECT ut.item_name, ut.target_count, ut.notes, up.display_name 
            FROM user_tracked_items ut
            JOIN user_profiles up ON ut.user_id = up.user_id
            WHERE lower(ut.item_slug) LIKE ? OR lower(ut.item_name) LIKE ?
        """, (f"%{item_clean}%", f"%{item_clean}%"))
        rows = c.fetchall()

    conn.close()

    if rows:
        needs = []
        for r in rows:
            u_disp = r["display_name"] if "display_name" in r.keys() else user_name
            needs.append(f"• **{u_disp}** : {r['target_count']}x **{r['item_name']}** ({r['notes']})")
        return {
            "needed": True,
            "message": "\n".join(needs)
        }
    else:
        return {
            "needed": False,
            "message": f"Non, {user_name} n'a pas besoin de '{item_query}' pour ses quêtes actuelles ou à venir."
        }

if __name__ == "__main__":
    # Test syncing Abdallah with Making Dough and A Bitter Draught
    res = sync_player_quests("abdallah_123", "Abdallah", ["making dough", "a-bitter-draught"])
    print("Sync result:", res)

    # Check if Abdallah needs flour
    need1 = check_player_item_need("Abdallah", "flour")
    print("Need Flour:", need1)

    # Check if Abdallah needs bezoar
    need2 = check_player_item_need("Abdallah", "bezoar")
    print("Need Bezoar:", need2)

    # Check if Abdallah needs something random
    need3 = check_player_item_need("Abdallah", "salpetre")
    print("Need Salpetre:", need3)
