def ecrire_log(message):

    with open(
        "logs/recette.log",
        "a",
        encoding="utf-8"
    ) as fichier:

        fichier.write(message + "\n")