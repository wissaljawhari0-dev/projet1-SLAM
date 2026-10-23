
CATALOGUE_CONTROLES = [
    "Nom du poste",
    "Compte administrateur",
    "Comptes locaux autorisés",
    "Mémoire RAM",
    "Espace disque",
    "Santé du disque SMART",
    "Type de disque",
    "Version de Windows",
    "Activation Windows",
    "Heure et synchronisation",
    "Mises à jour Windows",
    "Antivirus",
    "Signatures antivirus",
    "BitLocker",
    "Pare-feu",
    "Logiciels obligatoires",
    "Logiciels interdits",
    "État des services",
    "NumLock",
    "Extensions de fichiers visibles",
    "Fichiers cachés visibles",
    "Confirmation de suppression",
    "Page d'accueil Chrome",
    "Imprimante",
    "Journaux Windows",
]


def verifier_catalogue():
    return len(CATALOGUE_CONTROLES) == 25
