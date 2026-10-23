import psutil
import socket


from source.controles.ram import verifier_ram
from source.controles.parefeu import verifier_parefeu
from source.controles.chrome import verifier_chrome
from source.controles.antivirus import verifier_antivirus
from source.controles.windows_update import verifier_windows_update
from source.controles.bitlocker import verifier_bitlocker
from source.controles.services import verifier_service
from source.controles.version_windows import verifier_version_windows
from source.controles.activation_windows import verifier_activation_windows
from source.controles.dhcp import verifier_dhcp
from source.controles.heure_windows import verifier_heure
from source.controles.numlock import verifier_numlock
from source.controles.extensions import verifier_extensions
from source.controles.fichiers_caches import verifier_fichiers_caches
from source.controles.imprimante import verifier_imprimante
from source.controles.winget import verifier_winget
from source.controles.defender import verifier_defender
from source.controles.comptes import verifier_compte_admin
from source.controles.smart import verifier_smart
from source.controles.type_disque import verifier_type_disque
from source.controles.signatures_antivirus import verifier_signatures_antivirus
from source.controles.logiciels_interdits import verifier_logiciels_interdits
from source.controles.logiciels_obligatoires import verifier_logiciels_obligatoires
from source.controles.journaux_windows import verifier_journaux_windows
from source.corrections.corriger_parefeu import corriger_parefeu
from source.corrections.corriger_defender import corriger_defender
from source.corrections.corriger_windows_update import corriger_windows_update
from source.corrections.corriger_dhcp import corriger_dhcp
from source.corrections.corriger_winget import corriger_winget

resultats = []

def ajouter_resultat(nom_controle, etat):

    resultat = {
        "controle": nom_controle,
        "etat": etat
    }

    resultats.append(resultat)

def afficher_resultats():

    print("\n___RESULTATS___")

    for resultat in resultats:

        print(
            resultat["controle"],
            "-",
            resultat["etat"]
        )

def recuperer_resultats():
    return resultats

def vider_resultats():
    resultats.clear()

def lancer_recette_complete(profil):

    vider_resultats()

    ram_min = profil["ram_min"]

    if verifier_ram(ram_min)[0]:
        ajouter_resultat("RAM", "Conforme")
    else:
        ajouter_resultat("RAM", "Non conforme")


    if verifier_parefeu():
        ajouter_resultat("Pare-feu", "Conforme")
    else:
        ajouter_resultat("Pare-feu", "Non conforme")

    if verifier_chrome():
        ajouter_resultat("Chrome", "Conforme")
    else:
        ajouter_resultat("Chrome", "Non conforme")

    # CONTROLE DISQUE
    disque_min = profil["espace_disque_min"]

    disque_reel = (
        psutil.disk_usage("C:\\").free / (1024 ** 3)
    )

    if disque_reel >= disque_min:
        ajouter_resultat("Disque", "Conforme")
    else:
        ajouter_resultat("Disque", "Non conforme")


    # CONTROLE NOM PC
    nom_attendu = profil["nom_pc"]
    nom_reel = socket.gethostname()

    if nom_attendu.lower() == nom_reel.lower():
        ajouter_resultat("Nom PC", "Conforme")
    else:
        ajouter_resultat("Nom PC", "Non conforme")


    #### Antivirus######
    if verifier_antivirus():
        ajouter_resultat(
            "Antivirus",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "Antivirus",
            "Non conforme"
        )

    #####Verifier_windows_update####
    if verifier_windows_update():
        ajouter_resultat(
            "Windows Update",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "Windows Update",
            "Non conforme"
        )
    #######verifier_bitlocker######
    if verifier_bitlocker():
        ajouter_resultat(
            "BitLocker",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "BitLocker",
            "Non conforme"
        )


    ######verifier_serivice####
    if verifier_service("Spooler"):
        ajouter_resultat(
            "Service Spooler",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "Service Spooler",
            "Non conforme"
        )

    # VERSION WINDOWS

    if verifier_version_windows():
        ajouter_resultat(
            "Version Windows",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "Version Windows",
            "Non conforme"
        )

    # ACTIVATION WINDOWS


    if controle_actif(profil, "Activation Windows"):
        ajouter_resultat(
            "Activation Windows",
            "Conforme" if verifier_activation_windows()
            else "Non conforme"
        )
    else:
        ajouter_resultat("Activation Windows", "Non évalué")


    # DHCP

    if verifier_dhcp():
        ajouter_resultat(
            "DHCP",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "DHCP",
            "Non conforme"
        )

    # HEURE

    if verifier_heure():
        ajouter_resultat(
            "Heure Windows",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "Heure Windows",
            "Non conforme"
        )

    # NUMLOCK

    if verifier_numlock():
        ajouter_resultat(
            "NumLock",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "NumLock",
            "Non conforme"
        )

    # EXTENSIONS

    if verifier_extensions():
        ajouter_resultat(
            "Extensions fichiers",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "Extensions fichiers",
            "Non conforme"
        )

    # FICHIERS CACHES

    if verifier_fichiers_caches():
        ajouter_resultat(
            "Fichiers caches",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "Fichiers caches",
            "Non conforme"
        )

    # IMPRIMANTE

    if verifier_imprimante():
        ajouter_resultat(
            "Imprimante",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "Imprimante",
            "Non conforme"
        )

    # WINGET

    if verifier_winget():
        ajouter_resultat(
            "Winget",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "Winget",
            "Non conforme"
        )

    # DEFENDER

    if verifier_defender():
        ajouter_resultat(
            "Defender",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "Defender",
            "Non conforme"
        )

    # COMPTE ADMIN

    if verifier_compte_admin():
        ajouter_resultat(
            "Compte Admin",
            "Conforme"
        )
    else:
        ajouter_resultat(
            "Compte Admin",
            "Non conforme"
        )

    # Type de disque (SSD)


    if controle_actif(profil, "Type de disque"):
        ajouter_resultat(
            "Type disque SSD",
            "Conforme" if verifier_type_disque()
            else "Non conforme"
        )
    else:
        ajouter_resultat("Type disque SSD", "Non évalué")


    # Signatures antivirus

    ajouter_resultat(
        "Signatures antivirus",
        "Conforme" if verifier_signatures_antivirus()
        else "Non conforme"
    )

    # Logiciels interdits

    ajouter_resultat(
        "Logiciels interdits",
        "Conforme" if verifier_logiciels_interdits()
        else "Non conforme"
    )

    # SMART


    if controle_actif(profil, "Santé du disque SMART"):
        ajouter_resultat(
            "SMART disque",
            "Conforme" if verifier_smart()
            else "Non conforme"
        )
    else:
        ajouter_resultat("SMART disque", "Non évalué")


    # Logiciels obligatoires

    ajouter_resultat(
        "Logiciels obligatoires",
        "Conforme" if verifier_logiciels_obligatoires()
        else "Non conforme"
    )

    # Journaux Windows

    ajouter_resultat(
        "Journaux Windows",
        "Conforme" if verifier_journaux_windows()
        else "Non conforme"
    )

    
    return resultats


def controle_actif(profil, nom_controle):
    controles = profil.get("controles", [])

    for controle in controles:
        if controle.get("nom") == nom_controle:
            return controle.get("actif", True)

    return True



def calculer_verdict(resultats):
    if not resultats:
        return "POSTE NON CONFORME"

    non_conformes = 0
    controles_evalues = 0

    for resultat in resultats:
        etat = resultat.get("etat")

        if etat == "Désactivé" or etat == "Non évalué":
            continue

        if etat == "Conforme":
            controles_evalues += 1
        elif etat == "Non conforme":
            controles_evalues += 1
            non_conformes += 1
        else:
            # Un état inconnu ne doit jamais être considéré conforme.
            return "POSTE NON CONFORME"

    if controles_evalues == 0:
        return "POSTE NON CONFORME"

    if non_conformes == 0:
        return "POSTE CONFORME"
    elif non_conformes <= 3:
        return "POSTE CONFORME AVEC RESERVES"
    else:
        return "POSTE NON CONFORME"


def lancer_corrections_automatiques():

    confirmation = input(
        "Voulez-vous lancer les corrections automatiques ? (oui/non) : "
    )

    if confirmation.lower() != "oui":
        return ["Corrections annulées par l'utilisateur"]

    resultats = []

    if corriger_parefeu():
        resultats.append("Pare-feu corrigé")
    else:
        resultats.append("Échec Pare-feu")

    if corriger_defender():
        resultats.append("Defender corrigé")
    else:
        resultats.append("Échec Defender")

    if corriger_windows_update():
        resultats.append("Windows Update vérifié")
    else:
        resultats.append("Échec Windows Update")

    if corriger_dhcp():
        resultats.append("DHCP corrigé")
    else:
        resultats.append("Échec DHCP")

    if corriger_winget():
        resultats.append("Winget corrigé")
    else:
        resultats.append("Échec Winget")

    return resultats
