# Projet Recette des postes

## Présentation

Ce projet est une application Python qui permet de vérifier la conformité d'un poste informatique à partir d'un profil de recette.

L'application dispose d'une interface graphique permettant de lancer les contrôles, de consulter les résultats, d'identifier les anomalies et de générer un procès-verbal au format PDF.

## Profils disponibles

Le projet prévoit trois profils de recette :

- POSTE-COMPTABLE
- POSTE-ACCUEIL
- POSTE-DIRECTION

Chaque profil définit les valeurs attendues pour le poste informatique concerné.

## Technologies utilisées

- Python
- Tkinter pour l'interface graphique
- JSON pour les profils de recette
- ReportLab pour la génération des PDF

## Installation

1. Installer Python sur le poste de développement.
2. Ouvrir un terminal dans le dossier principal du projet.
3. Installer les dépendances avec la commande suivante :

```bash
py -m pip install -r requirements.txt
```

## Lancement

Depuis le dossier principal du projet, lancer la commande :

```bash
py source/interface/fenetre_principale.py
```

## Utilisation

1. Ouvrir l'application.
2. Choisir le profil de recette adapté.
3. Lancer les contrôles.
4. Consulter les résultats et les anomalies.
5. Appliquer les corrections proposées lorsqu'elles sont disponibles et autorisées.
6. Relancer les contrôles pour vérifier les résultats.
7. Générer le procès-verbal PDF.

## Génération du procès-verbal

Le module `source/pdf/generateur_pdf.py` est chargé de générer le procès-verbal de recette au format PDF.

Le fichier généré est nommé `PV_Recette.pdf`.

## Précautions

- Réaliser les tests de modification sur une machine virtuelle de test.
- Lire les messages de confirmation avant d'appliquer une correction.
- Ne jamais enregistrer de mots de passe dans les fichiers livrés.
- Vérifier les résultats avant de conclure qu'un poste est conforme.

## Limites connues

Les contrôles non disponibles, les corrections nécessitant une intervention humaine et les limites de l'environnement de test devront être documentés après vérification du fonctionnement complet de l'application.

## Livraison

Le code source, les profils JSON, le fichier de configuration, les dépendances et les scripts nécessaires devront être inclus dans l'archive du projet.

Le dépôt Git devra contenir les instructions d'installation et de lancement ainsi que les fichiers nécessaires à l'utilisation du projet.

