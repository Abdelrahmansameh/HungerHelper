# Design Plan for Hunger Companion Optimizer

## Overview
We will build a local **SQLite** database that mirrors the relevant data from `hunger-companion.com` (quests, NPCs, items, drop locations, raid maps). A **Python CLI** tool will query this database and produce an **optimized raid plan** per wipe, maximizing quests completed per raid while pre‑farming needed items.

## Data Sources
| Endpoint / Page | What it provides | Access method |
|-----------------|------------------|----------------|
| `/api/tracker`  | Currently tracked quests for a user (JSON). | HTTP GET (no auth needed for public data). |
| `/api/item-card/` | Item details, including drop locations and odds. | HTTP GET (JSON). |
| `/quests/tree`  | Full quest progression tree (HTML with `data-quest` attributes). | Scrape HTML, parse `data-quest` / `data-after`. |
| `/maps/*`       | Map identifiers for raid locations. | Scrape HTML, extract map IDs. |
| `/items/*`      | Item pages with loot tables. | Scrape HTML if API missing. |

## Database Schema (SQLite)
```sql
CREATE TABLE quests (
    id INTEGER PRIMARY KEY,
    slug TEXT UNIQUE,
    name TEXT,
    giver TEXT,
    prerequisite_slug TEXT,   -- NULL if none
    location TEXT,            -- Map name where quest starts / ends
    reward_item TEXT,
    reward_quantity INTEGER
);

CREATE TABLE quest_objectives (
    quest_id INTEGER REFERENCES quests(id),
    obj_id TEXT,               -- e.g. "a-warm-welcome|Character.NPC.Louis"
    description TEXT,
    required_item TEXT,        -- optional item needed for this objective
    UNIQUE(quest_id, obj_id)
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    slug TEXT UNIQUE,
    name TEXT,
    type TEXT,                 -- weapon, ammo, food, etc.
    rarity TEXT
);

CREATE TABLE item_drops (
    item_id INTEGER REFERENCES items(id),
    location TEXT,               -- map / container name
    drop_rate REAL,              -- probability (0‑1)
    source TEXT                  -- e.g. "container", "enemy"
);

CREATE TABLE maps (
    name TEXT PRIMARY KEY,
    region TEXT,
    raid_type TEXT               -- e.g. "Raid 1", "Raid 2"
);
```

## Extraction Pipeline (Python)
1. **Fetch quest tree** (`https://hunger-companion.com/quests/tree`).
   - Parse all `<a … data-quest="…" data-after="…" …>` elements.
   - Build a DAG of quests (edges from `after` → `quest`).
   - Store into `quests` and `quest_objectives` tables.
2. **Download each quest page** (e.g. `/quests/eloise/a-warm-welcome`).
   - Extract objectives, required items, NPCs.
   - Populate `quest_objectives`.
3. **Item data** – call `/api/item-card/` for each unique item slug discovered.
   - Populate `items` and `item_drops`.
4. **Map data** – scrape `/maps/*` pages to get raid identifiers.
5. **Persist** the data in `hunger_helper.db` under the workspace `c:\Users\PC\Documents\HungerHelper`.

## Optimizer Algorithm (CLI)
1. **Input**: list of target quests (e.g. all quests for a new wipe) – can be auto‑generated as “all leaf quests”.
2. **Dependency resolution**: walk the quest DAG to include all prerequisite quests.
3. **Item requirement aggregation**:
   - For each quest, collect needed items from its objectives.
   - Sum quantities across all selected quests.
4. **Location clustering**:
   - Group quests by the *raid map* where they are completed.
   - For each map, also list items that drop there (from `item_drops`).
5. **Route generation**:
   - For each map, compute a “farm list” of items that can be collected on the way, respecting drop odds (suggest gathering the most probable items first).
   - Output a step‑by‑step plan: *Raid X → Quest A → Quest B → Farm Item Y → …*.
6. **Scoring**: simple heuristic – maximize `quests_completed / raid_time` where raid time is approximated by the number of quests plus number of distinct item farms.
   - Provide alternative routes if user wants more aggressive farming.

## CLI Usage Example
```
$ python hunger_optimizer.py --new-wipe
Generating full quest list …
Optimized routes:

Raid 1 – Château
  1. Quest: A Warm Welcome (Eloise)
  2. Quest: Making Dough (Eloise)
  3. Quest: The Gavroche Family (Eloise)
  Farm items: Brown Betty (70% @ Château), Crude Ammunition (45% @ Château)

Raid 2 – Sombre Forest
  …
```

## Next Steps / Decisions Needed
- **Programming language**: Python (recommended) or Node/TS?
- **User interface**: pure terminal, or simple web UI (Flask)?
- **Refresh schedule**: run a nightly script to re‑scrape data? (could use `/schedule` slash command.)
- **Authentication**: Some API endpoints may require a session cookie for full data. Do we need to support logging in?
- **Optimization depth**: Simple greedy grouping vs. full combinatorial search (could be added later).

---
**Please let me know**:
1. Preferred language / runtime.
2. Whether you want a CLI only or also a minimal web UI.
3. If you’d like the optimizer to run automatically each day (we can set up a scheduled background task).
4. Any constraints on storage size or external libraries.

Once we have those specs, I can start scaffolding the project structure and implement the first data‑import script.
