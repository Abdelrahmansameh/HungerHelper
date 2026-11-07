import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "SCREENSHOT INVENTORY" in l:
        for j in range(i, min(len(lines), i+80)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
