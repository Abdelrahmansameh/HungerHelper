@echo off
title ELOISE TACTICAL CO-PILOT - THE HUNGER
mode con: cols=95 lines=32
color 0B
cls
echo ==============================================================================
echo                      ELOISE TACTICAL CO-PILOT - THE HUNGER
echo               Voice AI & Interactive Tactical Companion for Raids
echo ==============================================================================
echo.
echo [1/3] Verifying Python Environment...
cd /d "C:\Users\PC\Documents\HungerHelper"
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python not found in system PATH.
    pause
    exit /b 1
)

echo [2/3] Initializing NVIDIA RTX 3070 CUDA Acceleration...
echo       Faster-Whisper Large-v3-Turbo + Edge-TTS Neural Vocal Streamer
echo.
echo [3/3] Launching Eloise Discord Bot Daemon...
echo       * Discord Voice Channel: Auto-joins HUNGER
echo       * Hardware Mic: HyperX Headset calibrated
echo       * Standalone Mode: Antigravity is NOT required to be open!
echo.
echo ==============================================================================
echo                     BOT IS RUNNING IN STANDALONE MODE
echo             To stop Eloise cleanly, run ARRETER_ELOISE on Desktop.
echo ==============================================================================
echo.
python -m co_pilot.discord_bot
pause
