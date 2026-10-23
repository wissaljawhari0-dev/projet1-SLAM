import subprocess

def verifier_windows_update():
    try:
        resultat = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "$service = Get-Service -Name 'wuauserv' "
                "-ErrorAction Stop; "
                "if ($service.Status -eq 'Running') "
                "{ exit 0 } else { exit 1 }"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )

        return resultat.returncode == 0

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False