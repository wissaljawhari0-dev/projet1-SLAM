import subprocess

def verifier_activation_windows():
    try:
        resultat = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "$licence = Get-CimInstance "
                "SoftwareLicensingProduct "
                "-Filter \"PartialProductKey IS NOT NULL\" "
                "| Where-Object { $_.Name -like '*Windows*' "
                "-and $_.LicenseStatus -eq 1 }; "
                "if ($licence) { exit 0 } else { exit 1 }"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )

        return resultat.returncode == 0

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False