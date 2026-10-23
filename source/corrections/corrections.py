
import subprocess


def executer_commande(commande):
    try:
        resultat = subprocess.run(
            commande,
            shell=True,
            capture_output=True,
            text=True
        )
        return resultat.returncode == 0
    except Exception:
        return False


def corriger_pare_feu():
    return executer_commande(
        "netsh advfirewall set allprofiles state on"
    )


def corriger_spooler():
    configuration = executer_commande(
        "sc config spooler start= auto"
    )
    demarrage = executer_commande("net start spooler")
    return configuration and demarrage


def corriger_defender():
    return executer_commande(
        "powershell Set-MpPreference -DisableRealtimeMonitoring $false"
    )


def corriger_windows_update():
    configuration = executer_commande(
        "sc config wuauserv start= auto"
    )
    demarrage = executer_commande("net start wuauserv")
    return configuration and demarrage


def corriger_dhcp():
    return executer_commande(
        'netsh interface ip set address name="Ethernet" source=dhcp'
    )
