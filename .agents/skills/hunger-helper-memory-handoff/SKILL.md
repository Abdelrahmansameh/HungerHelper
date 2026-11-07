---
name: hunger-helper-memory-handoff
description: >-
  Maintains permanent memory, historical prompt chronicle, context continuity,
  and session handoffs for the Hunger Helper / Eloise Tactical Assistant codebase.
  Use this skill whenever starting a new session, when context has been summarized or
  truncated, when verifying historical user instructions, or when handing off work
  to ensure all prior user requirements, data rules, and regression tests are strictly preserved.
---

# Hunger Helper Memory & Session Handoff Skill

This skill guarantees that **no instruction, critique, screenshot detail, or requirement from the user is ever lost** across context truncations, session restarts, or agent handoffs.

---

## 🚀 Procedure for Any New Session or Handoff

Follow these 5 steps sequentially:

### Step 1: Recover Complete Memory
Before responding to the user or making assumptions about their project preferences:
1. Open and read [`PROJECT_PROMPTS_CHRONICLE.md`](file:///C:/Users/PC/Documents/HungerHelper/PROJECT_PROMPTS_CHRONICLE.md).
2. Check the most recent turns and user feedback to understand the current trajectory.
3. Review [`session_handoff_protocol.md`](./references/session_handoff_protocol.md) for strict architectural invariants.

### Step 2: Verify System Health & Run Regression Suite
Ensure that the codebase is completely green and functional:
1. Run the test suite:
   ```powershell
   python test_suite.py
   ```
2. Verify that **54/54 automated tests pass**. If any test fails, fix it immediately before introducing new changes.

### Step 3: Check Live Bot Daemon
Éloïse runs as a persistent background daemon:
1. Run `manage_task` with action `list`.
2. If `python -m co_pilot.discord_bot` is not running, launch it with `IsDaemon: true`:
   ```powershell
   python -m co_pilot.discord_bot
   ```
3. Confirm connection in task logs (`Whisper Large-v3-Turbo on NVIDIA RTX 3070 CUDA fp16`).

### Step 4: Enforce Inviolable Project Invariants
When modifying code or generating responses, never violate these core rules:
* **100% Datamined Data Only:** Coordinates, per-raid numbers, and drop chances must come from [`companion_bestiary_spawns.json`](file:///C:/Users/PC/Documents/HungerHelper/data/companion_bestiary_spawns.json), never approximated from screenshots.
* **Language Default:** Pure English by default unless French is explicitly spoken or requested.
* **Canonical Character Name:** Default character name is **Hugo** (never use Discord usernames or personal names like Abdallah in generated graphics).
* **6 Armor Tiers:** Weapon HTK cards must always include **Grey Armor (120 HP)** with helmet and chest icons.
* **Master Skins Showcase:** If a weapon has > 2 skins (especially Dagger with 8 skins), render a **Master Weapon Skins Showcase Sheet** (`skin_{weapon}_all_8_showcase.jpg`) so Discord desktop never hides items 5–8 behind previews.

### Step 5: Finalize & Sync Before Handoff
Before concluding a major turn or handing off the workspace:
1. Run the memory & GitHub synchronization helper:
   ```powershell
   python .agents/skills/hunger-helper-memory-handoff/scripts/sync_memory.py
   ```
2. Verify that [`PROJECT_PROMPTS_CHRONICLE.md`](file:///C:/Users/PC/Documents/HungerHelper/PROJECT_PROMPTS_CHRONICLE.md) is updated.
3. Verify that all modified files have been committed and pushed to GitHub (`https://github.com/Aab06300/HungerHelper`).
4. Confirm that the background daemon remains active.

---

## 📚 References & Resources

* [Session Handoff Protocol & Rules](./references/session_handoff_protocol.md)
* [System Architecture & File Sitemap](./references/project_architecture.md)
* [Memory Sync Script](./scripts/sync_memory.py)
