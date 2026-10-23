
import winreg

def verifier_numlock():
    try:
        cle = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Control Panel\Keyboard"
        )

        valeur, _ = winreg.QueryValueEx(
            cle,
            "InitialKeyboardIndicators"
        )

        winreg.CloseKey(cle)

        return str(valeur) == "2"

    except (FileNotFoundError, OSError):
        return False
