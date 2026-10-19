resultats = []

def ajouter_resultat(nom_controle,etat):
    resultat = {
        "controle": nom_controle,
        "etat": etat
    }

    resultats.append(resultat)

def afficher_resultats():

    print("\n ___RESULTATS___")

    for resultat in resultats:

        print(
            resultat["controle"],
            "-",
            resultat["etat"]
        )

def recuperer_resultats():
    return resultats