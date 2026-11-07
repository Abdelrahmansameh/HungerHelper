with open("co_pilot/vision_analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'print(f"[Vision Analyzer Error]: {e}", flush=True)',
    'import traceback\n        traceback.print_exc()\n        print(f"[Vision Analyzer Error]: {e}", flush=True)'
)

with open("co_pilot/vision_analyzer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Added traceback to vision_analyzer.py")
