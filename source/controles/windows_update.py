import subprocess

def verifier_windows_update():

    commande = subprocess.run(
        [
            "powershell",
            "-Command",
            "Get-Service wuauserv | Select-Object -ExpandProperty Status"
        ],
        capture_output=True,
        text=True
    )

    resultat = commande.stdout.strip()

    if resultat == "Running":
        return True

    return False
#print(verifier_windows_update())