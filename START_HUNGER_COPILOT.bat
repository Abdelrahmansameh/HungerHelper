@echo off
title Eloise - Hunger Tactical Voice Co-Pilot
cd /d "%~dp0"
chcp 65001 >nul
echo ===================================================
echo   Starting Eloise Discord Voice Co-Pilot...
echo ===================================================
python -m co_pilot.discord_bot
pause
