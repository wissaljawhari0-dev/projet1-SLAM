import winreg

def verifier_extensions():
    try:
        cle = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
        )

        valeur, _ = winreg.QueryValueEx(cle, "HideFileExt")
        winreg.CloseKey(cle)

        return int(valeur) == 0

    except (FileNotFoundError, OSError, ValueError, TypeError):
        return False