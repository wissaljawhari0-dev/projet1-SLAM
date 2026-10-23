import subprocess

def verifier_imprimante():

    commande = subprocess.run(
        [
            "powershell",
            "-Command",
            "Get-Printer"
        ],
        capture_output=True,
        text=True
    )

    return len(
        commande.stdout.strip()
    ) > 0

#print(verifier_imprimante())
