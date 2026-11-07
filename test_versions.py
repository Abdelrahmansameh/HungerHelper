import os, sys

def test_script(name):
    path = os.path.join(r"C:\Users\PC\Documents\HungerHelper", name)
    if os.path.exists(path):
        print(f"Testing {name}...")
        # check imports
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        print(f"  {name} lines: {len(code.splitlines())}")

test_script("generate_perfect_briefings_v6.py")
test_script("generate_perfect_briefings_v13.py")
test_script("generate_perfect_briefings_v20.py")
test_script("generate_perfect_briefings_v22.py")
test_script("generate_perfect_briefings_v25.py")
