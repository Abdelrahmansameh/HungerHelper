with open('mastery.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx = js.find('buildCode')
if idx != -1:
    print(js[idx-200:idx+1500])
