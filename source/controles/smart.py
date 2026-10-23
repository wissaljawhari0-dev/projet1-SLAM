import subprocess

def verifier_smart():

    commande = subprocess.run(
        [
            "powershell",
            "-Command",
            "Get-PhysicalDisk | Select-Object HealthStatus"
        ],
        capture_output=True,
        text=True
    )

    return "Healthy" in commande.stdout

#print(verifier_smart())