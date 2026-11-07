import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('build_eloise_raid_planner_v20.py', 'r', encoding='utf-8') as f:
    content = f.read()

idx_style = content.find('<style>')
if idx_style != -1:
    print(content[idx_style:idx_style+3000])
else:
    print(content[:1000])
