import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("--- Lines 480 to 510 ---")
for i in range(480, 510):
    print(f"{i+1}: {lines[i].rstrip()}")

print("\n--- Lines 1035 to 1060 ---")
for i in range(1035, min(len(lines), 1065)):
    print(f"{i+1}: {lines[i].rstrip()}")
