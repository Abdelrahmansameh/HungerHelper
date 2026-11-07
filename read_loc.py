with open("co_pilot/game_knowledge.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(1057, 1130):
    print(f"{j+1}: {lines[j].rstrip().encode('ascii', 'replace').decode('ascii')}")
