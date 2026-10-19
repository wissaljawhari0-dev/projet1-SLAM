from source.controles.ram import verifier_ram # pour avoire accé au fichier ram.py
from source.controles.journal import ecrire_log #  remplire fichier log de maniére 'auto', faire la jornalisation
from source.moteur.moteur_recette import ajouter_resultat, afficher_resultats
from source.controles.parefeu import verifier_parefeu
from source.controles.chrom import verifier_chrome
from source.controles.antivirus import verifier_antivirus
from source.controles.windows_update import verifier_windows_update
from source.controles.bitlocker import verifier_bitlocker
from source.controles.services import verifier_service
import json
import psutil
import socket # permet d avoire des information du pc 


score = 0
print("Choisissez un profil :")
print("1 - Comptable")
print("2 - Accueil")
print("3 - Direction")

choix = input("Votre choix : ")

if choix == "1":
    fichier_profil = "profils/posteComptable.json"

elif choix == "2":
    fichier_profil = "profils/posteAccueil.json"

elif choix == "3":
    fichier_profil = "profils/posteDirection.json"

else:
    print("Choix invalide")
    exit()

with open(fichier_profil, "r", encoding="utf-8") as fichier:
    profil = json.load(fichier)

####### Ram ######
ram_attendue = profil["ram_min"]

conforme_ram, ram_reelle = verifier_ram(
    ram_attendue
)

print("____CONTROLE RAM____")
print("RAM minimum :", ram_attendue)
print("RAM détectée :", ram_reelle)

if conforme_ram:
    print(" Conforme")
    ecrire_log("Controle RAM : Conforme")
    ajouter_resultat("RAM","Conforme")
    score += 1
else:
    print(" Non conforme")
    ecrire_log("Controle RAM : Non conforme")
    ajouter_resultat("RAM", "Non conforme")

####### DISQUE ########
disque_attendu = profil["espace_disque_min"] 

disque_reel = round(
    psutil.disk_usage("C:\\").free / (1024**3) #demande combien d espace reste sur le disque C:?
)

print("\n____CONTROLE DISQUE____")
print("Espace minimum demandé :", disque_attendu, "Go")
print("Espace libre détecté :", disque_reel, "Go")

if disque_reel >= disque_attendu:
    print(" Conforme")
    ecrire_log("Controle Disque : Conforme")
    ajouter_resultat("Disque", "Conforme")
    score +=1
else:
    print(" Non conforme")
    ecrire_log("Controle Disque : Non conforme")
    ajouter_resultat("Disque", "Non conforme")


####### nom PC #######
nom_attendu = profil ["nom_pc"]
nom_reel = socket.gethostname()

print ("\n ____Controle du nom du PC____")
print ("le nom du pc : ", nom_attendu)
print ("le nom détecté", nom_reel)

if nom_attendu == nom_reel:
    print("conforme")
    ecrire_log("Controle Nom PC : Conforme")
    ajouter_resultat("Nom PC", "Conforme")
    score +=1
else:
    print("non conforme")
    ecrire_log("Controle Nom PC : Non conforme")
    ajouter_resultat("Nom PC", "Non conforme")

afficher_resultats()

######## ANTIVIRUS ########

antivirus_actif = verifier_antivirus()

print("\n____CONTROLE ANTIVIRUS____")

if antivirus_actif:
    print("Antivirus activé")
    ecrire_log("Controle Antivirus : Conforme")
    ajouter_resultat("Antivirus", "Conforme")
    score += 1
else:
    print("Antivirus désactivé")
    ecrire_log("Controle Antivirus : Non conforme")
    ajouter_resultat("Antivirus", "Non conforme")

######## WINDOWS UPDATE ########

windows_update_actif = verifier_windows_update()

print("\n____CONTROLE WINDOWS UPDATE____")

if windows_update_actif:
    print("Service Windows Update actif")
    ecrire_log("Controle Windows Update : Conforme")
    ajouter_resultat("Windows Update", "Conforme")
    score += 1
else:
    print("Service Windows Update inactif")
    ecrire_log("Controle Windows Update : Non conforme")
    ajouter_resultat("Windows Update", "Non conforme")

######## PAREFEU ########

parefeu_actif = verifier_parefeu()

print("\n____CONTROLE PAREFEU____")

if parefeu_actif:
    print("Pare-feu activé")
    ecrire_log("Controle Pare-feu : Conforme")
    ajouter_resultat("Pare-feu", "Conforme")
    score += 1
else:
    print("Pare-feu désactivé")
    ecrire_log("Controle Pare-feu : Non conforme")
    ajouter_resultat("Pare-feu", "Non conforme")

######## CHROME ########

chrome_installe = verifier_chrome()

print("\n____CONTROLE CHROME____")

if chrome_installe:
    print("Chrome installé")
    ecrire_log("Controle Chrome : Conforme")
    ajouter_resultat("Chrome", "Conforme")
    score += 1
else:
    print("Chrome non installé")
    ecrire_log("Controle Chrome : Non conforme")
    ajouter_resultat("Chrome", "Non conforme")

######## BITLOCKER ########

bitlocker_actif = verifier_bitlocker()

print("\n____CONTROLE BITLOCKER____")

if bitlocker_actif:
    print("BitLocker activé")
    ecrire_log("Controle BitLocker : Conforme")
    ajouter_resultat("BitLocker", "Conforme")
    score += 1
else:
    print("BitLocker désactivé")
    ecrire_log("Controle BitLocker : Non conforme")
    ajouter_resultat("BitLocker", "Non conforme")

######## SERVICE SPOOLER ########

service_spooler = verifier_service("Spooler")

print("\n____CONTROLE SERVICE SPOOLER____")

if service_spooler:
    print("Service Spooler actif")
    ecrire_log("Controle Service Spooler : Conforme")
    ajouter_resultat("Service Spooler", "Conforme")
    score += 1
else:
    print("Service Spooler inactif")
    ecrire_log("Controle Service Spooler : Non conforme")
    ajouter_resultat("Service Spooler", "Non conforme")
    
####### RAPPORT FINAL #######
print("\n_____RAPPORT FINAL_____")
print("Nombre de contrôles conformes :", score)
print("Nombre total de contrôles : 9")

if score == 9:
    print("VERDICT : POSTE CONFORME")
else:
    print("VERDICT : POSTE NON CONFORME")
