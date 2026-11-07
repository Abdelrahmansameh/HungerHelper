with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    content = f.read()

import re
print("Views attached to message send in discord_bot.py:")
for m in re.finditer(r'view\s*=\s*([a-zA-Z0-9_]+)', content):
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 50)
    print(content[start:end])
    print("="*30)
