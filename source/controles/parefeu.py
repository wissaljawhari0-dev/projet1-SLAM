import subprocess #permet à Python d'exécuter des commandes Windows ou PowerShell.

def verifier_parefeu():

    commande = subprocess.run(
        [
            "powershell",
            "-Command",
            "Get-NetFirewallProfile | Select-Object -ExpandProperty Enabled" #Le pare-feu est-il activé ?
        ],
        capture_output=True,
        text=True
    )

    resultat = commande.stdout

    if "True" in resultat:
        return True

    return False
#print(verifier_parefeu())