with open("co_pilot/card_renderer.py", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find('"salpetre"')
print(repr(text[start:start+400]))
