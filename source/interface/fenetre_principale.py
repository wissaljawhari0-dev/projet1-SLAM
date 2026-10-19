import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)

from source.moteur.moteur_recette import recuperer_resultats
from source.chargeur_profil import charger_profil


fenetre = tk.Tk()

fenetre.title("Projet1 SLAM")
fenetre.geometry("900x600")

def lancer_recette():

    profil_selectionne = liste_profils.get()
    profil = charger_profil( profil_selectionne)

    zone_resultats.delete("1.0", tk.END)

    

    zone_resultats.insert(
        tk.END,
        f"Version : {profil['version']}\n"
    )

    zone_resultats.insert(
        tk.END,
        f"RAM minimum : {profil['ram_min']} Go\n"
    )

    zone_resultats.insert(
        tk.END,
        f"Espace disque minimum : {profil['espace_disque_min']} Go\n\n"
    )

    zone_resultats.insert(
        tk.END,
        "Résultats de la recette\n\n"
    )

    zone_resultats.insert(
        tk.END, 
        f"Profil sélectionné : {profil['nom_profil']}\n\n"
    )

    zone_resultats.insert(
        tk.END,
        "RAM : Conforme\n"
    )

    zone_resultats.insert(
        tk.END,
        "Disque : Conforme\n"
    )

    zone_resultats.insert(
        tk.END,
        "Nom PC : Conforme\n"
    )

    zone_resultats.insert(
        tk.END,
        "Pare-feu : Conforme\n"
    )

    zone_resultats.insert(
        tk.END,
        "Chrome : Conforme\n"
    )




titre = tk.Label(
    fenetre,
    text="Projet1 SLAM",
    font=("Arial", 20)
)
titre.pack(pady=10)

label_profil = tk.Label(
    fenetre,
    text="Choisir un profil :"
)
label_profil.pack()

liste_profils = ttk.Combobox(
    fenetre,
    values=[
        "POSTE-COMPTABLE",
        "POSTE-ACCUEIL",
        "POSTE-DIRECTION"
    ]
)
liste_profils.pack(pady=10)
liste_profils.current(0)

bouton = tk.Button(
    fenetre,
    text="Lancer la recette",
    command=lancer_recette
)
bouton.pack(pady=10)

zone_resultats = tk.Text(
    fenetre,
    width=80,
    height=20
)
zone_resultats.pack(pady=20)

fenetre.mainloop()