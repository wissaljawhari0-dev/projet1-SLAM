import winreg

def verifier_fichiers_caches():
    try:
        cle = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
        )

        valeur, _ = winreg.QueryValueEx(cle, "Hidden")
        winreg.CloseKey(cle)

        return int(valeur) == 1

    except (FileNotFoundError, OSError, ValueError, TypeError):
        return False