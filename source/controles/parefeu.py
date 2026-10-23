
import subprocess

def verifier_parefeu():
    try:
        resultat = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "$profils = Get-NetFirewallProfile; "
                "if ($profils.Count -eq 3 -and "
                "($profils | Where-Object { "
                "$_.Enabled -ne $true }).Count -eq 0) "
                "{ exit 0 } else { exit 1 }"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        return resultat.returncode == 0

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
