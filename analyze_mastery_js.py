import re

with open('mastery.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's search for hash or 'b=' or encode/decode in mastery.js
for match in re.finditer(r'(?:hash|encode|decode|deserialize|serialize|build)[^;]{10,200}', js, re.IGNORECASE):
    print(match.group(0))
    print('-'*20)
