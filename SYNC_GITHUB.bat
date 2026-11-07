@echo off
title SYNC HUNGER HELPER TO GITHUB
color 0A
cls
echo ==============================================================================
echo                 HUNGER HELPER : GITHUB AUTOMATIC SYNCHRONIZER
echo ==============================================================================
echo.
cd /d "C:\Users\PC\Documents\HungerHelper"

echo [1/2] Synchronizing Project Memory & Prompts Chronicle...
python .agents\skills\hunger-helper-memory-handoff\scripts\sync_memory.py

echo.
echo ==============================================================================
echo                 GITHUB SYNCHRONIZATION COMPLETE!
echo       Repository: https://github.com/Aab06300/HungerHelper
echo ==============================================================================
echo.
pause
