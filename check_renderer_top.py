with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(40, 100):
    print(f"{i+1}: {lines[i].rstrip()}")
