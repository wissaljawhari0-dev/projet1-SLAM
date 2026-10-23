
import winreg


def verifier_logiciels_interdits():
    logiciels_interdits = ["utorrent", "cheat engine"]

    emplacements = [
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        ),
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ),
        (
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        )
    ]

    try:
        for racine, chemin in emplacements:
            try:
                cle = winreg.OpenKey(racine, chemin)
            except OSError:
                continue

            with cle:
                nombre = winreg.QueryInfoKey(cle)[0]

                for i in range(nombre):
                    try:
                        nom_sous_cle = winreg.EnumKey(cle, i)

                        with winreg.OpenKey(cle, nom_sous_cle) as sous_cle:
                            try:
                                nom, _ = winreg.QueryValueEx(
                                    sous_cle, "DisplayName"
                                )
                            except OSError:
                                continue

                            nom = str(nom).lower()

                            if any(
                                interdit in nom
                                for interdit in logiciels_interdits
                            ):
                                return False

                    except OSError:
                        continue

        return True

    except OSError:
        return False
