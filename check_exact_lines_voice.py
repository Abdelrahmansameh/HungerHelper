import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(480, 515):
    print(f"{i+1}: {repr(lines[i])}")
