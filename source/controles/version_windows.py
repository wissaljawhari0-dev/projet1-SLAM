import platform

def verifier_version_windows():
    try:
        systeme = platform.system()
        version = platform.version()

        return systeme == "Windows" and bool(version)

    except Exception:
        return False