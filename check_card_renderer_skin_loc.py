with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def render_skin_card" in line:
        for j in range(max(0, i-5), min(len(lines), i+40)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
