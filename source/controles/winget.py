
import subprocess

def verifier_winget():
    try:
        resultat = subprocess.run(
            ["winget", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return resultat.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
