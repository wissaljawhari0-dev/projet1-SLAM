import os

def verifier_chrome():

    chemin_chrome = (
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    )

    if os.path.exists(chemin_chrome): # si chemin_chrome existe ?
        return True

    return False
#print (verifier_chrome())