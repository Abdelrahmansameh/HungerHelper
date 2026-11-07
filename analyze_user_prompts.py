import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open("extracted_all_user_prompts.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("Extracted text length:", len(text))
# Let's inspect unique queries and key commands mentioned by the user
lines = text.splitlines()
steps = []
cur_step = 0
cur_lines = []
for l in lines:
    if l.startswith("--- STEP "):
        if cur_lines:
            steps.append((cur_step, "\n".join(cur_lines)))
        cur_step = int(l.replace("--- STEP ", "").replace(" ---", ""))
        cur_lines = []
    else:
        cur_lines.append(l)
if cur_lines:
    steps.append((cur_step, "\n".join(cur_lines)))

print(f"Total steps: {len(steps)}")
for s, content in steps:
    summary = content.strip().replace("\n", " ")[:100]
    print(f"Step {s}: {summary}")
