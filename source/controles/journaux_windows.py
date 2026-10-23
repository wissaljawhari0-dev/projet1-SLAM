
import subprocess

def verifier_journaux_windows():
    try:
        resultat = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-WinEvent -LogName System -MaxEvents 1 -ErrorAction Stop | Out-Null"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        return resultat.returncode == 0

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
