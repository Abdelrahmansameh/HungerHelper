with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(266, min(len(lines), 340)):
    cleaned = lines[j].encode("ascii", "replace").decode("ascii")
    print(f"{j+1}: {cleaned.rstrip()}")
