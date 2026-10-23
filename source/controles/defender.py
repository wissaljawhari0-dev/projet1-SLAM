import subprocess

def verifier_defender():

    commande = subprocess.run(
        [
            "powershell",
            "-Command",
            "(Get-Service WinDefend).Status"
        ],
        capture_output=True,
        text=True
    )

    return "Running" in commande.stdout

#print(verifier_defender())