import json, sys
sys.stdout.reconfigure(encoding='utf-8')

log_path = r'C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49\.system_generated\logs\transcript.jsonl'

user_prompts = []
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            if entry.get("source") == "USER_EXPLICIT" or entry.get("type") == "USER_INPUT":
                content = entry.get("content", "")
                if content:
                    user_prompts.append((entry.get("step_index", 0), content))
        except Exception:
            pass

print(f"Extracted {len(user_prompts)} user inputs from transcript.")
with open("extracted_all_user_prompts.txt", "w", encoding="utf-8") as out:
    for idx, p in user_prompts:
        out.write(f"\n--- STEP {idx} ---\n{p}\n")

print("Saved to extracted_all_user_prompts.txt!")
