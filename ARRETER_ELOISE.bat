@echo off
title ARRETER ELOISE - FERMETURE PROPRE
mode con: cols=75 lines=14
color 0E
cls
echo ===========================================================================
echo               FERMETURE DU CO-PILOTE TACTIQUE ELOISE
echo ===========================================================================
echo.
echo Arret des processus Python et Discord Bot en cours...
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*co_pilot.discord_bot*' -or $_.CommandLine -like '*discord_bot*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force; Write-Host ('[OK] Processus ' + $_.ProcessId + ' arrete.') }"
echo.
echo [SUCCES] Eloise a ete arretee proprement.
echo.
timeout /t 2 >nul
exit
