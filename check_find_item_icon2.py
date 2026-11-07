with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(140, min(len(lines), 195)):
    print(f"{j+1}: {lines[j].rstrip()}")
