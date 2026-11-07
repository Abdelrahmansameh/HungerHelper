with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "TacticalMapQuickView" in l or "QuestCardQuickView" in l or "ItemCardQuickView" in l:
        print(f"Line {i+1}: {l.strip()}")
