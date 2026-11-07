with open(r"C:\Users\PC\Documents\HungerHelper\test_run_node.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Line count:", len(lines))
for i in range(max(0, 20), min(len(lines), 35)):
    print(f"{i+1}: {lines[i][:80]}")
