# 🏛️ Hunger Helper & Éloïse System Architecture

---

## 📁 Key Files & Core Modules

Module / File | Purpose & Responsibilities
:--- | :---
[`co_pilot/discord_bot.py`](file:///C:/Users/PC/Documents/HungerHelper/co_pilot/discord_bot.py) | **Live Daemon & Discord Gateway.** Runs Faster-Whisper Large-v3-Turbo on NVIDIA RTX 3070 CUDA fp16. Handles voice loop, slash commands (`/eloise`), multi-guild messaging, and DM replies.
[`co_pilot/brain.py`](file:///C:/Users/PC/Documents/HungerHelper/co_pilot/brain.py) | **Central Intelligence Router.** `CoPilotBrain.process_message()` parses user intent, extracts targets, selects bilingual responses, and dispatches to card/map renderers.
[`co_pilot/map_generator.py`](file:///C:/Users/PC/Documents/HungerHelper/co_pilot/map_generator.py) | **Tactical Map Engine.** Generates 2400×1400 Obsidian briefings (`render_dynamic_v25_briefing`) and universal datamined bestiary patrol maps (`generate_universal_bestiary_map`).
[`universal_v8_engine.py`](file:///C:/Users/PC/Documents/HungerHelper/universal_v8_engine.py) | **Universal Card Renderer.** Melee & Firearm HTK profiles (6 armor tiers), 3D skin dossiers, Master Weapon Skins Showcase Sheets, and crafting schemas.
[`perfect_briefings_core_v25.py`](file:///C:/Users/PC/Documents/HungerHelper/perfect_briefings_core_v25.py) | **Design System & Canvas Palette.** Obsidian dark theme (`#0b0b09`), typography fonts, declustering coordinates algorithms, and container/item icon caches.
[`data/companion_bestiary_spawns.json`](file:///C:/Users/PC/Documents/HungerHelper/data/companion_bestiary_spawns.json) | **100% Datamined Coordinates.** 24 Sarlat spawners, 20 Jacques spawners, 21 Sombre spawners, Farmer Dreg static spawner, per-raid densities, and roll rates.
[`test_suite.py`](file:///C:/Users/PC/Documents/HungerHelper/test_suite.py) | **Master Regression Suite.** 54 automated unit and integration tests simulating all historical user prompts, responses, and image attachments.
[`PROJECT_PROMPTS_CHRONICLE.md`](file:///C:/Users/PC/Documents/HungerHelper/PROJECT_PROMPTS_CHRONICLE.md) | **Permanent Memory Store.** Lossless chronicle of all user turns, screenshots, requirements, and development evolution.

---

## 🎮 One-Click Desktop Launchers

Launcher | Purpose
:--- | :---
[`LANCER_ELOISE.bat`](file:///C:/Users/PC/Documents/HungerHelper/LANCER_ELOISE.bat) | Starts the Discord bot daemon and speech engine in a visible window.
[`LANCER_ELOISE_SILENCIEUX.vbs`](file:///C:/Users/PC/Documents/HungerHelper/LANCER_ELOISE_SILENCIEUX.vbs) | Starts Éloïse silently in the background without opening a terminal window.
[`ARRETER_ELOISE.bat`](file:///C:/Users/PC/Documents/HungerHelper/ARRETER_ELOISE.bat) | Kills all active Éloïse and Python background processes cleanly.
