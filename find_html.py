import os

for root in [r"C:\Users\PC\.gemini\antigravity\brain\d8f00a68-a5af-4b09-aa15-7c0d58ac69ee", r"C:\Users\PC\Documents\HungerHelper"]:
    for f in os.listdir(root):
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
                if "ROUTE WALKTHROUGH" in c or "Walkthrough" in c or "walkthrough" in c:
                    print(f"Found in {f}")
