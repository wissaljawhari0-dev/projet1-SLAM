import subprocess

def verifier_antivirus():

    commande = subprocess.run(
        [
            "powershell",
            "-Command",
            "(Get-MpComputerStatus).AntivirusEnabled" #L'antivirus est-il activé ?
        ],
        capture_output=True,
        text=True
    )

    resultat = commande.stdout.strip()

    if resultat == "True":
        return True

    return False
#print(verifier_antivirus())