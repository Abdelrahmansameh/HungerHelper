import re
import json

with open('mastery_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html)
print('Script srcs:', scripts)

# Look for tree data or build parsing
for match in re.finditer(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', html, re.DOTALL):
    content = match.group(1).strip()
    if 'mastery' in content.lower() or 'trees' in content.lower() or 'build' in content.lower() or len(content) > 500:
        print("Found interesting inline script, length:", len(content))
        print(content[:500])
        print("="*40)
