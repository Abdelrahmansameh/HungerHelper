import os
import subprocess

ps_script = """
$ws = New-Object -ComObject WScript.Shell

# 1. LANCER ELOISE (SILENCIEUX PAR DEFAUT)
$s1 = $ws.CreateShortcut('C:\\Users\\PC\\Desktop\\LANCER_ELOISE.lnk')
$s1.TargetPath = 'C:\\Users\\PC\\Desktop\\Hunger_Helper\\LANCER_ELOISE_SILENCIEUX.vbs'
$s1.WorkingDirectory = 'C:\\Users\\PC\\Documents\\HungerHelper'
$s1.Description = 'Lancer Eloise Co-Pilote Tactique HUNGER (Mode Silencieux)'
$s1.Save()

# 2. ARRETER ELOISE
$s2 = $ws.CreateShortcut('C:\\Users\\PC\\Desktop\\ARRETER_ELOISE.lnk')
$s2.TargetPath = 'C:\\Users\\PC\\Desktop\\Hunger_Helper\\ARRETER_ELOISE.bat'
$s2.WorkingDirectory = 'C:\\Users\\PC\\Documents\\HungerHelper'
$s2.Description = 'Arreter le Co-Pilote Eloise'
$s2.Save()
"""

with open("temp_shortcuts.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "temp_shortcuts.ps1"], check=True)
if os.path.exists("temp_shortcuts.ps1"):
    os.remove("temp_shortcuts.ps1")
print("DESKTOP SHORTCUTS UPDATED: SILENT LAUNCH & ONE-CLICK STOP READY")
