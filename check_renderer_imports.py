with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    for i in range(40):
        print(f"{i+1}: {f.readline().rstrip()}")
