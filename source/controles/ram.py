import psutil

def verifier_ram(ram_attendue):
    try:
        ram_reelle = psutil.virtual_memory().total / (1024 ** 3)

        return (
            ram_reelle >= ram_attendue,
            round(ram_reelle, 2)
        )

    except Exception:
        return False, 0