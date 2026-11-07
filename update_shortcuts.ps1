$WshShell = New-Object -ComObject WScript.Shell

# 1. Update LANCER_ELOISE.lnk
$Shortcut = $WshShell.CreateShortcut("C:\Users\PC\Desktop\LANCER_ELOISE.lnk")
$Shortcut.TargetPath = "C:\Users\PC\Desktop\Hunger_Helper\LANCER_ELOISE.bat"
$Shortcut.WorkingDirectory = "C:\Users\PC\Documents\HungerHelper"
$Shortcut.WindowStyle = 1
$Shortcut.Description = "Lancer Eloise Tactical Co-Pilot en mode autonome"
$Shortcut.Save()

# 2. Update ARRETER_ELOISE.lnk
$Shortcut = $WshShell.CreateShortcut("C:\Users\PC\Desktop\ARRETER_ELOISE.lnk")
$Shortcut.TargetPath = "C:\Users\PC\Desktop\Hunger_Helper\ARRETER_ELOISE.bat"
$Shortcut.WorkingDirectory = "C:\Users\PC\Documents\HungerHelper"
$Shortcut.WindowStyle = 1
$Shortcut.Description = "Fermer proprement Eloise Tactical Co-Pilot"
$Shortcut.Save()

Write-Output "Shortcuts on Desktop updated successfully."
