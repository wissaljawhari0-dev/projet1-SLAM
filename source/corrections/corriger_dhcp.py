import subprocess

def corriger_dhcp():
    try:
        subprocess.run(
            "sc config Dhcp start= auto",
            shell=True
        )

        subprocess.run(
            "net start Dhcp",
            shell=True
        )

        return True
    except:
        return False