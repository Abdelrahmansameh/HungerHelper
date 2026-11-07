import os
import subprocess

ps_script = """
$ws = New-Object -ComObject WScript.Shell
$s = $ws.CreateShortcut('C:\\Users\\PC\\Desktop\\LANCER_ELOISE.lnk')
$s.TargetPath = 'C:\\Users\\PC\\Desktop\\Hunger_Helper\\LANCER_ELOISE.bat'
$s.WorkingDirectory = 'C:\\Users\\PC\\Documents\\HungerHelper'
$s.Description = 'Lancer Eloise Co-Pilote Tactique HUNGER'
$s.Save()
"""

with open("temp_shortcut.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "temp_shortcut.ps1"], check=True)
if os.path.exists("temp_shortcut.ps1"):
    os.remove("temp_shortcut.ps1")
print("DESKTOP SHORTCUT CREATED SUCCESSFULLY")
