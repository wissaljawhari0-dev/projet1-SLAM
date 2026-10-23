import subprocess

def verifier_bitlocker():
    try:
        resultat = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "$b = Get-BitLockerVolume -MountPoint 'C:' "
                "-ErrorAction Stop; "
                "if ($b.ProtectionStatus -eq 'On') "
                "{ exit 0 } else { exit 1 }"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )

        return resultat.returncode == 0

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False