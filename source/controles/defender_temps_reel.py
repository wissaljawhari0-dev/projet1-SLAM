import subprocess

def verifier_defender_temps_reel():

    commande = subprocess.run(
        [
            "powershell",
            "-Command",
            "(Get-MpPreference).DisableRealtimeMonitoring"
        ],
        capture_output=True,
        text=True
    )

    resultat = commande.stdout.strip()

    return resultat == "False"
