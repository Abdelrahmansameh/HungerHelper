with open("co_pilot/brain.py", "r", encoding="utf-8") as f:
    content = f.read()

old_fi = '"capacite"\n        ]'
new_fi = '"capacite", "ma", "mon", "mes", "vendre", "stash", "inventaire"\n        ]'

assert old_fi in content, "old_fi not found!"
content = content.replace(old_fi, new_fi, 1)

with open("co_pilot/brain.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated french_indicators successfully!")
