import subprocess

def verifier_dhcp():
    try:
        resultat = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "$interfaces = Get-NetIPInterface "
                "-AddressFamily IPv4 "
                "-ErrorAction Stop | "
                "Where-Object { $_.ConnectionState -eq 'Connected' }; "
                "if ($interfaces -and "
                "($interfaces | Where-Object { $_.Dhcp -ne 'Enabled' }).Count -eq 0) "
                "{ exit 0 } else { exit 1 }"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )

        return resultat.returncode == 0

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False