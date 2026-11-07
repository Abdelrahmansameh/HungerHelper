import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if ".send(" in line:
        for j in range(max(0, i-3), min(len(lines), i+15)):
            print(f"{j+1}: {lines[j].rstrip()}")
        print("="*40)
