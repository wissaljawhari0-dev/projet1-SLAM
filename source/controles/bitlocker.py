import subprocess

def verifier_bitlocker():

    commande = subprocess.run(
        [
            "powershell",
            "-Command",
            "(Get-BitLockerVolume -MountPoint 'C:').ProtectionStatus"
        ],
        capture_output=True,
        text=True
    )

    resultat = commande.stdout.strip()

    if resultat == "1":
        return True

    return False
#print(verifier_bitlocker())