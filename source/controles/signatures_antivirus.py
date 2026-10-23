
import subprocess


def verifier_signatures_antivirus():
    try:
        resultat = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "$s = Get-MpComputerStatus -ErrorAction Stop; "
                "if ($null -eq $s.AntivirusSignatureAge) "
                "{ exit 2 }; "
                "if ($s.AntivirusSignatureAge -ge 0 -and "
                "$s.AntivirusSignatureAge -le 7) "
                "{ exit 0 } else { exit 1 }"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )

        return resultat.returncode == 0

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
