
import subprocess

def verifier_heure():
    try:
        resultat = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-Service W32Time -ErrorAction Stop).Status"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        return (
            resultat.returncode == 0
            and resultat.stdout.strip() == "Running"
        )

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
