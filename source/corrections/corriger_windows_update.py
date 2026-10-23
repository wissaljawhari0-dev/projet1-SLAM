
import subprocess


def corriger_windows_update():
    try:
        resultat = subprocess.run(
            "sc config wuauserv start= auto",
            shell=True,
            capture_output=True,
            text=True
        )

        if resultat.returncode != 0:
            return False

        resultat = subprocess.run(
            "net start wuauserv",
            shell=True,
            capture_output=True,
            text=True
        )

        return resultat.returncode == 0

    except Exception:
        return False
