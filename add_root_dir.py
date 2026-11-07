with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    text = f.read()

target = "from typing import Dict, Any, Optional, Tuple, List"
replacement = "from typing import Dict, Any, Optional, Tuple, List\n\nROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))"

new_text = text.replace(target, replacement)
with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.write(new_text)

print("ROOT_DIR successfully added.")
