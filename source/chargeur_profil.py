
import json
from pathlib import Path

# Chemin vers le dossier principal du projet
DOSSIER_PROJET = Path(__file__).resolve().parents[1]

FICHIERS_PROFILS = {
    "POSTE-COMPTABLE": "posteComptable.json",
    "POSTE-ACCUEIL": "posteAccueil.json",
    "POSTE-DIRECTION": "posteDirection.json",
}


def charger_profil(nom_profil):
    nom_fichier = FICHIERS_PROFILS.get(nom_profil)

    if nom_fichier is None:
        return None

    chemin = DOSSIER_PROJET / "profils" / nom_fichier

    try:
        with open(chemin, "r", encoding="utf-8") as fichier:
            return json.load(fichier)

    except (OSError, json.JSONDecodeError) as erreur:
        print(f"Erreur de chargement du profil {nom_profil} : {erreur}")
        return None
