import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("--- Lines 235 to 255 ---")
for i in range(235, 255):
    print(f"{i+1}: {lines[i].rstrip()}")

print("\n--- Lines 498 to 515 ---")
for i in range(498, 515):
    print(f"{i+1}: {lines[i].rstrip()}")
