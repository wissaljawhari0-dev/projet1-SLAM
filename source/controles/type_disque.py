
import subprocess

def verifier_type_disque():
    try:
        resultat = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-PhysicalDisk | Select-Object -ExpandProperty MediaType) -join ','"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if resultat.returncode != 0:
            return False

        types_disques = resultat.stdout.strip().lower()

        return bool(types_disques) and (
            "ssd" in types_disques or "hdd" in types_disques
        )

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
