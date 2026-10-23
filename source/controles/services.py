
import subprocess


def verifier_service(nom_service):
    try:
        resultat = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f"(Get-Service -Name '{nom_service}' "
                "-ErrorAction Stop).Status"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )

        return (
            resultat.returncode == 0
            and resultat.stdout.strip() == "Running"
        )

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
