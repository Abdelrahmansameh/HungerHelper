# 🔄 Session Handoff & Continuity Protocol
**Project:** Hunger Helper / Éloïse Tactical Co-Pilot  
**Applies To:** Every new Antigravity session, subagent, or model context switch.

---

## 1. New Session Initialization Checklist (Do This First)

Whenever a new session starts or the model's context is truncated/summarized, follow these mandatory steps:

1. **Consult the Master Chronicle:**
   * Open and read [`PROJECT_PROMPTS_CHRONICLE.md`](file:///C:/Users/PC/Documents/HungerHelper/PROJECT_PROMPTS_CHRONICLE.md).
   * Review recent turns, user critiques, and exact constraints. Never ask the user to repeat past demands.

2. **Verify Regression Suite Health:**
   * Run the test suite:
     ```powershell
     python test_suite.py
     ```
   * Confirm **54/54 automated tests pass (100% green)** before making any changes.

3. **Check Live Bot Daemon Status:**
   * Check running background tasks using `manage_task` (`Action: 'list'`).
   * If `python -m co_pilot.discord_bot` is not running (e.g. after a system restart), launch it with `IsDaemon: true`:
     ```powershell
     python -m co_pilot.discord_bot
     ```
   * Confirm that the speech engine (Whisper Large-v3-Turbo on NVIDIA RTX 3070 CUDA fp16) logs in and connects to Discord.

---

## 2. Inviolable Core Project Invariants (Never Break)

* **Strict Data Source:** All coordinates, per-raid numbers, and roll rates MUST come 100% exclusively from official datamined Hunger Companion files (`data/companion_bestiary_spawns.json`, `data/full_companion_skins.json`, `data/high_rate_drops.json`). **NEVER approximate coordinates from screenshots.**
* **Language Default:** Pure English by default. Only respond in French if the user explicitly asks in French.
* **Character Name Rule:** Use canonical character names (**Hugo** by default, or Otto, Marie, Eva, Gabriel, Serine when specified). **NEVER write Discord usernames or real names (e.g., Abdallah) onto generated cards or talent trees.**
* **All 6 Armor Tiers in HTK Cards:** Melee and Firearm cards must always include the **Grey / Common Armor Tier (120 HP)** alongside Naked (100 HP), Green (140 HP), Blue (160 HP), Epic (180 HP), and Legendary (200 HP), with color-coded helmet and chest icons.
* **Multi-Skin Master Showcase Sheet:** For weapons with multiple skins (especially > 4 skins like Dagger with 8 skins), generate and send a **Master Weapon Skins Showcase Sheet** (`skin_{weapon}_all_8_showcase.jpg`) so Discord's 4-image collage preview never hides items 5–8.
* **Multi-Discord Plug-and-Play:**
  * Always respond directly in the channel where the message was received (`message.channel`).
  * Direct Messages (DMs) must be supported without crashing on guild checks.
  * Local headset audio (`speak_async`) must be isolated to the host PC only—never stream remote server members' voice to host speakers.

---

## 3. Session End / Handoff Checklist

Before ending your turn or concluding a major development milestone:

1. **Sync Prompts & Memory:**
   * Execute:
     ```powershell
     python .agents/skills/hunger-helper-memory-handoff/scripts/sync_memory.py
     ```
   * Confirm `PROJECT_PROMPTS_CHRONICLE.md` includes the latest user requests and corrections.
2. **Run Full Regression Suite:**
   * Run `python test_suite.py` and verify all tests pass.
3. **Verify Daemon Health:**
   * Ensure `discord_bot.py` is alive and responding on Discord.
4. **Synchronize GitHub Repository:**
   * Verify all project modifications are committed and pushed to `https://github.com/Aab06300/HungerHelper`.
   * Keep `config.json` strictly excluded via `.gitignore` at all times.
