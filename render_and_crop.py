import subprocess
import os
import shutil
from PIL import Image

output_file = 'mastery_build_summary.png'

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1840,2100',
    '--hide-scrollbars',
    f'--screenshot={os.path.abspath(output_file)}',
    f'file:///{os.path.abspath("mastery_build_card.html").replace(os.sep, "/")}'
]

print("Executing Chrome headless screenshot...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome stderr:", res.stderr.strip())

# Open and auto-crop bottom
img = Image.open(output_file)
w, h = img.size
print(f"Captured size: {w}x{h}")

bg_color = img.getpixel((w//2, h-1))

bottom_y = h - 1
for y in range(h - 1, 0, -1):
    has_content = False
    for x in range(100, w - 100, 100):
        p = img.getpixel((x, y))
        if max(abs(p[i] - bg_color[i]) for i in range(3)) > 15:
            has_content = True
            break
    if has_content:
        bottom_y = min(h, y + 36)
        break

print(f"Auto-cropping to height: {bottom_y}")
cropped = img.crop((0, 0, w, bottom_y))
cropped.save(output_file)
print(f"Cropped image saved: {output_file} ({w}x{bottom_y})")

# Copy to all target directories
targets = [
    r"C:\Users\PC\Desktop\Hunger_Helper\mastery_build_summary.png",
    r"C:\Users\PC\Desktop\Hunger_Helper\03_Mastery_Build_Planner\mastery_build_summary.png",
    r"C:\Users\PC\.gemini\antigravity\brain\b8e8e819-7440-402b-82cd-d5167e3dcf10\mastery_build_summary.png"
]

for t in targets:
    os.makedirs(os.path.dirname(t), exist_ok=True)
    shutil.copyfile(output_file, t)
    print(f"Updated: {t}")
