Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d C:\Users\PC\Documents\HungerHelper && python -m co_pilot.discord_bot", 0, False
