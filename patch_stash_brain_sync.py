import os

p = 'test_dynamic_stash_two_images.py'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

text_n = text.replace('\r\n', '\n')
if 'BRAIN_DIR' not in text_n:
    text_n = text_n.replace(
        'OUT_DIR = os.path.join(ROOT_DIR, "output_maps")',
        'OUT_DIR = os.path.join(ROOT_DIR, "output_maps")\nBRAIN_DIR = r"C:\\Users\\PC\\.gemini\\antigravity\\brain\\3867ac2b-acf9-4012-a98a-a6fd52e96d49"'
    )
    text_n = text_n.replace(
        'img1.convert("RGB").save(out_p1, quality=95)',
        'img1.convert("RGB").save(out_p1, quality=95)\n    if os.path.exists(BRAIN_DIR):\n        img1.convert("RGB").save(os.path.join(BRAIN_DIR, "stash_highlighted_grid.jpg"), quality=95)'
    )
    text_n = text_n.replace(
        'img2.convert("RGB").save(out_p2, quality=95)',
        'img2.convert("RGB").save(out_p2, quality=95)\n    if os.path.exists(BRAIN_DIR):\n        img2.convert("RGB").save(os.path.join(BRAIN_DIR, "stash_sell_manifest.jpg"), quality=95)'
    )
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text_n)
    print('BRAIN_SYNC_ADDED')
else:
    print('ALREADY_PRESENT')
