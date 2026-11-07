import subprocess

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--dump-dom',
    r'file:///C:/Users/PC/Documents/HungerHelper/mastery_build_card.html'
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("DOM length:", len(res.stdout))
