with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(240, min(len(lines), 310)):
    print(f"{i+1}: {lines[i].rstrip()}")
