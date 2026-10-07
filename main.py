import json
import psutil

with open("profil/posteComptable.json", "r", encoding="utf-8") as fichier:
    profil = json.load(fichier)

ram_attendue = profil["ram_min"]

ram_reelle = round(psutil.virtual_memory().total / (1024**3))

print("Profil :", profil["nom_profil"])
print("RAM minimum demandée :", ram_attendue, "Go")
print("RAM détectée :", ram_reelle, "Go")

if ram_reelle >= ram_attendue:
    print("Conforme")
else:
    print(" Non conforme")