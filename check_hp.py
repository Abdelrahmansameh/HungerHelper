import re

with open('gabriel_page.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Look for numbers near 'health' or 'hp' or 'armour'
for m in re.finditer(r'(?:health|hp|armour|armor|stamina|speed)[^<]{0,50}', text, re.IGNORECASE):
    print(m.group(0))
