import re

p = "co_pilot/brain.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

pattern = r"# Language Detection\s+french_indicators = \[.*?\]\s+is_french = any\(w in lowered for w in french_indicators\)"
replacement = """# Language Detection: Default to ENGLISH! French ONLY when explicitly asked!
        is_french = any(w in lowered for w in ["en français", "en francais", "in french", "traduis en français", "traduis en francais", "réponds en français", "reponds en francais"])"""

new_text = re.sub(pattern, replacement, text, flags=re.DOTALL)
with open(p, "w", encoding="utf-8") as f:
    f.write(new_text)

print("IS_FRENCH_SUCCESSFULLY_UPDATED")
