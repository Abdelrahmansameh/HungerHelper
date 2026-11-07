with open('mastery.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('CODE_ORDER')
if idx != -1:
    print(js[idx-100:idx+1500])
else:
    print("CODE_ORDER not found")
