import subprocess

def corriger_parefeu():
    try:
        subprocess.run(
            "netsh advfirewall set allprofiles state on",
            shell=True
        )
        return True
    except:
        return False