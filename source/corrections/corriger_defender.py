import subprocess

def corriger_defender():
    try:
        subprocess.run(
            'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $false"',
            shell=True
        )
        return True
    except:
        return False