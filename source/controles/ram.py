import psutil

def verifier_ram(ram_attendue): # pour verifier la rame

    ram_reelle = round(
        psutil.virtual_memory().total / (1024 ** 3)
    )

    if ram_reelle >= ram_attendue:
        return True, ram_reelle

    return False, ram_reelle