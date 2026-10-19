import json

def charger_profil(nom_profil):

    if nom_profil == "POSTE-COMPTABLE":
        fichier = "profils/posteComptable.json"

    elif nom_profil == "POSTE-ACCUEIL":
        fichier = "profils/posteAccueil.json"

    elif nom_profil == "POSTE-DIRECTION":
        fichier = "profils/posteDirection.json"

    else:
        return None

    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)