with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "alias_map = {" in l:
        for j in range(i, i+55):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
