import subprocess

def verifier_antivirus():
    try:
        resultat = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "$s = Get-MpComputerStatus -ErrorAction Stop; "
                "if ($s.AntivirusEnabled -and "
                "$s.RealTimeProtectionEnabled) "
                "{ exit 0 } else { exit 1 }"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )

        return resultat.returncode == 0

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False