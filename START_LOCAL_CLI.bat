@echo off
title Hunger Helper Local Voice CLI
cd /d "%~dp0"
echo ===================================================
echo   Starting Hunger Helper Local Voice Assistant...
echo ===================================================
python -m co_pilot.voice_cli
pause
