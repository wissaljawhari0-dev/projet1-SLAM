import subprocess

def verifier_service(nom_service):

    commande = subprocess.run(
        [
            "powershell",
            "-Command",
            f"(Get-Service '{nom_service}').Status"
        ],
        capture_output=True,
        text=True
    )

    resultat = commande.stdout.strip()

    if resultat == "Running":
        return True

    return False
#print(verifier_service("Spooler"))