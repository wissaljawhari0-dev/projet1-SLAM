

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from source.chargeur_profil import charger_profil
from source.moteur.moteur_recette import (
    lancer_recette_complete,
    calculer_verdict,
    lancer_corrections_automatiques
)
from source.pdf.generateur_pdf import generer_pdf


# =========================
# COULEURS
# =========================

BLEU_NUIT = "#14243A"
BLEU_FONCE = "#1D3557"
BLEU = "#2878D0"
BLEU_CLAIR = "#EAF2FB"
FOND = "#F4F7FB"
BLANC = "#FFFFFF"
TEXTE = "#253247"
GRIS = "#718096"
VERT = "#16865C"
ROUGE = "#C0392B"
ORANGE = "#C77700"


# =========================
# FENETRE PRINCIPALE
# =========================

fenetre = tk.Tk()
fenetre.title("Audit & Recette PC")
fenetre.geometry("1200x750")
fenetre.minsize(1000, 650)
fenetre.configure(bg=FOND)

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "TNotebook",
    background=FOND,
    borderwidth=0
)

style.configure(
    "TNotebook.Tab",
    font=("Segoe UI", 10, "bold"),
    padding=(22, 12),
    background="#E1E8F0",
    foreground=TEXTE
)

style.map(
    "TNotebook.Tab",
    background=[("selected", BLANC)],
    foreground=[("selected", BLEU)]
)

style.configure(
    "Profil.TCombobox",
    padding=8,
    font=("Segoe UI", 11)
)


# =========================
# FONCTIONS UTILITAIRES
# =========================

def afficher_statut(message):
    barre_statut.config(text=message)


def ouvrir_onglet(index):
    onglets.select(index)


def nouvelle_recette():
    zone_resultats.config(state="normal")
    zone_resultats.delete("1.0", tk.END)
    zone_resultats.insert(
        tk.END,
        "Aucune recette lancée.\n\n"
        "Sélectionnez un profil, puis cliquez sur "
        "« Lancer la recette »."
    )
    zone_resultats.config(state="disabled")

    carte_verdict.config(
        text="EN ATTENTE",
        bg=BLEU_CLAIR,
        fg=BLEU_FONCE
    )

    carte_conformes.config(text="—")
    carte_non_conformes.config(text="—")
    carte_total.config(text="—")

    afficher_statut("Nouvelle recette prête.")


def obtenir_profil():
    nom = liste_profils.get().strip()

    if not nom:
        messagebox.showwarning(
            "Profil manquant",
            "Veuillez sélectionner un profil."
        )
        return None

    profil = charger_profil(nom)

    if profil is None:
        messagebox.showerror(
            "Erreur",
            "Impossible de charger le profil sélectionné."
        )
        return None

    return profil


def mettre_a_jour_resume(resultats, verdict):
    conformes = 0
    non_conformes = 0

    for resultat in resultats:
        etat = str(resultat.get("etat", "")).lower()

        if "non conforme" in etat or "non-conforme" in etat:
            non_conformes += 1
        elif "conforme" in etat:
            conformes += 1

    carte_conformes.config(text=str(conformes))
    carte_non_conformes.config(text=str(non_conformes))
    carte_total.config(text=str(len(resultats)))

    verdict_minuscule = str(verdict).lower()

    if "non conforme" in verdict_minuscule:
        carte_verdict.config(
            text=verdict.upper(),
            bg="#FCE8E6",
            fg=ROUGE
        )
    elif "réserve" in verdict_minuscule or "reserve" in verdict_minuscule:
        carte_verdict.config(
            text=verdict.upper(),
            bg="#FFF1D6",
            fg=ORANGE
        )
    else:
        carte_verdict.config(
            text=verdict.upper(),
            bg="#DDF5E8",
            fg=VERT
        )


# =========================
# GENERATION PDF
# =========================

def creer_pdf():
    profil = obtenir_profil()

    if profil is None:
        return

    try:
        afficher_statut("Génération du rapport PDF...")

        resultats = lancer_recette_complete(profil)
        verdict = calculer_verdict(resultats)

        chemin_pdf = generer_pdf(
            profil["nom_profil"],
            resultats,
            verdict
        )

        mettre_a_jour_resume(resultats, verdict)

        afficher_statut("Rapport PDF généré.")

        messagebox.showinfo(
            "Rapport PDF",
            "Le rapport a été généré avec succès.\n\n"
            f"Fichier : {chemin_pdf}"
        )

    except Exception as erreur:
        afficher_statut("Erreur pendant la génération du PDF.")
        messagebox.showerror(
            "Erreur PDF",
            f"Impossible de générer le rapport.\n\n{erreur}"
        )


# =========================
# LANCEMENT DE LA RECETTE
# =========================

def lancer_recette():
    profil = obtenir_profil()

    if profil is None:
        return

    try:
        afficher_statut("Contrôle du poste en cours...")
        fenetre.update_idletasks()

        resultats = lancer_recette_complete(profil)
        verdict = calculer_verdict(resultats)

        mettre_a_jour_resume(resultats, verdict)

        zone_resultats.config(state="normal")
        zone_resultats.delete("1.0", tk.END)

        zone_resultats.insert(
            tk.END,
            "RAPPORT DE CONTRÔLE\n",
            "titre"
        )

        zone_resultats.insert(
            tk.END,
            f"Date : {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n"
        )
        zone_resultats.insert(
            tk.END,
            f"Profil : {profil['nom_profil']}\n"
        )
        zone_resultats.insert(
            tk.END,
            f"Version : {profil.get('version', 'Non renseignée')}\n"
        )
        zone_resultats.insert(
            tk.END,
            f"RAM minimum : {profil.get('ram_min', '—')} Go\n"
        )
        zone_resultats.insert(
            tk.END,
            f"Espace disque minimum : "
            f"{profil.get('espace_disque_min', '—')} Go\n\n"
        )

        zone_resultats.insert(
            tk.END,
            "DÉTAIL DES CONTRÔLES\n",
            "titre_section"
        )

        for resultat in resultats:
            nom_controle = str(
                resultat.get("controle", "Contrôle non renseigné")
            )
            etat = str(
                resultat.get("etat", "Résultat non renseigné")
            )

            if "non conforme" in etat.lower():
                tag = "non_conforme"
            elif "conforme" in etat.lower():
                tag = "conforme"
            else:
                tag = "normal"

            zone_resultats.insert(
                tk.END,
                f"  •  {nom_controle} : ",
                "normal"
            )
            zone_resultats.insert(
                tk.END,
                f"{etat}\n",
                tag
            )

        zone_resultats.insert(
            tk.END,
            "\nVERDICT FINAL\n",
            "titre_section"
        )
        zone_resultats.insert(
            tk.END,
            verdict.upper(),
            "verdict"
        )

        zone_resultats.config(state="disabled")

        afficher_statut("Recette terminée.")
        ouvrir_onglet(1)

    except Exception as erreur:
        afficher_statut("Erreur pendant la recette.")
        messagebox.showerror(
            "Erreur",
            f"La recette n'a pas pu se terminer.\n\n{erreur}"
        )


# =========================
# CORRECTIONS AUTOMATIQUES
# =========================

def executer_corrections():
    confirmation = messagebox.askyesno(
        "Confirmation",
        "Voulez-vous lancer les corrections automatiques ?\n\n"
        "Certaines corrections peuvent modifier la configuration "
        "de Windows. Vérifiez que vous êtes autorisée à les effectuer."
    )

    if not confirmation:
        return

    try:
        afficher_statut("Corrections automatiques en cours...")
        fenetre.update_idletasks()

        corrections = lancer_corrections_automatiques()

        if corrections:
            message = "\n".join(str(c) for c in corrections)
        else:
            message = "Aucune information de correction n'a été retournée."

        afficher_statut("Corrections terminées.")

        messagebox.showinfo(
            "Corrections automatiques",
            message
        )

    except Exception as erreur:
        afficher_statut("Erreur pendant les corrections.")
        messagebox.showerror(
            "Erreur",
            f"Les corrections ont rencontré un problème.\n\n{erreur}"
        )


# =========================
# MENU
# =========================

barre_menu = tk.Menu(
    fenetre,
    bg=BLANC,
    fg=TEXTE,
    tearoff=0
)

fenetre.config(menu=barre_menu)

menu_fichier = tk.Menu(barre_menu, tearoff=0)
barre_menu.add_cascade(label="Fichier", menu=menu_fichier)

menu_fichier.add_command(
    label="Nouvelle recette",
    command=nouvelle_recette
)
menu_fichier.add_separator()
menu_fichier.add_command(
    label="Quitter",
    command=fenetre.destroy
)

menu_rapport = tk.Menu(barre_menu, tearoff=0)
barre_menu.add_cascade(label="Rapport", menu=menu_rapport)

menu_rapport.add_command(
    label="Générer PDF",
    command=creer_pdf
)

menu_aide = tk.Menu(barre_menu, tearoff=0)
barre_menu.add_cascade(label="Aide", menu=menu_aide)

menu_aide.add_command(
    label="À propos",
    command=lambda: messagebox.showinfo(
        "À propos",
        "Audit & Recette PC\n"
        "Projet BTS SIO SLAM\n"
        "Application de contrôle des postes Windows\n"
        "Version 1.0"
    )
)


# =========================
# STRUCTURE PRINCIPALE
# =========================

conteneur = tk.Frame(fenetre, bg=FOND)
conteneur.pack(fill="both", expand=True)

# Menu latéral
menu_lateral = tk.Frame(
    conteneur,
    bg=BLEU_NUIT,
    width=225
)
menu_lateral.pack(side="left", fill="y")
menu_lateral.pack_propagate(False)

tk.Label(
    menu_lateral,
    text="AUDIT PC",
    font=("Segoe UI", 21, "bold"),
    bg=BLEU_NUIT,
    fg=BLANC
).pack(anchor="w", padx=24, pady=(30, 2))

tk.Label(
    menu_lateral,
    text="OUTIL DE RECETTE",
    font=("Segoe UI", 9, "bold"),
    bg=BLEU_NUIT,
    fg="#9DB9D9"
).pack(anchor="w", padx=25, pady=(0, 35))


def bouton_menu(texte, commande):
    bouton = tk.Button(
        menu_lateral,
        text=texte,
        command=commande,
        font=("Segoe UI", 10, "bold"),
        bg=BLEU_NUIT,
        fg=BLANC,
        activebackground=BLEU_FONCE,
        activeforeground=BLANC,
        relief="flat",
        bd=0,
        anchor="w",
        padx=24,
        pady=14,
        cursor="hand2"
    )
    bouton.pack(fill="x", padx=10, pady=3)
    return bouton


bouton_menu("⌂   Tableau de bord", lambda: ouvrir_onglet(0))
bouton_menu("▤   Résultats", lambda: ouvrir_onglet(1))
bouton_menu("▧   Générer le PDF", creer_pdf)

tk.Frame(menu_lateral, bg="#344A63", height=1).pack(
    fill="x", padx=20, pady=25
)

tk.Label(
    menu_lateral,
    text="PROJET BTS SIO\nSLAM • Version 1.0",
    font=("Segoe UI", 9),
    bg=BLEU_NUIT,
    fg="#A9B9CC",
    justify="left"
).pack(side="bottom", anchor="w", padx=24, pady=24)


# Zone centrale
zone_principale = tk.Frame(conteneur, bg=FOND)
zone_principale.pack(side="left", fill="both", expand=True)

# En-tête
entete = tk.Frame(zone_principale, bg=BLANC, height=95)
entete.pack(fill="x")
entete.pack_propagate(False)

tk.Label(
    entete,
    text="Audit & Recette PC",
    font=("Segoe UI", 22, "bold"),
    bg=BLANC,
    fg=BLEU_NUIT
).pack(anchor="w", padx=30, pady=(18, 0))

tk.Label(
    entete,
    text="Vérifiez la conformité et la configuration de vos postes Windows.",
    font=("Segoe UI", 10),
    bg=BLANC,
    fg=GRIS
).pack(anchor="w", padx=32, pady=(2, 12))


# =========================
# ONGLETS
# =========================

onglets = ttk.Notebook(zone_principale)
onglets.pack(fill="both", expand=True, padx=22, pady=20)

onglet_recette = tk.Frame(onglets, bg=FOND)
onglet_resultats = tk.Frame(onglets, bg=FOND)

onglets.add(onglet_recette, text="Tableau de bord")
onglets.add(onglet_resultats, text="Résultats")


# =========================
# TABLEAU DE BORD
# =========================

tk.Label(
    onglet_recette,
    text="Bienvenue",
    font=("Segoe UI", 19, "bold"),
    bg=FOND,
    fg=TEXTE
).pack(anchor="w", padx=22, pady=(18, 2))

tk.Label(
    onglet_recette,
    text="Sélectionnez le profil de référence avant de lancer les contrôles.",
    font=("Segoe UI", 10),
    bg=FOND,
    fg=GRIS
).pack(anchor="w", padx=23, pady=(0, 18))


# Profil
cadre_profil = tk.Frame(
    onglet_recette,
    bg=BLANC,
    highlightbackground="#DCE4EF",
    highlightthickness=1
)
cadre_profil.pack(fill="x", padx=22, pady=(0, 18))

tk.Label(
    cadre_profil,
    text="PROFIL DU POSTE",
    font=("Segoe UI", 10, "bold"),
    bg=BLANC,
    fg=BLEU_FONCE
).grid(row=0, column=0, sticky="w", padx=20, pady=(17, 5))

liste_profils = ttk.Combobox(
    cadre_profil,
    values=[
        "POSTE-COMPTABLE",
        "POSTE-ACCUEIL",
        "POSTE-DIRECTION"
    ],
    state="readonly",
    width=32,
    style="Profil.TCombobox"
)
liste_profils.grid(
    row=1,
    column=0,
    sticky="w",
    padx=20,
    pady=(0, 18)
)
liste_profils.current(0)

tk.Label(
    cadre_profil,
    text="Le profil définit les critères utilisés pour la recette.",
    font=("Segoe UI", 9),
    bg=BLANC,
    fg=GRIS
).grid(row=1, column=1, sticky="w", padx=20, pady=(0, 18))

cadre_profil.columnconfigure(1, weight=1)


# Boutons d'action
tk.Label(
    onglet_recette,
    text="ACTIONS RAPIDES",
    font=("Segoe UI", 11, "bold"),
    bg=FOND,
    fg=TEXTE
).pack(anchor="w", padx=23, pady=(0, 10))

cadre_actions = tk.Frame(onglet_recette, bg=FOND)
cadre_actions.pack(fill="x", padx=22)

def bouton_action(parent, texte, description, couleur, commande):
    carte = tk.Frame(
        parent,
        bg=BLANC,
        highlightbackground="#DCE4EF",
        highlightthickness=1
    )

    tk.Label(
        carte,
        text=texte,
        font=("Segoe UI", 12, "bold"),
        bg=BLANC,
        fg=couleur
    ).pack(anchor="w", padx=15, pady=(15, 5))

    tk.Label(
        carte,
        text=description,
        font=("Segoe UI", 9),
        bg=BLANC,
        fg=GRIS,
        wraplength=210,
        justify="left"
    ).pack(anchor="w", padx=15, pady=(0, 14))

    tk.Button(
        carte,
        text="Lancer  →",
        command=commande,
        font=("Segoe UI", 10, "bold"),
        bg=couleur,
        fg=BLANC,
        activebackground=BLEU_FONCE,
        activeforeground=BLANC,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=12,
        pady=9
    ).pack(anchor="w", padx=15, pady=(0, 15))

    return carte


carte_recette = bouton_action(
    cadre_actions,
    "Lancer la recette",
    "Exécuter les contrôles et afficher le verdict du poste.",
    BLEU,
    lancer_recette
)
carte_recette.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

carte_correction = bouton_action(
    cadre_actions,
    "Corrections",
    "Lancer les corrections automatiques disponibles.",
    ORANGE,
    executer_corrections
)
carte_correction.grid(row=0, column=1, sticky="nsew", padx=4)

carte_pdf = bouton_action(
    cadre_actions,
    "Rapport PDF",
    "Créer un procès-verbal de recette au format PDF.",
    VERT,
    creer_pdf
)
carte_pdf.grid(row=0, column=2, sticky="nsew", padx=(8, 0))

for colonne in range(3):
    cadre_actions.columnconfigure(colonne, weight=1, uniform="actions")


# Informations du projet
cadre_info = tk.Frame(
    onglet_recette,
    bg=BLEU_CLAIR
)
cadre_info.pack(fill="x", padx=22, pady=22)

tk.Label(
    cadre_info,
    text="À PROPOS DE L'APPLICATION",
    font=("Segoe UI", 10, "bold"),
    bg=BLEU_CLAIR,
    fg=BLEU_FONCE
).pack(anchor="w", padx=18, pady=(14, 5))

tk.Label(
    cadre_info,
    text=(
        "Contrôles matériels • Sécurité Windows • Logiciels\n"
        "Vérification de la configuration • Corrections • Rapport PDF"
    ),
    font=("Segoe UI", 10),
    bg=BLEU_CLAIR,
    fg=TEXTE,
    justify="left"
).pack(anchor="w", padx=18, pady=(0, 14))


# =========================
# ONGLET RESULTATS
# =========================

tk.Label(
    onglet_resultats,
    text="Résumé de la recette",
    font=("Segoe UI", 18, "bold"),
    bg=FOND,
    fg=TEXTE
).pack(anchor="w", padx=20, pady=(18, 14))

cadre_resume = tk.Frame(onglet_resultats, bg=FOND)
cadre_resume.pack(fill="x", padx=20, pady=(0, 15))


def creer_indicateur(parent, titre, couleur, texte_initial):
    cadre = tk.Frame(
        parent,
        bg=BLANC,
        highlightbackground="#DCE4EF",
        highlightthickness=1
    )

    tk.Label(
        cadre,
        text=titre,
        font=("Segoe UI", 9, "bold"),
        bg=BLANC,
        fg=GRIS
    ).pack(anchor="w", padx=15, pady=(12, 3))

    valeur = tk.Label(
        cadre,
        text=texte_initial,
        font=("Segoe UI", 21, "bold"),
        bg=BLANC,
        fg=couleur
    )
    valeur.pack(anchor="w", padx=15, pady=(0, 12))

    return cadre, valeur


cadre_indicateur, carte_conformes = creer_indicateur(
    cadre_resume, "CONFORMES", VERT, "—"
)
cadre_indicateur.grid(row=0, column=0, sticky="nsew", padx=(0, 7))

cadre_indicateur, carte_non_conformes = creer_indicateur(
    cadre_resume, "NON CONFORMES", ROUGE, "—"
)
cadre_indicateur.grid(row=0, column=1, sticky="nsew", padx=7)

cadre_indicateur, carte_total = creer_indicateur(
    cadre_resume, "TOTAL CONTRÔLES", BLEU, "—"
)
cadre_indicateur.grid(row=0, column=2, sticky="nsew", padx=(7, 0))

for colonne in range(3):
    cadre_resume.columnconfigure(colonne, weight=1, uniform="resume")


tk.Label(
    onglet_resultats,
    text="VERDICT FINAL",
    font=("Segoe UI", 10, "bold"),
    bg=FOND,
    fg=GRIS
).pack(anchor="w", padx=20, pady=(2, 5))

carte_verdict = tk.Label(
    onglet_resultats,
    text="EN ATTENTE",
    font=("Segoe UI", 12, "bold"),
    bg=BLEU_CLAIR,
    fg=BLEU_FONCE,
    padx=15,
    pady=12,
    anchor="w"
)
carte_verdict.pack(fill="x", padx=20, pady=(0, 15))


cadre_details = tk.Frame(onglet_resultats, bg=BLANC)
cadre_details.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 15)
)

scrollbar = ttk.Scrollbar(cadre_details, orient="vertical")
scrollbar.pack(side="right", fill="y")

zone_resultats = tk.Text(
    cadre_details,
    wrap="word",
    font=("Consolas", 10),
    bg=BLANC,
    fg=TEXTE,
    relief="flat",
    padx=15,
    pady=15,
    spacing1=3,
    spacing3=3,
    yscrollcommand=scrollbar.set,
    state="disabled"
)
zone_resultats.pack(fill="both", expand=True)

scrollbar.config(command=zone_resultats.yview)

zone_resultats.tag_configure(
    "titre",
    font=("Segoe UI", 16, "bold"),
    foreground=BLEU_FONCE,
    spacing3=10
)
zone_resultats.tag_configure(
    "titre_section",
    font=("Segoe UI", 11, "bold"),
    foreground=BLEU,
    spacing1=10,
    spacing3=5
)
zone_resultats.tag_configure(
    "conforme",
    foreground=VERT,
    font=("Consolas", 10, "bold")
)
zone_resultats.tag_configure(
    "non_conforme",
    foreground=ROUGE,
    font=("Consolas", 10, "bold")
)
zone_resultats.tag_configure(
    "normal",
    foreground=TEXTE
)

zone_resultats.config(state="normal")
zone_resultats.insert(
    tk.END,
    "Aucune recette lancée.\n\n"
    "Lancez une recette depuis le tableau de bord pour afficher "
    "les résultats ici."
)
zone_resultats.config(state="disabled")


# =========================
# BARRE DE STATUT
# =========================

barre_statut = tk.Label(
    fenetre,
    text="Prêt  |  Projet BTS SIO SLAM  |  Version 1.0",
    font=("Segoe UI", 9),
    bg="#E5EBF2",
    fg=GRIS,
    anchor="w",
    padx=12,
    pady=7
)
barre_statut.pack(side="bottom", fill="x")


# =========================
# DEMARRAGE
# =========================

fenetre.mainloop()
