import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(320, min(len(lines), 440)):
    print(f"{i+1}: {lines[i].rstrip()}")
