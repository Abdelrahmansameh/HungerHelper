# ⚔️ Éloïse Tactical Co-Pilot (Hunger Helper)

> **Autonomous AI Voice Co-Pilot & Raid Intelligence System for *The Hunger***  
> Powered by Whisper Large-v3-Turbo (CUDA fp16), Edge-TTS, and 100% datamined game intelligence.

---

## 🌟 Key Features

1. **🎙️ Voice & Text Discord Assistant**
   - Responds to voice in Discord voice channels, via local headset mic, or via Discord text chat (`/ask` slash command or direct mentions).
   - Powered by Faster-Whisper Large-v3-Turbo for ultra-fast low-latency speech recognition and Neural TTS voice streaming.

2. **🗺️ Tactical Raid Briefings (V10–V25)**
   - High-resolution dynamic tactical maps with 100% verified datamined spawn locations, POIs, crypts, extraction paths, and container clusters.
   - Dynamic Bestiary maps showing exact creature spawn coordinates, roll chances, and patrol perimeters.

3. **⚔️ Hit-to-Kill (HTK) & Ballistics Matrix**
   - Complete melee weapon and firearm breakdown covering all 6 armor tiers (including Naked 100 HP, Grey Armor 120 HP, Light 150 HP, Medium 200 HP, Heavy 250 HP, and Super Heavy 300 HP).
   - Computes TTK (time-to-kill), light vs. heavy hits, and headshot damage thresholds.

4. **🎨 Château Artisan Skins & Master Sheets**
   - Full skin database with drop locations, merchant barter schemas, and consolidated 8-skin master showcase sheets.

5. **🎒 Computer Vision Stash Scanner**
   - Dual-card visual analyzer: scans raid inventory and stash screenshots, highlights high-value loot, and computes total liquidation value.

6. **👤 Hero Kits & Mastery Cards**
   - In-depth mastery matrix and talent trees for Hugo, Otto, Marie, Eva, Gabriel, and Serine with cumulative stat aggregations.

7. **📖 Complete Raid Dossiers**
   - High-fidelity visual cards for Creatures, Traps & Hazards, Subterranean Crypts, Status Effects, and Crafting Schemas.

---

## 🚀 Quick Setup Guide

### 1. Prerequisites
- **Python 3.10+** (Python 3.12 recommended)
- **NVIDIA GPU** with CUDA support recommended (e.g. RTX 3070+) for real-time Whisper transcription, or CPU fallback.
- **Git**

### 2. Installation
Clone the repository:
```bash
git clone https://github.com/Aab06300/HungerHelper.git
cd HungerHelper
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration
Copy `config.example.json` to `config.json`:
```bash
copy config.example.json config.json
```
Edit `config.json` and insert your credentials:
```json
{
  "DISCORD_BOT_TOKEN": "YOUR_DISCORD_BOT_TOKEN_HERE",
  "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY_HERE",
  "TTS_VOICE": "fr-FR-VivienneMultilingualNeural",
  "VOICE_ACTIVATION_KEYWORD": "Éloïse"
}
```

> ⚠️ **Important:** Never commit or share your `config.json` file. It is excluded by `.gitignore`.

### 4. Running the Bot
Launch Éloïse in standalone mode:
```bash
python -m co_pilot.discord_bot
```
Or simply double-click **`LANCER_ELOISE.bat`** on Windows.

To stop the bot cleanly:
Double-click **`ARRETER_ELOISE.bat`**.

---

## 🧪 Testing & Verification

Run the full regression test suite (54 automated tests):
```bash
python test_suite.py
```

---

## 📂 Project Structure

```
HungerHelper/
├── co_pilot/              # Éloïse Core Engine
│   ├── discord_bot.py     # Discord Gateway, Voice Duplex & Slash Commands
│   ├── brain.py           # NLP Intent Parsing & Knowledge Router
│   ├── card_renderer.py   # High-resolution Infographic & Card Generator
│   ├── map_generator.py   # Tactical Map Renderers & Bestiary Pinning
│   └── vision_analyzer.py # Computer Vision Stash & Loot Scanner
├── data/                  # 100% Datamined Companion DBs (Spawns, Skins, Weapons)
├── assets/                # Base UI Cards, Fonts, and Item Icons
├── Raid_Maps/             # High-resolution Base Maps
├── test_suite.py          # Master Regression Suite (54 Tests)
├── LANCER_ELOISE.bat      # Windows 1-Click Launch Script
├── ARRETER_ELOISE.bat     # Windows 1-Click Stop Script
└── requirements.txt       # Project Dependencies
```

---

## 🤝 Collaboration & Sharing

To invite friends to your Discord server or share the bot across guilds:
1. Enable `Message Content Intent` and `Voice Receiving` in the [Discord Developer Portal](https://discord.com/developers/applications).
2. Generate an OAuth2 Invite URL with `bot` and `applications.commands` scopes.
3. Once invited, friends can interact with Éloïse via voice or text in any server!
