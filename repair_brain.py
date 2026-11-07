import sys

with open('co_pilot/brain.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

clean_lines = lines[:1119]
tail_lines = lines[2239:]
print(f'Head lines: {len(clean_lines)}')
print(f'Tail lines: {len(tail_lines)}')
tail_lines[0] = '            if quests and (re.search(r"\\b(qu[eèé]te|quest|quests)\\b", lowered) or "gavroche" in lowered):\n'
new_content = ''.join(clean_lines + tail_lines)
with open('co_pilot/brain.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('brain.py restored successfully!')
