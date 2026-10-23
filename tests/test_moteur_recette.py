
from source.moteur.moteur_recette import calculer_verdict


def test_tout_conforme():
    resultats = [
        {"controle": "RAM", "etat": "Conforme"},
        {"controle": "Pare-feu", "etat": "Conforme"},
    ]

    assert calculer_verdict(resultats) == "POSTE CONFORME"


def test_trois_non_conformites():
    resultats = [
        {"controle": "RAM", "etat": "Non conforme"},
        {"controle": "Pare-feu", "etat": "Non conforme"},
        {"controle": "Antivirus", "etat": "Non conforme"},
    ]

    assert calculer_verdict(resultats) == "POSTE CONFORME AVEC RESERVES"


def test_plus_de_trois_non_conformites():
    resultats = [
        {"controle": "RAM", "etat": "Non conforme"},
        {"controle": "Pare-feu", "etat": "Non conforme"},
        {"controle": "Antivirus", "etat": "Non conforme"},
        {"controle": "Chrome", "etat": "Non conforme"},
    ]

    assert calculer_verdict(resultats) == "POSTE NON CONFORME"


from source.moteur.moteur_recette import calculer_verdict


def test_resultats_vides():
    assert calculer_verdict([]) != "POSTE CONFORME"


def test_resultat_inconnu():
    resultats = [{"controle": "Test", "etat": "Inconnu"}]
    assert calculer_verdict(resultats) != "POSTE CONFORME"


def test_controle_desactive():
    from source.moteur.moteur_recette import controle_actif

    profil = {
        "controles": [
            {
                "id": "C06",
                "nom": "Santé du disque SMART",
                "actif": False
            }
        ]
    }

    assert controle_actif(profil, "Santé du disque SMART") is False
