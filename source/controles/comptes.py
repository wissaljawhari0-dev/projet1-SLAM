import subprocess

def verifier_compte_admin():

    commande = subprocess.run(
        [
            "powershell",
            "-Command",
            "Get-LocalUser"
        ],
        capture_output=True,
        text=True
    )

    resultat = commande.stdout

    if "adm-experty" in resultat.lower():
        return True

    return False

#print(verifier_compte_admin())